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



# =====================================================================
#  FASES 2 A 4  (cronograma do Gabriel)
# =====================================================================
import datetime as dt

# >>> CONFIRMAR COM A DECADE E A LIGA antes de publicar <<<
EVENTO = {
    "data": dt.date(2026, 10, 26),  # assumida: fim do período de divulgação (26/10)
    "local": "Unicamp · Campinas",
}
EV = EVENTO["data"]
MESES = ["", "janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro",
         "outubro", "novembro", "dezembro"]
SEMANA = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]
DATA = f"{EV.day:02d}/{EV.month:02d}"
DATA_EXT = f"{SEMANA[EV.weekday()]}, {EV.day} de {MESES[EV.month]}"


def save(im, name):
    im.save(os.path.join(OUT, name))


def wrap(d, x, y, txt, font, fill, maxw, lh):
    line = ""
    for w in txt.split():
        t = (line + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            line = t
        else:
            d.text((x, y), line, font=font, fill=fill)
            y += lh
            line = w
    if line:
        d.text((x, y), line, font=font, fill=fill)
        y += lh
    return y


def title(d, x, y, parts, size, maxw=W - 160):
    """Título em grotesca pesada; reduz o tamanho até todas as linhas caberem."""
    while max(sum(d.textlength(t, font=grotesk(size)) for t, _ in ln) for ln in parts) > maxw:
        size -= 4
    return lines(d, x, y, parts, size, size)


def rows(d, y, items, tsize=36, bsize=28):
    """Lista numerada com linhas finas, como as pistas do Post #1."""
    for n, t, b in items:
        d.line([(80, y), (W - 80, y)], fill=LINE, width=2)
        d.text((80, y + 30), n, font=mono(28, True), fill=YELLOW)
        d.text((170, y + 24), t, font=grotesk(tsize), fill=WHITE)
        y2 = y + 24 + tsize + 12
        if b:
            y2 = wrap(d, 170, y2, b, grotesk(bsize, "Regular"), GRAY, W - 250, bsize + 10)
        y = y2 + 24
    d.line([(80, y), (W - 80, y)], fill=LINE, width=2)
    return y


def info_rows(d, y, items, vx=330):
    """Tabela chave/valor (O QUÊ, QUANDO, ONDE...)."""
    for k, v in items:
        d.line([(80, y), (W - 80, y)], fill=LINE, width=2)
        d.text((80, y + 34), k, font=mono(26, True), fill=YELLOW)
        y = wrap(d, vx, y + 28, v, grotesk(36, "Medium"), WHITE, W - 80 - vx, 46) + 26
    d.line([(80, y), (W - 80, y)], fill=LINE, width=2)
    return y


def button(d, x, y, txt):
    f = mono(30, True)
    d.rectangle([x, y, x + d.textlength(txt, font=f) + 60, y + 80], fill=YELLOW)
    d.text((x + 30, y + 40), txt, font=f, fill=BLACK, anchor="lm")


def story_footer(im, d):
    y = SH - 400
    d.line([(80, y), (SW - 80, y)], fill=LINE, width=2)
    x = 80 + paste_h(im, LIGA, 80, y + 55, 90) + 30
    d.text((x, y + 100), "×", font=grotesk(52, "Regular"), fill=GRAY, anchor="lm")
    paste_h(im, DEC_W, x + 60, y + 73, 54)


def story(name, rotulo, titulo, sub, dica, bloco):
    """Story padrão: bloco amarelo, título, texto e faixa livre para o sticker (y ≈ 1330–1500)."""
    im, d = base(SW, SH)
    yellow_block(d, SW, bloco[0], bloco[1], h=300, bw=320)
    label(d, (80, 380), rotulo, size=24)
    y = title(d, 80, 470, titulo, 140)
    y = wrap(d, 80, y + 40, sub, grotesk(42, "Medium"), WHITE, SW - 160, 56)
    label(d, (80, max(y + 50, 1270)), dica, color=GRAY, size=22)
    story_footer(im, d)
    save(im, name)


# ---------- POST 2 · 04/10 · Lançamento: conheça a Decade (carrossel) ----------
im, d = base(W, H)
yellow_block(d, W, "UNICAMP", "REVELADO", bw=300)
label(d, (80, 110), "O SEGREDO FOI REVELADO")
y = title(d, 80, 330, [[("CONHEÇA", WHITE)], [("A ", WHITE), ("DECADE", YELLOW)]], 150)
wrap(d, 80, y + 60, "A startup financeira que vem à Unicamp com a Liga Empreendedora.",
     grotesk(40, "Medium"), WHITE, W - 160, 54)
footer(im, d, W, H)
save(im, "post2_slide1_conheca.png")

im, d = base(W, H)
label(d, (80, 110), "QUEM É A DECADE · 02 / 03")
y = title(d, 80, 200, [[("O QUE É A", WHITE)], [("DECADE", YELLOW), ("?", WHITE)]], 128)
rows(d, y + 50, [("01", "Gestão de patrimônio com IA", "Tecnologia para cuidar dos investimentos de forma completa e personalizada."),
                 ("02", "Time de peso", "Fundada por ex-executivos do Nubank."),
                 ("03", "Mais acesso", "Leva um serviço antes restrito a grandes fortunas para mais pessoas.")])
footer(im, d, W, H)
save(im, "post2_slide2_o_que_e.png")

im, d = base(W, H)
label(d, (80, 110), "03 / 03")
y = title(d, 80, 230, [[("E ELA VEM", WHITE)], [("ATÉ VOCÊ", YELLOW)]], 140)
y = wrap(d, 80, y + 50, "O encontro Decade × Liga Empreendedora acontece na Unicamp. No próximo post: data, local e inscrições.",
         grotesk(40, "Medium"), WHITE, W - 160, 54)
x = 80 + paste_h(im, DEC_W, 80, y + 90, 90) + 40
d.text((x, y + 135), "×", font=grotesk(80, "Light"), fill=YELLOW, anchor="lm")
paste_h(im, LIGA, x + 80, y + 60, 150)
button(d, 80, y + 280, "ative as notificações")
footer(im, d, W, H, left_txt=None)
save(im, "post2_slide3_ate_voce.png")

story("post2_story.png", "CONHEÇA A DECADE", [[("STARTUP", WHITE)], [("FINANCEIRA", WHITE)], [("COM IA", YELLOW)]],
      "Fundada por ex-executivos do Nubank, a Decade vem à Unicamp com a Liga Empreendedora.",
      "MANDE SUA PERGUNTA PARA A DECADE ↓", ("UNICAMP", "REVELADO"))

# ---------- POST 3 · 08/10 · Lançamento: o evento + inscrições (estático) ----------
im, d = base(W, H)
yellow_block(d, W, "INSCRIÇÕES", "ABERTAS", bw=330)
label(d, (80, 110), "DECADE × LIGA EMPREENDEDORA")
y = title(d, 80, 290, [[("DECADE", WHITE)], [("NA ", WHITE), ("UNICAMP", YELLOW)]], 130, maxw=W - 160)
y = info_rows(d, y + 40, [("O QUÊ", "Encontro com o time da Decade sobre finanças, IA e empreendedorismo."),
                          ("QUANDO", DATA_EXT[0].upper() + DATA_EXT[1:]),
                          ("ONDE", EVENTO["local"]),
                          ("PARA QUEM", "Estudantes de todos os cursos.")])
button(d, 80, y + 40, "inscreva-se: link na bio")
footer(im, d, W, H, left_txt=None)
save(im, "post3_evento.png")

story("post3_story.png", "INSCRIÇÕES ABERTAS", [[("GARANTA", WHITE)], [("SUA VAGA", YELLOW)]],
      f"Decade × Liga Empreendedora · {DATA_EXT} · {EVENTO['local']}. Aberto a todos os cursos.",
      "TOQUE NO LINK PARA SE INSCREVER ↓", ("INSCRIÇÕES", "ABERTAS"))

# ---------- POST 4 · 12/10 · Motivação: por que ir (carrossel) ----------
im, d = base(W, H)
yellow_block(d, W, "UNICAMP", DATA, bw=300)
label(d, (80, 110), "POR QUE IR?")
title(d, 80, 330, [[("4 MOTIVOS", WHITE)], [("PARA NÃO", WHITE)], [("FICAR", WHITE)], [("DE FORA", YELLOW)]], 140)
footer(im, d, W, H)
save(im, "post4_slide1_motivos.png")

im, d = base(W, H)
label(d, (80, 110), "POR QUE IR? · 02 / 02")
y = title(d, 80, 200, [[("POR QUE ", WHITE), ("IR", YELLOW), ("?", WHITE)]], 110)
rows(d, y + 40, [("01", "Bastidores de uma fintech", "Como se constrói uma startup financeira do zero."),
                 ("02", "IA aplicada a finanças", "Como a tecnologia está mudando o jeito de investir."),
                 ("03", "Conexões", "Converse com o time da Decade e com a rede da Liga."),
                 ("04", "Carreira", "Caminhos em finanças, tecnologia e empreendedorismo.")])
footer(im, d, W, H, left_txt="inscrições: link na bio")
save(im, "post4_slide2_por_que.png")

story("post4_story.png", "POR QUE IR?", [[("BASTIDORES", WHITE)], [("DE UMA", WHITE)], [("FINTECH", YELLOW)]],
      "Veja como se constrói uma startup financeira e converse com quem está fazendo isso.",
      "VOCÊ JÁ INVESTE? RESPONDA NA ENQUETE ↓", ("UNICAMP", DATA))

# ---------- POST 5 · 16/10 · Motivação: para quem é + autoridade (carrossel) ----------
im, d = base(W, H)
label(d, (80, 110), "PARA QUEM É? · 01 / 02")
y = title(d, 80, 200, [[("É PRA", WHITE)], [("VOCÊ QUE", YELLOW), ("...", WHITE)]], 128)
rows(d, y + 40, [("01", "estuda Economia ou Administração", "e quer ver o mercado financeiro por dentro."),
                 ("02", "estuda Computação ou Engenharia", "e quer entender IA aplicada a produtos reais."),
                 ("03", "pensa em empreender", "e quer aprender com quem fundou uma startup."),
                 ("04", "é de qualquer curso", "e tem curiosidade por finanças e tecnologia.")])
footer(im, d, W, H)
save(im, "post5_slide1_para_quem.png")

im, d = base(W, H)
yellow_block(d, W, "UNICAMP", DATA, bw=300)
label(d, (80, 110), "QUEM ESTÁ POR TRÁS")
y = title(d, 80, 330, [[("FUNDADA", WHITE)], [("POR", WHITE)], [("EX-NUBANK", YELLOW)]], 150)
y = wrap(d, 80, y + 50, "A Decade foi criada por ex-executivos do Nubank e chega à Unicamp com a Liga Empreendedora.",
         grotesk(40, "Medium"), WHITE, W - 160, 54)
button(d, 80, y + 50, "inscrições: link na bio")
footer(im, d, W, H, left_txt=None)
save(im, "post5_slide2_ex_nubank.png")

story("post5_story.png", "PARA QUEM É?", [[("QUAL O", WHITE)], [("SEU CURSO", YELLOW), ("?", WHITE)]],
      "O evento é aberto a estudantes de todos os cursos da Unicamp.",
      "RESPONDA NA CAIXINHA ↓", ("UNICAMP", DATA))


# ---------- POSTS 6 A 8 · Lembretes (estáticos) ----------
def countdown(d, top, dias, width, big=540, after_gap=40):
    """'FALTAM / N / DIAS' ou 'É AMANHÃ' / 'É HOJE'. Retorna o y final."""
    if dias > 1:
        d.text((80, top), "FALTAM", font=grotesk(110), fill=WHITE)
        base_y = top + 150 + int(big * 0.74)
        d.text((62, base_y), str(dias), font=grotesk(big), fill=YELLOW, anchor="ls")
        d.text((80, base_y + 30), "DIAS", font=grotesk(140), fill=WHITE)
        return base_y + 30 + 140 + after_gap
    palavra = "AMANHÃ" if dias == 1 else "HOJE"
    return title(d, 80, top, [[("É", WHITE)], [(palavra, YELLOW)]], 240, maxw=width - 160) + after_gap


for n, data_post in ((6, dt.date(2026, 10, 20)), (7, dt.date(2026, 10, 23)), (8, dt.date(2026, 10, 25))):
    dias = (EV - data_post).days
    tag = f"faltam_{dias}_dias" if dias > 1 else "e_amanha"
    sub = ("para o encontro com a Decade na Unicamp." if dias > 1
           else f"{DATA_EXT[0].upper() + DATA_EXT[1:]}, {EVENTO['local']}. Ainda dá tempo de se inscrever.")
    im, d = base(W, H)
    yellow_block(d, W, "DECADE × LIGA", DATA, bw=300)
    label(d, (80, 110), "LEMBRETE")
    y = countdown(d, 290, dias, W, big=500)
    wrap(d, 80, y, sub, grotesk(38, "Medium"), WHITE, W - 160, 50)
    footer(im, d, W, H, left_txt="inscrições: link na bio")
    save(im, f"post{n}_{tag}.png")

    im, d = base(SW, SH)
    yellow_block(d, SW, "DECADE × LIGA", DATA, h=300, bw=320)
    label(d, (80, 380), "LEMBRETE", size=24)
    y = countdown(d, 470, dias, SW, big=480)
    label(d, (80, max(y + 20, 1270)), "ADICIONE O LEMBRETE NO STICKER ↓", color=GRAY, size=22)
    story_footer(im, d)
    save(im, f"post{n}_story.png")

# ---------- EXTRA · 26/10 · Story "É HOJE" (sugestão do Octavio) ----------
im, d = base(SW, SH)
yellow_block(d, SW, "DECADE × LIGA", DATA, h=300, bw=320)
label(d, (80, 380), "É HOJE", size=24)
y = countdown(d, 470, 0, SW)
wrap(d, 80, y, f"Te esperamos na {EVENTO['local'].split(' ·')[0]}. Nos vemos lá!", grotesk(42, "Medium"), WHITE, SW - 160, 56)
label(d, (80, 1270), "MARQUE QUEM VAI COM VOCÊ ↓", color=GRAY, size=22)
story_footer(im, d)
save(im, "extra_story_e_hoje.png")

print("total:", len(os.listdir(OUT)), "peças")
