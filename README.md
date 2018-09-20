# TLDR Hacker News

A website that displays summarized stories from [Hacker News](https://news.ycombinator.com/).

View at [http://tldrhn.rkcf.me]

## Deployment

### Docker

```
git clone https://github.com/rkcf/tldr-hn
cd tldr-hn
docker-compose up
```

Add bin/docker-summarize-cron to your cron jobs to periodically summarize and cache stories.

### Locally

```
git clone https://github.com/rkcf/tldr-hn
cd tldr-hn
virtualenv .venv
. .venv/bin/activate
pip install -r requirements.txt
python -m nltk.dowloader punkt
bin/create_db
bin/cache_stories
uwsgi --ini tldrhn/uwsgi.ini
```

Create a cron script referencing bin/cache_stories to periodically summarize and cache stories.
