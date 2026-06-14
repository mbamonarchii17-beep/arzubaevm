require("dotenv").config();
const express = require("express");
const cors    = require("cors");
const fetch   = require("node-fetch");

const app  = express();
const PORT = process.env.PORT || 3000;

// ── CORS: faqat o'z frontend domeningizdan ruxsat bering ─────────────────────
// GitHub Pages domeningizni shu yerga yozing (deploy qilgandan keyin)
const ALLOWED_ORIGINS = [
  "http://localhost:5500",          // lokal test uchun
  "http://127.0.0.1:5500",
   "https://mbamonarchii17-beep.github.io"  // <-- deploydan keyin shu qatorni oching
];

app.use(cors({
  origin: function (origin, callback) {
    // origin yo'q bo'lsa (masalan, curl yoki Postman) ruxsat berma
    if (!origin) return callback(new Error("No origin"), false);
    if (ALLOWED_ORIGINS.some(o => origin.startsWith(o))) {
      return callback(null, true);
    }
    callback(new Error("CORS: ruxsat yo'q — " + origin), false);
  }
}));

app.use(express.json());

// ── Health check ─────────────────────────────────────────────────────────────
app.get("/", (req, res) => {
  res.json({ status: "ok", message: "MoodTune backend ishlayapti 🔥" });
});

// ── /api/chat  →  Anthropic API ──────────────────────────────────────────────
app.post("/api/chat", async (req, res) => {
  const { messages, system, max_tokens = 2000 } = req.body;

  if (!messages || !Array.isArray(messages)) {
    return res.status(400).json({ error: "messages maydoni kerak" });
  }

  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    return res.status(500).json({ error: "Server: ANTHROPIC_API_KEY sozlanmagan" });
  }

  try {
    const response = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "Content-Type":      "application/json",
        "x-api-key":         apiKey,
        "anthropic-version": "2023-06-01"
      },
      body: JSON.stringify({
        model:      "claude-sonnet-4-6",
        max_tokens,
        system,
        messages
      })
    });

    const data = await response.json();

    if (!response.ok) {
      return res.status(response.status).json({ error: data.error || data });
    }

    res.json(data);
  } catch (err) {
    console.error("Anthropic xatosi:", err);
    res.status(502).json({ error: "Anthropic API bilan muammo: " + err.message });
  }
});

app.listen(PORT, () => {
  console.log(`✅ MoodTune backend port ${PORT} da ishga tushdi`);
});
