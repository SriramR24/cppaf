
      var endpoint = 'forecast/api';

//      var $goldChart = $("#gold-forecast-api");

      $.ajax({
        method: "GET",
        url: endpoint,
        success: function (data) {

            console.log(data);

//            drawPredictGraph(data.predict_data, 'predict-line');
            drawRSIGraph(data.rsi_data, 'rsi-line');
            drawMACDGraph(data.macd_data, 'macd-line')
            drawBuySellGraph(data.buysell_data, 'buysell-line')

        },
        error: function(error_data) {
            console.log(error_data);
        }
        })

        Chart.defaults.global.legend.labels.usePointStyle = true;

        function drawPredictGraph(data, id) {

          var ctx1 = document.getElementById(id).getContext("2d");

          var chart = new Chart(ctx1, {
            type: 'line',
            data: {
              labels: data.labels,
              datasets: [{
                label: '',
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
                data: data.data,
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
                    display: true,
                    ticks: {
                        maxTicksLimit: 15,
                    }
                }]
              }
            }
          });
        }

        function drawRSIGraph(data, id) {

          var ctx2 = document.getElementById(id).getContext("2d");

          var chart = new Chart(ctx2, {
            type: 'line',
            data: {
              labels: data.labels,
              datasets: [{
                label: 'Close price',
                lineTension: 0.3,
                backgroundColor: "rgba(78, 115, 223, 0.05)",
                borderColor: "rgba(102, 115, 223, 1)",
                borderWidth: 5,
                pointRadius: 1.25,
                pointBackgroundColor: "rgba(78, 115, 223, 1)",
                pointBorderColor: "rgba(78, 115, 223, 1)",
                pointHoverRadius: 3,
                pointHoverBackgroundColor: "orange",
                pointHoverBorderColor: "orange",
                pointHitRadius: 10,
                pointBorderWidth: 2,
                data: data.data,
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
              scales: {
                xAxes: [{
                    display: true,
                    ticks: {
                        maxTicksLimit: 15,
                    }
                }],
                yAxes: [{
                    gridLines: {
                        display: true,
                        color: [
                            'gray',
                            'orange',
                            'green',
                            'red',
                            'Chart.defaults.borderColor',
                            'Chart.defaults.borderColor',
                            'Chart.defaults.borderColor',
                            'red',
                            'green',
                            'orange',
                            'gray',
                        ],
                        lineWidth: 2.5,
                        borderDash: [10,15],
                    },
                    ticks: {
                        beginAtZero: true
                    }
                }]
              }
            }
          });
        }

        function drawMACDGraph(data, id) {
            var ctx3 = document.getElementById(id).getContext("2d");

          var chart = new Chart(ctx3, {
            type: 'line',
            data: {
              labels: data.labels,
              datasets: [
                  {
                    label: 'MACD',
                    lineTension: 1,
                    backgroundColor: "rgba(78, 115, 223, 0.05)",
                    borderColor: "red",
                    borderWidth: 4.5,
                    pointRadius: 0.5,
                    pointBackgroundColor: "rgba(78, 115, 223, 1)",
//                    pointBorderColor: "rgba(78, 115, 223, 1)",
                    pointHoverRadius: 3,
                    pointHoverBackgroundColor: "rgba(78, 115, 223, 1)",
                    pointHoverBorderColor: "rgba(78, 115, 223, 1)",
                    pointHitRadius: 10,
                    pointBorderWidth: 2,
                    data: data.data.macd,
//                    hidden: true,
                  },
                  {
                    label: 'Signal Line',
                    lineTension: 1,
                    backgroundColor: "rgba(78, 115, 223, 0.05)",
                    borderColor: "blue",
                    borderWidth: 4.5,
                    pointRadius: 0.5,
                    pointBackgroundColor: "rgba(78, 115, 223, 1)",
//                    pointBorderColor: "rgba(78, 115, 223, 1)",
                    pointHoverRadius: 3,
                    pointHoverBackgroundColor: "red",
                    pointHoverBorderColor: "red",
                    pointHitRadius: 10,
                    pointBorderWidth: 2,
                    data: data.data.signal,
                  }
              ]
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
                display: true
              },
              scales: {
                xAxes: [{
                    display: true,
                    ticks: {
                        maxTicksLimit: 15,
                    }
                }],
                yAxes: [{
                    ticks: {
                        beginAtZero: false
                    }
                }]
              }
            }
          });
        }

        function drawBuySellGraph(data, id) {

            var ctx4 = document.getElementById(id).getContext("2d");

          var chart = new Chart(ctx4, {
            type: 'line',
            data: {
              labels: data.labels,
              datasets: [

                  {
                    label: 'Buy',
                    lineTension: 1,
                    backgroundColor: "rgba(78, 115, 223, 0.05)",
                    borderColor: "green",
                    borderWidth: 4.5,
                    pointRadius: 3.5,
                    pointStyle: 'triangle',
                    pointBackgroundColor: "green",
//                    pointBorderColor: "rgba(78, 115, 223, 1)",
                    pointHoverRadius: 9,
                    pointHoverBackgroundColor: "green",
                    pointHoverBorderColor: "green",
                    pointHitRadius: 10,
                    pointBorderWidth: 2,
                    data: data.data.buy,
                  },
                  {
                    label: 'Sell',
                    lineTension: 1,
                    backgroundColor: "rgba(78, 115, 223, 0.05)",
                    borderColor: "red",
                    borderWidth: 4.5,
                    pointRadius: 3.5,
                    pointStyle: 'triangle',
                    rotation: 60,
                    pointBackgroundColor: "red",
//                    pointBorderColor: "rgba(78, 115, 223, 1)",
                    pointHoverRadius: 9,
                    pointHoverBackgroundColor: "red",
                    pointHoverBorderColor: "red",
                    pointHitRadius: 10,
                    pointBorderWidth: 2,
                    data: data.data.sell,
                  },
                  {
                    label: 'Close price',
                    lineTension: 1,
                    backgroundColor: "rgba(78, 115, 223, 0.05)",
                    borderColor: "lightblue",
                    borderWidth: 4,
                    pointRadius: 0.5,
                    pointBackgroundColor: "rgba(78, 115, 223, 1)",
//                    pointBorderColor: "rgba(78, 115, 223, 1)",
                    pointHoverRadius: 3,
                    pointHoverBackgroundColor: "rgba(78, 115, 223, 1)",
                    pointHoverBorderColor: "rgba(78, 115, 223, 1)",
                    pointHitRadius: 10,
                    pointBorderWidth: 2,
                    data: data.data.close,
//                    hidden: true,
                  },
              ]
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
                display: true
              },
              scales: {
                xAxes: [{
                    display: true,
                    ticks: {
                        maxTicksLimit: 15,
                    }
                }],
                yAxes: [{
                    ticks: {
                        beginAtZero: false
                    }
                }]
              }
            }
          });
        }
