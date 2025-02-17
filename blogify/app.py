from flask import Flask, render_template, jsonify, request, abort
from fetch_news import fetch_ai_news
from process_article import summarize_article, categorize_article, detailed_summarize_article
from models import Session, Article, get_db_session
import datetime
from sqlalchemy.orm import joinedload

app = Flask(__name__)

@app.route('/')
def home():
    with get_db_session() as session:
        articles = session.query(Article).order_by(Article.published_at.desc()).all()
        if not articles:  # If no articles exist, fetch them
            news_articles = fetch_ai_news()
            for art in news_articles[:5]:  # Process first 5 articles
                try:
                    summary = summarize_article(art.get('content', art.get('description', '')))
                    category = categorize_article(art.get('content', art.get('description', '')))
                    
                    article = Article(
                        title=art['title'],
                        description=art.get('description', ''),
                        url=art['url'],
                        published_at=datetime.datetime.strptime(art['publishedAt'], "%Y-%m-%dT%H:%M:%SZ"),
                        summary=summary,
                        category=category
                    )
                    session.add(article)
                except Exception as e:
                    print(f"Error processing article: {e}")
                    continue
            session.commit()
            # Fetch the newly added articles
            articles = session.query(Article).order_by(Article.published_at.desc()).all()
        
        # Define trending_articles, for example, by selecting the top viewed articles
        trending_articles = session.query(Article).order_by(Article.viewer_count.desc()).limit(5).all()
        
        return render_template('index.html', articles=articles, trending_articles=trending_articles)

@app.route('/update')
def update_news():
    with get_db_session() as session:
        articles = fetch_ai_news()
        new_articles = 0
        for art in articles:
            if session.query(Article).filter_by(url=art['url']).first():
                continue
            
            summary = summarize_article(art.get('content', art.get('description', '')))
            category = categorize_article(art.get('content', art.get('description', '')))
            
            article = Article(
                title=art['title'],
                description=art.get('description', ''),
                url=art['url'],
                published_at=datetime.datetime.strptime(art['publishedAt'], "%Y-%m-%dT%H:%M:%SZ"),
                summary=summary,
                category=category
            )
            session.add(article)
            new_articles += 1
        
        return jsonify({"status": "success", "new_articles": new_articles})

@app.route('/ai-summarize', methods=['POST'])
def ai_summarize():
    data = request.json
    article_ids = data.get('article_ids', [])
    combined_text = ""

    with get_db_session() as session:
        articles = session.query(Article).filter(Article.id.in_(article_ids)).all()
        for article in articles:
            combined_text += article.description + "\n"

    summary = summarize_article(combined_text)
    return jsonify({"summary": summary})

@app.route('/article/<int:article_id>')
def article_detail(article_id):
    with get_db_session() as session:
        article = session.query(Article).get(article_id)
        if not article:
            abort(404)
        # Increment the view count and commit the change
        article.viewer_count = (article.viewer_count or 0) + 1
        session.commit()

        article_data = {
            'title': article.title,
            'description': article.description,
            'category': article.category,
            'published_at': article.published_at,
            'viewer_count': article.viewer_count  # Optionally include this in the context
        }
        deep_dive = detailed_summarize_article(article.description)
    return render_template('article_detail.html', article=article_data, detailed_summary=deep_dive)

@app.route('/increment-view/<int:article_id>', methods=['POST'])
def increment_view(article_id):
    with get_db_session() as session:
        article = session.query(Article).get(article_id)
        if article:
            article.viewer_count = (article.viewer_count or 0) + 1
            session.commit()
    return jsonify({"status": "success"})

@app.route('/articles-json')
def articles_json():
    with get_db_session() as session:
        articles_q = session.query(Article).order_by(Article.published_at.desc()).all()
        articles_list = []
        for article in articles_q:
            articles_list.append({
                "id": article.id,
                "title": article.title,
                "description": article.description,
                "url": article.url,
                "published_at": article.published_at.strftime('%Y-%m-%d %H:%M'),
                "summary": article.summary,
                "category": article.category,
                "viewer_count": article.viewer_count,
                "thumbnail_url": getattr(article, 'thumbnail_url', None)
            })
        return jsonify(articles_list)

if __name__ == '__main__':
    app.run(debug=True)