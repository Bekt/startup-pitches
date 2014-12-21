 # -*- coding: utf-8 -*-
"""Twitter Bot for One Sentence Startup Pitch Facebook group.

This script periodically updates the Twitter account @OneStartupPitch
with posts from the above Facebook group.

Potential enhancements:
    - Handle posts with pictures.
    - Link back to the FB post.

Twitter URL: https://twitter.com/OneStartupPitch
FB URL: http://www.facebook.com/groups/1500321840185061

Code: https://github.com/Bekt/startup-pitches
"""
import facebook
import tweepy
import time
import urlparse
import os

from datetime import datetime


from credentials import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret,
    app_access_token
)


class HHProbs(object):

    hh_tag = '#Startup Pitch: '
    # http://www.facebook.com/groups/1500321840185061/
    fb_group_id = '1500321840185061'

    def __init__(self):
        self._tw_api = None
        self._fb_api = None

    @property
    def tw_api(self):
        if self._tw_api is None:
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            self._tw_api = tweepy.API(auth)
        return self._tw_api

    @property
    def fb_api(self):
        if self._fb_api is None:
            self._fb_api = facebook.GraphAPI(app_access_token)
        return self._fb_api

    def run(self):
        posts = self.fb_posts()
        posts = filter(lambda x: self._filt(x, 10), posts)
        print(len(posts))
        self.tweet_posts(posts)

    def seed(self, since, until):
        """Run this when the account is brand new."""
        posts = self.fb_posts(since=since, until=until, count=15000)
        with open('posts_30.txt', 'w') as a, open('posts_10.txt', 'w') as b:
            post10 = { p['message'].strip() for p in posts if self._filt(p, 10) and not self._filt(p, 30) }
            post30 = { p['message'].strip() for p in posts if self._filt(p, 30) }
            a.write(os.linesep.join([p.replace('\n', ' ').encode('utf-8') for p in post30]))
            b.write(os.linesep.join([p.replace('\n', ' ').encode('utf-8') for p in post10]))
        posts = filter(lambda x: self._filt(x, 30), posts)
        print(len(posts))
        self.tweet_posts(posts, seed=True)

    def run_seed(self):
        """Gets one tweet from posts_30.txt and two from posts_10.txt."""
        # What do we say to efficiency? Not Today!
        af, bf = 'posts_30.txt', 'posts_10.txt'
        posts = []
        with open(af, 'r') as a, open(bf, 'r') as b:
            post30 = a.read().splitlines()
            post10 = b.read().splitlines()
        if len(post30) < 1 and len(post10) < 2:
            return self.run()
        if len(post10) > 1:
            posts.append({'message': post10[0]})
            posts.append({'message': post10[1]})
        if len(post30):
            posts.append({'message': post30[0]})
        with open(af, 'w') as a, open(bf, 'w') as b:
            a.write(os.linesep.join([p for p in post30[1:]] ))
            b.write(os.linesep.join([p for p in post10[2:]] ))
        self.tweet_posts(posts, seed=True)

    def tweet_posts(self, posts, seed=False):
        recent = self.last_tweet()
        for post in posts:
            if seed or post['created_time'] > recent.created_at:
                try:
                    print(post['message'])
                    self.tweet(post['message'])
                    # Don't make Twitter mad.
                    time.sleep(10)
                except:
                    pass

    def last_tweet(self):
        tweet = self.tw_api.home_timeline(count=1)
        return tweet[0] if tweet else None

    def tweet(self, text):
        status = (self.hh_tag + text)[:140]
        self.tw_api.update_status(status)

    @classmethod
    def _filt(self, post, likes):
        # 200 is random, anything that long is
        # most likely a rant or spam?
        msg = post.get('message', '')
        return (2 < len(msg) < 200
                and ('likes' in post and len(post['likes']['data']) >= likes))

    def fb_posts(self, since=None, until=None, count=30):
        def req(**kwargs):
            return self.fb_api.get_connections(
                    self.fb_group_id, 'feed', limit=min(200, count),
                    fields='message,created_time,likes.limit(50)', **kwargs)
        resp = req(until=until)
        posts = resp['data']
        while ('paging' in resp and 'next' in resp['paging']
                and resp['paging']['next']
                and since < until
                and len(resp['data']) > 1
                and len(posts) < count):
            try:
                print(len(posts))
                url = urlparse.urlparse(resp['paging']['next'])
                until = int(urlparse.parse_qs(url.query)['until'][0])
                resp = req(until=until)
                posts.extend(resp['data'])
            except:
                pass
        # Order by created_time (default is updated_time).
        for post in posts:
            created_date = datetime.strptime(post['created_time'][:-5],
                                             '%Y-%m-%dT%H:%M:%S')
            post['created_time'] = created_date
        posts.sort(key=lambda x: x['created_time'])
        return posts


if __name__ == '__main__':
    hh = HHProbs()
    #hh.run()
    #hh.seed(since=0, until=1419124509)
    hh.run_seed()
