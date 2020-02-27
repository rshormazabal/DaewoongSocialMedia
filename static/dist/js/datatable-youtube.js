// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#dataTable').DataTable({
                    "ajax": {
                        // "url": "static/objects2.txt", // This works for a static file
                        "url": "/data/data_youtube", // This now also works
                        "dataType": "json",
                        "dataSrc": "",
                        "contentType":"application/json"
                    },
                    "columns": [
                        {"data": "text"},
                        {"data": "time"},
                        {"data": "author"},
                        {"data": "votes"}
                        ]
                    });
});

// TODO: FIND HOW TO ORDER BY TIME, TIME FORMAT