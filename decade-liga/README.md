# Instagram · Decade × Liga Empreendedora

Todas as peças do cronograma do Gabriel (8 posts + 8 stories, mais 1 story extra), com a identidade da Liga Empreendedora.

## Cronograma

| Data | Fase | Post (feed) | Story | Interação no story |
|------|------|-------------|-------|--------------------|
| 29/09 | 1 · Aquecimento | `post1_slide1..3` (carrossel) | `post1_story` | Enquete "Quem você acha que vem?" |
| 04/10 | 2 · Lançamento | `post2_slide1..3` (carrossel: conheça a Decade) | `post2_story` | Caixinha "Mande sua pergunta para a Decade" |
| 08/10 | 2 · Lançamento | `post3_evento` (o quê, quando, onde, para quem) | `post3_story` | Sticker de link para inscrição |
| 12/10 | 3 · Motivação | `post4_slide1..2` (carrossel: 4 motivos) | `post4_story` | Enquete "Você já investe?" |
| 16/10 | 3 · Motivação | `post5_slide1..2` (carrossel: para quem é + ex-Nubank) | `post5_story` | Caixinha "Qual o seu curso?" |
| 20/10 | 4 · Lembretes | `post6_faltam_6_dias` | `post6_story` | Sticker de contagem regressiva |
| 23/10 | 4 · Lembretes | `post7_faltam_3_dias` | `post7_story` | Sticker de contagem regressiva |
| 25/10 | 4 · Lembretes | `post8_e_amanha` | `post8_story` | Sticker de contagem regressiva |
| 26/10 | Extra | – | `extra_story_e_hoje` | Marcar amigos (sugestão do Octavio: "é hoje") |

> ⚠️ **Data e local do evento são provisórios.** Usei **26/10 (segunda-feira), Unicamp · Campinas**, porque o período de divulgação termina em 26/10. Se mudar, altere `EVENTO` no topo da seção "FASES 2 A 4" de `gerar_posts.py` e rode o script de novo: data, dia da semana e contagem regressiva são recalculados.

## Post #1 (detalhes)

| Arquivo | O que é |
|---------|---------|
| `posts/post1_slide1_teaser.png` | Carrossel, slide 1: teaser "Algo grande está chegando" |
| `posts/post1_slide2_pistas.png` | Carrossel, slide 2: 3 pistas + "comente seu palpite" |
| `posts/post1_slide3_revelacao.png` | Carrossel, slide 3: revelação Decade × Liga |
| `posts/post1_story.png` | Story com espaço para o sticker de enquete |
| `PROMPT.md` | Prompt usado para criar as peças |
| `gerar_posts.py` | Script que gera as imagens |

## O que mudou em relação aos posts do Gabriel

| Posts do Gabriel | Nova versão |
|------------------|-------------|
| Só a identidade da Decade (creme/grafite, serifa) | Identidade da Liga: preto, amarelo forte e branco, grotesca pesada e rótulos em mono |
| Parceria não aparece: só a logo da Decade | Logo da Liga × logo da Decade em todas as peças |
| Imagem única, sem motivo para interagir | Carrossel "arraste para revelar", no formato que o Octavio usou no evento da XP |
| Nenhum gancho de engajamento | Pistas + "comente seu palpite" no feed, e enquete no story |
| Foto do campus em cores naturais | Mesma foto, em duotone preto e amarelo |

## Legendas sugeridas

**Post 1 · 29/09**

> algo grande está chegando à Unicamp. 👀
>
> uma startup financeira. fundada por quem ajudou a construir o Nubank. e agora ela vem até aqui, junto com a Liga.
>
> arraste até o fim ➡️ e conta pra gente nos comentários: você já sabia quem era?
>
> 🔔 ative as notificações. em breve, todos os detalhes.
>
> #LigaEmpreendedora #Decade #Unicamp #Empreendedorismo #Fintech

**Post 2 · 04/10**
> o segredo foi revelado: a Decade vem à Unicamp. 🟡
>
> startup financeira que usa inteligência artificial para cuidar de investimentos, fundada por ex-executivos do Nubank. e agora ela chega até aqui, em parceria com a Liga Empreendedora.
>
> arraste para conhecer ➡️ e fique de olho: no próximo post, data, local e inscrições.

**Post 3 · 08/10**
> inscrições abertas! 🚀
>
> Decade × Liga Empreendedora na Unicamp: um encontro sobre finanças, IA e empreendedorismo.
>
> 📅 segunda, 26 de outubro
> 📍 Unicamp · Campinas
> 🎓 aberto a estudantes de todos os cursos
>
> garanta sua vaga pelo link na bio.

**Post 4 · 12/10**
> 4 motivos para não ficar de fora: bastidores de uma fintech, IA aplicada a finanças, conexões com o time da Decade e com a rede da Liga, e novos caminhos de carreira.
>
> qual deles te convenceu? conta aqui embaixo 👇 inscrições no link da bio.

**Post 5 · 16/10**
> economia, computação, engenharia, administração… ou qualquer outro curso: esse evento é pra você.
>
> a Decade foi criada por ex-executivos do Nubank e vem à Unicamp com a Liga Empreendedora. marca aquele amigo que precisa ir com você 👀

**Posts 6 e 7 · 20/10 e 23/10**
> faltam 6 dias! ⏳ (no post 7: faltam 3 dias!)
>
> Decade × Liga Empreendedora, segunda, 26/10, na Unicamp. ainda não se inscreveu? link na bio.

**Post 8 · 25/10**
> é amanhã! 🟡
>
> nos vemos na Unicamp para o encontro Decade × Liga Empreendedora. últimas vagas no link da bio.

## Como publicar o story
1. Suba `post1_story.png` no Instagram.
2. Adicione o sticker **Enquete** na faixa vazia, logo abaixo de "VOTE NA ENQUETE ↓".
3. Pergunta: **"Quem você acha que vem?"**. Opções: **"Já sei quem é 😎"** / **"Não faço ideia 👀"**.
4. No dia seguinte, reposte o carrossel no story, mostrando a revelação.

## Stories com interação
- **Enquete / caixinha / link / contagem regressiva:** cada story tem uma faixa vazia logo abaixo do texto cinza com "↓". É ali que entra o sticker do Instagram indicado na tabela do cronograma.
- **Contagem regressiva (posts 6 a 8):** crie o sticker uma vez, com a data do evento. Quem tocar em "lembrar" recebe aviso na hora do evento, o que ajuda a reduzir faltas.

## Antes de publicar
- **Data, local e formato do evento:** confirme com a Decade e a Liga. O post 3 descreve o evento como "encontro com o time da Decade sobre finanças, IA e empreendedorismo"; ajuste se for palestra, workshop etc.
- **Aprovação da Decade:** o planejamento exige que o marketing da Decade aprove os posts. Mande as 4 peças e a legenda para eles.
- **Pistas do slide 2:** "fundada por ex-executivos do Nubank" e "usa IA para cuidar de investimentos" vêm de matérias sobre a Decade (Estadão, Yahoo Finanças). Peça à Decade para confirmar se pode divulgar essas informações.
- **Logo da Decade:** foi recortada do post do Gabriel. Se a Decade tiver o arquivo oficial em PNG/SVG, substitua em `gerar_posts.py` para ter mais nitidez.
- **Logo da Liga:** vem do site oficial da Liga (ligaempreendedora.com).
- **Fontes:** Space Grotesk e Space Mono, ambas gratuitas (licença OFL).
