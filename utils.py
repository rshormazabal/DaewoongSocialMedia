import io
import json
import os
import sys
import time
from datetime import datetime, date
import pandas as pd
import lxml.html
import requests

import twitterscraper
from igramscraper.instagram import Instagram
from lxml.cssselect import CSSSelector

from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from krwordrank.word import KRWordRank
from krwordrank.word import summarize_with_keywords


def get_tweets(word, begin_date, end_date='today', limit=None):
    """
    :return: tweets data as dataframe: returns a dictionary of twitter user data
    """
    if end_date == 'today':
        list_of_tweets = twitterscraper.query_tweets(word, limit=limit, begindate=begin_date)
    else:
        list_of_tweets = twitterscraper.query_tweets(word, begindate=begin_date, enddate=end_date)

    tweets_data = []
    for tweet in list_of_tweets:
        tweet_data = {}
        tweet_data['tweetID'] = tweet.tweet_id
        tweet_data['time'] = tweet.timestamp.strftime("%d-%b-%Y (%H:%M)")
        tweet_data['text'] = tweet.text
        tweet_data['likes'] = tweet.likes
        tweet_data['usedID'] = tweet.username
        tweet_data['URL'] = tweet.tweet_url
        tweet_data['timestamp'] = tweet.timestamp

        tweets_data.append(tweet_data)

    tweets_data = pd.DataFrame(tweets_data)
    return tweets_data, list_of_tweets


def comments_from_caption_id(ID):
    instagram = Instagram()
    comments = instagram.get_media_comments_by_id(ID, count=1000)['comments']
    comments = [a.text for a in comments]
    return comments


def captions_from_tag(tag,
                      begin_date,
                      number=1000,
                      ID='rshormazabal@gmail.com',
                      PASSWORD='1991Rsehc@'):
    instagram = Instagram()
    instagram.with_credentials(ID, PASSWORD)

    medias = instagram.get_medias_by_tag(tag, count=number, min_timestamp=begin_date)

    captions_data = []
    for media in medias:
        caption_data = {}
        caption_data['ID'] = media.identifier
        caption_data['time'] = datetime.fromtimestamp(media.created_time).strftime("%d-%b-%Y (%H:%M)")
        if type(media.caption) == 'str':
            caption_data['text'] = media.caption.replace("\n", " ")
        else:
            print("Possible error, no string datatype")
            caption_data['text'] = media.caption

        caption_data['likes'] = media.likes_count
        caption_data['comments'] = media.comments_count
        caption_data['usedID'] = media.owner.identifier
        caption_data['URL'] = media.link
        caption_data['timestamp'] = media.created_time
        captions_data.append(caption_data)

    captions_data = pd.DataFrame(captions_data)
    return captions_data, medias


def similar_tags(tag):
    instagram = Instagram()
    tags = instagram.search_tags_by_tag_name(tag)

    tags = [[x.name, x.media_count] for x in tags]
    return pd.DataFrame(tags, columns=['Tag', 'Posts'])


YOUTUBE_VIDEO_URL = 'https://www.youtube.com/watch?v={youtube_id}'
YOUTUBE_COMMENTS_AJAX_URL_OLD = 'https://www.youtube.com/comment_ajax'
YOUTUBE_COMMENTS_AJAX_URL_NEW = 'https://www.youtube.com/comment_service_ajax'

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'


def find_value(html, key, num_chars=2, separator='"'):
    pos_begin = html.find(key) + len(key) + num_chars
    pos_end = html.find(separator, pos_begin)
    return html[pos_begin: pos_end]


def ajax_request(session, url, params=None, data=None, headers=None, retries=5, sleep=20):
    for _ in range(retries):
        response = session.post(url, params=params, data=data, headers=headers)
        if response.status_code == 200:
            return response.json()
        if response.status_code == 413:
            return {}
        else:
            time.sleep(sleep)


def download_comments(youtube_id, sleep=.1):
    if 'liveStreamability' in requests.get(YOUTUBE_VIDEO_URL.format(youtube_id=youtube_id)).text:
        print('Live stream detected! Not all comments may be downloaded.')
        return download_comments_new_api(youtube_id, sleep)
    return download_comments_old_api(youtube_id, sleep)


def download_comments_new_api(youtube_id, sleep=1):
    # Use the new youtube API to download some comments
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT

    response = session.get(YOUTUBE_VIDEO_URL.format(youtube_id=youtube_id))
    html = response.text
    session_token = find_value(html, 'XSRF_TOKEN', 3)

    data = json.loads(find_value(html, 'window["ytInitialData"] = ', 0, '\n').rstrip(';'))
    ncd = next(search_dict(data, 'nextContinuationData'))
    continuations = [(ncd['continuation'], ncd['clickTrackingParams'])]

    while continuations:
        continuation, itct = continuations.pop()
        response = ajax_request(session, YOUTUBE_COMMENTS_AJAX_URL_NEW,
                                params={'action_get_comments': 1,
                                        'pbj': 1,
                                        'ctoken': continuation,
                                        'continuation': continuation,
                                        'itct': itct},
                                data={'session_token': session_token},
                                headers={'X-YouTube-Client-Name': '1',
                                         'X-YouTube-Client-Version': '2.20200207.03.01'})

        if not response:
            break
        if list(search_dict(response, 'externalErrorMessage')):
            raise RuntimeError('Error returned from server: ' + next(search_dict(response, 'externalErrorMessage')))

        # Ordering matters. The newest continuations should go first.
        continuations = [(ncd['continuation'], ncd['clickTrackingParams'])
                         for ncd in search_dict(response, 'nextContinuationData')] + continuations

        for comment in search_dict(response, 'commentRenderer'):
            yield {'cid': comment['commentId'],
                   'text': comment['contentText']['runs'][0]['text'],
                   'time': comment['publishedTimeText']['runs'][0]['text'],
                   'author': comment.get('authorText', {}).get('simpleText', ''),
                   'votes': comment.get('voteCount', {}).get('simpleText', '0'),
                   'photo': comment['authorThumbnail']['thumbnails'][-1]['url']}

        time.sleep(sleep)


def search_dict(partial, key):
    if isinstance(partial, dict):
        for k, v in partial.items():
            if k == key:
                yield v
            else:
                yield from search_dict(v, key)
    elif isinstance(partial, list):
        for i in partial:
            yield from search_dict(i, key)


def download_comments_old_api(youtube_id, sleep=1):
    # Use the old youtube API to download all comments (does not work for live streams)
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT

    # Get Youtube page with initial comments
    response = session.get(YOUTUBE_VIDEO_URL.format(youtube_id=youtube_id))
    html = response.text

    reply_cids = extract_reply_cids(html)

    ret_cids = []
    for comment in extract_comments(html):
        ret_cids.append(comment['cid'])
        yield comment

    page_token = find_value(html, 'data-token')
    session_token = find_value(html, 'XSRF_TOKEN', 3)

    first_iteration = True

    # Get remaining comments (the same as pressing the 'Show more' button)
    while page_token:
        data = {'video_id': youtube_id,
                'session_token': session_token}

        params = {'action_load_comments': 1,
                  'order_by_time': True,
                  'filter': youtube_id}

        if first_iteration:
            params['order_menu'] = True
        else:
            data['page_token'] = page_token

        response = ajax_request(session, YOUTUBE_COMMENTS_AJAX_URL_OLD, params, data)
        if not response:
            break

        page_token, html = response.get('page_token', None), response['html_content']

        reply_cids += extract_reply_cids(html)
        for comment in extract_comments(html):
            if comment['cid'] not in ret_cids:
                ret_cids.append(comment['cid'])
                yield comment

        first_iteration = False
        time.sleep(sleep)

    # Get replies (the same as pressing the 'View all X replies' link)
    for cid in reply_cids:
        data = {'comment_id': cid,
                'video_id': youtube_id,
                'can_reply': 1,
                'session_token': session_token}

        params = {'action_load_replies': 1,
                  'order_by_time': True,
                  'filter': youtube_id,
                  'tab': 'inbox'}

        response = ajax_request(session, YOUTUBE_COMMENTS_AJAX_URL_OLD, params, data)
        if not response:
            break

        html = response['html_content']

        for comment in extract_comments(html):
            if comment['cid'] not in ret_cids:
                ret_cids.append(comment['cid'])
                yield comment
        time.sleep(sleep)


def extract_comments(html):
    tree = lxml.html.fromstring(html)
    item_sel = CSSSelector('.comment-item')
    text_sel = CSSSelector('.comment-text-content')
    time_sel = CSSSelector('.time')
    author_sel = CSSSelector('.user-name')
    vote_sel = CSSSelector('.like-count')
    photo_sel = CSSSelector('.user-photo')

    for item in item_sel(tree):
        yield {'cid': item.get('data-cid'),
               'text': text_sel(item)[0].text_content(),
               'time': time_sel(item)[0].text_content().strip(),
               'author': author_sel(item)[0].text_content(),
               'votes': vote_sel(item)[0].text_content(),
               'photo': photo_sel(item)[0].get('src')}


def extract_reply_cids(html):
    tree = lxml.html.fromstring(html)
    sel = CSSSelector('.comment-replies-header > .load-comments')
    return [i.get('data-cid') for i in sel(tree)]


def comments_from_video_id(youtube_id):
    # youtube ID Link, output file, limit number of comments
    print('Downloading Youtube comments for video:', youtube_id)
    all_comments = download_comments(youtube_id)
    data = pd.DataFrame(all_comments)
    if ('cid' or 'photo') in data.columns:
        data.drop(['cid', 'photo'], axis=1, inplace=True)
    return data


def word_querry(querry_word,
                begin_date,
                check_boxes,
                DEVELOPER_KEY='AIzaSyCfT4W9Ca7qa5MFvqm1TVvQPS06WEj8yIc',
                youtube_order='viewCount',
                youtube_max_videos=10,
                twitter_max_messages=300):
    begin_date = int(datetime.strptime(begin_date, '%m/%d/%Y').strftime("%s"))

    data_instagram, data_twitter, data_youtube = [], [], []

    if check_boxes[0] == 'on':
        print("Fetching instagram data for '" + querry_word + "'")

        # instagram#
        data_instagram, _ = captions_from_tag(querry_word,
                                              begin_date,
                                              number=1000)
        # avoid None, messages without any text
        data_instagram = data_instagram[data_instagram['text'].apply(lambda x: isinstance(x, str))]

    # twitter#
    if check_boxes[1] == 'on':
        print("Fetching twitter data for '" + querry_word + "'")
        data_twitter, _ = get_tweets(querry_word,
                                     begin_date=date.fromtimestamp(begin_date),
                                     limit = twitter_max_messages)

    if check_boxes[2] == 'on':
        print("Fetching youtube data for '" + querry_word + "' - top 10 most viewed videos")

        # youtube top 10 videos#
        payload = {'part': 'snippet',
                   'key': DEVELOPER_KEY,
                   'order': youtube_order,
                   'q': querry_word,
                   'maxResults': youtube_max_videos}
        l = requests.Session().get('https://www.googleapis.com/youtube/v3/search', params=payload)
        resp_dict = json.loads(l.content)

        # eliminate ids from channels or playlists
        video_ids = []
        for item in resp_dict['items']:
            if 'videoId' in item['id'].keys():
                video_ids.append(item['id']['videoId'])

        data_youtube = pd.DataFrame(columns=['text', 'time', 'author', 'votes'])
        for video_id in video_ids:
            data_youtube = data_youtube.append(comments_from_video_id(video_id), ignore_index=True)

    dataframes_list = [data_twitter, data_instagram, data_youtube]
    # append only text comments for every different source
    text_list = []
    if check_boxes[0] == 'on':
        text_list.extend(data_instagram.text.to_list())
    if check_boxes[1] == 'on':
        text_list.extend(data_twitter.text.to_list())
    if check_boxes[2] == 'on':
        text_list.extend(data_youtube.text.to_list())
    print('{} number of messages scraped'.format(len(text_list)))
    return text_list, dataframes_list


def get_keywords(data,
                 add_stopwords=[],
                 min_count=5,
                 max_length=10,
                 beta=0.85,
                 max_iter=20,
                 verbose=False):

    list_of_texts = data.text.tolist()
    # load keywords from json file and create set
    with open('stopwords-ko.json') as json_file:
        stopwords = json.load(json_file)
    stopwords = set(stopwords)

    for word in add_stopwords:
        stopwords.add(word)

    keywords = summarize_with_keywords(list_of_texts,
                                       min_count=min_count,
                                       max_length=max_length,
                                       beta=beta,
                                       max_iter=max_iter,
                                       stopwords=stopwords,
                                       verbose=verbose)

    return keywords


def create_wordcloud(keywords, size=(800, 800)):
    # creating wordcloud
    wordcloud = WordCloud(font_path='NanumBarunGothic.ttf',
                          width=size[0],
                          height=size[1],
                          background_color="white")

    cloud = wordcloud.generate_from_frequencies(keywords)
    plt.figure(figsize=(16, 10))
    plt.imshow(cloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    return wordcloud


def save_wordclouds(dataframes,
                    begin_date,
                    add_stopwords=[],
                    min_count=5,
                    max_length=10,
                    beta=0.85,
                    max_iter=20,
                    verbose=False):
    platforms = ['twitter', 'instagram', 'youtube']
    begin_date = begin_date.replace('/', '-')
    for dataframe, platform in zip(dataframes, platforms):
        cloud = create_wordcloud(dataframe.text.to_list(),
                                 add_stopwords=add_stopwords,
                                 min_count=min_count,
                                 max_length=max_length,
                                 beta=beta,
                                 max_iter=max_iter,
                                 verbose=verbose)
        cloud.to_file('./outputData/' + platform + '-' + begin_date + '.png')

