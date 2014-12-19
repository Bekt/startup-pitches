"""Twitter Bot for HH Problems Facebook group.

This script periodically updates the Twitter account @hh_problems
with posts from the HH Hackers Problems Facebook group.

Potential enhancements:
    - Handle posts with pictures.
    - Link back to the FB post.

Twitter URL: https://twitter.com/hh_problems
FB URL: https://www.facebook.com/groups/hhproblems/

Code: https://github.com/Bekt/hh-problems-bot
"""
import facebook
import tweepy
import time

from datetime import datetime

from credentials import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret,
    app_access_token
)


class HHProbs(object):

    hh_tag = 'HH_Problems: '
    # http://www.facebook.com/groups/hhproblems/
    fb_group_id = '291381824396182'

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
        posts = filter(self._filt, posts)
        self.tweet_posts(posts)

    def tweet_posts(self, posts):
        recent = self.last_tweet()
        for post in posts:
            if not recent or post['created_time'] > recent.created_at:
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

    def fb_posts(self, limit=20):
        posts = self.fb_api.get_connections(self.fb_group_id, 'feed',
                                            limit=limit,
                                            fields='message,created_time')
        # Order by created_time (default is updated_time).
        for post in posts['data']:
            created_date = datetime.strptime(post['created_time'][:-5],
                                             '%Y-%m-%dT%H:%M:%S')
            post['created_time'] = created_date
        posts['data'].sort(key=lambda x: x['created_time'])
        return posts['data']

    @classmethod
    def _filt(self, post):
        # 200 is random, anything that long is
        # most likely a rant or spam?
        msg = post['message']
        return len(msg) < 200


if __name__ == '__main__':
    hh = HHProbs()
    hh.run()
