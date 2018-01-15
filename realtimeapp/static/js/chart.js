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
                label: 'Temperature',
                yAxisID: 'temperature',
                borderColor: "#97a0cd",
                // backgroundColor: "#97a0cd",
                fill: false,
                data: []
            },
            {
                label: 'Humidity',
                yAxisID: 'humidity',
                borderColor: "#cd97bb",
                // backgroundColor: "#97bbcd",
                fill: false,
                data: []
            }
        ]
        },
            options: {
            title: {
                display: true,
                text: 'Sensor1 temperature and humidity'
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
                    max: 25,
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

    var myLiveChart = new Chart(ctx, config);

    socket.on('my_chart', function (msg) {
        
        config.data.labels.push(msg.label);
        config.data.datasets[0].data.push(msg.dataa);
        config.data.datasets[1].data.push(msg.datab);
        myLiveChart.update();
    });
      
});

// https://stackoverflow.com/questions/17354163/dynamically-update-values-of-a-chartjs-chart