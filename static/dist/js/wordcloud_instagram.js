// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

$.getJSON("/data/wordcloud/wordcloud_instagram", function (json) {
    var text = json.series.map(function (item) {
        return item.text;
    });

    let chart = am4core.create("wordcloud-instagram", am4plugins_wordCloud.WordCloud);

    let series = chart.series.push(new am4plugins_wordCloud.WordCloudSeries());

    series.text = text[0];

    series.maxCount = 80;
    series.minWordLength = 2;
    series.excludeWords = ["the", "an", "to", "es", "de", "in", "of", "is", "me", "un", "con"];
    series.accuracy = 2;
    series.minFontSize = 18;
    series.maxFontSize = 92;
    series.randomness = 0.4;
    series.labelsContainer.rotation = -25;

    series.colors = new am4core.ColorSet();
    series.colors.passOptions = {};

    series.labels.template.tooltipText = "{word}:\n[bold]{value}[/]";


});


