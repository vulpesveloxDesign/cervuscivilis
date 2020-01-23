import time
import os
import requests
import praw
import config
from bitchy_remark import bitchy_reminder_01
from immigrants import immigrant_phrases
from greetings import greeting
from newsAPI import *

# print(dir(subreddit))
# TODO_1:   Maybe act a bit like a news channel, every now and then it could
#           release a post about the weather in niceria, or crime rates going
#           down, or how the election is going. I don’t know?
# TODO_2:   Fix read_write inconsistencies; norris_joke, salute_newcomer

BOT_ID = os.environ.get('BOT_ID')
BOT_SECRET = os.environ.get('BOT_SECRET')
BOT_PASSWORD = os.environ.get('BOT_PASSWORD')
BOT_USERNAME = os.environ.get('BOT_USERNAME')

def authenticate():
    print('logging in...')
    reddit = praw.Reddit(
        username = BOT_USERNAME,
        password = BOT_PASSWORD,
        client_id = BOT_ID,
        client_secret = BOT_SECRET,
        user_agent = 'cervusCivilis v2.0 by u/yo_funky_mama'
        )
    print('logged in as {}'.format(reddit.user.me()))
    return reddit

def write_to_file(txt_file, item):
    with open(txt_file, 'a') as append_to_paper:
        append_to_paper.write(item + '\n')


def read_from_file(txt_file):
    if not os.path.exists(os.path.join(os.getcwd(), txt_file)):
        dynamic_list = []
    else:
        with open(txt_file, 'r') as retrieve_from_paper:
            txt = retrieve_from_paper.read().split('\n')
            dynamic_list = []
            for i in txt:
                dynamic_list.append(i)
    return dynamic_list


def salute_newcomer(reddit):
    # submission = reddit.submission('https://www.reddit.com/r/Niceria/comments/ep3rah/new_immigrant_thread/')
    submission = reddit.submission(url='https://www.reddit.com/r/test/comments/er596x/testing_test_device/')
    saluted = read_from_file('saluted.txt')
    for top_level_comment in submission.comments:
        if submission.id not in saluted and submission.author != reddit.user.me():
            top_level_comment.reply(greeting())
            saluted.append(submission.id)
            write_to_file('saluted.txt', submission.id)
            time.sleep(10)
    print(saluted)


def complain(reddit):
    complain_a_lot = read_from_file('complaints.txt')
    print(type(complain_a_lot))
    for submission in reddit.subreddit('test').hot(limit=50):
        if 'immigra' in submission.selftext or 'immigra' in submission.title:
            if submission.id not in complain_a_lot and submission.author != reddit.user.me():
                submission.reply(bitchy_reminder_01)
                complain_a_lot.append(submission.id)
                write_to_file('complaints.txt', submission.id)
                time.sleep(10)
        else:
            print('no str found!')
    print(complain_a_lot)


def norris_joke(reddit):
    jokes_r_us = read_from_file('joke_received.txt')
    for comment in reddit.subreddit('test').comments(limit=50):
        if '!joke' in comment.body:
            if comment.id not in jokes_r_us and comment.author != reddit.user.me():
                joke = requests.get('http://api.icndb.com/jokes/random').json()['value']['joke']
                comment_reply = 'Courtesy of [icndb.com](http://www.icndb.com/the-jokes-2/):\n\n>\n{}'.format(joke)
                jokes_r_us.append(comment.id)
                comment.reply(comment_reply)
                print(comment_reply)
                write_to_file('joke_received.txt', comment.id)
                time.sleep(10)
    print(jokes_r_us)

def daily_news(reddit):
    pass

def main():
    reddit = authenticate()
    while True:
        salute_newcomer(reddit)
        norris_joke(reddit)
        complain(reddit)
        time.sleep(30)


if __name__ == "__main__":
    main()
