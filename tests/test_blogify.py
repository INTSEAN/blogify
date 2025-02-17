import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from blogify.process_article import summarize_article, categorize_article
from blogify.fetch_news import fetch_ai_news
from blogify.models import Article, Base, engine

class TestBlogify(unittest.TestCase):
    def setUp(self):
        # Create test database
        Base.metadata.create_all(engine)
        self.sample_text = "AI researchers at OpenAI have developed a new language model that shows remarkable improvements in understanding context and generating human-like responses."
        
    def tearDown(self):
        # Clean up test database
        Base.metadata.drop_all(engine)

    @patch('blogify.process_article.client')
    def test_summarize_article(self, mock_client):
        # Mock OpenAI response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Test summary"))]
        mock_client.chat.completions.create.return_value = mock_response
        
        result = summarize_article(self.sample_text)
        self.assertEqual(result, "Test summary")

    @patch('openai.OpenAI')
    def test_categorize_article(self, mock_openai):
        # Mock OpenAI response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Research"))]
        mock_openai.return_value.chat.completions.create.return_value = mock_response
        
        result = categorize_article(self.sample_text)
        self.assertEqual(result, "Research")

    @patch('requests.get')
    def test_fetch_ai_news(self, mock_get):
        # Mock news API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'articles': [
                {
                    'title': 'Test Article',
                    'description': 'Test Description',
                    'url': 'http://test.com',
                    'publishedAt': '2024-01-01T00:00:00Z'
                }
            ]
        }
        mock_get.return_value = mock_response
        
        result = fetch_ai_news()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['title'], 'Test Article')

if __name__ == '__main__':
    unittest.main() 