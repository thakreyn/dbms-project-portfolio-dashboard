function constructTable(username) {
    grid = new gridjs.Grid({
        columns: ["Name", "Price", "Quantity"],
        server: {
            url: 'http://127.0.0.1:5000/' + username,
            then: data => Object.values(data.portfolio.equity).map(movie =>
                [movie.name, Math.round(movie.price * 100) / 100, movie.quantity]
            )
        },
        pagination: {
            enabled: true,
            limit: 5,
            summary: true
        },
        sort: true,

        style: {
            table: {
                border: '0 px solid black',
            },

            th: {
                'background-color': 'rebeccapurple',
                'color': 'white',
                border: '1 px solid rebeccapurple',
                border: '0 px solid black'
            },

            td: {
                'background-color': '#171A22',
                border: '0 px solid black'
            },

            footer: {
                'background-color': '#171A22',
                border: '0 px solid black',
                color: 'white'
            }
        }

    }).render(document.getElementById("wrapper"));

}

function generateTable(username, category = 'equity') {

    {
        grid.updateConfig({
            server: {
                url: 'http://127.0.0.1:5000/' + USERNAME,
                then: data => Object.values(data.portfolio[category]).map(movie =>
                    [movie.name, Math.round(movie.price * 100) / 100, movie.quantity]
                )
            }
        }).forceRender();
    }

}

constructTable(USERNAME)

