from flask_pymongo import PyMongo
from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS

# Init App
app = Flask(__name__)
api = Api(app)
CORS(app)


# DB Setup
app.config['MONGO_URI'] = "mongodb://127.0.0.1:27017/testdb2"
mongodb_client = PyMongo(app)
db = mongodb_client.db

# Class representing a share
class Share:

    def __init__(self,data):
        self.category = data['category']
        self.name = data['name']
        self.quantity = data['quantity']
        self.price = data['price']

    def __repr__(self):
        return f'<Share : {self.quantity} of {self.name} @ {self.price}>'


class UserList(Resource):

    def get(self):
        result = db.users.find({}, {'_id' : 0, 'password' : 0})
        output = list()

        for e in result:
            output.append(e)

        return output


class User(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('fullname', required=True, type = str, help = 'Cannot be left blank')
    parser.add_argument('username', required=True, type = str, help = 'Cannot be left blank')
    parser.add_argument('password', required=True, type = str, help = 'Cannot be left blank')

    @classmethod
    def check_user_exists(cls, username):
        return db.users.find_one({'username' : username})
        

    def get(self, username):
        """ Get the details for a single user """
        user = db.users.find_one({'username' : username}, {'_id' : 0, 'password' : 0})
        print(User.methods)
        return (user, 200) if user else (user, 404)


    def post(self, username):
        """ Check if user exists, if no, then Create the new user """
        
        if User.check_user_exists(username):
            return {'message' : 'Username already exists'} , 400

        args = User.parser.parse_args()
        print(args)

        new_user = db.users.insert_one(
            {
                'username' : args['username'],
                'fullname' : args['fullname'],
                'password' : args['password'],
                'portfolio' : {
                    'equity' : [],
                    'crypto' : [],
                    'etf' : [],
                    'cash' : []
                }
            }
        )

        return {'message' : 'User added'}

    def delete(self, username):

        if User.check_user_exists(username):
            db.users.delete_one({'username' : username})
            return {'message' : 'User deleted'}, 200

        return {'message' : 'User does not exist'}, 404


class UserHolding(Resource):
    """ This holding can be anything from a share, etf, crypto, cash etc 

        Structure:
    {
        "action" : "sell",
        "category" : "equity",
        "name" : "AAPL",
        "price" : 200,
        "quantity" : 1
    }
    """
    
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument('name', required = True, type = str, help = 'Mandatory Field')
    parser.add_argument('category', required = True, type = str, choices = ('equity', 'crypto', 'etf', 'cash'), help = 'Mandatory Field. <Valid options : equity, crypto, etf, cash>')
    parser.add_argument('action', required = True, type = str, choices = ('buy', 'sell', 'status'), help = 'Mandatory Field. <Valid options : buy, sell, status>')
    parser.add_argument('price', required = True, help = 'Mandatory Field. Enter valid price')
    parser.add_argument('quantity', required = True, help = 'Mandatory field.')

    @classmethod
    def check_item_exists(cls, username, data):
        return db.users.find_one({'username' : username, f'portfolio.{data["category"]}.name' : data['name']}, {'_id' : 0,  f'portfolio.{data["category"]}' : 1})

    def get(self, username):
        """ Get a portfolio object for a given user with a particular holding """
        custom_parser = UserHolding.parser.copy()
        custom_parser.remove_argument('price')
        custom_parser.remove_argument('quantity')
        data = custom_parser.parse_args()

        if (user := UserHolding.check_item_exists(username, data)):
            return user

        return {'message' : 'Resource not found'}, 404


    def post(self, username):
        """ Add new holding to a particular category
            1. Check if username exists
                Yes -> Check if item already exists
                        Yes -> error
                        No -> Push new Holding
                No -> Return user exists error
        """

        if User.check_user_exists(username):
            # As user exists, check if item exists

            args = UserHolding.parser.parse_args()
            if UserHolding.check_item_exists(username, args):
                return {'message' : 'Item already exists'}

            # Create/ push new holding
            
            share = Share(args)

            query = db.users.update_one(
                {'username' : username},
                {'$push' : {
                    f'portfolio.{share.category}' : {
                        'name' : f"{share.name}",
                        'price' : float(share.price),
                        'quantity' : float(share.quantity)
                    } 
                }}
            )

            print(query, type(query))
            return {'message' : 'Updated'}

        return {'message' : 'Invalid user'}, 404


    def put(self, username):
        """
            Check if an item exists:
                Yes -> Update it (if buy then average out , else sell quantity)
                No -> Item not Found 404
        """

        if User.check_user_exists(username):

            args = UserHolding.parser.parse_args()
            if UserHolding.check_item_exists(username, args):
                # As item exists, check action
            
                if args['action'] == 'buy':
                    # Average out price
                    prev_status = self.get_portfolio_category(username, args)

                    new_quantity = (float(prev_status['quantity']) + float(args['quantity']))
                    new_price = ((float(prev_status['price']) * float(prev_status['quantity'])) + (float(args['price'])*float(args['quantity'])))/ new_quantity

                    # Querying

                    db.users.update_one(
                        {'username' : username , f'portfolio.{args["category"]}.name' : args['name']},
                        {'$set' : {
                            f'portfolio.{args["category"]}.$.quantity' : new_quantity,
                            f'portfolio.{args["category"]}.$.price' : new_price
                        }
                        }
                    )

                    return {'message' : 'Successfully Updated'}, 200

                if args['action'] == 'sell':
                    # Reduce quantity and also check for complete selling
                    prev_status = self.get_portfolio_category(username, args)

                    if float(prev_status['quantity']) < float(args['quantity']):
                        return {'message' : 'Invalid request'} , 409

                    if float(prev_status['quantity']) == float(args['quantity']):
                        # Remove from list

                        db.users.update_one(
                            {'username' : username},
                            {'$pull' : {
                                f'portfolio.{args["category"]}' : {'name' : args['name']}
                            }
                            }
                        )
                    
                        return {'message' : 'Updated Successfully. Entire Qty sold'}

                    # Simply update Quantity

                    new_quantity = float(prev_status['quantity']) - float(args['quantity'])

                    db.users.update_one(
                        {'username' : username , f'portfolio.{args["category"]}.name' : args['name']},
                        {'$set' : {
                            f'portfolio.{args["category"]}.$.quantity' : new_quantity
                        }
                        }
                    )

                    return {'message' : 'Successfully Updated'}, 200

            self.post(username)
            return {'message' : "Updated Succesfully"}, 200

        return {'message' : "user doesn't exist"}, 404



                    
    def get_portfolio_category(self, username, args):
        """ Queries the db for a particular item and returns
            a dict with its category as member
            eg:
            {
                portfolio: {
                equity: [
                    { name: 'AAPL', price: 1000, quantity: 15 },
                    { name: 'TSLA', price: 100, quantity: 5 },
                    { name: 'House of TATA', price: '120', quantity: '20' }
                ]
                }
            }

            Returns a dict of the share
        """

        query = db.users.find(
            {'username' : username, f'portfolio.{args["category"]}.name' : args["name"] },
            {'_id' : 0, f'portfolio.{args["category"]}' : 1}
        )

        if not query:
            # No object found
            return False

        portfolio = list(query)
        portfolio = portfolio[0]['portfolio']

        category = portfolio[f'{args["category"]}']

        for share in category:
            if share['name'] == args['name']:
                print(share)
                return share

    
api.add_resource(UserList, '/all')
api.add_resource(User, '/<username>')
api.add_resource(UserHolding, '/<username>/holdings')

if __name__ == "__main__":
    app.run(debug=True)