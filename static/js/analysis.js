
    var endpoint = 'analysis/api';

    $.ajax({
    method: "GET",
    url: endpoint,
    success: function(data) {
        console.log(data);

        drawCloseGraph(data.close_data, 'close-line');
        drawVolumeGraph(data.volume_data, 'volume-bar');
        drawVolatileGraph(data.volatile_data, 'volatile-line');
        drawCumulativeGraph(data.cumulative_data, 'cumulative-line');
    },
    error: function(error_data) {
        console.log(error_data);
    }
    })


    function drawCloseGraph(data, id) {
        var labels = data.labels;
        var chartLabel = data.chartLabel;
        var chartdata = data.chartdata;
        var ctx1 = document.getElementById(id).getContext('2d');
        var chart = new Chart(ctx1, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: chartLabel,
                    lineTension: 0.3,
                    backgroundColor: "rgba(78, 115, 223, 0.05)",
                    borderColor: "rgba(78, 115, 223, 1)",
                    pointRadius: 1.25,
                    pointBackgroundColor: "rgba(78, 115, 223, 1)",
                    pointBorderColor: "rgba(78, 115, 223, 1)",
                    pointHoverRadius: 3,
                    pointHoverBackgroundColor: "rgba(78, 115, 223, 1)",
                    pointHoverBorderColor: "rgba(78, 115, 223, 1)",
                    pointHitRadius: 10,
                    pointBorderWidth: 2,
                    data: chartdata,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                layout: {
                    padding: {
                        left: 10,
                        right: 25,
                        top: 25,
                        bottom: 0
                    }
                },
                legend: {
                   display: false
                },
                scales: {
                    xAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: 'Date',
                            fontColor: "rgba(78, 115, 223, 1)",
                            fontSize: 15,
                            padding: {
                                top: 20,
                            },
                        },
                        display: true,
                        ticks: {
                            maxTicksLimit: 10,
                        }
                    }],
                    yAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: 'Price in USD($)',
                            fontColor: "rgba(78, 115, 223, 1)",
                            fontSize: 15,
                            padding: {
                                bottom: 20,
                            },
                        },
                        ticks: {
                            beginAtZero: false
                        }
                    }]
                }
            }
        });
    }

    function drawVolumeGraph(data, id) {
        var labels = data.labels;
        var chartLabel = data.chartLabel;
        var chartdata = data.chartdata;
        var ctx2 = document.getElementById(id).getContext('2d');
        var myChart = new Chart(ctx2, {
            type: 'bar',
            data: {
            labels: labels,
            datasets: [{
                label: chartLabel,
                data: chartdata,
                backgroundColor: 'rgb(80, 200, 200)',
                borderColor: 'rgb(55, 99, 132)',
                hoverBackgroundColor: 'rgb(60, 99, 132)',
                borderWidth: 1,
                barThickness: 30,
            }]
            },
            options: {
            maintainAspectRatio: false,
            layout: {
                padding: {
                    left: 10,
                    right: 25,
                    top: 25,
                    bottom: 0
                }
            },
            responsive: true,
            legend: {
               display: false
            },
            scales: {
                xAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Date',
                        fontColor: "rgb(55, 99, 132)",
                        fontSize: 15,
                        padding: {
                            top: 20,
                        },
                    },
                    display: true,
                    ticks: {
                        maxTicksLimit: 10,
                    }
                }],
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Price in USD($)',
                        fontColor: "rgb(55, 99, 132)",
                        fontSize: 15,
                        padding: {
                            bottom: 20,
                        },
                    },
                }]
            }
            }
        });
    }

    function drawVolatileGraph(data, id) {
        var labels = data.labels;
        var chartLabel = data.chartLabel;
        var chartdata = data.chartdata;
        var ctx3 = document.getElementById(id).getContext('2d');
        var chart = new Chart(ctx3, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: chartLabel,
                    lineTension: 0.3,
                    backgroundColor: "rgba(78, 115, 223, 0.05)",
                    borderColor: 'rgba(255, 100, 100, 1)',
                    pointRadius: 1.25,
                    pointBackgroundColor: "rgba(78, 115, 223, 1)",
                    pointBorderColor: "rgba(78, 115, 223, 1)",
                    pointHoverRadius: 3,
                    pointHoverBackgroundColor: "rgba(78, 115, 223, 1)",
                    pointHoverBorderColor: "rgba(78, 115, 223, 1)",
                    pointHitRadius: 10,
                    pointBorderWidth: 2,
                    data: chartdata,
                    fill: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                layout: {
                    padding: {
                        left: 10,
                        right: 25,
                        top: 25,
                        bottom: 0
                    }
                },
                legend: {
                   display: false
                },
                scales: {
                    xAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: 'Date',
                            fontColor: "rgba(255, 100, 100, 1)",
                            fontSize: 15,
                            padding: {
                                top: 20,
                            },
                        },
                        display: true,
                        ticks: {
                            maxTicksLimit: 10,
                        }
                    }],
                    yAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: 'Daily Simple Returns',
                            fontColor: "rgba(255, 100, 100, 1)",
                            fontSize: 15,
                            padding: {
                                bottom: 20,
                            },
                        },
                        ticks: {
                            beginAtZero: false
                        }
                    }]
                }
            }
        });
    }

    function drawCumulativeGraph(data, id) {
        var labels = data.labels;
        var chartLabel = data.chartLabel;
        var chartdata = data.chartdata;
        var ctx4 = document.getElementById(id).getContext('2d');
        var chart = new Chart(ctx4, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: chartLabel,
                    lineTension: 0.3,
                    backgroundColor: "rgba(78, 115, 223, 0.05)",
                    borderColor: "green",
                    pointRadius: 1.25,
                    pointBackgroundColor: 'rgba(255, 100, 100, 1)',
                    pointBorderColor: 'rgb(55, 99, 132)',
                    pointHoverRadius: 3,
                    pointHoverBackgroundColor: 'rgba(255, 100, 100, 1)',
                    pointHoverBorderColor: 'rgba(255, 100, 100, 1)',
                    pointHitRadius: 10,
                    pointBorderWidth: 2,
                    data: chartdata,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                layout: {
                    padding: {
                        left: 10,
                        right: 25,
                        top: 25,
                        bottom: 0
                    }
                },
                legend: {
                   display: false
                },
                scales: {
                    xAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: 'Date',
                            fontColor: "rgba(78, 115, 223, 1)",
                            fontSize: 15,
                            padding: {
                                top: 20,
                            },
                        },
                        display: true,
                        ticks: {
                            maxTicksLimit: 10,
                        }
                    }],
                    yAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: 'Growth of $1 investment',
                            fontColor: "rgba(78, 115, 223, 1)",
                            fontSize: 15,
                            padding: {
                                bottom: 20,
                            },
                        },
                        ticks: {
                            beginAtZero: false
                        }
                    }]
                }
            }
        });
    }

