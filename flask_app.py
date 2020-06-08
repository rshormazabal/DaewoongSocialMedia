from datetime import datetime

from flask import Flask, render_template, jsonify, request, redirect
import json
from utils import captions_from_tag, similar_tags

#TODO: FIND A WAY TO RETURN JUST ONE RESPONSE FROM QUERRY

app = Flask(__name__)


@app.route("/", methods=['POST', 'GET'])
def home():
    return render_template("index.html")


@app.route('/data_table')
def data_table():
    # Assume data comes from somewhere else
    with open('static/data/data_instagram.json') as f:
        data = json.load(f)

    return jsonify(data)


@app.route('/data_lineplot')
def data_lineplot():
    # Assume data comes from somewhere else
    with open('static/data/data_author.json') as f:
        data = json.load(f)

    return jsonify(data)


@app.route('/data_tags')
def data_tags():
    # Assume data comes from somewhere else
    with open('static/data/data_tags.json') as f:
        data = json.load(f)

    return jsonify(data)


@app.route('/getQuerry', methods=['POST', 'GET'])
def get_querry():
    # get querry
    querry = request.form["searchBar"]
    begin_date = request.form["searchBar2"]
    #TODO: Write an error alert if any of the searches is empty.

    # Getting words
    #text_data, dataframes_list = utils.word_querry(querry,
    #                                               date,
    #                                               youtube_max_videos=1)
    #data_twitter, data_instagram, data_youtube = dataframes_list

    begin_date = int(datetime.strptime(begin_date, '%Y/%m/%d').strftime("%s"))

    # instagram#
    data_instagram, _ = captions_from_tag(querry,
                                          begin_date,
                                          number=1000)
    # avoid None, messages without any text
    data_instagram = data_instagram[data_instagram['text'].apply(lambda x: isinstance(x, str))]
    data_instagram = data_instagram[['text', 'time', 'likes', 'URL']]

    data_instagram.to_json('static/data/data_instagram.json', orient='records')

    # get similar tags
    tags = similar_tags(querry)
    tags[:8].to_json('static/data/data_tags.json', orient='records')

    # rerun pages with the data
    data_tags()
    data_table()
    return redirect('/')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5005)