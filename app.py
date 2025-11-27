import os
import json
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = Flask(__name__)

# --------- MODE FLAGS (ALL CONTROLLED BY ENV) ----------
USE_OPENAI = os.getenv("USE_OPENAI", "false").lower() == "true"
USE_MONGODB = os.getenv("USE_MONGODB", "false").lower() == "true"

# OpenAI client (only used if USE_OPENAI = true)
client = None
if USE_OPENAI:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# (Optional) MongoDB setup placeholder
mongo_client = None
moods_collection = None
if USE_MONGODB:
    from pymongo import MongoClient

    mongo_uri = os.getenv("MONGODB_URI")
    mongo_client = MongoClient(mongo_uri)
    db = mongo_client["emotion2color"]
    moods_collection = db["moods"]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/emotion-to-color", methods=["POST"])
def emotion_to_color():
    data = request.get_json(force=True) or {}
    emotion_text = (data.get("emotionText") or "").strip()

    if not emotion_text:
        emotion_text = "I feel something, but it's hard to describe."

    # ---------- MODE 1: COMPLETELY FREE (NO OPENAI) ----------
    if not USE_OPENAI:
        print("[MODE] Using MOCK palette (no OpenAI)")
        mock_palette = ["#2E294E", "#541388", "#FFD400", "#D90368"]

        # optionally save to Mongo if enabled
        if USE_MONGODB and moods_collection is not None:
            moods_collection.insert_one(
                {
                    "emotion_text": emotion_text,
                    "colors": mock_palette,
                    "source": "mock",
                }
            )

        return jsonify(
            {"success": True, "colors": mock_palette, "emotionText": emotion_text}
        )

    # ---------- MODE 2/3: REAL OPENAI CALL ----------
    prompt = f"""
    You are a color psychology AI.

    Analyze the following emotion description:
    "{emotion_text}"

    Choose 4 or 5 hex colors that best represent this emotional state.
    Consider mood, intensity, and contrast.

    Return ONLY a valid JSON object with this shape:
    {{
      "colors": ["#HEX1", "#HEX2", "#HEX3", "#HEX4"]
    }}

    No explanation, no extra text, no code fences. Only raw JSON.
    """

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        raw_text = completion.choices[0].message.content
        parsed = json.loads(raw_text)
        colors = parsed.get("colors", [])

        if not isinstance(colors, list) or not colors:
            raise ValueError("Bad colors from OpenAI")

        # optionally save to Mongo
        if USE_MONGODB and moods_collection is not None:
            moods_collection.insert_one(
                {
                    "emotion_text": emotion_text,
                    "colors": colors,
                    "source": "openai",
                }
            )

        return jsonify(
            {"success": True, "colors": colors, "emotionText": emotion_text}
        )

    except Exception as e:
        print("Error while talking to OpenAI:", repr(e))
        fallback_palette = ["#2E294E", "#541388", "#FFD400", "#D90368"]
        return jsonify(
            {
                "success": False,
                "colors": fallback_palette,
                "emotionText": emotion_text,
            }
        )


if __name__ == "__main__":
    app.run(debug=True)
