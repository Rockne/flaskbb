from flaskbb.forum.models import Topic


def test_all_posts_preserved(topic: Topic, other_topic: Topic):
    before = [post.content for post in [*topic.posts, *other_topic.posts]]
    merged_topic = topic.merge(other_topic)
    after = [post.content for post in merged_topic.posts]

    assert sorted(after) == sorted(before)
