function openForm() {
    document.getElementById("myForm").style.display = "block";
    document.getElementById("dark").style.display = "block";
}

function closeForm() {
    document.getElementById("myForm").style.display = "none";
    document.getElementById("dark").style.display = "none";
}

function showOverview() {
    document.getElementById("wrapper").style.display = "none";
    document.getElementById("wrapper2").style.display = "flex";
}

function hideOverview() {
    document.getElementById("wrapper").style.display = "flex";
    document.getElementById("wrapper2").style.display = "none";
}

function handleSubmit(event) {
    event.preventDefault();

    const data = new FormData(event.target);

    const name = data.get('name')
    const category = data.get('category')
    const quantity = data.get('quantity')
    const price = data.get('price')
    const action = data.get('action')

    output = {
        name: name,
        category: category === 'commodity'?'cash':category,
        quantity: quantity,
        price: price,
        action: action
    }

    putNewHolding(USERNAME, output)
        .then((data) => {
            if (typeof(data.message) === 'string')
                alert(data.message)
            else
                alert(data.message.category)

            closeForm()
            callOverview()
            generateTable(USERNAME)
        })

    

}

// Posts the given data to the api
async function putNewHolding(username, data = {}) {
    const response = await fetch(
        'http://127.0.0.1:5000/' + username + '/holdings',
        {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        }
    );

    return response.json()
}
