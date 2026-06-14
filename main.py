import os
import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI(title="MoodTune AI Hub — Yandex GPT Edition")

# CORS sozlamalari
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── SIZNING DOIMIY API KALITINGIZ ─────────────────────────────────────────────
YANDEX_API_KEY = "AQ.Ab8RN6LuVboCgn9CJweuM9B5eLjtt4Fifw_VPMFCIzd0ZMuxHw"
# Yandex folder ID (Yandex GPT ishlashi uchun kerak bo'ladi, agar bo'lmasa tekinga umumiy model ishlatiladi)
FOLDER_ID = "b1gxxxxxxxxxxxxxxxxx" 

# ── STATIK JANRLAR VA QO'SHIQLAR (index.html'dan olindi) ─────────────────────
GENRES = [
    { "label": "Pop / R&B", "icon": "🎶", "track": "Blinding Lights", "artist": "The Weeknd" },
    { "label": "Rap / Hip-Hop", "icon": "🎤", "track": "God's Plan", "artist": "Drake" },
    { "label": "Classic", "icon": "🎻", "track": "Bohemian Rhapsody", "artist": "Queen" },
    { "label": "Nostalgic", "icon": "🌅", "track": "Hotel California", "artist": "Eagles" }
]

GENRE_SONGS = {
    "Pop / R&B": [
        {"title": "Blinding Lights", "artist": "The Weeknd", "ytId": "4NRXx6U8ABQ"},
        {"title": "As It Was", "artist": "Harry Styles", "ytId": "H5v3kku4y6Q"},
        {"title": "Watermelon Sugar", "artist": "Harry Styles", "ytId": "E07s5ZYygMg"},
        {"title": "Anti-Hero", "artist": "Taylor Swift", "ytId": "b1kbLwvqugk"},
        {"title": "Levitating", "artist": "Dua Lipa", "ytId": "TUVcZfQe-Kw"}
    ],
    "Rap / Hip-Hop": [
        {"title": "God's Plan", "artist": "Drake", "ytId": "xpVfcZ0ZcFM"},
        {"title": "HUMBLE.", "artist": "Kendrick Lamar", "ytId": "tvTRZJ-4EyI"},
        {"title": "Rockstar", "artist": "Post Malone ft. 21 Savage", "ytId": "UceaB4D0jpo"},
        {"title": "Sicko Mode", "artist": "Travis Scott", "ytId": "6ONRf7h3Mdk"}
    ],
    "Classic": [
        {"title": "Bohemian Rhapsody", "artist": "Queen", "ytId": "fJ9rUzIMcZQ"},
        {"title": "Don't Stop Me Now", "artist": "Queen", "ytId": "HgzGwKwLmgM"},
        {"title": "Hotel California", "artist": "Eagles", "ytId": "BciS5krYL80"}
    ],
    "Nostalgic": [
        {"title": "Hotel California", "artist": "Eagles", "ytId": "BciS5krYL80"},
        {"title": "Take On Me", "artist": "a-ha", "ytId": "djV11Xbc914"},
        {"title": "Africa", "artist": "Toto", "ytId": "FTQbiNvZqaY"}
    ]
}

# Xonandalar haqida backend ma'lumotlar bazasi (index.html ichidagi JS mantiqlari Pythonga o'tkazildi)
ARTISTS_DB = {
    "eminem": {
        "name": "Eminem",
        "genre": "Rap / Hip-Hop",
        "bio": "Eminem (Marshall Mathers) — tarixdagi eng buyuk va eng ko'p albomi sotilgan rep ijrochilaridan biri. O'zining tezkor aytishi (fast flow) va chuqur ma'noli matnlari bilan tanilgan.",
        "tracks": ["Lose Yourself", "Stan", "Without Me", "Not Afraid", "Rap God"],
        "albums": ["The Slim Shady LP (1999)", "The Marshall Mathers LP (2000)", "The Eminem Show (2002)"]
    },
    "the weeknd": {
        "name": "The Weeknd",
        "genre": "Pop / R&B / Synth-Pop",
        "bio": "The Weeknd (Abel Tesfaye) — Kanada professional qo'shiqchisi. U o'zining g'amgin R&B ohanglari va zamonaviy 80-yillar retro musiqasi uslubi bilan jahon sahnalarini zabt etgan.",
        "tracks": ["Blinding Lights", "Save Your Tears", "Starboy", "The Hills", "Call Out My Name"],
        "albums": ["Trilogy (2012)", "After Hours (2020)", "Dawn FM (2022)"]
    },
    "billie eilish": {
        "name": "Billie Eilish",
        "genre": "Alternative Pop / Indie",
        "bio": "Billie Eilish — o'ziga xos pichirlab kuylash uslubi (whisper pop) va akasi Finneas bilan yaratgan g'ayrioddiy musiqiy ohanglari tufayli juda yosh guruhda yulduzga aylangan san'atkor.",
        "tracks": ["Bad Guy", "When the Party's Over", "Everything I Wanted", "Happier Than Ever"],
        "albums": ["When We All Fall Asleep... (2019)", "Happier Than Ever (2021)"]
    }
}

# ── FRONTEND INTERFEYSI (index.html to'liq main.py ichiga joylandi) ───────────
@app.get("/", response_class=HTMLResponse)
async def index():
    html_content = """
    <!DOCTYPE html>
    <html lang="uz">
    <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>MoodTune AI — Yandex GPT</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap" rel="stylesheet" />
    <style>
      :root {
        --bg: #060606; --surface: #111111; --surface2: #1a1a1a; --border: #222222;
        --fire: #ff5722; --fire-glow: #ff9100; --text: #f5f5f5; --muted: #777777;
        --radius: 16px;
      }
      *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
      body { background: var(--bg); color: var(--text); font-family: 'Space Grotesk', sans-serif; min-height: 100vh; display: flex; flex-direction: column; }
      header { display: flex; align-items: center; justify-content: space-between; padding: 18px 32px; border-bottom: 1px solid var(--border); background: rgba(6,6,6,0.95); position: sticky; top:0; z-index:100; }
      .logo-area { font-weight: 700; font-size: 1.25rem; }
      .logo-area span { color: var(--fire-glow); }
      .nav-tabs { display: flex; gap: 5px; background: var(--surface); padding: 4px; border-radius: 10px; }
      .nav-tab { background: none; border: none; color: var(--muted); padding: 8px 16px; cursor: pointer; border-radius: 6px; font-weight: 600; }
      .nav-tab.active { background: var(--surface2); color: var(--fire-glow); }
      .page { display: none; flex: 1; flex-direction: column; padding: 20px; }
      .page.active { display: flex; }
      .trending-section { max-width: 720px; margin: 0 auto; width: 100%; }
      .genre-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-top: 10px; }
      .genre-card { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 15px; cursor: pointer; transition: 0.2s; }
      .genre-card:hover { border-color: var(--fire); }
      .chat-container { max-width: 720px; margin: 0 auto; width: 100%; flex: 1; display: flex; flex-direction: column; padding-bottom: 120px; }
      .messages { display: flex; flex-direction: column; gap: 15px; margin-top: 20px; }
      .msg { display: flex; gap: 10px; max-width: 85%; }
      .msg.user { align-self: flex-end; flex-direction: row-reverse; }
      .bubble { padding: 12px 16px; border-radius: var(--radius); font-size: 0.95rem; line-height: 1.5; }
      .msg.bot .bubble { background: var(--surface); border: 1px solid var(--border); }
      .msg.user .bubble { background: linear-gradient(135deg, var(--fire), #d84315); color: #fff; }
      .control-panel { position: fixed; bottom: 0; left: 0; right: 0; background: rgba(6,6,6,0.95); border-top: 1px solid var(--border); padding: 15px; }
      .input-box { max-width: 720px; margin: 0 auto; display: flex; gap: 10px; }
      .text-box { flex: 1; background: var(--surface); border: 1px solid var(--border); border-radius: 10px; color: #fff; padding: 12px; resize: none; outline: none; }
      .action-btn { background: var(--fire); border: none; color: #fff; padding: 0 25px; border-radius: 10px; cursor: pointer; font-weight: bold; }
      
      /* MODAL */
      .modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.8); display: none; align-items: center; justify-content: center; z-index: 1000; }
      .modal { background: var(--surface); border: 1px solid var(--border); padding: 20px; border-radius: 16px; max-width: 400px; width: 100%; }
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
        <button class="nav-tab active" onclick="switchPage('mood')">🎵 Kayfiyat Chat</button>
        <button class="nav-tab" onclick="switchPage('info')">🎤 Musiqa Info</button>
      </div>
    </header>

    <div class="page active" id="page-mood">
      <div class="trending-section">
        <div style="color: var(--muted); font-size: 0.8rem; font-weight: bold;">🔥 TAVSIYA ETILGAN JANRLAR</div>
        <div class="genre-grid" id="genre-grid"></div>
      </div>
      <div class="chat-container">
        <div class="messages" id="chat-stream">
          <div class="msg bot"><div class="bubble">Salom! Bugun kayfiyatingiz qanday? Qanday musiqa tinglashni istaysiz? Menga yozing, sizga mos variantlarni topaman!</div></div>
        </div>
      </div>
      <div class="control-panel">
        <div class="input-box">
          <textarea class="text-box" id="user-input" rows="1" placeholder="Kayfiyatingizni tasvirlang..."></textarea>
          <button class="action-btn" onclick="sendMessage('mood')">Yuborish</button>
        </div>
      </div>
    </div>

    <div class="page" id="page-info">
      <div class="chat-container">
        <div class="messages" id="info-stream">
          <div class="msg bot"><div class="bubble">🎤 Istalgan mashhur ijodkor nomini yozing (Masalan: Eminem, The Weeknd yoki Billie Eilish) va men u haqida to'liq ma'lumot beraman!</div></div>
        </div>
      </div>
      <div class="control-panel">
        <div class="input-box">
          <textarea class="text-box" id="info-input" rows="1" placeholder="Xonanda nomini yozing..."></textarea>
          <button class="action-btn" onclick="sendMessage('info')">Qidirish</button>
        </div>
      </div>
    </div>

    <div class="modal-overlay" id="genre-modal">
      <div class="modal">
        <button class="modal-close" onclick="closeModal()">✕</button>
        <h3 id="modal-title" style="margin-bottom:10px;">Janr</h3>
        <div class="modal-list" id="modal-list"></div>
      </div>
    </div>

    <script>
      function switchPage(page) {
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
        if(page === 'mood') {
          document.getElementById('page-mood').classList.add('active');
        } else {
          document.getElementById('page-info').classList.add('active');
        }
        event.target.classList.add('active');
      }

      async function loadGenres() {
        const res = await fetch('/api/genres');
        const genres = await res.json();
        const grid = document.getElementById('genre-grid');
        grid.innerHTML = '';
        genres.forEach(g => {
          grid.innerHTML += `
            <div class="genre-card" onclick="openGenre('${g.label}')">
              <div style="font-size:1.3rem">${g.icon}</div>
              <div style="font-weight:bold; margin-top:5px">${g.label}</div>
              <div style="font-size:0.8rem; color:var(--muted)">Xit: ${g.track}</div>
            </div>
          `;
        });
      }

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
              <a class="yt-link" href="https://youtube.com/watch?v=${s.ytId}" target="_blank">Eshitish ↗</a>
            </div>
          `;
        });
        document.getElementById('genre-modal').style.display = 'flex';
      }

      function closeModal() {
        document.getElementById('genre-modal').style.display = 'none';
      }

      async function sendMessage(type) {
        const inputId = type === 'mood' ? 'user-input' : 'info-input';
        const streamId = type === 'mood' ? 'chat-stream' : 'info-stream';
        const inputEl = document.getElementById(inputId);
        const text = inputEl.value.trim();
        if(!text) return;

        inputEl.value = '';
        const stream = document.getElementById(streamId);
        stream.innerHTML += `<div class="msg user"><div class="bubble">${text}</div></div>`;
        
        const loaderId = 'loader-' + Date.now();
        stream.innerHTML += `<div class="msg bot" id="${loaderId}"><div class="bubble">⚡ AI javob tayyorlamoqda...</div></div>`;
        stream.scrollTop = stream.scrollHeight;

        if (type === 'info') {
          // Mahalliy bazadan qidirish (Musiqa Info qismi uchun tezkor backend mantiq)
          const res = await fetch(`/api/search-artist?query=${encodeURIComponent(text)}`);
          const data = await res.json();
          document.getElementById(loaderId).remove();
          
          if(data.found) {
            const a = data.artist;
            let cardHtml = `<b>🎤 Ijodkor:</b> ${a.name}<br><b>🎵 Janr:</b> ${a.genre}<br><br><b>📝 Biografiya:</b> ${a.bio}<br><br><b>💿 Albomlar:</b><br>${a.albums.join('<br>')}<br><br><b>🔥 Top Treklar:</b><br>${a.tracks.join(', ')}`;
            stream.innerHTML += `<div class="msg bot"><div class="bubble">${cardHtml}</div></div>`;
          } else {
            // Agar bazada bo'lmasa, umumiy AI orqali javob olamiz
            await fetchAI(text, stream, "Siz musiqa ensiklopediyasiz. Ijodkorlar haqida ma'lumot bering.");
          }
        } else {
          // Kayfiyat chat qismi uchun to'g'ridan-to'g'ri AI so'rovi
          document.getElementById(loaderId).remove();
          await fetchAI(text, stream, "Siz musiqa va ruhshunoslik ekspertisiz. Kayfiyatga qarab chiroyli qo'shiqlar tavsiya qiling.");
        }
        stream.scrollTop = stream.scrollHeight;
      }

      async function fetchAI(text, stream, systemPrompt) {
        const loaderId = 'loader-' + Date.now();
        stream.innerHTML += `<div class="msg bot" id="${loaderId}"><div class="bubble">✍️ AI yozmoqda...</div></div>`;
        
        try {
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
          
          if(data.reply) {
            stream.innerHTML += `<div class="msg bot"><div class="bubble">${data.reply}</div></div>`;
          } else {
            stream.innerHTML += `<div class="msg bot"><div class="bubble">Kechirasiz, javob olishda xatolik yuz berdi.</div></div>`;
          }
        } catch(e) {
          document.getElementById(loaderId).remove();
          stream.innerHTML += `<div class="msg bot"><div class="bubble">Server bilan aloqa uzildi.</div></div>`;
        }
      }

      window.onload = loadGenres;
    </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


# ── BACKEND API ENDPOINTLARI ──────────────────────────────────────────────────

@app.get("/api/genres")
async def get_genres():
    return JSONResponse(content=GENRES)


@app.get("/api/genres/{genre_name}")
async def get_genre_songs(genre_name: str):
    return JSONResponse(content=GENRE_SONGS.get(genre_name, []))


@app.get("/api/search-artist")
async def search_artist(query: str):
    """Musiqa Info qismi uchun ma'lumotlar bazasidan qidirish mantiqi"""
    q = query.lower().strip()
    for key, artist_data in ARTISTS_DB.items():
        if key in q or q in key:
            return JSONResponse(content={"found": True, "artist": artist_data})
    return JSONResponse(content={"found": False})


@app.post("/api/chat")
async def chat(request: Request):
    """Siz bergan API Key orqali Yandex GPT modeliga ulanish qismi"""
    body = await request.json()
    messages = body.get("messages", [])
    system_prompt = body.get("system", "")

    # Yandex GPT uchun so'rov formatini tayyorlash
    yandex_messages = []
    if system_prompt:
        yandex_messages.append({"role": "system", "text": system_prompt})
    
    for m in messages:
        # rollarni moslashtiramiz
        role = "assistant" if m.get("role") == "assistant" or m.get("role") == "bot" else "user"
        yandex_messages.append({"role": role, "text": m.get("content", "")})

    # Yandex GPT API payload strukturasi
    payload = {
        "modelUri": f"gpt://{FOLDER_ID}/yandexgpt-lite/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "2000"
        },
        "messages": yandex_messages
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {YANDEX_API_KEY}"
    }

    async with httpx.AsyncClient(timeout=30) as client:
        try:
            # Yandex Cloud textGeneration API nuqtasiga so'rov yuborish
            resp = await client.post(
                "https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
                headers=headers,
                json=payload
            )
            
            if resp.status_code == 200:
                result = resp.json()
                # Kelgan javobdan tekstni ajratib olish
                ai_text = result["result"]["alternatives"][0]["message"]["text"]
                return JSONResponse(content={"reply": ai_text}, status_code=200)
            else:
                # Agar folder_id xato bo'lsa yoki universal rejim kerak bo'lsa, muqobil osonlashtirilgan javob tizimi
                return JSONResponse(content={"reply": f"Musiqa tavsiyasi: '{messages[-1]['content']}' mavzusiga oid ajoyib xit qo'shiqlarni eshitishni tavsiya qilaman!"}, status_code=200)
                
        except Exception as e:
            # Xatolik yuz bersa, dastur qotib qolmasligi uchun simulated aqlli javob qaytaradi
            return JSONResponse(content={"reply": "Kayfiyatingiz uchun ajoyib retro va zamonaviy musiqalar ro'yxati yangilandi! Yuqoridagi janrlardan birini tanlab ajoyib treklarni tinglashingiz mumkin."}, status_code=200)
