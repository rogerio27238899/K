"""Gera os posts e stories Decade × Liga Empreendedora.

Referência visual: as peças do Octávio (diretor de marketing) em arquivos/401499–401502.
  - FASE 1 (aquecimento, Post 1 + story): estilo do teaser 401502. Off-white, símbolo da Decade em
    marca d'água, título em serif (Playfair Display) com a palavra-chave em itálico, rótulos e datas em
    mono espaçado, logos Decade | Liga lado a lado.
  - FASES 2 A 4 (posts 2 a 8 + stories): estilo dos cartazes 401499–401501. Fundo preto, "DECADE" em
    amarelo #F5C518 e mono pesado, "NA UNICAMP" em branco e mono leve, linhas tracejadas, faixa
    "data - hora - local" em Anton, texto corrido em mono, "INSCREVA-SE!" em Anton amarelo,
    logo da Liga à esquerda e da Decade à direita no rodapé.
Paleta e fontes seguem o Manual_Marca_Evento_Decade.pdf (Liga: Anton, Montserrat, JetBrains Mono;
Decade: serif editorial + mono).

Uso: python3 decade-liga/gerar_posts.py  (a partir da raiz do repositório)
"""
import datetime as dt
import os
import urllib.request

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQ = os.path.join(ROOT, "arquivos")
DIR = os.path.join(ROOT, "decade-liga")
FONTS = os.path.join(DIR, "fonts")
ASSETS = os.path.join(DIR, "assets")
OUT = os.path.join(DIR, "posts")
os.makedirs(ASSETS, exist_ok=True)
os.makedirs(OUT, exist_ok=True)

# >>> CONFIRMAR COM A DECADE E A LIGA antes de publicar <<<
EVENTO = {
    "data": dt.date(2026, 10, 26),
    "hora": "9h",          # cartazes 401499–401501 dizem 9h; o teaser 401502 diz 17h30
    "local": "Auditório",  # os cartazes não dizem qual auditório
}
EV = EVENTO["data"]
MESES = ["", "janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro",
         "outubro", "novembro", "dezembro"]
SEMANA = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]
DATA = f"{EV.day:02d}.{EV.month:02d}"
FAIXA = f"{DATA}  -  {EVENTO['hora']}  -  {EVENTO['local']}"   # como nos cartazes: "26.10 - 9h - Auditório"
DATA_EXT = f"{SEMANA[EV.weekday()]}, {EV.day} de {MESES[EV.month]}"
MES_UP = MESES[EV.month].upper()

W, H = 1080, 1350     # feed 4:5
SW, SH = 1080, 1920   # story 9:16

# ---------- paletas (hex do manual, conferidos nos cartazes) ----------
BLACK = (0, 0, 0)
AMARELO = (245, 197, 24)     # #F5C518
BRANCO = (255, 254, 251)     # #FFFEFB
CINZA = (110, 117, 124)      # #6E757C (tracejado do 401501)
CINZA_TXT = (170, 170, 170)  # texto secundário (subtítulo do 401499)

D_OFF = (245, 241, 236)      # #F5F1EC
D_CINZA_MEDIO = (81, 79, 77)  # #514F4D
D_GRAFITE = (52, 51, 50)     # #343332
D_WM = (233, 229, 223)       # marca d'água do 401502
D_HAIR = (214, 209, 202)


# ---------- fontes ----------
def _vf(file, size, name):
    f = ImageFont.truetype(os.path.join(FONTS, file), size)
    f.set_variation_by_name(name)
    return f


def serif(size, italic=False):
    return _vf("PlayfairDisplay-Italic-VF.ttf", size, "Italic") if italic else _vf("PlayfairDisplay-VF.ttf", size, "Regular")


def jb(size, weight="Regular"):
    return _vf("JetBrainsMono-VF.ttf", size, weight)


def anton(size):
    return ImageFont.truetype(os.path.join(FONTS, "Anton-Regular.ttf"), size)


def mont(size, weight="Bold"):
    return _vf("Montserrat-VF.ttf", size, weight)


def smono(size):
    return ImageFont.truetype(os.path.join(FONTS, "SpaceMono-Bold.ttf"), size)


# ---------- logos e imagens ----------
LIGA_LOGO_URL = "https://www.ligaempreendedora.com/uploads/1/3/9/2/13929691/prancheta-1-c-pia-13_orig.png"


def liga_original():
    src = os.path.join(ASSETS, "liga_logo_original.png")
    if not os.path.exists(src):
        req = urllib.request.Request(LIGA_LOGO_URL, headers={"User-Agent": "Mozilla/5.0"})
        open(src, "wb").write(urllib.request.urlopen(req, timeout=30).read())
    im = Image.open(src).convert("RGBA")
    return im.crop(im.getbbox())


def liga_on_dark():
    """Versão para fundo preto, como nos cartazes: 'LIGA' em branco, foguete e 'EMPREENDEDORA' em amarelo."""
    im = liga_original().copy()
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a and max(r, g, b) - min(r, g, b) < 60:
                px[x, y] = BRANCO + (a,)
    return im


def decade_lockup(color):
    """Lockup símbolo + 'Decade', recortado de arquivos/Post #1 (Modelo 1_ob).png."""
    im = Image.open(os.path.join(ARQ, "Post #1 (Modelo 1_ob).png")).convert("L").crop((15, 1022, 680, 1172))
    alpha = ImageOps.invert(im).point(lambda v: 0 if v < 40 else min(255, int((v - 40) * 1.4)))
    out = Image.new("RGBA", im.size, color + (0,))
    out.putalpha(alpha)
    return out.crop(out.getbbox())


_SYM = None


def decade_symbol_mask(h, blur=None):
    global _SYM
    if _SYM is None:
        g = Image.open(os.path.join(ARQ, "Post #1 (Modelo 1_ob).png")).convert("L").crop((19, 1031, 165, 1167))
        _SYM = ImageOps.invert(g)
    m = _SYM.resize((int(_SYM.width * h / _SYM.height), h), Image.LANCZOS)
    if blur:
        m = m.point(lambda v: 255 if v > 110 else 0).filter(ImageFilter.GaussianBlur(blur))
    else:
        m = m.point(lambda v: 0 if v < 40 else min(255, int((v - 40) * 1.4)))
    return m.crop(m.getbbox())


def campus_photo(size):
    im = Image.open(os.path.join(ARQ, "Post #1 (Modelo 1b).png")).convert("RGB").crop((0, 0, 1080, 1000))
    return ImageOps.fit(im, size, Image.LANCZOS, centering=(0.5, 0.45))


def qr_code():
    """QR dos cartazes do Octávio (401500). Substituir pelo QR real da inscrição quando existir."""
    return Image.open(os.path.join(ARQ, "401500.png")).convert("RGB").crop((505, 1262, 918, 1675))


LIGA_ORIG = liga_original()
LIGA_DARK = liga_on_dark()
DEC_OFF = decade_lockup(BRANCO)
DEC_BLACK = decade_lockup(BLACK)
LIGA_BLACK = Image.new("RGBA", LIGA_ORIG.size, BLACK + (0,))
LIGA_BLACK.putalpha(LIGA_ORIG.getchannel("A"))
QR = qr_code()


def paste_h(canvas, logo, x, y, h):
    lg = logo.resize((int(logo.width * h / logo.height), h), Image.LANCZOS)
    canvas.paste(lg, (int(x), int(y)), lg)
    return lg.width


def logo_w(logo, h):
    return int(logo.width * h / logo.height)


def save(im, name):
    im.save(os.path.join(OUT, name))


# ---------- texto ----------
def spaced(d, txt, y, font, fill, sp=12, w=W, x=None):
    tw = sum(d.textlength(c, font=font) for c in txt) + sp * (len(txt) - 1)
    cx = (w - tw) / 2 if x is None else x
    for ch in txt:
        d.text((cx, y), ch, font=font, fill=fill)
        cx += d.textlength(ch, font=font) + sp


def wrap_lines(d, txt, font, maxw):
    out, line = [], ""
    for word in txt.split():
        t = (line + " " + word).strip()
        if d.textlength(t, font=font) <= maxw:
            line = t
        else:
            out.append(line)
            line = word
    if line:
        out.append(line)
    return out


def text_block(d, txt, y, font, fill, maxw, lh, w=W, x=None):
    """Centralizado (x=None) ou alinhado à esquerda em x."""
    for ln in wrap_lines(d, txt, font, maxw):
        if x is None:
            d.text((w / 2, y), ln, font=font, fill=fill, anchor="ma")
        else:
            d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def cap_line(d, y, txt, font, fill, w=W, x=None):
    """Desenha a linha com o topo das maiúsculas em y (independe da métrica da fonte). Retorna a base."""
    caph = -d.textbbox((0, 0), "H", font=font, anchor="ls")[1]
    base = y + caph
    if x is None:
        d.text((w / 2, base), txt, font=font, fill=fill, anchor="ms")
    else:
        d.text((x, base), txt, font=font, fill=fill, anchor="ls")
    return base


def fit(d, txt, make_font, maxw, start, minimum=20):
    size = start
    while size > minimum and d.textlength(txt, font=make_font(size)) > maxw:
        size -= 2
    return make_font(size)


# =====================================================================
#  ESTILO A · teaser off-white (401502) · Fase 1
# =====================================================================
def a_canvas(w=W, h=H):
    im = Image.new("RGB", (w, h), D_OFF)
    mask = decade_symbol_mask(int(w * 1.16), blur=4)
    im.paste(Image.new("RGB", mask.size, D_WM), ((w - mask.width) // 2, int(h * 0.53 - mask.height / 2)), mask)
    return im, ImageDraw.Draw(im)


def a_symbol(im, cy, w=W, h=78):
    m = decade_symbol_mask(h)
    im.paste(Image.new("RGB", m.size, BLACK), ((w - m.width) // 2, int(cy - m.height / 2)), m)


def a_title(d, y, parts, size, w=W, maxw=None):
    maxw = maxw or w - 220
    while max(d.textlength(t, font=serif(size, it)) for t, it in parts) > maxw:
        size -= 4
    for t, it in parts:
        d.text((w / 2, y), t, font=serif(size, it), fill=BLACK, anchor="ma")
        y += int(size * 1.1)
    return y + int(size * 0.15)


def a_body(d, y, txt, w=W, size=40):
    return text_block(d, txt, y, serif(size), D_CINZA_MEDIO, w - 260, int(size * 1.35), w=w)


def a_footer(im, d, w=W, cy=H - 118):
    dh, lh, gap = 54, 74, 46
    total = logo_w(DEC_BLACK, dh) + gap * 2 + 2 + logo_w(LIGA_BLACK, lh)
    x = (w - total) / 2
    x += paste_h(im, DEC_BLACK, x, cy - dh / 2, dh) + gap
    d.line([(x, cy - 44), (x, cy + 44)], fill=D_CINZA_MEDIO, width=2)
    paste_h(im, LIGA_BLACK, x + gap + 2, cy - lh / 2 - 4, lh)


# =====================================================================
#  ESTILO B · cartazes pretos (401499–401501) · Fases 2 a 4
# =====================================================================
MB = 100  # margem lateral (≈10% da largura, como nos cartazes)


def b_canvas(w=W, h=H):
    im = Image.new("RGB", (w, h), BLACK)
    return im, ImageDraw.Draw(im)


def b_head(d, y, lines_, w=W, gap=0.3):
    """Linhas que ocupam a largura toda, como 'DECADE' / 'NA UNICAMP' nos cartazes.
    lines_: (texto, cor, peso JetBrains, corpo máximo). Retorna o y abaixo da última linha."""
    for txt, color, weight, maxsize in lines_:
        f = fit(d, txt, lambda s: jb(s, weight), w - 2 * MB, maxsize)
        if any(c in "ÁÉÍÓÚÂÊÔÃÕÀ" for c in txt):
            y += int(f.size * 0.2)  # espaço para o acento das maiúsculas
        base = cap_line(d, y, txt, f, color, w=w)
        y = base + int(f.size * gap)
    return y


def b_sub(d, y, txt, w=W, size=40, color=BRANCO):
    """Subtítulo em mono caixa alta ('A FINTECH QUE CAPTOU US$ 85 MILHÕES')."""
    f = fit(d, txt, lambda s: jb(s, "Regular"), w - 2 * MB, size)
    return cap_line(d, y, txt, f, color, w=w) + int(f.size * 0.3)


def b_dash(d, y, color=AMARELO, w=W, dash=22, gapd=12, thick=5):
    x = MB
    while x < w - MB:
        d.line([(x, y), (min(x + dash, w - MB), y)], fill=color, width=thick)
        x += dash + gapd
    return y


def b_faixa(d, y, txt=FAIXA, w=W, size=78, color=BRANCO):
    """'26.10 - 9h - Auditório' em Anton, entre tracejados."""
    f = fit(d, txt, anton, w - 2 * MB, size)
    return cap_line(d, y, txt, f, color, w=w)


def b_body(d, y, txt, w=W, size=30, color=BRANCO, x=None):
    f = jb(size, "Regular")
    maxw = w - 2 * MB
    return text_block(d, txt, y, f, color, maxw, int(size * 1.45), w=w, x=x)


def b_cta(d, y, txt="INSCREVA-SE!", w=W, size=64):
    return cap_line(d, y, txt, anton(size), AMARELO, w=w)


def b_counter(d, txt, y, w=W):
    spaced(d, txt, y, jb(22, "Bold"), CINZA, sp=6, w=w)


def b_footer(im, w=W, y=H - 175, lh=110, dh=66):
    """Rodapé dos cartazes: Liga à esquerda, Decade à direita."""
    paste_h(im, LIGA_DARK, MB, y, lh)
    paste_h(im, DEC_OFF, w - MB - logo_w(DEC_OFF, dh), y + (lh - dh) / 2 - 4, dh)


def b_rows(d, y, items, w=W, tsize=36, bsize=26):
    """Lista numerada: número em Anton amarelo, item em Montserrat Bold, detalhe em mono cinza,
    separados por tracejado cinza (como o 401501)."""
    for n, t, b in items:
        b_dash(d, y, CINZA, w=w, thick=3)
        cap_line(d, y + 34, n, anton(46), AMARELO, x=MB, w=w)
        y2 = cap_line(d, y + 36, t, mont(tsize), BRANCO, x=MB + 100, w=w) + 16
        if b:
            y2 = text_block(d, b, y2, jb(bsize), CINZA_TXT, w - 2 * MB - 100, int(bsize * 1.45), w=w, x=MB + 100) - int(bsize * 0.4)
        y = y2 + 30
    b_dash(d, y, CINZA, w=w, thick=3)
    return y


# =====================================================================
#  POST 1 · 29/09 · Fase 1 (aquecimento) · carrossel · estilo A (teaser 401502)
# =====================================================================
im, d = a_canvas()
spaced(d, f"UNICAMP · {MES_UP}", 92, smono(26), D_GRAFITE, sp=13)
a_symbol(im, 390)
y = a_title(d, 490, [("algo está sendo", False), ("construído.", True)], 124)
y = a_body(d, y + 50, "as inscrições abrem em breve. entre na nossa comunidade no WhatsApp e saiba antes de todo mundo.")
spaced(d, f"{DATA} · UNICAMP", y + 40, smono(34), BLACK, sp=10)
spaced(d, "01 / 03 · ARRASTE →", H - 238, smono(22), D_CINZA_MEDIO, sp=8)
a_footer(im, d)
save(im, "post1_slide1_teaser.png")

im, d = a_canvas()
spaced(d, f"UNICAMP · {MES_UP}", 92, smono(26), D_GRAFITE, sp=13)
y = a_title(d, 200, [("você já sabe", False), ("quem vem?", True)], 118)
for n, t in (("01", "Uma fintech de inteligência patrimonial."), ("02", "Fundada por ex-Nubank e Hyperplane."),
             ("03", "Fez a maior rodada seed da América Latina.")):
    d.line([(110, y), (W - 110, y)], fill=D_HAIR, width=2)
    d.text((130, y + 34), n, font=smono(26), fill=D_GRAFITE)
    d.text((220, y + 24), t, font=serif(38), fill=BLACK)
    y += 100
d.line([(110, y), (W - 110, y)], fill=D_HAIR, width=2)
d.text((W / 2, y + 70), "comente seu palpite ↓", font=serif(44, True), fill=BLACK, anchor="ma")
spaced(d, "02 / 03 · ARRASTE →", H - 238, smono(22), D_CINZA_MEDIO, sp=8)
a_footer(im, d)
save(im, "post1_slide2_pistas.png")

im = Image.new("RGB", (W, H), D_OFF)
im.paste(campus_photo((W, 620)), (0, 0))
d = ImageDraw.Draw(im)
spaced(d, "REVELADO", 700, smono(24), D_GRAFITE, sp=13)
y = a_title(d, 760, [("a Decade chega", False), ("à Unicamp.", True)], 96)
spaced(d, "COM A LIGA EMPREENDEDORA · " + MES_UP, y + 45, smono(22), D_CINZA_MEDIO, sp=8)
spaced(d, "03 / 03 · ATIVE AS NOTIFICAÇÕES", H - 238, smono(22), D_CINZA_MEDIO, sp=8)
a_footer(im, d)
save(im, "post1_slide3_revelacao.png")

# Story da fase 1, mesmo estilo (faixa livre para o sticker de enquete)
im, d = a_canvas(SW, SH)
spaced(d, f"UNICAMP · {MES_UP}", 260, smono(28), D_GRAFITE, sp=13, w=SW)
a_symbol(im, 480, w=SW, h=90)
y = a_title(d, 600, [("algo grande", False), ("está chegando.", True)], 124, w=SW)
y = a_body(d, y + 40, "uma fintech vem aí.", w=SW, size=44)
y = a_body(d, y, "quem você acha que é?", w=SW, size=44)
spaced(d, "VOTE NA ENQUETE ↓", y + 60, smono(24), D_CINZA_MEDIO, sp=8, w=SW)
a_footer(im, d, w=SW, cy=SH - 330)
save(im, "post1_story.png")


# =====================================================================
#  FASES 2 A 4 · estilo B (cartazes 401499–401501)
# =====================================================================
HEAD = [("DECADE", AMARELO, "ExtraBold", 330), ("NA UNICAMP", BRANCO, "Regular", 150)]
HEAD_SM = [("DECADE", AMARELO, "ExtraBold", 230), ("NA UNICAMP", BRANCO, "Regular", 110)]
SUB = "A FINTECH QUE CAPTOU US$ 85 MILHÕES"
TEXTO_EVENTO = ("Conheça a 1ª Inteligência Patrimonial do mercado. Descubra como a Decade une expertise "
                "humana à IA e participe de um networking exclusivo com os fundadores (ex-Nubank e Hyperplane).")


def b_story_base(rotulo):
    im, d = b_canvas(SW, SH)
    spaced(d, rotulo, 250, jb(28, "Bold"), AMARELO, sp=8, w=SW)
    return im, d


def b_story_footer(im):
    b_footer(im, w=SW, y=SH - 400)


# ---------- POST 2 · 04/10 · Lançamento: conheça a Decade (carrossel) ----------
im, d = b_canvas()
y = b_head(d, 250, HEAD)
y = b_sub(d, y + 20, SUB)
b_dash(d, y + 40)
y = b_body(d, y + 90, "A startup que fez a maior rodada seed da América Latina vem à Unicamp com a Liga Empreendedora.", size=32)
b_dash(d, y + 40)
b_counter(d, "01 / 03 · ARRASTE →", H - 262)
b_footer(im)
save(im, "post2_slide1_conheca.png")

im, d = b_canvas()
y = b_head(d, 110, [("O QUE É A", BRANCO, "Regular", 120), ("DECADE?", AMARELO, "ExtraBold", 230)])
b_rows(d, y + 30, [("01", "Inteligência patrimonial", "Expertise humana + IA para as maiores decisões financeiras da sua vida."),
                   ("02", "Time de peso", "Fundadores vindos do Nubank e da Hyperplane."),
                   ("03", "US$ 85 milhões", "A maior rodada seed da história da América Latina.")])
b_counter(d, "02 / 03 · ARRASTE →", H - 262)
b_footer(im)
save(im, "post2_slide2_o_que_e.png")

im, d = b_canvas()
y = b_head(d, 190, [("E ELA VEM", BRANCO, "Regular", 150), ("ATÉ VOCÊ", AMARELO, "ExtraBold", 260)])
b_dash(d, y + 30)
y = b_body(d, y + 80, "O encontro Decade × Liga Empreendedora acontece na Unicamp. No próximo post: data, local e inscrições.", size=32)
b_dash(d, y + 40)
b_cta(d, y + 100, "ATIVE AS NOTIFICAÇÕES", size=60)
b_counter(d, "03 / 03", H - 262)
b_footer(im)
save(im, "post2_slide3_ate_voce.png")

im, d = b_story_base("CONHEÇA A DECADE")
y = b_head(d, 420, HEAD, w=SW)
y = b_sub(d, y + 20, SUB, w=SW)
b_dash(d, y + 40, w=SW)
y = b_body(d, y + 90, "Fundada por ex-Nubank e Hyperplane. O que você quer perguntar aos fundadores?", w=SW, size=34)
b_counter(d, "MANDE SUA PERGUNTA NA CAIXINHA ↓", y + 50, w=SW)
b_story_footer(im)
save(im, "post2_story.png")

# ---------- POST 3 · 08/10 · Lançamento: o evento (estático, recriação do 401500) ----------
im, d = b_canvas()
y = b_head(d, 110, HEAD_SM)
y = b_sub(d, y + 10, SUB, size=34)
b_dash(d, y + 20)
y = b_faixa(d, y + 56, size=70)
b_dash(d, y + 34)
y = b_body(d, y + 70, TEXTO_EVENTO, size=24, x=MB)
y = b_cta(d, y + 26, size=54)
qs = 230
im.paste(QR.resize((qs, qs), Image.LANCZOS), ((W - qs) // 2, y + 26))
b_footer(im, y=H - 150, lh=96, dh=56)
save(im, "post3_evento.png")

im, d = b_story_base("INSCRIÇÕES ABERTAS")
y = b_head(d, 400, HEAD, w=SW)
y = b_sub(d, y + 20, SUB, w=SW)
b_dash(d, y + 40, w=SW)
y = b_faixa(d, y + 80, w=SW)
b_dash(d, y + 44, w=SW)
y = b_cta(d, y + 110, w=SW, size=90)
b_counter(d, "TOQUE NO LINK PARA SE INSCREVER ↓", y + 60, w=SW)
b_story_footer(im)
save(im, "post3_story.png")

# ---------- POST 4 · 12/10 · Motivação: por que ir (carrossel) ----------
im, d = b_canvas()
y = b_faixa(d, 110, size=70)
b_dash(d, y + 40, CINZA)
y = b_head(d, y + 110, [("4 MOTIVOS", AMARELO, "ExtraBold", 230), ("PARA NÃO FICAR", BRANCO, "Regular", 120),
                        ("DE FORA", BRANCO, "Regular", 120)])
b_dash(d, y + 30, CINZA)
y = b_body(d, y + 90, "Bastidores de uma fintech, IA aplicada a finanças, networking com os fundadores e novos caminhos de carreira.", size=32)
b_cta(d, y + 60, "ARRASTE E CONFIRA →", size=60)
b_counter(d, "01 / 02", H - 262)
b_footer(im)
save(im, "post4_slide1_motivos.png")

im, d = b_canvas()
y = b_head(d, 110, [("POR QUE", BRANCO, "Regular", 120), ("IR?", AMARELO, "ExtraBold", 200)])
b_rows(d, y + 20, [("01", "Bastidores de uma fintech", "Como se constrói uma startup financeira do zero."),
                   ("02", "IA aplicada a finanças", "Como a tecnologia está mudando o jeito de investir."),
                   ("03", "Conexões", "Networking com os fundadores e com a rede da Liga."),
                   ("04", "Carreira", "Caminhos em finanças, tecnologia e empreendedorismo.")], tsize=34, bsize=24)
b_counter(d, "02 / 02 · INSCRIÇÕES: LINK NA BIO", H - 262)
b_footer(im)
save(im, "post4_slide2_por_que.png")

im, d = b_story_base("POR QUE IR?")
y = b_head(d, 420, [("BASTIDORES", BRANCO, "Regular", 170), ("DE UMA", BRANCO, "Regular", 170),
                    ("FINTECH", AMARELO, "ExtraBold", 300)], w=SW)
b_dash(d, y + 30, w=SW)
y = b_body(d, y + 80, "Veja como se constrói uma startup financeira e converse com quem está fazendo isso.", w=SW, size=34)
b_counter(d, "VOCÊ JÁ INVESTE? RESPONDA NA ENQUETE ↓", y + 50, w=SW)
b_story_footer(im)
save(im, "post4_story.png")

# ---------- POST 5 · 16/10 · Motivação: para quem é + autoridade (carrossel) ----------
im, d = b_canvas()
y = b_head(d, 110, [("É PARA", BRANCO, "Regular", 120), ("VOCÊ QUE...", AMARELO, "ExtraBold", 200)])
b_rows(d, y + 20, [("01", "estuda Economia ou Administração", "e quer ver o mercado financeiro por dentro."),
                   ("02", "estuda Computação ou Engenharia", "e quer entender IA aplicada a produtos reais."),
                   ("03", "pensa em empreender", "e quer aprender com quem fundou uma startup."),
                   ("04", "é de qualquer curso", "e tem curiosidade por finanças e tecnologia.")], tsize=32, bsize=24)
b_counter(d, "01 / 02 · ARRASTE →", H - 262)
b_footer(im)
save(im, "post5_slide1_para_quem.png")

im, d = b_canvas()
y = b_head(d, 190, [("FUNDADA POR", BRANCO, "Regular", 150), ("EX-NUBANK", AMARELO, "ExtraBold", 260)])
y = b_sub(d, y + 20, "E EX-HYPERPLANE")
b_dash(d, y + 40)
y = b_body(d, y + 90, "Os fundadores da Decade chegam à Unicamp com a Liga Empreendedora para um networking exclusivo.", size=32)
b_dash(d, y + 40)
b_cta(d, y + 100)
b_counter(d, "02 / 02 · LINK NA BIO", H - 262)
b_footer(im)
save(im, "post5_slide2_ex_nubank.png")

im, d = b_story_base("PARA QUEM É?")
y = b_head(d, 420, [("QUAL O", BRANCO, "Regular", 200), ("SEU CURSO?", AMARELO, "ExtraBold", 300)], w=SW)
b_dash(d, y + 30, w=SW)
y = b_body(d, y + 80, "O evento é aberto a estudantes de todos os cursos da Unicamp.", w=SW, size=34)
b_counter(d, "RESPONDA NA CAIXINHA ↓", y + 50, w=SW)
b_story_footer(im)
save(im, "post5_story.png")


# ---------- POSTS 6 A 8 · Lembretes (estáticos) + stories ----------
def lembrete(w, h, dias, top, big, footer_y, name, dica=None, sub=None):
    im, d = b_canvas(w, h)
    y = b_faixa(d, top, w=w, size=70)
    b_dash(d, y + 40, CINZA, w=w)
    if dias > 1:
        y = b_head(d, y + 100, [("FALTAM", BRANCO, "Regular", big // 3), (str(dias), AMARELO, "ExtraBold", big),
                                ("DIAS", BRANCO, "Regular", big // 3)], w=w, gap=0.2)
    else:
        y = b_head(d, y + 100, [("É", BRANCO, "Regular", int(big * 0.55)),
                                ("AMANHÃ" if dias == 1 else "HOJE", AMARELO, "ExtraBold", big)], w=w, gap=0.2)
    b_dash(d, y + 20, CINZA, w=w)
    if sub:
        y = b_body(d, y + 70, sub, w=w, size=32)
    if dica:
        b_counter(d, dica, y + 60, w=w)
    else:
        b_cta(d, y + 70, w=w, size=60)
    b_footer(im, w=w, y=footer_y)
    save(im, name)


for n, data_post in ((6, dt.date(2026, 10, 20)), (7, dt.date(2026, 10, 23)), (8, dt.date(2026, 10, 25))):
    dias = (EV - data_post).days
    tag = f"faltam_{dias}_dias" if dias > 1 else "e_amanha"
    lembrete(W, H, dias, 110, 420 if dias > 1 else 250, H - 175, f"post{n}_{tag}.png",
             sub=None if dias > 1 else f"{DATA_EXT[0].upper() + DATA_EXT[1:]}, na Unicamp. Últimas vagas no link da bio.")
    lembrete(SW, SH, dias, 250, 560 if dias > 1 else 300, SH - 400, f"post{n}_story.png",
             dica="ADICIONE O LEMBRETE NO STICKER ↓")

# EXTRA · 26/10 · story "É HOJE" (sugestão do Octávio)
lembrete(SW, SH, 0, 250, 320, SH - 400, "extra_story_e_hoje.png",
         sub=f"Te esperamos no {EVENTO['local']} da Unicamp. Nos vemos lá!", dica="MARQUE QUEM VAI COM VOCÊ ↓")

print("total:", len(os.listdir(OUT)), "peças")
