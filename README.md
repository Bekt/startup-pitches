## One Sentence Startup Pitches Twitter Bot

Demo: https://twitter.com/OneStartupPitch
Forked from: [hh-problems](https://github.com/Bekt/hh-problems-bot)

A bot that periodically (every hour) checks the 
[One Sentence Startup Pitches](https://www.facebook.com/groups/1500321840185061/)
Facebook group feed and tweets if there is anything interesting with 
[@OneStartupPitch](https://twitter.com/OneStartupPitch).

## Installation

```bash
git clone git@github.com:Bekt/startup-pitches.git
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

3. `cp credentials.txt credentials.py`

4. Edit `credentials.py` with outputted values.

## Running
Invoke the script using `cron` or some other kind of scheduling tool:
```
python ossp.py
```

## License
[The MIT License](http://opensource.org/licenses/MIT)

