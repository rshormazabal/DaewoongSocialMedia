import utils
import pandas as pd

if __name__ == '__main__':
    begin_date = '2020/02/01'
    text_data, dataframes_list = utils.word_querry('임팩타민',
                                                   begin_date,
                                                   youtube_max_videos=1)
    data_twitter, data_instagram, data_youtube = dataframes_list

