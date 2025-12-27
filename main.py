from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# --- מודלים של נתונים ---

class Flashcard(BaseModel):
    question: str
    answer: str

# מודל חדש: מייצג משפט מסונכרן בזמן (בשביל הכתוביות)
class TranscriptSegment(BaseModel):
    text: str
    start: float  # זמן התחלה בשניות
    end: float    # זמן סיום בשניות

class LectureResult(BaseModel):
    id: int
    title: str
    video_url: str  # הוספנו לינק לווידאו (חשוב ל-Frontend)
    transcript: List[TranscriptSegment]  # עברנו מרשימה פשוטה לרשימה מסונכרנת
    summary: List[str]  # סיכום כרשימת נקודות (יותר נוח לתצוגה)
    flashcards: List[Flashcard]

# --- נתוני דמה (Mock Data) משודרגים ---

db_mock = [
    {
        "id": 1,
        "title": "מבוא לסיבוכיות - הרצאה 1",
        "video_url": "https://www.w3schools.com/html/mov_bbb.mp4", # וידאו לדוגמה
        "transcript": [
            {"text": "שלום לכולם, היום נלמד על Big O", "start": 0.5, "end": 3.2},
            {"text": "סיבוכיות זמן היא מדד ליעילות אלגוריתם", "start": 3.5, "end": 6.8},
            {"text": "אנחנו נתמקד במקרה הגרוע ביותר", "start": 7.0, "end": 10.1}
        ],
        "summary": [
            "הגדרה של סיבוכיות זמן",
            "הסבר על סימון Big O",
            "ההבדל בין המקרה הממוצע למקרה הגרוע"
        ],
        "flashcards": [
            {"question": "מה זה O(n)?", "answer": "זמן ריצה ליניארי שגדל עם הקלט"},
            {"question": "מה מייצג ה-Pivot ב-QuickSort?", "answer": "איבר להשוואה שעל פיו מחלקים את המערך"}
        ]
    }
]

# --- Endpoints ---

@app.get("/")
def read_root():
    return {
        "status": "Online",
        "project": "Accessible Academic",
        "version": "1.0.0-HLD"
    }

@app.get("/lectures", response_model=List[LectureResult])
def get_all_lectures():
    return db_mock

@app.get("/lectures/{lecture_id}", response_model=LectureResult)
def get_lecture(lecture_id: int):
    lecture = next((item for item in db_mock if item["id"] == lecture_id), None)
    if not lecture:
        raise HTTPException(status_code=404, detail="Lecture not found")
    return lecture

# נתיב חדש: שליפת רק הכתוביות (SRT-like)
@app.get("/lectures/{lecture_id}/transcript", response_model=List[TranscriptSegment])
def get_transcript(lecture_id: int):
    lecture = next((item for item in db_mock if item["id"] == lecture_id), None)
    if not lecture:
        raise HTTPException(status_code=404, detail="Lecture not found")
    return lecture["transcript"]