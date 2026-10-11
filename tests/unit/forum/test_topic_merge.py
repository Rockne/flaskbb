import sqlalchemy as sa
import copy
from flaskbb.extensions import db
from flaskbb.forum.models import Forum, Topic

def test_new_topic_created(forum : Forum, topic: Topic, other_topic: Topic):
    new_topic = forum.merge_topics(topic, other_topic)
    assert new_topic is not topic
    assert new_topic is not other_topic
    assert new_topic.id is not None

def test_new_topic_stored_in_database(forum: Forum, topic: Topic, other_topic: Topic):
    merged_topic = forum.merge_topics(topic, other_topic)
    topic_ids = db.session.scalars(sa.select(Topic.id)).all()
    assert merged_topic.id in topic_ids

def test_merged_topics_deleted(forum : Forum, topic: Topic, other_topic: Topic):
    forum.merge_topics(topic, other_topic)
    topic_ids = db.session.scalars(sa.select(Topic.id)).all()
    assert topic.id not in topic_ids
    assert other_topic.id not in topic_ids

def test_all_posts_preserved(forum : Forum, topic: Topic, other_topic: Topic):
    posts = [*topic.posts, *other_topic.posts]
    new_topic = forum.merge_topics(topic, other_topic)
    merged_posts = new_topic.posts.all()
    for post in posts:
        assert post in merged_posts
    assert len(merged_posts) == len(posts)

def test_forum_owns_topics(forum : Forum, topic: Topic, other_topic: Topic):
    assert topic.forum is forum
    assert other_topic.forum is forum
    new_topic = forum.merge_topics(topic, other_topic)
    assert new_topic.forum is forum
    assert new_topic.forum_id == forum.id
    assert new_topic in forum.topics
    