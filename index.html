import os
import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from dotenv import load_dotenv

# .env faylini yuklash
load_dotenv()

app = FastAPI(title="MoodTune AI Hub")

# CORS barcha tashqi so'rovlar uchun ochiq qilinadi
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── RENDER TOMONIDAN SAQLANADIGAN STATIK DATA (index.html'dan olindi) ─────────
GENRES = [
    { "label": "Pop / R&B", "icon": "🎶", "track": "Blinding Lights", "artist": "The Weeknd", "ytId": "4NRXx6U8ABQ", "search": "The Weeknd Blinding Lights Official" },
    { "label": "Rap / Hip-Hop", "icon": "🎤", "track": "God's Plan", "artist": "Drake", "ytId": "xpVfcZ0ZcFM", "search": "Drake Gods Plan Official Music Video" },
    { "label": "Classic", "icon": "🎻", "track": "Bohemian Rhapsody", "artist": "Queen", "ytId": "fJ9rUzIMcZQ", "search": "Queen Bohemian Rhapsody Official Video" },
    { "label": "Nostalgic", "icon": "🌅", "track": "Hotel California", "artist": "Eagles", "ytId": "BciS5krYL80", "search": "Eagles Hotel California Official" }
]

GENRE_SONGS = {
    "Pop / R&B": [
        {"title": "Blinding Lights", "artist": "The Weeknd", "ytId": "4NRXx6U8ABQ"},
        {"title": "As It Was", "artist": "Harry Styles", "ytId": "H5v3kku4y6Q"},
        {"title": "Watermelon Sugar", "artist": "Harry Styles", "ytId": "E07s5ZYygMg"},
        {"title": "Anti-Hero", "artist": "Taylor Swift", "ytId": "b1kbLwvqugk"},
        {"title": "Levitating", "artist": "Dua Lipa", "ytId": "TUVcZfQe-Kw"},
        {"title": "Save Your Tears", "artist": "The Weeknd", "ytId": "XXYlFuWEuKI"},
        {"title": "Peaches", "artist": "Justin Bieber", "ytId": "tQ0yjYUFKAE"},
        {"title": "Stay", "artist": "The Kid LAROI & Justin Bieber", "ytId": "kTJczUoc26U"}
    ],
    "Rap / Hip-Hop": [
        {"title": "God's Plan", "artist": "Drake", "ytId": "xpVfcZ0ZcFM"},
        {"title": "HUMBLE.", "artist": "Kendrick Lamar", "ytId": "tvTRZJ-4EyI"},
        {"title": "Rockstar", "artist": "Post Malone ft. 21 Savage", "ytId": "UceaB4D0jpo"},
        {"title": "Sicko Mode", "artist": "Travis Scott", "ytId": "6ONRf7h3Mdk"},
        {"title": "Congratulations", "artist": "Post Malone", "ytId": "SC4xMk98Pdc"},
        {"title": "Eminem - Rap God", "artist": "Eminem", "ytId": "XbGs_qK2PQA"}
    ],
    "Classic": [
        {"title": "Bohemian Rhapsody", "artist": "Queen", "ytId": "fJ9rUzIMcZQ"},
        {"title": "Don't Stop Me Now", "artist": "Queen", "ytId": "HgzGwKwLmgM"},
        {"title": "Hotel California", "artist": "Eagles", "ytId": "BciS5krYL80"},
        {"title": "Stairway to Heaven", "artist": "Led Zeppelin", "ytId": "QkF3oxziUI4"},
        {"title": "Sweet Child O' Mine", "artist": "Guns N' Roses", "ytId": "1w7OgIMMRc4"}
    ],
    "Nostalgic": [
        {"title": "Hotel California", "artist": "Eagles", "ytId": "BciS5krYL80"},
        {"title": "Take On Me", "artist": "a-ha", "ytId": "djV11Xbc914"},
        {"title": "Africa", "artist": "Toto", "ytId": "FTQbiNvZqaY"},
        {"title": "Every Breath You Take", "artist": "The Police", "ytId": "OMOGaugKpzs"}
    ]
}

# ── ASOSIY SAHIFA: HTML + CSS + JS (Birlashtirilgan interfeys) ────────────────
@app.get("/", response_class=HTMLResponse)
async def index():
    html_content = """
    <!DOCTYPE html>
    <html lang="uz">
    <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>MoodTune AI</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet" />
    <style>
      :root {
        --bg: #060606; --surface: #111111; --surface2: #1a1a1a; --border: #222222;
        --fire: #ff5722; --fire-glow: #ff9100; --text: #f5f5f5; --muted: #777777;
        --radius: 16px; --font-head: 'Space Grotesk', sans-serif; --font-mono: 'Space Mono', monospace;
      }
      *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
      body { background: var(--bg); color: var(--text); font-family: var(--font-head); min-height: 100vh; display: flex; flex-direction: column; overflow-x: hidden; }
      header { display: flex; align-items: center; justify-content: space-between; padding: 18px 32px; border-bottom: 1px solid var(--border); position: sticky; top: 0; background: rgba(6,6,6,0.95); backdrop-filter: blur(16px); z-index: 100; }
      .logo-area { display: flex; align-items: center; gap: 14px; font-weight: 700; font-size: 1.25rem; }
      .logo-area span { color: transparent; background: linear-gradient(to right, var(--fire-glow), #fff); -webkit-background-clip: text; background-clip: text; }
      .nav-tabs { display: flex; gap: 4px; background: var(--surface); padding: 4px; border-radius: 10px; border: 1px solid var(--border); }
      .nav-tab { background: none; border: none; color: var(--muted); padding: 7px 14px; cursor: pointer; border-radius: 6px; font-weight: 600; }
      .nav-tab.active { background: var(--surface2); color: var(--fire-glow); }
      .page { display: none; flex: 1; flex-direction: column; padding: 20px; }
      .page.active { display: flex; }
      .trending-section { max-width: 720px; margin: 0 auto; width: 100%; }
      .genre-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-top: 10px; }
      .genre-card { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 15px; cursor: pointer; transition: all 0.2s; }
      .genre-card:hover { border-color: var(--fire); transform: translateY(-2px); }
      .chat-container { max-width: 720px; margin: 0 auto; width: 100%; flex: 1; display: flex; flex-direction: column; padding-bottom: 120px; }
      .messages { display: flex; flex-direction: column; gap: 15px; margin-top: 20px; }
      .msg { display: flex; gap: 10px; max-width: 80%; }
      .msg.user { align-self: flex-end; flex-direction: row-reverse; }
      .bubble { padding: 12px 16px; border-radius: var(--radius); font-size: 0.95rem; line-height: 1.5; }
      .msg.bot .bubble { background: var(--surface); border: 1px solid var(--border); }
      .msg.user .bubble { background: linear-gradient(135deg, var(--fire), #d84315); color: #fff; }
      .control-panel { position: fixed; bottom: 0; left: 0; right: 0; background: rgba(6,6,6,0.95); border-top: 1px solid var(--border); padding: 15px; backdrop-filter: blur(10px); }
      .input-box { max-width: 720px; margin: 0 auto; display: flex; gap: 10px; }
      .text-box { flex: 1; background: var(--surface); border: 1px solid var(--border); border-radius: 10px; color: #fff; padding: 12px; resize: none; outline: none; }
      .action-btn { background: var(--fire); border: none; color: #fff; padding: 0 20px; border-radius: 10px; cursor: pointer; }
      
      /* MODAL STYLES */
      .modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.8); display: none; align-items: center; justify-content: center; z-index: 1000; }
      .modal { background: var(--surface); border: 1px solid var(--border); padding: 20px; border-radius: 16px; max-width: 400px; width: 100%; color: #fff; }
      .modal-close { background: var(--surface2); border: none; color: #fff; padding: 5px 10px; cursor: pointer; float: right; border-radius: 5px; }
      .modal-list { margin-top: 15px; display: flex; flex-direction: column; gap: 8px; }
      .modal-item { background: var(--surface2); padding: 10px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; }
      .yt-link { color: #ff4444; text-decoration: none; font-size: 0.8rem; font-weight: bold; }
    </style>
    </head>
    <body>

    <header>
      <div class="logo-area">🎵 MoodTune<span>AI</span></div>
      <div class="nav-tabs">
        <button class="nav-tab active" onclick="switchPage('mood')">🎵 Mood Chat</button>
        <button class="nav-tab" onclick="switchPage('info')">🎤 Music Info</button>
      </div>
    </header>

    <div class="page active" id="page-mood">
      <div class="trending-section">
        <div style="color: var(--muted); font-size: 0.8rem; font-weight: bold;">🔥 TRENDING HOZIR</div>
        <div class="genre-grid" id="genre-grid"></div>
      </div>
      <div class="chat-container">
        <div class="messages" id="chat-stream">
          <div class="msg bot"><div class="bubble">Salom! Bugun kayfiyatingiz qanday? Qaysi janrdagi musiqalarni yoqtirasiz?</div></div>
        </div>
      </div>
      <div class="control-panel">
        <div class="input-box">
          <textarea class="text-box" id="user-input" rows="1" placeholder="Yoqtirgan musiqangiz yoki kayfiyatingizni yozing..."></textarea>
          <button class="action-btn" onclick="sendMessage('mood')">Yuborish</button>
        </div>
      </div>
    </div>

    <div class="page" id="page-info">
      <div class="chat-container">
        <div class="messages" id="info-stream">
          <div class="msg bot"><div class="bubble">🎤 Istalgan xonanda, albom yoki qo'shiq haqida ma'lumotsiz so'rang (Masalan: Eminem yoki Billie Eilish)</div></div>
        </div>
      </div>
      <div class="control-panel">
        <div class="input-box">
          <textarea class="text-box" id="info-input" rows="1" placeholder="Xonanda yoki trek nomini yozing..."></textarea>
          <button class="action-btn" onclick="sendMessage('info')">So'rash</button>
        </div>
      </div>
    </div>

    <div class="modal-overlay" id="genre-modal">
      <div class="modal">
        <button class="modal-close" onclick="closeModal()">✕</button>
        <h3 id="modal-title">Janr Qo'shiqlari</h3>
        <div class="modal-list" id="modal-list"></div>
      </div>
    </div>

    <script>
      // Sahifalarni almashtirish
      function switchPage(page) {
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
        
        if(page === 'mood') {
          document.getElementById('page-mood').classList.add('active');
          event.target.classList.add('active');
        } else {
          document.getElementById('page-info').classList.add('active');
          event.target.classList.add('active');
        }
      }

      // Backend API'dan janrlarni yuklash va chizish
      async function loadGenres() {
        const res = await fetch('/api/genres');
        const genres = await res.json();
        const grid = document.getElementById('genre-grid');
        grid.innerHTML = '';
        genres.forEach(g => {
          grid.innerHTML += `
            <div class="genre-card" onclick="openGenre('${g.label}')">
              <div style="font-size:1.5rem">${g.icon}</div>
              <div style="font-weight:bold; margin-top:5px">${g.label}</div>
              <div style="font-size:0.8rem; color:var(--muted)">${g.artist} - ${g.track}</div>
            </div>
          `;
        });
      }

      // Janr modal oynasini ochish
      async function openGenre(genreName) {
        document.getElementById('modal-title').innerText = genreName;
        const res = await fetch(`/api/genres/${encodeURIComponent(genreName)}`);
        const songs = await res.json();
        
        const list = document.getElementById('modal-list');
        list.innerHTML = '';
        songs.forEach(s => {
          list.innerHTML += `
            <div class="modal-item">
              <div>
                <div style="font-weight:bold; font-size:0.9rem">${s.title}</div>
                <div style="font-size:0.75rem; color:var(--muted)">${s.artist}</div>
              </div>
              <a class="yt-link" href="https://youtube.com/watch?v=${s.ytId}" target="_blank">YouTube ↗</a>
            </div>
          `;
        });
        document.getElementById('genre-modal').style.display = 'flex';
      }

      function closeModal() {
        document.getElementById('genre-modal').style.display = 'none';
      }

      // Claude AI bilan Chat aloqasi
      async function sendMessage(type) {
        const inputId = type === 'mood' ? 'user-input' : 'info-input';
        const streamId = type === 'mood' ? 'chat-stream' : 'info-stream';
        const inputEl = document.getElementById(inputId);
        const text = inputEl.value.trim();
        if(!text) return;

        inputEl.value = '';
        const stream = document.getElementById(streamId);
        
        // Foydalanuvchi xabari
        stream.innerHTML += `<div class="msg user"><div class="bubble">${text}</div></div>`;
        
        // Loader (Kutish)
        const loaderId = 'loader-' + Date.now();
        stream.innerHTML += `<div class="msg bot" id="${loaderId}"><div class="bubble">✍️ O'ylamoqdaman...</div></div>`;
        stream.scrollTop = stream.scrollHeight;

        try {
          const systemPrompt = type === 'mood' 
            ? "Siz professional musiqa ekspertisiz. Foydalanuvchining kayfiyatiga mos qo'shiqlar va ijodkorlarni tavsiya qiling."
            : "Siz musiqa ensiklopediyasiz. Ijodkorlar, albomlar va treklar tarixi haqida aniq ma'lumot bering.";

          const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
              system: systemPrompt,
              messages: [{role: "user", content: text}]
            })
          });
          
          const data = await response.json();
          document.getElementById(loaderId).remove();

          if(data.content && data.content[0]) {
            stream.innerHTML += `<div class="msg bot"><div class="bubble">${data.content[0].text}</div></div>`;
          } else {
            stream.innerHTML += `<div class="msg bot"><div class="bubble">Xatolik yuz berdi, qaytadan urinib ko'ring.</div></div>`;
          }
        } catch (e) {
          document.getElementById(loaderId).remove();
          stream.innerHTML += `<div class="msg bot"><div class="bubble">Serverga ulanishda xatolik.</div></div>`;
        }
        stream.scrollTop = stream.scrollHeight;
      }

      // Birinchi yuklanganda janrlarni chiqarish
      window.onload = loadGenres;
    </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


# ── INTERNAL ROUTERS (JS Mantiqlari Pythonga o'tkazildi) ─────────────────────

@app.get("/api/genres")
async def get_genres():
    """Barcha mavjud janrlar ro'yxatini qaytaradi"""
    return JSONResponse(content=GENRES)


@app.get("/api/genres/{genre_name}")
async def get_genre_songs(genre_name: str):
    """Tanlangan janr ichidagi qo'shiqlar ro'yxatini qaytaradi"""
    songs = GENRE_SONGS.get(genre_name, [])
    return JSONResponse(content=songs)


@app.post("/api/chat")
async def chat(request: Request):
    """Claude API orqali javob olish qismi"""
    body = await request.json()
    messages = body.get("messages", [])
    system_prompt = body.get("system", "")
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return JSONResponse({"error": "ANTHROPIC_API_KEY topilmadi"}, status_code=500)

    payload = {
        "model": "claude-3-5-sonnet-latest",
        "max_tokens": 2000,
        "system": system_prompt,
        "messages": messages,
    }

    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
    }

    async with httpx.AsyncClient(timeout=60) as client:
        try:
            resp = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=payload
            )
            return JSONResponse(content=resp.json(), status_code=resp.status_code)
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)
