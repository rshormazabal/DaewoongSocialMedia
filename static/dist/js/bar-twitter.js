
$.getJSON("/data/keywords_twitter", function (json) {
    var words = json.map(function (item) {
        return item.Word;
    });

    var importance = json.map(function (item) {
        return item.Importance;
    });

    console.log(words);

    var ctxB = document.getElementById('myBarChart').getContext('2d');
    var chartBar = new Chart(ctxB, {
        type: 'bar',
        data: {
            labels: words,
            datasets: [{
                label: '단어 중요성',
                data: importance,
                backgroundColor: [
                    'rgba(10,0,203,0.55)',
                    'rgba(194,41,67,0.56)',
                    'rgba(85,186,132,0.73)',
                    'rgba(13,184,22,0.82)',
                    'rgba(203,48,176,0.55)',
                    'rgba(194,41,67,0.56)',
                    'rgba(185,186,78,0.73)',
                    'rgba(13,184,22,0.82)',
                    'rgba(185,186,78,0.73)',
                    'rgba(217,54,61,0.82)'
                ],
                borderColor: [
                    'rgba(10,0,203,0.82)',
                    'rgba(191,35,59,0.56)',
                    'rgba(185,186,78,0.78)',
                    'rgba(13,174,21,0.88)',
                    'rgba(203,47,126,0.82)',
                    'rgba(191,35,59,0.56)',
                    'rgba(185,186,78,0.78)',
                    'rgba(228,48,64,0.88)',
                    'rgba(39,54,174,0.88)',
                    'rgba(32,213,54,0.88)'
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
})