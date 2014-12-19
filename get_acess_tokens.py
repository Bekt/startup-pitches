"""Generate access tokens.

This script generates access_tokens for Twitter and Facebook APIs
so they can be used for authentication.
"""
import facebook
import tweepy

# Twitter app (https://apps.twitter.com)
# Create a new app or use existing.
consumer_key = 'REPLACE_ME'
consumer_secret = 'REPLACE_ME'

# Facebook app (https://developers.facebook.com/)
# Create a new app or use existing.
app_id = 'REPLACE_ME'
app_secret = 'REPLACE_ME'


def main():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    redir_url = auth.get_authorization_url()
    print('Go here on your browser:\n' + redir_url)
    pin = raw_input('PIN: ')
    tw = auth.get_access_token(pin)
    fb = facebook.get_app_access_token(app_id, app_secret)

    print('== Twitter ==')
    print('consumer_key: ' + consumer_key)
    print('consumer_secret: ' + consumer_secret)
    print('access_token: ' + tw[0])
    print('access_token_secret: ' + tw[1])
    print('')

    print('== Facebook ==')
    print('app_id: ' + app_id)
    print('app_secret: ' + app_secret)
    print('app_access_token: ' + fb)
    print('')

    print('Don\'t share these with anybody!')


if __name__ == '__main__':
    main()
