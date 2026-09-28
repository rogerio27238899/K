"""Gera o currículo de Matteo Lucato em PDF.

Texto: versão nova ("Currículo - Matteo Lucato.pdf").
Formatação: versão anterior ("CV - Matteo Lucato.pdf", Word) — cabeçalho centralizado,
títulos de seção com filete, marcadores "●", local/datas alinhados à direita,
cargo e período em itálico e fonte Times (Liberation Serif, métrica idêntica à Times New Roman).

Uso: python gerar_curriculo.py   (requer: pip install playwright && python -m playwright install chromium)
"""
from pathlib import Path

BASE = Path(__file__).resolve().parent
FONTS = BASE / "fonts"
SAIDA = BASE / "Curriculo - Matteo Lucato (atualizado).pdf"

NOME = "Matteo Lucato"
CONTATO = ["São Paulo, SP | (11) 94591-1942",
           "m246226@dac.unicamp.br | linkedin.com/in/matteo-lucato"]

# Cada entrada: (organização, local, cargo/curso, período, [bullets])  — bullets aceitam HTML (<b>, <i>)
SECOES = [
    ("FORMAÇÃO ACADÊMICA", [
        ("UNICAMP", "Campinas, SP", "Bacharelado em Economia (Instituto de Economia)",
         "Fevereiro 2023 – Dezembro 2027",
         ["<b>Disciplinas Relevantes:</b> Finanças Corporativas, Contabilidade e Análise de Balanços, "
          "Econometria, Estatística, Derivativos e Gestão de Portfólio, Matemática Financeira, "
          "Mercado de Capitais e Métodos Computacionais."]),
        ("Agostiniano Mendel / Calvert Academy", "São Paulo, SP",
         "Ensino Médio com currículo internacional norte-americano (AP Economics e AP Statistics), "
         "com ênfase em Economia, Tecnologia, Finanças e Matemática", "", []),
    ]),
    ("EXPERIÊNCIA PROFISSIONAL", [
        ("V4 Company", "Campinas, SP", "Analista Financeiro Júnior", "Janeiro 2026 – Setembro 2026", [
            "Conduzi as análises mensais de DRE, a modelagem financeira e as projeções de fluxo de caixa da "
            "empresa, acompanhando receitas, custos e margens de cada período e consolidando os resultados em "
            "relatórios gerenciais que a diretoria utilizava como base para decidir a alocação de um orçamento "
            "anual superior a R$ 5M.",
            "Administrei o fluxo de caixa, a conciliação bancária e as rotinas de contas a pagar e a receber, "
            "com volume superior a 400 transações mensais, e implantei um controle diário de vencimentos que "
            "antecipou a cobrança dos recebíveis e reduziu a inadimplência da carteira.",
            "Reestruturei as rotinas de fechamento mensal e a documentação dos controles internos, reduzindo a "
            "exposição a riscos operacionais e deixando cada lançamento rastreável até o comprovante de origem, "
            "formando a base documental que sustentou as auditorias e os processos de <i>Due Diligence</i> da empresa.",
        ]),
        ("Nunes&amp;Lucato", "São Paulo, SP", "Gestor de Projetos", "Fevereiro 2023 – Dezembro 2025", [
            "Conduzi a prospecção e a negociação das parcerias de coleta com a NK Store e a Track&amp;Field, "
            "garantindo a destinação integral do resíduo têxtil recebido e assegurando fluxo contínuo de "
            "matéria-prima ao longo de 2023 e 2024, período em que a receita e o volume do negócio cresceram "
            "de forma sustentada.",
            "Gerenciei projetos de <i>upcycling</i> para a Midea, a Carrier e a Santista S.A., administrando um "
            "orçamento de R$ 150 mil, coordenando a produção e a entrega de mais de 2.500 itens às marcas como "
            "parte de suas iniciativas de sustentabilidade.",
            "Supervisionei o projeto Bom Retiro Recicla, acompanhando o volume de resíduo têxtil recebido e "
            "realocando mais de 40 toneladas por mês para a reciclagem, o que evitou que esse material fosse "
            "encaminhado a descarte inadequado.",
        ]),
    ]),
    ("ATIVIDADES EXTRACURRICULARES E LIDERANÇA", [
        ("Clube de Consultoria da Unicamp", "Campinas, SP", "Diretor de Gestão de Pessoas",
         "Agosto 2025 – Setembro 2026", [
            "Atuei como instrutor do programa Prep4Consulting, ministrando aulas de Finanças e de resolução de "
            "<i>cases</i> para mais de 100 alunos e capacitando os participantes na estruturação e na resolução "
            "dos problemas exigidos nos processos seletivos de consultoria.",
            "Conduzi as sessões de preparação do programa <i>Getting the Job</i>, rodando simulações de entrevista "
            "com devolutiva de desempenho e revisões estratégicas de currículo com os candidatos que disputavam "
            "vagas nas principais consultorias do mercado.",
            "Colaborei na divulgação do XRAY 2025, censo da Unicamp voltado a mapear o interesse dos alunos pelo "
            "mercado de consultoria, levantamento que alcançou o recorde de 626 respostas em apenas duas semanas.",
        ]),
        ("IME Jr", "São Paulo, SP", "Analista Financeiro, Departamento Jurídico-Financeiro",
         "Agosto 2024 – Dezembro 2025", [
            "Estruturei modelos preditivos em Python e rotinas de extração de dados em SQL para projetos nos "
            "setores de Saúde e Transporte, tratando e analisando bases com mais de 1,2 milhão de registros.",
            "Conduzi a análise SWOT da empresa júnior, identificando a captação de recursos como principal ponto "
            "forte, e analisei as despesas operacionais em Excel para apontar as linhas de custo com maior "
            "potencial de redução, o que gerou economia mensal recorrente.",
            "Padronizei o arquivo financeiro e jurídico do departamento, reunindo fluxo de caixa, orçamentos, "
            "contratos e notas fiscais em uma estrutura única de pastas, com convenção de nomes que tornou cada "
            "documento localizável por período e por contraparte.",
        ]),
    ]),
]

HABILIDADES = [
    ("Certificações", "CPA-20 (ANBIMA), candidato ao Nível I do CFA, <i>Financial &amp; Valuation Modeling</i> "
     "(WSP), Excel Avançado (Fundação Bradesco), Derivativos e Gestão de Portfólio (GMF) e Análise de "
     "Demonstrações Financeiras (GMF)."),
    ("Habilidades Técnicas", "Pacote Office (avançado), Excel e VBA, Python, SQL e Power BI."),
    ("Competições", "Semifinalista do Challenge Ágora."),
    ("Línguas", "Português (nativo), Inglês (avançado) e Espanhol (intermediário)."),
    ("Interesses", "Tênis, xadrez e leitura de livros de não-ficção."),
]

CSS = """
@font-face{font-family:TNR;src:url('%(f)s/LiberationSerif-Regular.ttf')}
@font-face{font-family:TNR;font-weight:bold;src:url('%(f)s/LiberationSerif-Bold.ttf')}
@font-face{font-family:TNR;font-style:italic;src:url('%(f)s/LiberationSerif-Italic.ttf')}
@font-face{font-family:TNR;font-weight:bold;font-style:italic;src:url('%(f)s/LiberationSerif-BoldItalic.ttf')}
@page{size:A4;margin:9mm 11mm 7mm 11mm}
body{font-family:TNR,'Times New Roman',serif;font-size:10pt;line-height:1.15;color:#000;margin:0}
header{text-align:center;margin-bottom:6pt}
header .nome{font-weight:bold;font-size:11.5pt}
h2{font-size:10.9pt;font-weight:bold;margin:6pt 0 3.5pt;padding-bottom:1.2pt;border-bottom:1pt solid #000}
.e{margin-bottom:3pt}
.l{display:flex;justify-content:space-between;gap:12pt}
.org,.loc{font-weight:bold}
.cargo,.per{font-style:italic}
.per{white-space:nowrap}
ul{margin:2pt 0 0;padding-left:30pt;list-style:none}
li{position:relative;text-align:left;margin-bottom:0.5pt}
li::before{content:'●';position:absolute;left:-15pt;font-size:7.5pt;top:1.3pt}
p.h{margin:0 0 1pt;text-align:justify}
"""


def html():
    out = [f"<header><div class=nome>{NOME}</div>" + "".join(f"<div>{c}</div>" for c in CONTATO) + "</header>"]
    for titulo, entradas in SECOES:
        out.append(f"<h2>{titulo}</h2>")
        for org, loc, cargo, per, bullets in entradas:
            out.append(f"<div class=e><div class=l><span class=org>{org}</span><span class=loc>{loc}</span></div>"
                       f"<div class=l><span class=cargo>{cargo}</span><span class=per>{per}</span></div>")
            if bullets:
                out.append("<ul>" + "".join(f"<li>{b}</li>" for b in bullets) + "</ul>")
            out.append("</div>")
    out.append("<h2>HABILIDADES, CERTIFICAÇÕES E INTERESSES</h2>")
    out += [f"<p class=h><b>{k}:</b> {v}</p>" for k, v in HABILIDADES]
    return ("<!DOCTYPE html><html lang=pt-BR><head><meta charset=utf-8><style>"
            + CSS % {"f": FONTS.as_uri()} + "</style></head><body>" + "".join(out) + "</body></html>")


def gerar():
    from playwright.sync_api import sync_playwright
    tmp = BASE / "_cv.html"
    tmp.write_text(html(), encoding="utf-8")
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.goto(tmp.as_uri())
        pg.evaluate("document.fonts.ready")
        pg.pdf(path=str(SAIDA), format="A4", prefer_css_page_size=True)
        b.close()
    tmp.unlink()
    return SAIDA


if __name__ == "__main__":
    print("Gerado:", gerar())
