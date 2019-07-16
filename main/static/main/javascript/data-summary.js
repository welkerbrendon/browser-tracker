window.onload = getGraphs;

function getGraphs() {
    var pieChartOverallCanvasContext = document.getElementById("pie-chart-overall").getContext("2d");
    var pieChartProductiveCanvasContext = document.getElementById("pie-chart-productive").getContext("2d");
    var pieChartUnproductiveCanvasContext = document.getElementById("pie-chart-unproductive").getContext("2d");
    var barGraphCanvasContext = document.getElementById("bar-graph").getContext("2d");
    var lineGraphCanvasContext = document.getElementById("line-graph").getContext("2d");

    $.get("/main/data-summary/raw-data", {}, function (result, status) {
        if (status == "success") {
            console.log(JSON.stringify(result));
            const pieChartDataJSON = result.pie_chart_data;
            const barGraphDataJSON = result.bar_graph;
            const lineGraphDataJSON = result.line_graph;
            const productivePieChartDataJSON = result.productive_pie_chart_data;
            const unproductivePieChartDataJSON = result.unproductive_pie_chart_data;

            var pieChartDataset = getData(pieChartDataJSON);
            var barGraphDataset = getData(barGraphDataJSON);
            var lineGraphDataset = getData(lineGraphDataJSON);
            var productivePieChartDataset = getData(productivePieChartDataJSON);
            var unproductivePidChartDataset = getData(unproductivePieChartDataJSON);

            var overallPieChart = new Chart(pieChartOverallCanvasContext, {
                type: 'pie',
                data: {
                    labels: Object.keys(pieChartDataJSON),
                    datasets: [ {
                        data: pieChartDataset
                    }]
                },
                options: {
                    title: {
                        display: true,
                        text: "Websites Visted"
                    },
                    legend: {
                        display: true,
                        position: 'right'
                    }
                }
            });
        }
        else {
            console.log(status);
        }
    });
}

function getData(dataJSON) {
    dataset = []
    for (var key in dataJSON) {
        dataset.append(dataJSON[key]);
    }
    return dataset;
}