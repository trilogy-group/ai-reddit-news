import os

from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

from gpt4_llm import PostRatingLLM
from reddit_client import get_reddit_client


class SubRedditParser:

    MAX_WORKER_COUNT = int(os.environ.get("MAX_WORKER_COUNT")) if os.environ.get("MAX_WORKER_COUNT") else None

    def __init__(self):
        self.reddit = get_reddit_client()

    def rate_post(self, post):
        top_comments = post.comments.list()[:5]  # Adjust as needed

        # Use the LLM to rate the content
        return post, PostRatingLLM().rate(
            post_title=post.title,
            post_body=post.selftext,
            post_comments=" ".join(comment.body for comment in top_comments),
        )

    def find_subreddits_by_topic(self, topic, limit=100):
        # Search for posts related to the topic
        posts = self.reddit.subreddit("all").search(topic, limit=limit)

        # Rate the posts and aggregate the ratings for each subreddit
        subreddit_scores = defaultdict(int)
        subreddit_counts = defaultdict(int)

        with ThreadPoolExecutor(max_workers=self.MAX_WORKER_COUNT) as executor:
            for post, rating in executor.map(self.rate_post, posts):
                if rating > 0:
                    subreddit_scores[post.subreddit.display_name] += rating
                    subreddit_counts[post.subreddit.display_name] += 1

        # Calculate the average rating for each subreddit
        subreddit_ratings = {
            subreddit: score / subreddit_counts[subreddit]
            for subreddit, score in subreddit_scores.items()
        }

        # Sort the subreddits by their average rating and return them
        sorted_subreddits = sorted(
            subreddit_ratings.items(), key=lambda x: x[1], reverse=True
        )

        return sorted_subreddits
