$(document).ready(function() {
    // Use a "/test" namespace.
    // An application can open a connection on multiple namespaces, and
    // Socket.IO will multiplex all those connections on a single
    // physical channel. If you don't care about multiple channels, you
    // can set the namespace to an empty string.
    namespace = '/charts';

    // Connect to the Socket.IO server.
    // The connection URL has the following format:
    //     http[s]://<domain>:<port>[/<namespace>]
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

    // request chart data
    socket.on('connect', function() {
        socket.emit('get-data');
    });
    
    socket.on('my_response', function(msg) {
        $('#log').append('<br>' + $('<div/>').text('Received #' + msg.count + ': ' + msg.data).html());
    });

    var myLiveChart
    var config = {type: 'line'}

  
    socket.on('my_chart_init', function (msg) {

        var canvas = document.getElementById('updating-chart'),
        ctx = canvas.getContext('2d')
        config = {
            type: 'line',
            data: {
                labels: msg.label,
                datasets: [
                {
                    label: 'Temperature',
                    yAxisID: 'temperature',
                    borderColor: "#97a0cd",
                    // backgroundColor: "#97a0cd",
                    fill: false,
                    data: msg.dataa
                },
                {
                    label: 'Humidity',
                    yAxisID: 'humidity',
                    borderColor: "#cd97bb",
                    // backgroundColor: "#97bbcd",
                    fill: false,
                    data: msg.datab
                }
            ]
            },
                options: {
                title: {
                    display: true,
                    text: 'Sensor temperature and humidity'
                    },
                scales: {
                    xAxes: [{
                        type: 'time',
                        ticks: {
                            autoSkip: true,
                            maxTicksLimit: 20,
                        },
                        scaleLabel: {
                            display: true,
                            labelString: 'datetime',
                        }
                    }],
                    yAxes: [{
                    id: 'temperature',
                    type: 'linear',
                    position: 'left',
                    scaleLabel: {
                        display: true,
                        labelString: '°C',
                    },
                    ticks: {
                        max: 35,
                        min: -5
                    }
                    }, {
                    id: 'humidity',
                    type: 'linear',
                    position: 'right',
                    scaleLabel: {
                        display: true,
                        labelString: '%',
                    },
                    ticks: {
                        max: 100,
                        min: 0
                    }
                    }]
                }
                }
            }
        
        myLiveChart = new Chart(ctx, config);
    
    });
    
    socket.on('my_chart', function (msg) {
        
        config.data.labels.push(msg.label);
        config.data.datasets[0].data.push(msg.dataa);
        config.data.datasets[1].data.push(msg.datab);
        myLiveChart.update();
    });
      
    socket.on('my_chart_stats', function(msg) {
          //Build an array containing Customer records.
          var customers = new Array();
          customers.push(["Metric", "Temperature", "Humidity"]);
          customers.push(["Minimum", msg.tempmin + "°C - " + msg.tempmindate, msg.hummin + "% - " + msg.hummindate]);
          customers.push(["Maximum", msg.tempmax + "°C - " + msg.tempmaxdate, msg.hummax + "% - " + msg.hummaxdate]);
          customers.push(["Mean", msg.tempmean, msg.hummean]);
          customers.push(["Median", msg.tempmedian, msg.hummedian]);
   
          //Create a HTML Table element.
          var table = $("<table />");
          table[0].border = "1";
   
          //Get the count of columns.
          var columnCount = customers[0].length;
   
          //Add the header row.
          var row = $(table[0].insertRow(-1));
          for (var i = 0; i < columnCount; i++) {
              var headerCell = $("<th />");
              headerCell.html(customers[0][i]);
              row.append(headerCell);
          }
   
          //Add the data rows.
          for (var i = 1; i < customers.length; i++) {
              row = $(table[0].insertRow(-1));
              for (var j = 0; j < columnCount; j++) {
                  var cell = $("<td />");
                  cell.html(customers[i][j]);
                  row.append(cell);
              }
          }
   
          var dvTable = $("#statistics");
          dvTable.html("");
          dvTable.append(table);
    });

    socket.on('last_reading', function(msg) {
        $('#last-reading').text(msg.label + ", " +  msg.dataa + " °C - " +  msg.datab + " %"  );
    });


});

// https://stackoverflow.com/questions/17354163/dynamically-update-values-of-a-chartjs-chart
