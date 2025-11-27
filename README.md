# Emotion2Color — AI-Driven Emotion Visualization App 🎨

Emotion2Color turns what you *feel* into living color art.

You type your current mood in plain English, and the app generates a smooth gradient and color palette that represents that emotion. The project is built as a full-stack app with a Flask backend and a static frontend, both deployed on free tiers.

---

## 🔗 Live Links

- **Live Frontend (GitHub Pages)**  
  https://shimpisharma21.github.io/emotion2color-frontend/

- **Live Backend API (Render)**  
  https://emotion2color-app.onrender.com/

---

## 📦 Repositories

This project is split into two small repos:

- **Main / Backend (this repo)** – Flask API + deployment config  
  https://github.com/shimpisharma21/Emotion2Color-App  

- **Frontend** – Static HTML/CSS/JS UI that consumes the API  
  https://github.com/shimpisharma21/emotion2color-frontend  

> For portfolio / resume, treat these as a single project:  
> *“Emotion2Color — AI-Driven Emotion Visualization App (Flask + JS, Render + GitHub Pages)”*

---

## 🏗 Architecture (current version)

**Frontend (GitHub Pages)**

- Landing page with:
  - Hero section and “emotion preview” gradient card
  - “Try Live Demo” section with textarea + “Generate Color Art” button
  - Mood journal preview cards (static for now)
- Responsive design for desktop and mobile
- Calls backend using `fetch` via a single base URL:  
  `https://emotion2color-app.onrender.com/api/...`

**Backend (Render)**

- Python **Flask** app exposing JSON APIs
- `POST /api/emotion-to-color`
  - Request body: `{ "emotionText": "<user text>" }`
  - Response: `{"emotionText": "...", "colors": ["#2E294E", ...] }`
  - Currently uses a **mock AI/heuristic mapping** so the demo is 100% free
- Ready to plug in:
  - **OpenAI API** for real sentiment + color mapping
  - **MongoDB Atlas** for storing mood journal entries

---

## 🛠 Tech Stack

- **Backend**
  - Python 3, Flask
  - gunicorn (for production on Render)
  - JSON REST APIs

- **Frontend**
  - HTML5, modern CSS, vanilla JavaScript
  - Hosted on GitHub Pages

- **Infra**
  - Render (free web service) for the Flask app
  - GitHub Pages (free) for static frontend hosting

---

## 📂 Project Structure (this repo)

```text
Emotion2Color-App/
├── app.py             # Flask application & API routes
├── requirements.txt   # Python dependencies
├── Procfile           # Render start command
├── static/            # Shared static assets (CSS, JS, logo) for server-side templates
└── templates/         # Server-rendered HTML (kept for local dev)
