import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Mongo is optional: if URI not provided, app still works
from pymongo import MongoClient

load_dotenv()

app = Flask(__name__)

# ---------- MongoDB setup (optional, free Atlas) ----------
MONGODB_URI = os.getenv("MONGODB_URI", "").strip()
mongo_client = None
moods_collection = None

if MONGODB_URI:
    try:
        mongo_client = MongoClient(MONGODB_URI)
        db = mongo_client["emotion2color"]
        moods_collection = db["moods"]
        print("[Mongo] Connected to Atlas")
    except Exception as e:
        print("[Mongo] Failed to connect:", repr(e))
        mongo_client = None
        moods_collection = None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/emotion-to-color", methods=["POST"])
def emotion_to_color():
    data = request.get_json(force=True) or {}
    emotion_text = (data.get("emotionText") or "").strip()
    if not emotion_text:
        emotion_text = "I feel something, but it's hard to describe."

    # ---------- MOCK AI: fixed palette (always free) ----------
    mock_palette = ["#2E294E", "#541388", "#FFD400", "#D90368"]

    # Save to Mongo if available
    if moods_collection is not None:
        try:
            moods_collection.insert_one(
                {
                    "emotion_text": emotion_text,
                    "colors": mock_palette,
                    "created_at": datetime.utcnow(),
                    "source": "mock",
                }
            )
        except Exception as e:
            print("[Mongo] Insert error:", repr(e))

    return jsonify(
        {
            "success": True,
            "colors": mock_palette,
            "emotionText": emotion_text,
        }
    )


@app.route("/api/mood-journal", methods=["GET"])
def mood_journal():
    """Return last 20 mood entries from Mongo (if configured)."""
    if moods_collection is None:
        return jsonify({"entries": []})

    try:
        cursor = (
            moods_collection.find({}, {"_id": 0})
            .sort("created_at", -1)
            .limit(20)
        )
        entries = list(cursor)
    except Exception as e:
        print("[Mongo] Query error:", repr(e))
        entries = []

    # Convert datetime to string
    for entry in entries:
        if isinstance(entry.get("created_at"), datetime):
            entry["created_at"] = entry["created_at"].isoformat() + "Z"

    return jsonify({"entries": entries})


if __name__ == "__main__":
    app.run(debug=True)
