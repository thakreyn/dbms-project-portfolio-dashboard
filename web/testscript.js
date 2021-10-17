document.getElementById("overview-btn").addEventListener('click', function () {
    callOverview()
    showOverview()
});

document.getElementById("equity-btn").addEventListener('click', function () {
    hideOverview()
    generateTable(USERNAME, 'equity')
    categoryChart('equity') 
});

document.getElementById("crypto-btn").addEventListener('click', function () {
    hideOverview()
    generateTable(USERNAME, 'crypto')
    categoryChart('crypto')
});

document.getElementById("etf-btn").addEventListener('click', function () {
    hideOverview()
    generateTable(USERNAME, 'etf')
    categoryChart('etf')
});

document.getElementById("cash-btn").addEventListener('click', function () {
    hideOverview()
    generateTable(USERNAME, 'cash')
    categoryChart('cash')
});


const form = document.querySelector('form');
form.addEventListener('submit', handleSubmit);


//////////////////////////////////////////////////////////
const USERNAME = 'thakreyn'
//////////////////////////////////////////////////////////




function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function makeChart(data, categoryName) {
    categoryName = capitalizeFirstLetter(categoryName)
    var chart = new CanvasJS.Chart("chartContainer", {
        animationEnabled: true,
        theme: "dark1",
        title:{
            text: categoryName==='Cash'?'Commodity':categoryName,
            horizontalAlign: "center",
            fontFamily: "tahoma",
            fontSize : 30
        },
        data: [{
            type: "doughnut",
            startAngle: 60,
            innerRadius: 115,
            indexLabelFontSize: 17,
            indexLabel: "{label} - #percent%",
            toolTipContent: "<b>{label}:</b> {y} (#percent%)",
            dataPoints: data
        }]
    });
    chart.render();
}

async function categoryChart(categoryName){
    userData = ''

    await getUserData('http://127.0.0.1:5000/' + USERNAME)
        .then(data => (userData = data))


    category = userData.portfolio[categoryName]

    categoryTotal = 0

    for (item in category){
        categoryTotal += category[item].price * category[item].quantity
    }

    data = []

    for (item in category){
        temp = {y : ((category[item].price * category[item].quantity)/categoryTotal) * 100 , label : category[item].name}
        data.push(temp)
    }

    // console.log(data)
    makeChart(data, categoryName)

}

callOverview()
showOverview()