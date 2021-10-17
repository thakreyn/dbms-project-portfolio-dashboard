function chartFunction(sampleData) {
    console.log(sampleData)
    var chart = new CanvasJS.Chart("chartContainer", {
        animationEnabled: true,
        title: {
            text: "ANY"
        },
        data: [{
            type: "pie",
            startAngle: 240,
            yValueFormatString: "##0.00\"%\"",
            indexLabel: "{label} {y}",
            dataPoints: sampleData
        }]
    });
    chart.render();

}

async function getUserData(url = '') {
    const response = await fetch(
        url,
        {
            method: 'GET'
        }
    );

    return response.json();
}

function genChart() {
    getUserData('http://127.0.0.1:5000/thakreyn')
        .then(data => data.portfolio.crypto)
        .then(data => chartFunction(data))
}
