from hackernews import HackerNews
from newspaper import Article
from newspaper.article import ArticleException
from . import db
from . import Story
from . import Position


def gen_summary(url):
    """ Generate summary given story url """
    article = Article(url)
    try:
        # Get text
        article.download()
        article.parse()
    except ArticleException:
        return "Unable to generate summary"

    # Tokenize text
    article.nlp()
    # Generate summary
    return article.summary


def main():
    """ Gets top 30 stories on HN, summarizes and stores in the database """
    # Grab top 30 stories
    hn = HackerNews()
    stories = hn.top_stories(limit=30)
    front_page_list = []

    for story in stories:
        # Only continue if not a job, or ask (ie external link) and not in db
        if story.url:
            # Put story id into front page list
            front_page_list.append(story.item_id)
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

    # Delete all rows in front page list
    Position.query.delete()
    # Add story ids to positions list
    for i in range(0, len(front_page_list)):
        db.session.add(Position(id=front_page_list[i],
                                position=i))
    db.session.commit()
