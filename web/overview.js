// Utility Function to create a GET api call
async function getUserData(url = '') {
    const response = await fetch(
        url,
        {
            method: 'GET'
        }
    );

    return response.json();
}

// Responsible for Overview 'view'
// Calculates statistics for a given username and
// Finally calls make chart for the overview chart
async function callOverview() {
    var userData = "apple"

    await getUserData('http://127.0.0.1:5000/' + USERNAME)
        .then(data => (userData = data))

    // console.log((userData))
    totalAmount = 0

    categoryAmount = {
        'equity': 0,
        'crypto': 0,
        'etf': 0,
        'cash': 0
    }

    for (category in userData.portfolio) {
        for (list in userData.portfolio[category]) {
            // console.log(list, userData.portfolio[category][list])
            item = userData.portfolio[category][list]
            totalAmount += item.price * item.quantity
            categoryAmount[category] += item.price * item.quantity
        }
    }
    
    // Sets overview text in the div
    generateOverviewText(totalAmount, categoryAmount)

    data = []

    for (category in categoryAmount) {
        temp = { y: (categoryAmount[category] / totalAmount) * 100, label: category==='cash'?'commodity':category }
        data.push(temp)
    }

    // Send cateegory data to make chart to render chart
    makeChart(data, "Overview")
}


// Function for generating User summary/overview
// Takes in statistics calculated in callOverview
function generateOverviewText(totalAmount, categoryAmount) {

    document.getElementById("wrapper2").innerHTML =
    `
    <h1>Summary for ${USERNAME} </h1>
            <br>    
            <div class = "overview-indent">
            <h3>Equity Amount : ${Math.round(categoryAmount.equity * 100) / 100}</h3>
            <h3>Crypto Amount : ${Math.round(categoryAmount.crypto * 100) / 100}</h3>
            <h3>ETF Amount : ${Math.round(categoryAmount.etf * 100) / 100}</h3>
            <br>
            <h3>Total Amount : ${totalAmount}</h3>
            </div>
    `
}