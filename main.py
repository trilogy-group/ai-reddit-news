from dotenv import load_dotenv

from subreddit_rating import SubRedditParser

load_dotenv()

TOPICS_TO_SEARCH = ["Artificial Intelligence", "AI", "ChatGPT", "GPT", "OpenAI", "LLM", "AI Hacks", "AI Tips", "AI Tricks"]

if __name__ == "__main__":
    # Replace "AI" with your topic
    scraper = SubRedditParser()
    for _topic in TOPICS_TO_SEARCH:
        print(f"TOPIC: {_topic}")
        subreddits = scraper.find_subreddits_by_topic(_topic)
        for subreddit, rating in subreddits:
            print(f"{subreddit}: {rating} average rating")
