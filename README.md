## HH Problems Twitter Bot
A bot that periodically (every hour) checks the 
[HH Hacker Problems](https://www.facebook.com/groups/hhproblems/) Facebook 
group feed and tweets if there is anything interesting with 
[@hh_problems](https://twitter.com/hh_problems).

## Installation

```bash
git clone git@github.com:Bekt/hh-problems-bot.git
cd hh-problems-bot

# (Optional)
virtualenv venv

pip install -r requirements.txt
```

## Access Tokens
Valid [Facebook app](https://developers.facebook.com) and
[Twitter app](https://apps.twitter.com) are required for the bot to work.

1. Edit `get_access_tokens.py`:
  - `consumer_key` and `consumer_secret`: Twitter API credentials
  - `app_id` and `app_secret`: Facebook API credentials.

2. Run `python get_access_tokens.py` to generate access tokens.

3. Edit `credentials.txt` with outputted values.

4. `cp credentials.txt credentials.py`

## License
[The MIT License](http://opensource.org/licenses/MIT)

