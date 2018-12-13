function setupLatestSolves() {
  var el = document.getElementById("dtVerticalScroll");
  if (el) {
    $(el).DataTable({
        "scrollY": "50vh",
        "scrollCollapse": true,
        "ajax": "/analytics/latest_solves.json",
        "columns": [
          { "data": "id" },
          { "data": "user" },
          { "data": "challenge" },
          { "data": "category" },
          { "data": "points" },
          { "data": "date" }
        ],
        order : [0, 'desc']
    });

    $('.dataTables_length').addClass('bs-select');
  }
}

function setupLastWeek() {
  var el = document.getElementById("lineChart");
  if (el) {
    $.get({
      url: "/analytics/last_week.json",
      success: drawChart
    });

    function drawChart(response) {

      var backgroundColors = [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(255, 159, 64, 0.2)'
      ];

      var borderColors = [
        'rgba(255,99,132,1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)'
      ];

      var categories = response['categories']
      var data = response['data']
      var labels = response['labels']
      var datasets = []

      categories.forEach(function(category, i) {
        datasets.push({
          'label': category,
          'data': data[category],
          'backgroundColor': [ backgroundColors[i]],
          'borderColor': [ borderColors[i] ],
          'borderWidth': 2
        });
      });

      var context = el.getContext('2d');
      var linechart = new Chart(context, {
        'type': 'line',
        'data': {
          'labels': labels,
          'datasets': datasets
        },
        'options': {
          'responsive': true
        }
      });
    }
  }

}

$(document).ready(function() {
  setupLastWeek();
  setupLatestSolves();
});



