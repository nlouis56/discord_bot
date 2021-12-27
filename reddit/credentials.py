#!/usr/bin/env python3
#coding=utf8

import praw

def main() :
    print ("in main")
    reddit = praw.Reddit(
        client_id = 'id',
        client_secret = 'secret',
        username = '<username>',
        password = '<password>',
        user_agent = 'get posts for a discord bot')
    print ("after credentials")
    post = reddit.subreddit("all").random()
    print (f"titre : {post.title}\nurl : {post.url}\nsub : {post.subreddit}")