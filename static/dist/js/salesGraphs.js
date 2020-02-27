var ctxB = document.getElementById('salesBarChart').getContext('2d');
var chartBar = new Chart(ctxB, {
    type: 'bar',
    data: {
        labels: ['란스톤', '놀텍', '판토록', '덱실란트디알'],
        datasets: [{
            label: 'Sales in 억원',
            data: [2.4, 1.8, 1.7, 1.4],
            backgroundColor: [
                'rgba(10,0,203,0.55)',
                'rgba(194,41,67,0.56)',
                'rgba(185,186,78,0.73)',
                'rgba(13,184,22,0.82)'
            ],
            borderColor: [
                'rgba(10,0,203,0.82)',
                'rgba(191,35,59,0.56)',
                'rgba(185,186,78,0.78)',
                'rgba(13,174,21,0.88)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                }
            }]
        }
    }
});

//doughnut
var ctxD = document.getElementById("salesPieChart").getContext('2d');
var myLineChart = new Chart(ctxD, {
    type: 'doughnut',
    data: {
        labels: ['란스톤', '놀텍', '판토록', '덱실란트디알'],
        datasets: [{
            data: [2.4, 1.8, 1.7, 1.4],
            backgroundColor: ["#F7464A", "#46BFBD", "#FDB45C", "#949FB1", "#4D5360"],
            hoverBackgroundColor: ["#FF5A5E", "#5AD3D1", "#FFC870", "#A8B3C5", "#616774"]
        }]
    },
    options: {
        responsive: true
    }
});

//line
var ctxL = document.getElementById("salesLineChart").getContext('2d');
var myLineChart = new Chart(ctxL, {
    type: 'line',
    data: {
        labels: ["2019년11월", "2019년12월", "2020년01월"],
        datasets: [{
            label: '란스톤',
            data: [2.4, 3.1, 1.9],
            backgroundColor: [
                'rgba(105, 0, 132, .2)',
            ],
            borderColor: [
                'rgba(200, 99, 132, .7)',
            ],
            borderWidth: 2
        },
            {
                label: '놀텍',
                data: [1.2, 1.7, 2.9],
                backgroundColor: [
                    'rgba(0, 137, 132, .2)',
                ],
                borderColor: [
                    'rgba(0, 10, 130, .7)',
                ],
                borderWidth: 2
            }
        ]
    },
    options: {
        responsive: true
    }
});