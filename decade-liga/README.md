# Instagram · Decade × Liga Empreendedora

8 posts + 8 stories (e 1 story extra) do cronograma, redesenhados com base nas peças do Octávio (`arquivos/401499.png`, `401500.png`, `401501.png`, `401502.jpg`) e no `Manual_Marca_Evento_Decade.pdf`.

Para gerar de novo: `python3 decade-liga/gerar_posts.py` (a partir da raiz do repositório; precisa do Pillow).

## Identidade visual

| Fase | Referência do Octávio | Como ficou |
|------|-----------------------|------------|
| 1 · Aquecimento (Post 1 + story) | `401502.jpg`: "algo está sendo construído" | Off-white `#F5F1EC`, símbolo da Decade em marca d'água, título em serif (Playfair Display) com a palavra-chave em itálico, rótulos e datas em mono espaçado, logos Decade \| Liga no rodapé |
| 2 a 4 (posts 2 a 8 + stories) | `401499–401501`: cartazes "DECADE NA UNICAMP" | Fundo preto, "DECADE" em amarelo `#F5C518` e mono pesado (JetBrains Mono), "NA UNICAMP" em branco e mono leve, tracejados amarelos ou cinza `#6E757C`, faixa "26.10 - 9h - Auditório" em Anton, texto em mono, "INSCREVA-SE!" em Anton amarelo, logo da Liga à esquerda e da Decade à direita |

Cores e fontes seguem o manual: Anton, Montserrat e JetBrains Mono da Liga; serif editorial e mono da Decade. Todas as fontes estão em `fonts/` (licença OFL).

> ⚠️ O manual diz que o amarelo da Liga não entra na arte oficial do evento, mas os cartazes 401499–401501 do Octávio usam "DECADE" em amarelo. Segui os cartazes, como pedido. Vale confirmar com a Decade na aprovação.

## Cronograma

| Data | Fase | Post (feed) | Story | Interação no story |
|------|------|-------------|-------|--------------------|
| 29/09 | 1 · Aquecimento | `post1_slide1..3` (carrossel: teaser, pistas, revelação) | `post1_story` | Enquete "Quem você acha que vem?" |
| 04/10 | 2 · Lançamento | `post2_slide1..3` (carrossel: conheça a Decade) | `post2_story` | Caixinha de perguntas para os fundadores |
| 08/10 | 2 · Lançamento | `post3_evento` (recriação do cartaz 401500, com QR) | `post3_story` | Sticker de link para inscrição |
| 12/10 | 3 · Motivação | `post4_slide1..2` (carrossel: 4 motivos) | `post4_story` | Enquete "Você já investe?" |
| 16/10 | 3 · Motivação | `post5_slide1..2` (carrossel: para quem é + ex-Nubank) | `post5_story` | Caixinha "Qual o seu curso?" |
| 20/10 | 4 · Lembretes | `post6_faltam_6_dias` | `post6_story` | Sticker de contagem regressiva |
| 23/10 | 4 · Lembretes | `post7_faltam_3_dias` | `post7_story` | Sticker de contagem regressiva |
| 25/10 | 4 · Lembretes | `post8_e_amanha` | `post8_story` | Sticker de contagem regressiva |
| 26/10 | Extra | – | `extra_story_e_hoje` | Marcar amigos |

Nos stories, o texto cinza com "↓" marca a faixa vazia onde entra o sticker do Instagram.

## Legendas sugeridas

**Post 1 · 29/09**
> algo está sendo construído. 🏗️
>
> uma fintech que fez história no mercado vem para a Unicamp em outubro, junto com a Liga.
>
> arraste até o fim ➡️ e conta nos comentários: você já sabia quem era?
>
> 🔔 ative as notificações. link da comunidade do WhatsApp na bio.

**Post 2 · 04/10**
> o segredo foi revelado: a Decade vem à Unicamp. 🟡
>
> a fintech que captou US$ 85 milhões, a maior rodada seed da América Latina, une expertise humana e IA na primeira inteligência patrimonial do mercado.
>
> arraste para conhecer ➡️ no próximo post: data, local e inscrições.

**Post 3 · 08/10**
> inscrições abertas! 🚀
>
> Decade na Unicamp: palestra e networking exclusivo com os fundadores (ex-Nubank e Hyperplane).
>
> 📅 26.10 · 9h
> 📍 Auditório · Unicamp
> 🎟️ vagas limitadas, inscrição pelo QR ou pelo link na bio.

**Post 4 · 12/10**
> 4 motivos para não ficar de fora: bastidores de uma fintech, IA aplicada a finanças, networking com os fundadores e novos caminhos de carreira.
>
> qual deles te convenceu? conta aqui embaixo 👇 inscrições no link da bio.

**Post 5 · 16/10**
> economia, computação, engenharia, administração… ou qualquer outro curso: esse evento é pra você.
>
> a Decade foi fundada por ex-Nubank e ex-Hyperplane. marca aquele amigo que precisa ir com você 👀

**Posts 6 e 7 · 20/10 e 23/10**
> faltam 6 dias! ⏳ (no post 7: faltam 3 dias!)
>
> Decade na Unicamp · 26.10 · 9h · Auditório. ainda não se inscreveu? link na bio.

**Post 8 · 25/10**
> é amanhã! 🟡
>
> segunda, 9h, no Auditório da Unicamp. últimas vagas no link da bio.

## Antes de publicar
- **Horário:** os cartazes dizem **9h** e o teaser 401502 diz **17h30**. Usei 9h. Para trocar, altere `EVENTO` no topo de `gerar_posts.py` e rode o script de novo (data, contagem regressiva e faixas são recalculadas).
- **Local:** os cartazes dizem só "Auditório". Informe qual e atualize `EVENTO["local"]`.
- **QR do post 3:** foi recortado do cartaz 401500. Troque pelo QR real da inscrição em `qr_code()`.
- **Aprovação da Decade:** o manual pede validação de cada peça com a Decade, que é rígida com a marca.
- **Logos:** a da Decade foi recortada do post do Gabriel; a da Liga vem do site oficial. Se houver arquivos oficiais em PNG/SVG, substitua para ganhar nitidez.
