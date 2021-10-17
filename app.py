from flask_pymongo import PyMongo
from flask import Flask, jsonify, request

app = Flask(__name__)

app.config['MONGO_URI'] = "mongodb://127.0.0.1:27017/testdb"
mongodb_client = PyMongo(app)

db = mongodb_client.db

##############################

class Share:

    def __init__(self, data):
        self.category = data['category']
        self.name = data['name']
        self.quantity = data['quantity']
        self.price = data['price']

    def __repr__(self):
        return f'<Share : {self.quantity} of {self.name} @ {self.price}>'


def check_if_user_exists(username):
    """
        If user exists -> returns a dict
        else -> None
    """
    user = db.users.find_one({'username' : username})
    return user


def check_if_entry_exists(username, share):
    """
        None -> Not found
    """

    # Returns the portfolio in list format
    portfolio = db.users.find_one({'username' : username}, {'portfolio' : 1, '_id' : 0})['portfolio']
    
    # Returns a category in list form
    slot = None
    for category in portfolio:
        if share.category in category:
            slot = category[share.category]
            break

    # Check for share in slot
    for single_share in slot:
        if  single_share['name'] == share.name:
            return Share(single_share)

    return None

def add_new_entry(username, share):
    """ Adds new share to the list """

    q = db.users.update_one(
        {'username' : username},
        { '$push' : {
            f"portfolio.$[portfolio].{share.category}" : {
                'name' : share.name,
                'price' : share.price,
                'quantity' : share.quantity
            }
        }
        },
        array_filters=  [
                {
                    f"portfolio.{share.category}" : {
                        '$exists' : 'True'
                    }
                }
            ]
        ,
        upsert = True
    )

def sell_quantity(username, share):

    prev_share_status = check_if_entry_exists(username, share)
    prev_qty = prev_share_status.quantity

    if share.quantity > prev_qty:
        return jsonify('message : Invalid Action [Sell qty greater than holding qty]')
    
    elif share.quantity == prev_qty:
        q = db.users.update_one(
            {'username' : username},
            { '$unset' : {
                f"portfolio.$[portfolio].{data['category']}" : {
                    'name' : "",
                    'price' : "",
                    'quantity' : ""
                }
            }
            },
            array_filters=  [
                    {
                        f"portfolio.{data['category']}" : {
                            '$exists' : 'True'
                        }
                    }
                ]
            ,
            upsert = True
        )

##############################

# Add new Stock (BUY)
# Update existing Stock (BUY + average)
# Sell Existing Stock (SELL)

"""
    Structure:
{
    "action" : "sell",
    "category" : "equity",
    "name" : "AAPL",
    "price" : 200,
    "quantity" : 1
}
"""

@app.route("/all", methods = ['GET'])
def all():
    x = db.users.find({},{'_id' : 0, 'password' : 0})

    output = list()

    for e in x:
        output.append(e)
    return jsonify(output)


@app.route("/<username>", methods = ['GET'])
def single_user(username):

    user = db.users.find_one({'username' : username}, {'_id' : 0, 'password' : 0})

    if user:
        return jsonify(user), 200
    else:
        return jsonify(user), 404


@app.route('/test/<username>', methods = ['PUT'])
def modify_values(username):

    # Get Request Data
    data = request.get_json()

    # Check if exists
    # Exists if user is None
    if not check_if_user_exists(username):
        return jsonify("User does not exist")

    # Check action

    action = data['action']

    share = Share(data)
    print(share)

    if check_if_entry_exists(username, share):
        """ Average Price Or sell"""

        if action == 'buy':
            # BUY

        elif action == 'sell':
            # SEll

    else:
        """ Add new entry Or Sell Error"""
        if action == 'buy':
            add_new_entry(username, share)
        else:
            return jsonify({'message' : "Cannot Sell something you don't own!!!"})


    return jsonify("done")
    # if action == 'buy':

        #We check if entry exists or not



# @app.route("/<username>", methods = ['POST'])
# def add_new_entry(username):
#     """ Request should have:
#         0. action (buy / sell)
#         1. Category
#         2. Name
#         3. Price
#         4. Quantity
#     """
#     data = request.get_json()

#     q = db.users.update_one(
#         {'username' : username},
#         { '$push' : {
#             f"portfolio.$[portfolio].{data['category']}" : {
#                 'name' : data['name'],
#                 'price' : data['price'],
#                 'quantity' : data['quantity']
#             }
#         }
#         },
#         array_filters=  [
#                 {
#                     f"portfolio.{data['category']}" : {
#                         '$exists' : 'True'
#                     }
#                 }
#             ]
#         ,
#         upsert = True
#     )

#     return jsonify(message = "Success")


@app.route("/<username>", methods = ['PUT'])
def update_entry(username):

    data = request.get_json()

    # Get the last one

    prev = db.users.find_one({'username' : username}, {'portfolio' : 1, '_id' : 0})

    print(prev, type(prev))


    category = {}
    for entry in prev['portfolio']:    
        if data['category'] in entry:
            category = entry
            break
    
    prev_value = {}
    for share in category[data['category']]:
        if share['name'] == data['name']:
            prev_value = share
            break

    prev_total_cost = prev_value['price'] * prev_value['quantity']
    new_total_cost = data['price'] * data['quantity']

    new_quantity = data['quantity'] + prev_value['quantity']
    average_price = (new_total_cost + prev_total_cost)/new_quantity

    q = db.users.update_one(
        {'username' : username},
        { '$set' : {
            f"portfolio.$[portfolio].{data['category']}" : {
                'name' : data['name'],
                'price' : average_price,
                'quantity' : new_quantity
            }
        }
        },
        array_filters=  [
                {
                    f"portfolio.{data['category']}" : {
                        '$exists' : 'True'
                    }
                }
            ]
        ,
        upsert = True
    )



    # prev_value = prev['portfolio'][data['category']]

    return jsonify(message = "success   ")


@app.route('/test/<username>')
def test(username):

    x = db.users.find_one({'username' : username})

    print(x, type(x))

    return jsonify("ok")



if __name__ == "__main__":
    app.run(debug=True)