#encoding:utf-8

import os
import random

from utils import (get_url, download_file, telegram_autoplay_limit,
                   just_send_an_album)


def weighted_random(d):
    r = random.uniform(0, sum(val for val in d.values()))
    s = 0.0
    for k, w in d.items():
        s += w
        if r < s: return k
    return k


def define_channel_for_today():
    channels = {'dataisbeautiful': 8,
        'MapPorn': 5,
        'datasets': 1,
        'datascience': 2,
        'MachineLearning': 2,
        'visualization': 1,
        'Infographics': 2,
        'wordcloud': 0.7,
        'SampleSize': 0.7,
        'dataisugly': 1.2,
        'FunnyCharts': 0.6,
        'usdataisbeautiful': 0.2,
        'mathpics': 0.5,
        'statistics': 1,
        'pystats': 0.5,
        'opendata': 0.3,
        'bigdatajobs': 0.1,
        'bigdata': 0.2,
        'IPython': 0.1,
        'JupyterNotebooks': 0.1
    }
    return weighted_random(channels)


subreddit = define_channel_for_today()
t_channel = '@datascientology'


def just_send_message(submission, bot):
    title = submission.title
    link = submission.short_link
    if submission.is_self is True:    
        punchline = submission.selftext
        text = '{}\n\n{}\n\n/r/{}\n{}'.format(title, punchline, subreddit, link)
    else:
        url = submission.url
        text = '{}\n{}\n\n/r/{}\n{}'.format(title, url, subreddit, link)
    bot.sendMessage(t_channel, text)
    return True


def send_post(submission, bot):
    what, url, ext = get_url(submission)
    title = submission.title
    link = submission.short_link
    text = '{}\n\n/r/{}\n{}'.format(title, subreddit, link)

    if what == 'text':
        return just_send_message(submission, bot)

    elif what == 'other':
        return just_send_message(submission, bot)

    filename = 'r_data_related.{}'.format(ext)
    if not download_file(url, filename):
        return just_send_message(submission, bot)
    if os.path.getsize(filename) > telegram_autoplay_limit:
        return just_send_message(submission, bot)

    if what == 'gif':
        f = open(filename, 'rb')
        bot.sendDocument(t_channel, f, caption=text)
        f.close()
        return True

    elif what == 'img':
        f = open(filename, 'rb')
        bot.sendPhoto(t_channel, f, caption=text)
        f.close()
        return True

    elif what == 'album':
        just_send_message(submission, bot)
        just_send_an_album(t_channel, url, bot)
        return True

    else:
        return False
