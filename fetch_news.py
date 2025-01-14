from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from loguru import logger
from db import current_session, NewsModel
from sqlalchemy import func
from typing import List, Dict


app = FastAPI()

# Configure CORS
origins = [
    "*"  # Allows all origins. Adjust this list to restrict access as needed.
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,             # Specifies the allowed origins
    allow_credentials=True,            # Allows cookies and authentication headers
    allow_methods=["*"],               # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],               # Allows all headers
)

@app.get("/api/news/{company}", response_model=List[Dict])
def get_company_news(company: str):
    """
    Retrieve news articles for a specified company from the database.
    
    Args:
        company (str): The name of the company to retrieve news for.
    
    Returns:
        List[Dict]: A list of news articles represented as dictionaries.
    """
    try:
        # Query the database for news articles matching the company name (case-insensitive)
        query = current_session.query(NewsModel).filter(
            func.lower(NewsModel.company_name) == company.lower()
        )
        result = query.all()

        # Convert the SQLAlchemy objects to dictionaries
        response = [
            {column.name: getattr(row, column.name) for column in NewsModel.__table__.columns}
            for row in result
        ]

        logger.info(f"Request Successful for company {company}")
        return response

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        # Raise an HTTP 500 error with a custom message
        raise HTTPException(status_code=500, detail=f"Failed to retrieve DB: {e}")

    finally:
        # Ensure the database session is closed
        current_session.close()

if __name__ == "__main__":
    import uvicorn

    # Retrieve the port from environment variables or default to 8080
    port = int(os.environ.get("PORT", 8080))
    
    # Run the FastAPI app using Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
