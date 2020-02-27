from datetime import datetime

from flask import Flask, render_template, jsonify, request, redirect
import json
import utils
from flask_pymongo import PyMongo
import urllib
import pandas as pd
from pathlib import Path

# TODO: FIND A WAY TO RETURN JUST ONE RESPONSE FROM QUERRY
# SOLUTION IS TO GIVE THE

app = Flask(__name__)
app.config.update(TEMPLATES_AUTO_RELOAD=True)

password = urllib.parse.quote_plus('1991Rsehc@')
app.config['MONGO_URI'] = 'mongodb+srv://Rodrigo:' + urllib.parse.quote_plus(
    password) + '@daewoongsns-jlwri.mongodb.net/test?retryWrites=true&w=majority'
mongo = PyMongo(app)


# <---- Load main structure ----> #
@app.route("/", methods=['POST', 'GET'])
def home():
    return render_template("index.html")


@app.route('/search_history')
def previous_search():
    return render_template('search_history.html')


@app.route('/currentsearch/<sns>')
def platform(sns):
    return render_template('/currentsearch/current_' + sns + '.html')


@app.route("/data-analysis/sales")
def sales():
    return render_template('data-analysis/sales.html')


@app.route("/charts")
def charts():
    return render_template('charts.html')


# <---- End main structure ----> #

# <---- Routing data for graphs ----> #


@app.route('/data/<data_type>')
def jason_data(data_type):
    # Assume data comes from somewhere else
    with open('static/data/' + data_type + '.json') as f:
        data = json.load(f)

    return jsonify(data)


@app.route('/data/wordcloud/<sns>')
def wordclouds_data(sns):
    # Assume data comes from somewhere else
    with open('static/data/wordcloud/' + sns + '.json') as f:
        data = json.load(f)

    return jsonify(data)


# <---- End data for graphs ----> #

# <---- Get querry and save data ----> #


@app.route('/getProducts', methods=['POST', 'GET'])
def get_products():
    variable = request.form("dropdown-TCA").Text.data
    return variable


@app.route('/results', methods=['POST', 'GET'])
def get_querry():
    # get querry
    querry = request.form["word-search-sns"]
    start_date = request.form["from"]
    end_date = request.form["until"]

    # check boxes
    check_boxes = ['add-instagram', 'add-twitter', 'add-youtube']
    check_box_data = []
    for box in check_boxes:
        try:
            check_box_data.append(request.form[box])
        except:
            check_box_data.append('off')

    # TODO: Write an error alert if any of the searches is empty.

    # Getting words
    text_data, dataframes_list = utils.word_querry(querry,
                                                   start_date,
                                                   check_box_data,
                                                   youtube_max_videos=5,
                                                   twitter_max_messages=150)

    data_twitter, data_instagram, data_youtube = dataframes_list

    # save history
    history = pd.read_json('static/data/history.json')
    history = history.append({'Word': querry,
                              'startDate': start_date,
                              'endDate': end_date,
                              'Instagram': check_box_data[0],
                              'Twitter': check_box_data[1],
                              'Youtube': check_box_data[2]},
                             ignore_index=True)
    history.to_json('static/data/history.json', orient='records')

    # save data - create directory a dump 3 datafiles
    history_path = 'static/data/history_data/' + str(history.shape[0])
    Path(history_path).mkdir(parents=True, exist_ok=True)

    # lists for number of data
    number_instagram, number_twitter, number_youtube = [0, 0, 0]

    # check instagram
    if check_box_data[0] == 'on':
        data_instagram = data_instagram[data_instagram['text'].apply(lambda x: isinstance(x, str))]
        data_instagram = data_instagram[['text', 'time', 'likes', 'URL']]
        data_instagram.to_json('static/data/data_instagram.json', orient='records')
        data_instagram.to_json(history_path + '/data_instagram.json', orient='records')
        number_instagram = data_instagram.shape[0]

        # key words
        keywords = utils.get_keywords(data_instagram)
        key_df = pd.DataFrame(list(keywords.items()), columns=['Word', 'Importance'])
        key_df[:10].to_json('static/data/keywords_instagram.json', orient='records')

    if check_box_data[1] == 'on':
        # check twitter
        data_twitter = data_twitter[data_twitter['text'].apply(lambda x: isinstance(x, str))]
        data_twitter = data_twitter[['text', 'timestamp', 'likes', 'URL']]
        data_twitter.columns = ['text', 'time', 'likes', 'URL']
        data_twitter.to_json('static/data/data_twitter.json', orient='records')
        data_twitter.to_json(history_path + '/data_twitter.json', orient='records')
        number_twitter = data_twitter.shape[0]

        # key words
        keywords = utils.get_keywords(data_twitter)
        key_df = pd.DataFrame(list(keywords.items()), columns=['Word', 'Importance'])
        key_df[:10].to_json('static/data/keywords_twitter.json', orient='records')

    if check_box_data[2] == 'on':
        data_youtube.to_json('static/data/data_youtube.json', orient='records')
        data_youtube.to_json(history_path + '/data_youtube.json', orient='records')
        number_youtube = data_youtube.shape[0]

        # key words
        keywords = utils.get_keywords(data_youtube)
        key_df = pd.DataFrame(list(keywords.items()), columns=['Word', 'Importance'])
        key_df[:10].to_json('static/data/keywords_youtube.json', orient='records')

    # get similar tags
    tags = utils.similar_tags(querry)
    tags[:8].to_json('static/data/data_tags.json', orient='records')

    # data percentages
    platform_percentages_json = {"series": [{
        "name": "Youtube",
        "counts": number_youtube}, {
        "name": "Instagram",
        "counts": number_instagram}, {
        "name": "twitter",
        "counts": number_twitter}]}

    # for graph
    with open('static/data/data_platform_percentages.json', 'w') as json_file:
        json.dump(platform_percentages_json, json_file)

    # for
    with open(history_path + '/data_platform_percentages.json', 'w') as json_file:
        json.dump(platform_percentages_json, json_file)

    # cloud data
    create_datacloud_data()
    return render_template('currentsearch/current_instagram.html')


def create_datacloud_data():
    files = ['instagram', 'twitter', 'youtube']
    for file in files:
        data = pd.read_json('static/data/data_' + file + '.json')
        all_text = ' '.join(data.text.tolist())

        json_data = {"series": [{
            "type": "WordCloudSeries",
            "text": all_text
        }]
        }
        with open('static/data/wordcloud/wordcloud_' + file + '.json', 'w') as json_file:
            json.dump(json_data, json_file)
    return 'done'


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5005)
