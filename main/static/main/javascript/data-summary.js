window.onload = getGraphs;

// const darkerBackgroundColors = [
    
// ]

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

            const ligtBackgroundColors = [
                "rgb(114, 147, 203)",
                "rgb(225, 151, 76)",
                "rgb(132, 186, 91)",
                "rgb(211, 94, 96)",
                "rgb(128, 133, 133)",
                "rgb(144, 103, 167)",
                "rgb(171, 104, 87)",
                "rgb(204, 194, 16)"
            ];

            const darkerBackgroundColors = [
                "rgb(57, 106, 177)",
                "rgb(218, 124, 48)",
                "rgb(62, 150, 81)",
                "rgb(204, 37, 41)",
                "rgb(83, 81, 84)",
                "rgb(107, 76, 154)",
                "rgb(146, 36, 40)",
                "rgb(148, 139, 61)"
            ];

            new Chart(pieChartOverallCanvasContext, {
                type: 'pie',
                data: {
                    labels: Object.keys(pieChartDataJSON),
                    datasets: [ {
                        data: pieChartDataset
                    }],
                },
                options: {
                    title: {
                        display: true,
                        text: "Websites Visted"
                    },
                    legend: {
                        display: true,
                        position: 'right'
                    },
                    plugins: {
                        colorschemes: {
                            scheme: 'tableau.Classic20'
                        }
                    }
                }
            });

            new Chart(barGraphCanvasContext, {
                type: 'bar',
                data: {
                    labels: Object.keys(barGraphDataJSON),
                    datasets: [ {
                        data: barGraphDataset
                    }],
                },
                options: {
                    title: {
                        display: true,
                        text: "Daily Internet Usage"
                    },
                    plugins: {
                        colorschemes: {
                            scheme: 'brewer.SetOne7'
                        }
                    },
                    scales: {
                        yAxes: [{
                            scaleLabel: {
                                display: true,
                                labelString: "Average Hours"
                            }
                        }]
                    }
                }
            });

            new Chart(pieChartOverallCanvasContext, {
                type: 'pie',
                data: {
                    labels: Object.keys(pieChartDataJSON),
                    datasets: [ {
                        data: pieChartDataset
                    }],
                },
                options: {
                    title: {
                        display: true,
                        text: "Websites Visted"
                    },
                    legend: {
                        display: true,
                        position: 'right'
                    },
                    plugins: {
                        colorschemes: {
                            scheme: 'tableau.Classic20'
                        }
                    }
                }
            });

            new Chart(pieChartOverallCanvasContext, {
                type: 'pie',
                data: {
                    labels: Object.keys(pieChartDataJSON),
                    datasets: [ {
                        data: pieChartDataset
                    }],
                },
                options: {
                    title: {
                        display: true,
                        text: "Websites Visted"
                    },
                    legend: {
                        display: true,
                        position: 'right'
                    },
                    plugins: {
                        colorschemes: {
                            scheme: 'tableau.Classic20'
                        }
                    }
                }
            });

            new Chart(pieChartOverallCanvasContext, {
                type: 'pie',
                data: {
                    labels: Object.keys(pieChartDataJSON),
                    datasets: [ {
                        data: pieChartDataset
                    }],
                },
                options: {
                    title: {
                        display: true,
                        text: "Websites Visted"
                    },
                    legend: {
                        display: true,
                        position: 'right'
                    },
                    plugins: {
                        colorschemes: {
                            scheme: 'tableau.Classic20'
                        }
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
        dataset.push(dataJSON[key]);
    }
    return dataset;
}