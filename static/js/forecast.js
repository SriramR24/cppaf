
      var endpoint = 'forecast/api';

//      var $goldChart = $("#gold-forecast-api");

      $.ajax({
        method: "GET",
        url: endpoint,
        success: function (data) {

            console.log(data);

            drawPredictGraph(data.predict_data, 'predict-line');
            drawRSIGraph(data.rsi_data, 'rsi-line');

        },
        error: function(error_data) {
            console.log(error_data);
        }
        })


        function drawPredictGraph(data, id) {

          var ctx1 = document.getElementById(id).getContext("2d");

          var chart = new Chart(ctx1, {
            type: 'line',
            data: {
              labels: data.labels,
              datasets: [{
                label: 'Gold',
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
                label: 'Gold',
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