// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#dataTable').DataTable({
                    "ajax": {
                        // "url": "static/objects2.txt", // This works for a static file
                        "url": "/data/history", // This now also works
                        "dataType": "json",
                        "dataSrc": "",
                        "contentType":"application/json"
                    },
                    "columns": [
                        {"data": "Word"},
                        {"data": "startDate"},
                        {"data": "endDate"},
                        {"data": "Instagram"},
                        {"data": "Twitter"},
                        {"data": "Youtube"}
                        ]
                    });
});

// TODO: FIND HOW TO ORDER BY TIME, TIME FORMAT