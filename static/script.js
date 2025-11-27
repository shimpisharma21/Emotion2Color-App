// ================== CONFIG ==================

// For LOCAL development (Flask running on 127.0.0.1:5000)
const API_BASE = ""; 

// When you deploy backend to Render, change this to e.g.:
// const API_BASE = "https://emotion2color-backend.onrender.com";


// ================== NAVBAR TOGGLE ==================

const navToggle = document.getElementById("navToggle");
const navLinks = document.getElementById("navLinks");

if (navToggle && navLinks) {
  navToggle.addEventListener("click", () => {
    navLinks.classList.toggle("open");
  });

  navLinks.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      navLinks.classList.remove("open");
    });
  });
}


// ================== DEMO + GRADIENT LOGIC ==================

const generateBtn = document.getElementById("generateBtn");
const demoArt = document.getElementById("demoArt");
const demoEmotionText = document.getElementById("demoEmotionText");
const demoSwatches = document.getElementById("demoSwatches");
const emotionTextArea = document.getElementById("emotionText");
const heroPreviewArt = document.getElementById("heroPreviewArt");

// Example palettes (used for hero + fallback)
const palettes = [
  ["#2E294E", "#541388", "#FFD400", "#D90368"],
  ["#8EC5FC", "#E0C3FC", "#A1C4FD", "#C2E9FB"],
  ["#FF512F", "#DD2476", "#FF9A9E", "#FBD786"],
  ["#F6D365", "#FDA085", "#FFDEE9", "#B5FFFC"],
  ["#00C9FF", "#92FE9D", "#3EECAC", "#EE74E1"]
];

function setGradientFromPalette(element, colors) {
  if (!element) return;
  const gradient = `linear-gradient(135deg, ${colors.join(", ")})`;
  element.style.backgroundImage = gradient;
}

function renderSwatches(container, colors) {
  if (!container) return;
  container.innerHTML = "";
  colors.forEach((color) => {
    const span = document.createElement("span");
    span.className = "swatch";
    span.style.setProperty("--swatch-color", color);
    container.appendChild(span);
  });
}

// Initial hero gradient
if (heroPreviewArt) {
  setGradientFromPalette(heroPreviewArt, palettes[0]);
}


// ================== BUTTON HANDLER ==================

if (generateBtn) {
  generateBtn.addEventListener("click", () => {
    const text = emotionTextArea.value.trim() || "I feel something.";

    if (demoEmotionText) {
      demoEmotionText.textContent = "Analyzing emotion...";
    }

    // Call backend (Flask locally or Render in deployment)
    fetch(`${API_BASE}/api/emotion-to-color`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ emotionText: text })
    })
      .then((res) => res.json())
      .then((data) => {
        const colors = (data && data.colors && data.colors.length)
          ? data.colors
          : palettes[Math.floor(Math.random() * palettes.length)];

        setGradientFromPalette(demoArt, colors);
        renderSwatches(demoSwatches, colors);

        const shownText = data && data.emotionText ? data.emotionText : text;
        if (demoEmotionText) {
          demoEmotionText.textContent =
            `“${shownText.slice(0, 120)}${shownText.length > 120 ? "..." : ""}”`;
        }

        if (demoArt) {
          demoArt.classList.add("pulse");
          setTimeout(() => demoArt.classList.remove("pulse"), 400);
        }
      })
      .catch((err) => {
        console.error("Error calling backend:", err);
        // Fallback: random local palette
        const fallback = palettes[Math.floor(Math.random() * palettes.length)];
        setGradientFromPalette(demoArt, fallback);
        renderSwatches(demoSwatches, fallback);
        if (demoEmotionText) {
          demoEmotionText.textContent =
            "Backend error. Showing a random mood palette.";
        }
      });
  });
}

// ================== OPTIONAL PULSE ANIMATION ==================
// Make sure you have this in styles.css:
//
// .pulse { animation: pulse 0.3s ease-out; }
// @keyframes pulse { from { transform: scale(0.98); } to { transform: scale(1); } }
