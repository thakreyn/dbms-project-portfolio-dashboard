// Utility functions to show and hide divs / elements on trigger

// Order Form
function openForm() {
    document.getElementById("myForm").style.display = "block";
    document.getElementById("dark").style.display = "block";
}

// Order Form
function closeForm() {
    document.getElementById("myForm").style.display = "none";
    document.getElementById("dark").style.display = "none";
}

// Overview Div
function showOverview() {
    document.getElementById("wrapper").style.display = "none";
    document.getElementById("wrapper2").style.display = "flex";
}

// Overview Div
function hideOverview() {
    document.getElementById("wrapper").style.display = "flex";
    document.getElementById("wrapper2").style.display = "none";
}

// Take in form data and convert to suitable JSON 
// which is then passed on to the API for PUT request
function handleSubmit(event) {
    event.preventDefault();

    const data = new FormData(event.target);

    // Form fields
    const name = data.get('name')
    const category = data.get('category')
    const quantity = data.get('quantity')
    const price = data.get('price')
    const action = data.get('action')

    // Mapping form to JSON
    output = {
        name: name,
        category: category === 'commodity'?'cash':category,
        quantity: quantity,
        price: price,
        action: action
    }

    // Calling PUT request with above data
    putNewHolding(USERNAME, output)
        .then((data) => {
            // Check response for success message or error object
            if (typeof(data.message) === 'string')
                alert(data.message)
            else
                alert(data.message.category)

            // Close form
            closeForm()
            // Show Overview page and refresh
            callOverview()
            // Generate and refresh table
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
