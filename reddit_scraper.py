from reddit_client import get_reddit_client


class RedditScraper:
    def __init__(self):
        self.reddit = get_reddit_client()

    def get_hot_posts(self, subreddit_name, limit=5):
        subreddit = self.reddit.subreddit(subreddit_name)
        hot_posts = subreddit.hot(limit=limit)

        posts = []
        for post in hot_posts:
            post_dict = vars(post)
            post_dict["comments"] = self.get_top_comments(post)
            posts.append(post_dict)

        return posts

    def get_top_comments(self, post):
        comments = []
        post.comments.replace_more(limit=None)
        for comment in post.comments.list():
            comments.append(comment.body)
        return comments
