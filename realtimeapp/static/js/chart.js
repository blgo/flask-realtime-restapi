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

    var canvas = document.getElementById('updating-chart'),
    ctx = canvas.getContext('2d')
    var config = {
        type: 'line',
        data: {
            labels: [],
            datasets: [
            {
                label: 'A',
                yAxisID: 'A',
                fillColor: "rgba(220,220,220,0.2)",
                strokeColor: "rgba(220,220,220,1)",
                pointColor: "rgba(220,220,220,1)",
                pointStrokeColor: "#fff",
                data: []
            },
            {
                label: 'B',
                yAxisID: 'B',
                fillColor: "rgba(151,187,205,0.2)",
                strokeColor: "rgba(151,187,205,1)",
                pointColor: "rgba(151,187,205,1)",
                pointStrokeColor: "#fff",
                data: []
            }
        ]
        },
            options: {
            scales: {
                xAxes: [{
                    type: 'time',
                    ticks: {
                        autoSkip: true,
                        maxTicksLimit: 20
                    }
                }],
                yAxes: [{
                id: 'A',
                type: 'linear',
                position: 'left',
                ticks: {
                    max: 50,
                    min: 0
                }
                }, {
                id: 'B',
                type: 'linear',
                position: 'right',
                ticks: {
                    max: 100,
                    min: 0
                }
                }]
            }
            }
        }

    var myLiveChart = new Chart(ctx, config);

    socket.on('my_chart', function (msg) {
        
        config.data.labels.push(msg.label);
        config.data.datasets[0].data.push(msg.dataa);
        config.data.datasets[1].data.push(msg.datab);
        myLiveChart.update();
    });
      
});

// https://stackoverflow.com/questions/17354163/dynamically-update-values-of-a-chartjs-chart