"""Gera o Post #1 (aquecimento) Decade × Liga Empreendedora: carrossel 3 slides + story.
Uso: python3 decade-liga/gerar_posts.py  (a partir da raiz do repositório)
"""
import os
import urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQ = os.path.join(ROOT, "arquivos")
DIR = os.path.join(ROOT, "decade-liga")
FONTS = os.path.join(DIR, "fonts")
ASSETS = os.path.join(DIR, "assets")
OUT = os.path.join(DIR, "posts")
os.makedirs(ASSETS, exist_ok=True)
os.makedirs(OUT, exist_ok=True)

BLACK = (10, 10, 10)
YELLOW = (243, 196, 29)
WHITE = (255, 255, 255)
GRAY = (140, 140, 140)
LINE = (32, 32, 32)
LIGA_LOGO_URL = "https://www.ligaempreendedora.com/uploads/1/3/9/2/13929691/prancheta-1-c-pia-13_orig.png"


def grotesk(size, weight="Bold"):
    f = ImageFont.truetype(os.path.join(FONTS, "SpaceGrotesk-VF.ttf"), size)
    f.set_variation_by_name(weight)
    return f


def mono(size, bold=False):
    return ImageFont.truetype(os.path.join(FONTS, "SpaceMono-Bold.ttf" if bold else "SpaceMono-Regular.ttf"), size)


# ---------- logos ----------
def liga_logo_white():
    """Logo oficial (site da Liga): letras escuras viram brancas, amarelo é mantido."""
    src = os.path.join(ASSETS, "liga_logo_original.png")
    if not os.path.exists(src):
        req = urllib.request.Request(LIGA_LOGO_URL, headers={"User-Agent": "Mozilla/5.0"})
        open(src, "wb").write(urllib.request.urlopen(req, timeout=30).read())
    im = Image.open(src).convert("RGBA")
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a and max(r, g, b) - min(r, g, b) < 60:  # tons neutros (letras) -> branco
                px[x, y] = (255, 255, 255, a)
    return im.crop(im.getbbox())


def decade_logo(color):
    """Recorta a logo da Decade do post do Gabriel (versão escura sobre fundo claro)."""
    im = Image.open(os.path.join(ARQ, "Post #1 (Modelo 1_ob).png")).convert("L").crop((15, 1022, 680, 1172))
    alpha = ImageOps.invert(im).point(lambda v: 0 if v < 40 else min(255, int((v - 40) * 1.4)))
    out = Image.new("RGBA", im.size, color + (0,))
    out.putalpha(alpha)
    return out.crop(out.getbbox())


def campus_photo(size):
    """Foto aérea do campus (dos posts do Gabriel) em duotone preto e amarelo."""
    im = Image.open(os.path.join(ARQ, "Post #1 (Modelo 1b).png")).convert("L").crop((0, 0, 1080, 1000))
    im = ImageEnhance.Contrast(im).enhance(1.25)
    im = ImageOps.colorize(im, black=BLACK, white=YELLOW, mid=(70, 56, 12))
    return ImageOps.fit(im, size, Image.LANCZOS)


LIGA = liga_logo_white()
DEC_W = decade_logo(WHITE)
DEC_B = decade_logo(BLACK)


def paste_h(canvas, logo, x, y, h):
    lg = logo.resize((int(logo.width * h / logo.height), h), Image.LANCZOS)
    canvas.paste(lg, (int(x), int(y)), lg)
    return lg.width


# ---------- base ----------
def base(w, h):
    im = Image.new("RGB", (w, h), BLACK)
    d = ImageDraw.Draw(im)
    for x in range(0, w, 180):  # grade sutil, como no post da Liga
        d.line([(x, 0), (x, h)], fill=(20, 20, 20), width=1)
    return im, d


def label(d, xy, txt, color=YELLOW, size=26, spacing=6):
    x, y = xy
    f = mono(size, bold=True)
    for ch in txt:
        d.text((x, y), ch, font=f, fill=color)
        x += d.textlength(ch, font=f) + spacing
    return x


def yellow_block(d, w, top_txt, big_txt, x1=None, h=250, bw=260):
    x1 = x1 or w
    d.rectangle([x1 - bw, 0, x1, h], fill=YELLOW)
    d.text((x1 - 40, 36), top_txt, font=mono(24, True), fill=BLACK, anchor="ra")
    size = 80
    while d.textlength(big_txt, font=grotesk(size)) > bw - 60:
        size -= 2
    d.text((x1 - bw / 2, h - 44), big_txt, font=grotesk(size), fill=BLACK, anchor="ms")


def footer(im, d, w, h, left_txt="arraste →"):
    y = h - 170
    d.line([(80, y), (w - 80, y)], fill=LINE, width=2)
    x = 80
    x += paste_h(im, LIGA, x, y + 42, 78) + 30
    d.text((x, y + 81), "×", font=grotesk(46, "Regular"), fill=GRAY, anchor="lm")
    x += 55
    paste_h(im, DEC_W, x, y + 58, 46)
    if left_txt:
        d.text((w - 80, y + 81), left_txt, font=mono(26, True), fill=YELLOW, anchor="rm")


def lines(d, x, y, parts, size, lh):
    """parts: lista de linhas; cada linha é lista de (texto, cor)."""
    f = grotesk(size)
    for ln in parts:
        cx = x
        for t, c in ln:
            d.text((cx, y), t, font=f, fill=c)
            cx += d.textlength(t, font=f)
        y += lh
    return y


W, H = 1080, 1350

# ---------- SLIDE 1: teaser ----------
im, d = base(W, H)
yellow_block(d, W, "UNICAMP", "EM BREVE", bw=300)
label(d, (80, 110), "LIGA EMPREENDEDORA APRESENTA")
y = lines(d, 80, 330, [[("ALGO", WHITE)], [("GRANDE", WHITE)], [("ESTÁ", WHITE)], [("CHEGANDO", YELLOW)]], 150, 150)
d.text((80, y + 60), "à Unicamp. E você vai querer estar lá.", font=grotesk(40, "Medium"), fill=WHITE)
d.text((80, y + 120), "fique de olho nos próximos dias.", font=grotesk(30, "Regular"), fill=GRAY)
footer(im, d, W, H)
im.save(os.path.join(OUT, "post1_slide1_teaser.png"))

# ---------- SLIDE 2: pistas ----------
im, d = base(W, H)
label(d, (80, 110), "PISTAS · 01 / 03")
y = lines(d, 80, 200, [[("VOCÊ JÁ", WHITE)], [("SABE QUEM", WHITE)], [("VEM", YELLOW), ("?", WHITE)]], 128, 132)
clues = [("01", "É uma startup financeira."), ("02", "Foi fundada por ex-executivos do Nubank."),
         ("03", "Usa IA para cuidar de investimentos.")]
y += 50
for n, t in clues:
    d.line([(80, y), (W - 80, y)], fill=LINE, width=2)
    d.text((80, y + 34), n, font=mono(30, True), fill=YELLOW)
    d.text((170, y + 28), t, font=grotesk(38, "Medium"), fill=WHITE)
    y += 118
d.line([(80, y), (W - 80, y)], fill=LINE, width=2)
d.rectangle([80, y + 50, 80 + 560, y + 130], fill=YELLOW)
d.text((110, y + 90), "comente seu palpite ↓", font=mono(30, True), fill=BLACK, anchor="lm")
footer(im, d, W, H)
im.save(os.path.join(OUT, "post1_slide2_pistas.png"))

# ---------- SLIDE 3: revelação ----------
im, d = base(W, H)
photo = campus_photo((W, 640))
im.paste(photo, (0, 0))
fade = Image.new("L", (1, 640))
for i in range(640):
    fade.putpixel((0, i), int(255 * max(0, (i - 360) / 280)))
im.paste(Image.new("RGB", (W, 640), BLACK), (0, 0), fade.resize((W, 640)))
d = ImageDraw.Draw(im)
d.rectangle([60, 64, 290, 124], fill=YELLOW)
label(d, (80, 80), "REVELADO", color=BLACK)
paste_h(im, DEC_W, 80, 610, 120)
d.text((80, 800), "×", font=grotesk(90, "Light"), fill=YELLOW)
paste_h(im, LIGA, 190, 770, 160)
d.text((80, 1000), "A Decade chega à Unicamp", font=grotesk(52), fill=WHITE)
d.text((80, 1062), "em parceria com a Liga Empreendedora.", font=grotesk(40, "Medium"), fill=YELLOW)
label(d, (80, 1150), "EM BREVE · FIQUE DE OLHO", color=GRAY, size=24)
d.line([(80, H - 110), (W - 80, H - 110)], fill=LINE, width=2)
d.text((80, H - 60), "@liga_empreendedora", font=mono(24, True), fill=GRAY, anchor="lm")
d.text((W - 80, H - 60), "ative as notificações", font=mono(24, True), fill=YELLOW, anchor="rm")
im.save(os.path.join(OUT, "post1_slide3_revelacao.png"))

# ---------- STORY ----------
SW, SH = 1080, 1920
im, d = base(SW, SH)
yellow_block(d, SW, "UNICAMP", "EM BREVE", h=300, bw=320)
label(d, (80, 380), "LIGA EMPREENDEDORA APRESENTA", size=24)
y = lines(d, 80, 470, [[("ALGO", WHITE)], [("GRANDE", WHITE)], [("ESTÁ", WHITE)], [("CHEGANDO", YELLOW)]], 150, 150)
d.text((80, y + 30), "Uma startup financeira vem aí.", font=grotesk(44, "Medium"), fill=WHITE)
d.text((80, y + 92), "Quem você acha que é?", font=grotesk(44, "Medium"), fill=YELLOW)
# espaço livre (y ≈ 1330–1500) para o sticker de enquete no app
label(d, (80, 1290), "VOTE NA ENQUETE ↓", color=GRAY, size=22)
y = SH - 400
d.line([(80, y), (SW - 80, y)], fill=LINE, width=2)
x = 80
x += paste_h(im, LIGA, x, y + 55, 90) + 30
d.text((x, y + 100), "×", font=grotesk(52, "Regular"), fill=GRAY, anchor="lm")
paste_h(im, DEC_W, x + 60, y + 73, 54)
im.save(os.path.join(OUT, "post1_story.png"))

print("ok:", sorted(os.listdir(OUT)))
