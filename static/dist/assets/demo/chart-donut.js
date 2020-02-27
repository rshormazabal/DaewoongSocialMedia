// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

$.getJSON("/data/data_platform_percentages", function (json) {
  var labels = json.series.map(function(item) {
    return item.name;
  });
  var counts = json.series.map(function(item) {
    return item.counts;
  });

  
  // Bar Chart Example
  var ctx = document.getElementById("myDonutChart");

  var myDonutChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        data: counts,
        backgroundColor: ['#007bff', '#dc3545', '#ffc107', '#28a745'],
      }],
    },
  });
}
)