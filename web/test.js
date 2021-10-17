const url = 'http://127.0.0.1:5000/thakreyn'

// User functions
async function getUserData(url = '') {
  const response = await fetch(
    url , 
    {
      method : 'GET'
    }
  );

  return response.json();
}

async function postNewUser(username = 'all', data = {}) {
  const response = await fetch(
    'http://127.0.0.1:5000/' + username,
    {
      method : 'POST',
      headers : {
        'Content-Type' : 'application/json'
      },
      body : JSON.stringify(data)
    }
  );

  return response.json();
}

async function deleteNewUser(username = 'all', data = {}) {
  const response = await fetch(
    'http://127.0.0.1:5000/' + username,
    {
      method : 'DELETE',
      headers : {
        'Content-Type' : 'application/json'
      },
      body : JSON.stringify(data)
    }
  );

  return response.json();
}

getUserData(url)
.then(data => {
  console.log(Object.values(data.portfolio.equity))
})


// postNewUser('rinzller', {
//   "fullname" : "rinzller",
//   "username" : "rinzller",
//   "password" : "rinzllerpass"
// })
// .then(data => console.log(data))

// deleteNewUser('rinzller', {
//   "fullname" : "rinzller",
//   "username" : "rinzller",
//   "password" : "rinzllerpass"
// })
// .then(data => console.log(data))

// Holdings

async function postNewHolding(username, data = {}) {
  const response = await fetch(
    'http://127.0.0.1:5000/' + username + '/holdings',
    {
      method : 'POST',
      headers : {
        'Content-Type' : 'application/json'
      },
      body : JSON.stringify(data)
    }
  );

  return response.json();
}

async function putNewHolding(username, data = {}) {
  const response = await fetch (
    'http://127.0.0.1:5000/' + username + '/holdings',
    {
      method : 'PUT',
      headers : {
        'Content-Type' : 'application/json'
      },
      body : JSON.stringify(data)
    }
  );

  return response.json()
}

// putNewHolding('thakreyn' , {
//   "name" : "AAPL EF",
//   "category" : "equity",
//   "action" : "sell",
//   "quantity" : 10,
//   "price" : 3000
// })
// .then(data => console.log(data))  

// postNewHolding('thakreyn', {
//   "name" : "AAPL EF",
//   "category" : "etf",
//   "action" : "buy",
//   "quantity" : 1000,
//   "price" : 1500
// })
// .then(data => console.log(data))