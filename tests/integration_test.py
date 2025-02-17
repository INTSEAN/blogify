from blogify.fetch_news import fetch_ai_news
from blogify.process_article import summarize_article, categorize_article
from blogify.models import Article, Session

def test_full_workflow():
    # Fetch news
    articles = fetch_ai_news()
    
    if articles:
        article = articles[0]
        
        # Process first article
        summary = summarize_article(article['description'])
        category = categorize_article(article['description'])
        
        # Save to database
        session = Session()
        db_article = Article(
            title=article['title'],
            description=article['description'],
            url=article['url'],
            summary=summary,
            category=category
        )
        session.add(db_article)
        session.commit()
        session.close()
        
        print(f"Processed article: {article['title']}")
        print(f"Summary: {summary}")
        print(f"Category: {category}")

if __name__ == "__main__":
    test_full_workflow() 