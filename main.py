from fastapi import APIRouter, FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import sqlite3
import uvicorn

app = FastAPI(title="Reviews service")
router = APIRouter(prefix="/api", tags=["Отзывы"])


DB_NAME = "reviews.db"

POSITIVE_CONST = [
    "хорош", "люблю"
]

NEGATIVE_CONST = [
    "плохо", "ненавиж"
]


def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            sentiment TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        """)
        conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_sentiment ON reviews(sentiment)
        """)
init_db()


class ReviewCreate(BaseModel):
    text: str

class ReviewResponse(BaseModel):
    id: int
    text: str
    sentiment: str
    created_at: str



def analyze_sentiment(text: str) -> str:
    text = text.lower()
    if any(word in text for word in POSITIVE_CONST):
        return "positive"
    elif any(word in text for word in NEGATIVE_CONST):
        return "negative"
    return "neutral"


@router.post("/reviews", response_model=ReviewResponse, summary='Добавить отзыв', description="""
Создаёт новый отзыв, определяет его настроение
и сохраняет в базу данных. Настроение определяется 
по простому словарю 
(словосочетаниям “хорош”, “люблю” → positive; “плохо”, “ненавиж” → negative; иначе neutral).
""")
def create_review(review: ReviewCreate):
    sentiment = analyze_sentiment(review.text)
    created_at = datetime.utcnow().isoformat()

    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO reviews (text, sentiment, created_at) VALUES (?, ?, ?)",
                (review.text, sentiment, created_at)
            )
            review_id = cursor.lastrowid
    except sqlite3.Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при сохранении отзыва: {str(e)}"
        )

    return ReviewResponse(
        id=review_id,
        text=review.text,
        sentiment=sentiment,
        created_at=created_at
    )


@router.get("/reviews", response_model=List[ReviewResponse], summary='Получить отзывы', description="""
Возвращает список всех отзывов. Можно отфильтровать по sentiment,
указав в query-параметре:
- positive
- negative
- neutral

Если параметр не указан — вернутся все отзывы.
""")
def get_reviews(sentiment: Optional[str] = Query(None)):
    query = "SELECT id, text, sentiment, created_at FROM reviews"
    params = []

    if sentiment:
        query += " WHERE sentiment = ?"
        params.append(sentiment)

    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            rows = cursor.execute(query, params).fetchall()
    except sqlite3.Error as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при получении отзывов: {str(e)}"
        )

    return list(map(lambda row: ReviewResponse(
        id=row[0],
        text=row[1],
        sentiment=row[2],
        created_at=row[3]
    ), rows))


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)