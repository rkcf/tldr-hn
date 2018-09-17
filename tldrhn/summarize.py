from hackernews import HackerNews
from . import db
from . import Story


def gen_summary(url):
    """ Generate summary given story url """
    return "Sit non provident perspiciatis doloribus omnis. Voluptates qui vel"


def main():
    # Grab top 30 stories
    hn = HackerNews()
    stories = hn.top_stories(limit=30)

    for story in stories:
        # Only continue if not a job and not in db
        if story.item_type != 'job':
            if Story.query.filter_by(id=story.item_id).first() is None:
                # Generate summary
                summary = gen_summary(story.url)
                # Store in db
                s = Story(id=story.item_id,
                          title=story.title,
                          summary=summary,
                          url=story.url)
                db.session.add(s)
                db.session.commit()
