// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

$.getJSON("/data_tags", function (json) {
  var labels = json.map(function(item) {
    return item.Tag;
  });
  var counts = json.map(function(item) {
    return item.Posts;
  });

  // Bar Chart Example
  var ctx = document.getElementById("myBarChart");
  var myLineChart = new Chart(ctx, {
    type: 'horizontalBar',
    data: {
      labels: labels,
      datasets: [{
        label: "Posts",
        backgroundColor: "rgba(2,117,216,1)",
        borderColor: "rgba(2,117,216,1)",
        data: counts,
      }],
    },
    options: {
      scales: {
        xAxes: [{
          gridLines: {
            zeroLineColor: "black",
            zeroLineWidth: 2
          },
          ticks: {
            min: 0,
            max: 15000,
            maxTicksLimit: 5
          }
        }],
        yAxes: [{
          barPercentage: 0.5,
          gridLines: {
            display: false
          }
        }],
      },
      legend: {
        display: false
      }
    }
  });
})

