import os, json
import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# ── DATASET ───────────────────────────────────────────────────────────────────
GENRES = [
  {"label":"Pop / R&B","icon":"🎶","track":"Blinding Lights","artist":"The Weeknd","ytId":"4NRXx6U8ABQ"},
  {"label":"Rap / Hip-Hop","icon":"🎤","track":"God's Plan","artist":"Drake","ytId":"xpVfcZ0ZcFM"},
  {"label":"Classic","icon":"🎻","track":"Bohemian Rhapsody","artist":"Queen","ytId":"fJ9rUzIMcZQ"},
  {"label":"Nostalgic","icon":"🌅","track":"Hotel California","artist":"Eagles","ytId":"BciS5krYL80"},
]

GENRE_SONGS = {
  "Pop / R&B": [
    {"title":"Blinding Lights","artist":"The Weeknd","ytId":"4NRXx6U8ABQ"},
    {"title":"As It Was","artist":"Harry Styles","ytId":"H5v3kku4y6Q"},
    {"title":"Watermelon Sugar","artist":"Harry Styles","ytId":"E07s5ZYygMg"},
    {"title":"Anti-Hero","artist":"Taylor Swift","ytId":"b1kbLwvqugk"},
    {"title":"Levitating","artist":"Dua Lipa","ytId":"TUVcZfQe-Kw"},
    {"title":"Save Your Tears","artist":"The Weeknd","ytId":"XXYlFuWEuKI"},
    {"title":"Peaches","artist":"Justin Bieber","ytId":"tQ0yjYUFKAE"},
    {"title":"Stay","artist":"The Kid LAROI & Justin Bieber","ytId":"kTJczUoc26U"},
    {"title":"Positions","artist":"Ariana Grande","ytId":"tcYodQoapMg"},
    {"title":"Good 4 U","artist":"Olivia Rodrigo","ytId":"gNi_6U5Pm_o"},
    {"title":"drivers license","artist":"Olivia Rodrigo","ytId":"ZmDBbnmKpqQ"},
    {"title":"Love Story (Taylor's Version)","artist":"Taylor Swift","ytId":"8xg3vE8Ie_E"},
    {"title":"Circles","artist":"Post Malone","ytId":"wXhTHyIgQ_U"},
    {"title":"Starboy","artist":"The Weeknd","ytId":"34Na4j8AVgA"},
    {"title":"Shape of You","artist":"Ed Sheeran","ytId":"JGwWNGJdvx8"},
  ],
  "Rap / Hip-Hop": [
    {"title":"God's Plan","artist":"Drake","ytId":"xpVfcZ0ZcFM"},
    {"title":"HUMBLE.","artist":"Kendrick Lamar","ytId":"tvTRZJ-4EyI"},
    {"title":"Rockstar","artist":"Post Malone ft. 21 Savage","ytId":"UceaB4D0jpo"},
    {"title":"Sicko Mode","artist":"Travis Scott","ytId":"6ONRf7h3Mdk"},
    {"title":"Congratulations","artist":"Post Malone","ytId":"SC4xMk98Pdc"},
    {"title":"Lucid Dreams","artist":"Juice WRLD","ytId":"mzB1VGEGcSU"},
    {"title":"XO Tour Llif3","artist":"Lil Uzi Vert","ytId":"WrsFXgrun6g"},
    {"title":"Old Town Road","artist":"Lil Nas X","ytId":"w2Ov5jzm3j8"},
    {"title":"Hotline Bling","artist":"Drake","ytId":"uxpDa-c-4Mc"},
    {"title":"Rap God","artist":"Eminem","ytId":"XbGs_qK2PQA"},
    {"title":"MIDDLE CHILD","artist":"J. Cole","ytId":"MaT4Jk77af8"},
    {"title":"Fefe","artist":"6ix9ine ft. Nicki Minaj","ytId":"qNkR6y_kBjg"},
    {"title":"Money In The Grave","artist":"Drake ft. Rick Ross","ytId":"RjWGetUKqzM"},
    {"title":"Big Rings","artist":"Drake & Future","ytId":"7GaRr2GGzao"},
    {"title":"Wow.","artist":"Post Malone","ytId":"SsodjxbHdcE"},
  ],
  "Classic": [
    {"title":"Bohemian Rhapsody","artist":"Queen","ytId":"fJ9rUzIMcZQ"},
    {"title":"Don't Stop Me Now","artist":"Queen","ytId":"HgzGwKwLmgM"},
    {"title":"Hotel California","artist":"Eagles","ytId":"BciS5krYL80"},
    {"title":"Stairway to Heaven","artist":"Led Zeppelin","ytId":"QkF3oxziUI4"},
    {"title":"Sweet Child O' Mine","artist":"Guns N' Roses","ytId":"1w7OgIMMRc4"},
    {"title":"November Rain","artist":"Guns N' Roses","ytId":"8SbUC-UaAxE"},
    {"title":"Sultans of Swing","artist":"Dire Straits","ytId":"0fAQhSRLQnM"},
    {"title":"Eye of the Tiger","artist":"Survivor","ytId":"btPJPFnesV4"},
    {"title":"Livin' on a Prayer","artist":"Bon Jovi","ytId":"lDK9QqIzhwk"},
    {"title":"Jump","artist":"Van Halen","ytId":"SwYN7mTi6HM"},
    {"title":"Purple Rain","artist":"Prince","ytId":"TvnYmWpD_T8"},
    {"title":"With or Without You","artist":"U2","ytId":"ujNeHIo9dAU"},
    {"title":"We Will Rock You","artist":"Queen","ytId":"-tJYN-eG1zk"},
    {"title":"Dream On","artist":"Aerosmith","ytId":"89dGtCN_cPg"},
    {"title":"Should I Stay or Should I Go","artist":"The Clash","ytId":"BN1WwnEDWAM"},
  ],
  "Nostalgic": [
    {"title":"Hotel California","artist":"Eagles","ytId":"BciS5krYL80"},
    {"title":"Take On Me","artist":"a-ha","ytId":"djV11Xbc914"},
    {"title":"Africa","artist":"Toto","ytId":"FTQbiNvZqaY"},
    {"title":"Don't You (Forget About Me)","artist":"Simple Minds","ytId":"CdqoNKCCt7A"},
    {"title":"Every Breath You Take","artist":"The Police","ytId":"OMOGaugKpzs"},
    {"title":"Come On Eileen","artist":"Dexys Midnight Runners","ytId":"qpbIaE5Bhdk"},
    {"title":"Girls Just Want to Have Fun","artist":"Cyndi Lauper","ytId":"PIb6AZdTr-A"},
    {"title":"Wake Me Up Before You Go-Go","artist":"Wham!","ytId":"pITmCFYkWN8"},
    {"title":"Walking on Sunshine","artist":"Katrina & The Waves","ytId":"iPUmE-tne5U"},
    {"title":"Sweet Home Alabama","artist":"Lynyrd Skynyrd","ytId":"ye5BuYf8q4o"},
    {"title":"Piano Man","artist":"Billy Joel","ytId":"gxEPV4kolz0"},
    {"title":"Summer of '69","artist":"Bryan Adams","ytId":"9f06QZCVUHg"},
    {"title":"99 Luftballons","artist":"Nena","ytId":"La4Dcd1aUcI"},
    {"title":"Kokomo","artist":"The Beach Boys","ytId":"pAwR6C82TCI"},
    {"title":"867-5309/Jenny","artist":"Tommy Tutone","ytId":"6dx_8mHxMI0"},
  ],
}

MUSIC_DB = [
  {"name":"The Weeknd","aliases":["the weeknd","weeknd","уикенд"],"emoji":"🌃",
   "photo":"https://img.youtube.com/vi/4NRXx6U8ABQ/mqdefault.jpg",
   "tagline":"Kanadalik R&B/Pop yulduzi, 'Blinding Lights' ijrochisi",
   "facts":[{"key":"Janr","val":"R&B, Pop, Synth-pop"},{"key":"Mamlakat","val":"Kanada"},{"key":"Faoliyati","val":"2010 - hozirgacha"}],
   "sections":[
     {"title":"Biografiya","icon":"📖","type":"prose","content":"Abel Tesfaye (The Weeknd) - zamonaviy R&B sohasidagi eng katta yulduzlardan biri. Uning 80-yillar sintipopiga yaqin uslubi butun dunyo bo'ylab milliardlab tinglashlarga ega bo'ldi."},
     {"title":"Albomlar","icon":"💿","type":"albums","content":[{"name":"Beauty Behind the Madness","year":"2015"},{"name":"Starboy","year":"2016"},{"name":"After Hours","year":"2020"},{"name":"Dawn FM","year":"2022"}]},
     {"title":"Top qo'shiqlar","icon":"🎵","type":"tracks","content":[{"title":"Blinding Lights","ytId":"4NRXx6U8ABQ"},{"title":"Starboy","ytId":"34Na4j8AVgA"},{"title":"The Hills","ytId":"yzTuBuRdAyA"},{"title":"Can't Feel My Face","ytId":"KEI4qSrkPAs"},{"title":"Save Your Tears","ytId":"XXYlFuWEuKI"}]}
   ],"summary":"The Weeknd zamonaviy pop/R&B sahnasidagi eng nufuzli ijrochilardan biri hisoblanadi."},

  {"name":"Drake","aliases":["drake","дрейк"],"emoji":"🦉",
   "photo":"https://img.youtube.com/vi/xpVfcZ0ZcFM/mqdefault.jpg",
   "tagline":"Kanadalik rap yulduzi, hip-hop sohasining eng ko'p sotuvchi artistlaridan biri",
   "facts":[{"key":"Janr","val":"Hip-Hop, R&B, Rap"},{"key":"Mamlakat","val":"Kanada"},{"key":"Faoliyati","val":"2006 - hozirgacha"}],
   "sections":[
     {"title":"Biografiya","icon":"📖","type":"prose","content":"Drake zamonaviy hip-hop sanoatining eng muvaffaqiyatli artistlaridan biri. U OVO mehnat tashkiloti orqali boshqa artistlarni ham qo'llab-quvvatlaydi."},
     {"title":"Albomlar","icon":"💿","type":"albums","content":[{"name":"Take Care","year":"2011"},{"name":"Views","year":"2016"},{"name":"Scorpion","year":"2018"},{"name":"Certified Lover Boy","year":"2021"}]},
     {"title":"Top qo'shiqlar","icon":"🎵","type":"tracks","content":[{"title":"God's Plan","ytId":"xpVfcZ0ZcFM"},{"title":"One Dance","ytId":"iHCn3a3YIOU"},{"title":"Hotline Bling","ytId":"uxpDa-c-4Mc"},{"title":"In My Feelings","ytId":"DRS_PpOrUZ4"},{"title":"Started From the Bottom","ytId":"RubczQuh47k"}]}
   ],"summary":"Drake hip-hop sanoatining eng nufuzli va ta'sirli figuralaridan biri."},

  {"name":"Taylor Swift","aliases":["taylor swift","тейлор свифт"],"emoji":"🎀",
   "photo":"https://img.youtube.com/vi/nfWlot6h_JM/mqdefault.jpg",
   "tagline":"Amerikalik pop/country yulduzi va eng ko'p mukofotga ega qo'shiqchi sozandalardan biri",
   "facts":[{"key":"Janr","val":"Pop, Country, Folk-pop"},{"key":"Mamlakat","val":"AQSH"},{"key":"Faoliyati","val":"2006 - hozirgacha"}],
   "sections":[
     {"title":"Biografiya","icon":"📖","type":"prose","content":"Taylor Swift country sahnasidan boshlab, keyinchalik pop musiqaning eng yirik yulduziga aylangan. U o'z qo'shiqlarini o'zi yozadi va shaxsiy hayotini ijodida aks ettiradi."},
     {"title":"Albomlar","icon":"💿","type":"albums","content":[{"name":"1989","year":"2014"},{"name":"Reputation","year":"2017"},{"name":"Folklore","year":"2020"},{"name":"Midnights","year":"2022"}]},
     {"title":"Top qo'shiqlar","icon":"🎵","type":"tracks","content":[{"title":"Shake It Off","ytId":"nfWlot6h_JM"},{"title":"Blank Space","ytId":"e-ORhEE9VVg"},{"title":"Anti-Hero","ytId":"b1kbLwvqugk"},{"title":"Love Story","ytId":"8xg3vE8Ie_E"},{"title":"Cruel Summer","ytId":"ic8j13piAhQ"}]}
   ],"summary":"Taylor Swift zamonaviy pop musiqaning eng nufuzli va ta'sirchan ijrochisi hisoblanadi."},

  {"name":"Ed Sheeran","aliases":["ed sheeran","эд ширан"],"emoji":"🎸",
   "photo":"https://img.youtube.com/vi/JGwWNGJdvx8/mqdefault.jpg",
   "tagline":"Britaniyalik pop/akustik gitara qo'shiqchisi va bastakor",
   "facts":[{"key":"Janr","val":"Pop, Folk-pop, Acoustic"},{"key":"Mamlakat","val":"Buyuk Britaniya"},{"key":"Faoliyati","val":"2011 - hozirgacha"}],
   "sections":[
     {"title":"Biografiya","icon":"📖","type":"prose","content":"Ed Sheeran gitara bilan kontsert berishdan boshlab, dunyo bo'ylab eng ko'p sotuvchi pop artistlardan biriga aylandi. Uning qo'shiqlari romantik va samimiy uslubda yoziladi."},
     {"title":"Albomlar","icon":"💿","type":"albums","content":[{"name":"+ (Plus)","year":"2011"},{"name":"x (Multiply)","year":"2014"},{"name":"÷ (Divide)","year":"2017"},{"name":"= (Equals)","year":"2021"}]},
     {"title":"Top qo'shiqlar","icon":"🎵","type":"tracks","content":[{"title":"Shape of You","ytId":"JGwWNGJdvx8"},{"title":"Perfect","ytId":"2Vv-BfVoq4g"},{"title":"Thinking Out Loud","ytId":"lp-EO5I60KA"},{"title":"Photograph","ytId":"nSDgHBxUbVQ"},{"title":"Bad Habits","ytId":"orJSJGHjBLI"}]}
   ],"summary":"Ed Sheeran zamonaviy pop musiqaning eng yumshoq va ommabop ovozlaridan biri."},

  {"name":"Adele","aliases":["adele","адель"],"emoji":"🎤",
   "photo":"https://img.youtube.com/vi/rYEDA3JcQqw/mqdefault.jpg",
   "tagline":"Britaniyalik soul/pop qo'shiqchisi, kuchli vokal ovozi bilan tanilgan",
   "facts":[{"key":"Janr","val":"Soul, Pop, Ballad"},{"key":"Mamlakat","val":"Buyuk Britaniya"},{"key":"Faoliyati","val":"2006 - hozirgacha"}],
   "sections":[
     {"title":"Biografiya","icon":"📖","type":"prose","content":"Adele o'zining kuchli va his-tuyg'uga boy ovozi bilan butun dunyoda tanilgan. Uning albomlari ko'pincha shaxsiy hayotidagi munosabatlar haqida bo'ladi."},
     {"title":"Albomlar","icon":"💿","type":"albums","content":[{"name":"19","year":"2008"},{"name":"21","year":"2011"},{"name":"25","year":"2015"},{"name":"30","year":"2021"}]},
     {"title":"Top qo'shiqlar","icon":"🎵","type":"tracks","content":[{"title":"Rolling in the Deep","ytId":"rYEDA3JcQqw"},{"title":"Someone Like You","ytId":"hLQl3WQQoQ0"},{"title":"Hello","ytId":"YQHsXMglC9A"},{"title":"Set Fire to the Rain","ytId":"Ri7-vnrJD3k"},{"title":"Easy on Me","ytId":"U3ASj1L6_sY"}]}
   ],"summary":"Adele zamonaviy soul-pop musiqaning eng kuchli ovozlaridan biri sifatida tanilgan."},

  {"name":"Billie Eilish","aliases":["billie eilish","билли айлиш"],"emoji":"🖤",
   "photo":"https://img.youtube.com/vi/DyDfgMOUjCI/mqdefault.jpg",
   "tagline":"Amerikalik pop yulduzi, alternativ va minimalistik uslubi bilan tanilgan",
   "facts":[{"key":"Janr","val":"Pop, Alternative, Electropop"},{"key":"Mamlakat","val":"AQSH"},{"key":"Faoliyati","val":"2015 - hozirgacha"}],
   "sections":[
     {"title":"Biografiya","icon":"📖","type":"prose","content":"Billie Eilish o'zining shivirlovchi vokal uslubi va qoraygan alternativ pop sound'i bilan yosh avlod orasida juda mashhur bo'ldi. U ukasi Finneas bilan birga ko'p qo'shiqlar yozadi."},
     {"title":"Albomlar","icon":"💿","type":"albums","content":[{"name":"When We All Fall Asleep, Where Do We Go?","year":"2019"},{"name":"Happier Than Ever","year":"2021"},{"name":"Hit Me Hard and Soft","year":"2024"}]},
     {"title":"Top qo'shiqlar","icon":"🎵","type":"tracks","content":[{"title":"Bad Guy","ytId":"DyDfgMOUjCI"},{"title":"Ocean Eyes","ytId":"viimfQi_pUw"},{"title":"Happier Than Ever","ytId":"5GJWxDKyk3A"},{"title":"Birds of a Feather","ytId":"_XYLD-gOe0I"},{"title":"Lovely","ytId":"AKlqpxFtS2k"}]}
   ],"summary":"Billie Eilish zamonaviy alternativ pop sohasining eng noyob ovozlaridan biri."},

  {"name":"Ariana Grande","aliases":["ariana grande","ариана гранде"],"emoji":"🎀",
   "photo":"https://img.youtube.com/vi/gl1aHhXnN1k/mqdefault.jpg",
   "tagline":"Amerikalik pop/R&B qo'shiqchisi, keng diapazonli ovozi bilan tanilgan",
   "facts":[{"key":"Janr","val":"Pop, R&B"},{"key":"Mamlakat","val":"AQSH"},{"key":"Faoliyati","val":"2008 - hozirgacha"}],
   "sections":[
     {"title":"Biografiya","icon":"📖","type":"prose","content":"Ariana Grande aktrisalikdan musiqaga o'tib, zamonaviy pop musiqaning yetakchi ovozlaridan biriga aylandi. Uning vokal diapazoni va R&B ta'siri uning uslubini ajratib turadi."},
     {"title":"Albomlar","icon":"💿","type":"albums","content":[{"name":"Dangerous Woman","year":"2016"},{"name":"Sweetener","year":"2018"},{"name":"Thank U, Next","year":"2019"},{"name":"Eternal Sunshine","year":"2024"}]},
     {"title":"Top qo'shiqlar","icon":"🎵","type":"tracks","content":[{"title":"Thank U, Next","ytId":"gl1aHhXnN1k"},{"title":"7 Rings","ytId":"QYh6mYIJG2Y"},{"title":"No Tears Left to Cry","ytId":"ffxKSjUwKdU"},{"title":"Problem","ytId":"iS1g8G_njx8"},{"title":"Positions","ytId":"tcYodQoapMg"}]}
   ],"summary":"Ariana Grande zamonaviy pop-R&B sohasining eng kuchli vokalchilaridan biri."},

  {"name":"Eminem","aliases":["eminem","эминем","marshall mathers"],"emoji":"🎤",
   "photo":"https://img.youtube.com/vi/_Yhyp-_hX2s/mqdefault.jpg",
   "tagline":"Amerikalik rap legendasi, tarixdagi eng ko'p sotilgan reperlardan biri",
   "facts":[{"key":"Janr","val":"Hip-Hop, Rap"},{"key":"Mamlakat","val":"AQSH"},{"key":"Faoliyati","val":"1996 - hozirgacha"}],
   "sections":[
     {"title":"Biografiya","icon":"📖","type":"prose","content":"Eminem tezkor va texnik jihatdan murakkab rep uslubi bilan hip-hop tarixidagi eng nufuzli artistlardan biriga aylandi. Uning qo'shiqlari ko'pincha shaxsiy kurashlari va ijtimoiy mavzularga bag'ishlangan."},
     {"title":"Albomlar","icon":"💿","type":"albums","content":[{"name":"The Marshall Mathers LP","year":"2000"},{"name":"The Eminem Show","year":"2002"},{"name":"Recovery","year":"2010"},{"name":"Curtain Call","year":"2005"}]},
     {"title":"Top qo'shiqlar","icon":"🎵","type":"tracks","content":[{"title":"Lose Yourself","ytId":"_Yhyp-_hX2s"},{"title":"Not Afraid","ytId":"j5-yKhDd64s"},{"title":"Stan","ytId":"gOMhN-hfMtY"},{"title":"Without Me","ytId":"YVkUvmDQ3HY"},{"title":"Love the Way You Lie","ytId":"uelHwf8o7_U"}]}
   ],"summary":"Eminem hip-hop tarixidagi eng texnik va ta'sirli reperlardan biri hisoblanadi."},

  {"name":"Michael Jackson","aliases":["michael jackson","майкл джексон","mj"],"emoji":"🕺",
   "photo":"https://img.youtube.com/vi/Zi_XLOBDo_Y/mqdefault.jpg",
   "tagline":"'Pop qiroli' nomi bilan tanilgan, musiqa tarixidagi eng ta'sirli san'atkor",
   "facts":[{"key":"Janr","val":"Pop, R&B, Funk"},{"key":"Mamlakat","val":"AQSH"},{"key":"Faoliyati","val":"1964-2009"}],
   "sections":[
     {"title":"Biografiya","icon":"📖","type":"prose","content":"Michael Jackson dunyo tarixidagi eng katta sotuvchi va eng ta'sirli pop ijrochisiga aylandi. Uning raqs uslubi va video-kliplari musiqa sanoatini o'zgartirdi."},
     {"title":"Albomlar","icon":"💿","type":"albums","content":[{"name":"Off the Wall","year":"1979"},{"name":"Thriller","year":"1982"},{"name":"Bad","year":"1987"},{"name":"Dangerous","year":"1991"}]},
     {"title":"Top qo'shiqlar","icon":"🎵","type":"tracks","content":[{"title":"Billie Jean","ytId":"Zi_XLOBDo_Y"},{"title":"Thriller","ytId":"sOnqjkJTMaA"},{"title":"Beat It","ytId":"oRdxUFDoQe0"},{"title":"Smooth Criminal","ytId":"h_D3VFfhvs4"},{"title":"Man in the Mirror","ytId":"PivWY9wn5ps"}]}
   ],"summary":"Michael Jackson 'Pop qiroli' sifatida musiqa tarixiga abadiy muhrlangan."},

  {"name":"Beyoncé","aliases":["beyonce","beyoncé","бейонсе"],"emoji":"👑",
   "photo":"https://img.youtube.com/vi/bnVUHWCynig/mqdefault.jpg",
   "tagline":"Amerikalik R&B/Pop qirolichasi, Grammy mukofotlarining rekordchisi",
   "facts":[{"key":"Janr","val":"R&B, Pop, Soul"},{"key":"Mamlakat","val":"AQSH"},{"key":"Faoliyati","val":"1997 - hozirgacha"}],
   "sections":[
     {"title":"Biografiya","icon":"📖","type":"prose","content":"Beyoncé Destiny's Child guruhidan boshlab, mustaqil ravishda zamonaviy R&B va pop musiqaning eng nufuzli ovozlaridan biriga aylandi. U sahna mahorati va vokal kuchi bilan ajralib turadi."},
     {"title":"Albomlar","icon":"💿","type":"albums","content":[{"name":"Dangerously in Love","year":"2003"},{"name":"Lemonade","year":"2016"},{"name":"Renaissance","year":"2022"},{"name":"Cowboy Carter","year":"2024"}]},
     {"title":"Top qo'shiqlar","icon":"🎵","type":"tracks","content":[{"title":"Halo","ytId":"bnVUHWCynig"},{"title":"Single Ladies","ytId":"4m1EFMoRFvY"},{"title":"Crazy in Love","ytId":"ViwtNLUqkMY"},{"title":"Formation","ytId":"WDZJPJV__bQ"},{"title":"Texas Hold 'Em","ytId":"SdMODhMlyMY"}]}
   ],"summary":"Beyoncé zamonaviy musiqa sanoatining eng nufuzli va ko'p mukofotlangan yulduzlaridan biri."},

  {"name":"Bruno Mars","aliases":["bruno mars","бруно марс"],"emoji":"🎩",
   "photo":"https://img.youtube.com/vi/OPf0YbXqDm0/mqdefault.jpg",
   "tagline":"Amerikalik pop/funk qo'shiqchisi, sahna mahorati va retro uslubi bilan tanilgan",
   "facts":[{"key":"Janr","val":"Pop, Funk, R&B"},{"key":"Mamlakat","val":"AQSH"},{"key":"Faoliyati","val":"2004 - hozirgacha"}],
   "sections":[
     {"title":"Biografiya","icon":"📖","type":"prose","content":"Bruno Mars zamonaviy pop musiqaga 70-80-yillar funk va soul uslublarini qaytargan ijrochi. Uning jonli ijro mahorati alohida e'tirof etiladi."},
     {"title":"Albomlar","icon":"💿","type":"albums","content":[{"name":"Doo-Wops & Hooligans","year":"2010"},{"name":"Unorthodox Jukebox","year":"2012"},{"name":"24K Magic","year":"2016"}]},
     {"title":"Top qo'shiqlar","icon":"🎵","type":"tracks","content":[{"title":"Uptown Funk","ytId":"OPf0YbXqDm0"},{"title":"24K Magic","ytId":"UqyT8IEBkvY"},{"title":"Just the Way You Are","ytId":"LjhCEhWiKXk"},{"title":"That's What I Like","ytId":"PMivT7MJ41M"},{"title":"Grenade","ytId":"XjVNlgyjcpM"}]}
   ],"summary":"Bruno Mars zamonaviy pop-funk uslubining eng ko'zga ko'ringan vakili."},

  {"name":"Coldplay","aliases":["coldplay","колдплей"],"emoji":"🌈",
   "photo":"https://img.youtube.com/vi/dvgZkm1xWPE/mqdefault.jpg",
   "tagline":"Britaniyalik rok guruhi, dunyoda eng ko'p tinglanadigan jamoalardan biri",
   "facts":[{"key":"Janr","val":"Alternative Rock, Pop Rock"},{"key":"Mamlakat","val":"Buyuk Britaniya"},{"key":"Faoliyati","val":"1996 - hozirgacha"}],
   "sections":[
     {"title":"Biografiya","icon":"📖","type":"prose","content":"Coldplay - Chris Martin boshchiligidagi guruh, ularning musiqasi keng auditoriyaga ega va katta stadion kontsertlari bilan mashhur."},
     {"title":"Albomlar","icon":"💿","type":"albums","content":[{"name":"Parachutes","year":"2000"},{"name":"A Rush of Blood to the Head","year":"2002"},{"name":"Viva la Vida","year":"2008"},{"name":"Music of the Spheres","year":"2021"}]},
     {"title":"Top qo'shiqlar","icon":"🎵","type":"tracks","content":[{"title":"Yellow","ytId":"yKNxeF4KMsY"},{"title":"Viva la Vida","ytId":"dvgZkm1xWPE"},{"title":"The Scientist","ytId":"RB-RcX5DS5A"},{"title":"Paradise","ytId":"1G4isv_Fylg"},{"title":"Hymn for the Weekend","ytId":"YykjpeuMNEk"}]}
   ],"summary":"Coldplay dunyodagi eng katta stadion-rok guruhlaridan biri hisoblanadi."},

  {"name":"Imagine Dragons","aliases":["imagine dragons","имеджин драгонс"],"emoji":"🐉",
   "photo":"https://img.youtube.com/vi/W2TE0DjdNqI/mqdefault.jpg",
   "tagline":"Amerikalik rok guruhi, anthem-uslubdagi xitlari bilan tanilgan",
   "facts":[{"key":"Janr","val":"Alternative Rock, Pop Rock, Electronic"},{"key":"Mamlakat","val":"AQSH"},{"key":"Faoliyati","val":"2008 - hozirgacha"}],
   "sections":[
     {"title":"Biografiya","icon":"📖","type":"prose","content":"Imagine Dragons rok va elektron musiqani birlashtirib, kuchli, energetik va keng auditoriyaga mos qo'shiqlar yaratadi."},
     {"title":"Albomlar","icon":"💿","type":"albums","content":[{"name":"Night Visions","year":"2012"},{"name":"Evolve","year":"2017"},{"name":"Mercury - Act 1","year":"2021"},{"name":"Mercury - Act 2","year":"2022"}]},
     {"title":"Top qo'shiqlar","icon":"🎵","type":"tracks","content":[{"title":"Believer","ytId":"W2TE0DjdNqI"},{"title":"Radioactive","ytId":"ktvTqknDobU"},{"title":"Thunder","ytId":"fKopy74weus"},{"title":"Demons","ytId":"mWRsgZuwf_8"},{"title":"Enemy","ytId":"D9G1VOjN_84"}]}
   ],"summary":"Imagine Dragons zamonaviy alternativ-pop-rok sohasining eng ommabop guruhlaridan biri."},

  {"name":"Dua Lipa","aliases":["dua lipa","дуа липа"],"emoji":"✨",
   "photo":"https://img.youtube.com/vi/DyHkM3YFQVY/mqdefault.jpg",
   "tagline":"Britaniyalik pop/disko-pop yulduzi, retro-disko uyg'onishining yetakchisi",
   "facts":[{"key":"Janr","val":"Pop, Disco-pop, Dance"},{"key":"Mamlakat","val":"Buyuk Britaniya"},{"key":"Faoliyati","val":"2015 - hozirgacha"}],
   "sections":[
     {"title":"Biografiya","icon":"📖","type":"prose","content":"Dua Lipa zamonaviy pop musiqaga 70-80-yillar disko ta'sirini qaytargan eng yorqin ovozlardan biri. Uning raqsga tushiriladigan xitlari butun dunyo bo'ylab mashhur."},
     {"title":"Albomlar","icon":"💿","type":"albums","content":[{"name":"Dua Lipa","year":"2017"},{"name":"Future Nostalgia","year":"2020"},{"name":"Radical Optimism","year":"2024"}]},
     {"title":"Top qo'shiqlar","icon":"🎵","type":"tracks","content":[{"title":"Levitating","ytId":"TUVcZfQe-Kw"},{"title":"Don't Start Now","ytId":"oygrmKOqttA"},{"title":"New Rules","ytId":"k2qgadSvNyU"},{"title":"IDGAF","ytId":"DyHkM3YFQVY"},{"title":"Houdini","ytId":"5OBDFaLCDzQ"}]}
   ],"summary":"Dua Lipa 2020-yillar pop-disko uyg'onishining yetakchi ovozi hisoblanadi."},

  {"name":"Скриптонит","aliases":["скриптонит","scriptonite","scriptonit"],"emoji":"🔮",
   "photo":"https://img.youtube.com/vi/FZIKzFpVLRM/mqdefault.jpg",
   "tagline":"Qozog'istonlik trap/rap ijrochisi, MDH trap musiqasining asoschisi",
   "facts":[{"key":"Janr","val":"Trap, Hip-Hop, Rap"},{"key":"Mamlakat","val":"Qozog'iston"},{"key":"Faoliyati","val":"2012 - hozirgacha"},{"key":"Til","val":"Rus"}],
   "sections":[
     {"title":"Biografiya","icon":"📖","type":"prose","content":"Скриптонит (Adil Zhalelov) MDH trap musiqasining asoschilaridan biri hisoblanadi. Uning melanxolik trap uslubi va chuqur lirikasi uni o'ziga xos qiladi."},
     {"title":"Albomlar","icon":"💿","type":"albums","content":[{"name":"Смутное Время","year":"2016"},{"name":"Дом с нормальным светом","year":"2018"},{"name":"Дети Адама","year":"2023"}]},
     {"title":"Top qo'shiqlar","icon":"🎵","type":"tracks","content":[{"title":"Властелин Калец","ytId":"FZIKzFpVLRM"},{"title":"На Нас","ytId":"jPz5A7SEARCH"},{"title":"Незнакомка","ytId":"SEARCH"},{"title":"Первый Снег","ytId":"SEARCH"},{"title":"Пыяла","ytId":"SEARCH"}]}
   ],"summary":"Скриптонит MDH rap sahnasining eng ta'sirli va noyob ovozlaridan biri."},

  {"name":"BAKR","aliases":["bakr","бакр"],"emoji":"🏔️",
   "photo":"https://img.youtube.com/vi/Rn5GNpGSrMQ/mqdefault.jpg",
   "tagline":"Qirg'izistonlik trap/hip-hop ijrochisi, MDH yoshlar orasida mashhur",
   "facts":[{"key":"Janr","val":"Hip-Hop, Trap, Rap"},{"key":"Mamlakat","val":"Qirg'iziston"},{"key":"Faoliyati","val":"2015 - hozirgacha"},{"key":"Til","val":"Qirg'iz, Rus"}],
   "sections":[
     {"title":"Biografiya","icon":"📖","type":"prose","content":"BAKR Qirg'izistondan chiqqan zamonaviy trap va hip-hop ijrochisi. U qirg'iz va rus tillarida ijro etib, MDH yoshlari orasida katta muxlislar bazasini to'plagan."},
     {"title":"Top qo'shiqlar","icon":"🎵","type":"tracks","content":[{"title":"BAKR - Пустота","ytId":"Rn5GNpGSrMQ"},{"title":"BAKR - Больно","ytId":"SEARCH"},{"title":"BAKR - Холодно","ytId":"SEARCH"},{"title":"BAKR - Дорога","ytId":"SEARCH"},{"title":"BAKR - Небо","ytId":"SEARCH"}]},
     {"title":"Uslub","icon":"🎨","type":"tags","content":["Trap","Hip-Hop","Qirg'iz rap","MDH rap","Yoshlar"]}
   ],"summary":"BAKR Qirg'iziston rap sahnasining eng tanilgan vakili, MDH bo'ylab keng auditoriyaga ega ijrochi."},
]

# ── FUZZY SEARCH ──────────────────────────────────────────────────────────────
def levenshtein(a, b):
    m, n = len(a), len(b)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1): dp[i][0] = i
    for j in range(n+1): dp[0][j] = j
    for i in range(1, m+1):
        for j in range(1, n+1):
            if a[i-1] == b[j-1]: dp[i][j] = dp[i-1][j-1]
            else: dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    return dp[m][n]

def find_artist(text):
    norm = text.lower().strip()
    best, best_len = None, 0
    for a in MUSIC_DB:
        for alias in a["aliases"]:
            if alias in norm and len(alias) > best_len:
                best, best_len = a, len(alias)
    if best: return {"artist": best, "fuzzy": False}
    closest, closest_dist = None, float("inf")
    MAX_DIST = 3
    for a in MUSIC_DB:
        for alias in a["aliases"]:
            d = levenshtein(norm, alias)
            if d < closest_dist:
                closest_dist, closest = d, a
    if closest and closest_dist <= MAX_DIST:
        return {"artist": closest, "fuzzy": True, "dist": closest_dist}
    return None

# ── ENDPOINTS ─────────────────────────────────────────────────────────────────
@app.get("/api/genres")
def get_genres(): return JSONResponse(GENRES)

@app.get("/api/genres/{genre_name}")
def get_genre_songs(genre_name: str): return JSONResponse(GENRE_SONGS.get(genre_name, []))

@app.get("/api/search-artist")
def search_artist(query: str = ""):
    found = find_artist(query)
    if found: return JSONResponse({"found": True, "artist": found["artist"], "fuzzy": found.get("fuzzy", False)})
    return JSONResponse({"found": False})

@app.post("/api/chat")
async def chat(request: Request):
    body = await request.json()
    messages   = body.get("messages", [])
    system     = body.get("system", "")
    max_tokens = body.get("max_tokens", 2000)
    if not ANTHROPIC_API_KEY:
        return JSONResponse({"error": "ANTHROPIC_API_KEY sozlanmagan"}, status_code=500)
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={"Content-Type":"application/json","x-api-key":ANTHROPIC_API_KEY,"anthropic-version":"2023-06-01"},
            json={"model":"claude-sonnet-4-6","max_tokens":max_tokens,"system":system,"messages":messages}
        )
    if resp.status_code != 200:
        return JSONResponse(resp.json(), status_code=resp.status_code)
    return JSONResponse(resp.json())

# ── FRONTEND (HTML) ───────────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
async def index():
    with open("frontend/index.html", "r", encoding="utf-8") as f:
        html = f.read()
    return HTMLResponse(html)
