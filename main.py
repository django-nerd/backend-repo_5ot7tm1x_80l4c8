import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from database import db, create_document, get_documents
from schemas import (
    Booking,
    Admission,
    TrainerApplication,
    Review,
    ChatRequest,
    ChatResponse,
    ClassBooking,
    ClassJoin,
    LoginRequest,
    LoginResponse,
)

app = FastAPI(title="Vector Strength Gym API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Vector Strength Gym Backend Running"}


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = os.getenv("DATABASE_NAME") or "❌ Not Set"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"

    return response


# Booking endpoint
@app.post("/api/booking")
def create_booking(payload: Booking):
    try:
        booking_id = create_document("booking", payload)
        return {"ok": True, "id": booking_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Admission endpoint
@app.post("/api/admission")
def create_admission(payload: Admission):
    try:
        admission_id = create_document("admission", payload)
        return {"ok": True, "id": admission_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Hire trainer endpoint
@app.post("/api/trainer")
def create_trainer_application(payload: TrainerApplication):
    try:
        trainer_id = create_document("trainerapplication", payload)
        return {"ok": True, "id": trainer_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Reviews
@app.post("/api/reviews")
def create_review(payload: Review):
    try:
        review_id = create_document("review", payload)
        return {"ok": True, "id": review_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/reviews")
def list_reviews(limit: int = 20):
    try:
        reviews = get_documents("review", {}, limit)
        return {"ok": True, "items": reviews}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Classes: book and join
@app.post("/api/book-class")
def api_book_class(payload: ClassBooking):
    try:
        doc_id = create_document("classbooking", payload)
        return {"ok": True, "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/join-class")
def api_join_class(payload: ClassJoin):
    try:
        doc_id = create_document("classjoin", payload)
        return {"ok": True, "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Very simple rule-based chatbot (no external dependencies)
@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    text = req.message.lower().strip()
    reply = ""
    if any(k in text for k in ["price", "membership", "plan", "cost"]):
        reply = (
            "Our plans: Monthly $49, Quarterly $129, Yearly $449. "
            "All plans include group classes and sauna access."
        )
    elif any(k in text for k in ["time", "open", "hour", "hours"]):
        reply = "We're open 5am–11pm on weekdays, 6am–10pm on weekends."
    elif any(k in text for k in ["trainer", "coach", "hire"]):
        reply = (
            "You can hire a personal trainer from the Hire Trainer section. "
            "Sessions start at $35/hour."
        )
    elif any(k in text for k in ["class", "schedule", "book"]):
        reply = (
            "Check the Booking or Classes section to reserve sessions like HIIT, Strength, or Yoga."
        )
    else:
        reply = (
            "Welcome to Vector Strength! Ask me about memberships, hours, classes, or trainers."
        )
    return ChatResponse(reply=reply)


# Simple demo login (email+password); on success returns a fake token.
@app.post("/api/login", response_model=LoginResponse)
def login(payload: LoginRequest):
    # For demo purposes, accept any non-empty password of length >= 6
    if payload.password and len(payload.password) >= 6:
        return LoginResponse(ok=True, token="vs_demo_token")
    return LoginResponse(ok=False, detail="Invalid email or password")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
