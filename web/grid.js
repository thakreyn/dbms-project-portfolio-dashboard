// Gridjs is
// Creates a new grid object with the given data
// After that, whenever the table needs to be refreshed,
// Update table config is used
function constructTable(username) {
    grid = new gridjs.Grid({
        columns: ["Name", "Price", "Quantity"],
        // Take data from server via api call
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

        // Styling in CSS
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

// Function to update the table
// Simply calls the API for refreshed data 
// According to the category
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

// Initial Table construction
// By default : Equity
constructTable(USERNAME)

