import os
from dotenv import load_dotenv
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

NEWS_API_KEY = os.getenv('NEWS_API_KEY')
NEWS_API_ENDPOINT = 'https://newsapi.org/v2/everything'
QUERY = 'artificial intelligence OR machine learning'

def fetch_ai_news():
    """
    Fetch AI-related news articles from NewsAPI.
    
    Returns:
        list: List of article dictionaries, empty list if error occurs
    """
    if not NEWS_API_KEY:
        logger.error("NEWS_API_KEY not found in environment variables")
        return []

    params = {
        'q': QUERY,
        'sortBy': 'publishedAt',
        'language': 'en',
        'apiKey': NEWS_API_KEY,
        'pageSize': 20
    }
    
    try:
        response = requests.get(NEWS_API_ENDPOINT, params=params)
        if response.status_code == 200:
            return response.json().get('articles', [])
        else:
            logger.error(f"Error fetching news: {response.status_code}")
            if response.status_code == 401:
                logger.error("Invalid API key. Please check your NEWS_API_KEY")
            return []
    except Exception as e:
        logger.error(f"Exception while fetching news: {str(e)}")
        return []

if __name__ == "__main__":
    # Test the function
    articles = fetch_ai_news()
    print(f"Found {len(articles)} articles")