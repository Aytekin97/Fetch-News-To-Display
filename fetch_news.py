from flask import Flask, jsonify
from flask_cors import CORS
import os
from loguru import logger
from db import current_session, NewsModel


app = Flask(__name__)
CORS(app)

@app.route('/api/news/<company>', methods = ["GET"])
def get_company_news(company):
    try:
        """Implement code to send a request to retrieve news articles from DB here"""
        query = current_session.query(NewsModel).filter(NewsModel.company_name == company)
        result = query.all()

        response = [
            {column.name: getattr(row, column.name) for column in NewsModel.__table__.columns}
            for row in result
        ]
        logger.info("Request Successful for company {company}".format(company=company))
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"An error occured: {e}")
        return {"error": "Failed to retrieve DB: {e}".format(e=e)}
    
    finally:
        current_session.close()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)