var ctxL = document.getElementById("myAreaChart").getContext('2d');
var myLineChart = new Chart(ctxL, {
    type: 'line',
    data: {
        labels: ["2019년8월", "2019년9월", "2020년10월", "2019년11월", "2019년12월", "2020년1월", "2020년2월"],
        datasets: [{
            label: '유튜브',
            data: [143, 12, 159, 41, 243, 160, 41],
            backgroundColor: [
                'rgba(105, 0, 132, .2)',
            ],
            borderColor: [
                'rgba(200, 99, 132, .7)',
            ],
            borderWidth: 2
        },
            {
                label: '인스타그램',
                data: [88, 57, 161, 85, 112, 36, 151],
                backgroundColor: [
                    'rgba(217,216,73,0.2)',
                ],
                borderColor: [
                    'rgba(200,95,88,0.7)',
                ],
                borderWidth: 2
            },
            {
                label: '트위터',
                data: [162, 291, 112, 165, 199, 241, 160],
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