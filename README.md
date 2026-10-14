# Z-Move, site

Site de https://zmove.click: uma só página em inglês (`/`) e em português (`/pt/`), mais a
política de privacidade e os termos. O AWS Amplify publica o repositório tal como está a cada
push para `main` (sem passo de build no Amplify).

## Estrutura

```
src/content.json       todo o texto, EN e PT lado a lado (as duas línguas ficam sempre iguais)
src/build.py           gera as páginas a partir do content.json (só biblioteca padrão do Python)
src/legal/*.html       texto da privacidade e dos termos (só em inglês)
index.html, pt/        gerados: não editar à mão
privacy.html, terms.html, sitemap.xml, site.webmanifest   gerados
blog/, case-studies/, compare/   gerados: redireccionam as páginas do site antigo para a secção nova
assets/site.css        estilos (cores e tipos da plataforma; tema claro/escuro)
assets/site.js         tema, menu, passos, seletor de rotas, comparador de marca, formulário
assets/theme-init.js   aplica o tema escolhido antes do primeiro desenho
assets/fonts/          IBM Plex Sans e Mono (licença OFL em OFL.txt), servidas localmente
assets/shots/          capturas da plataforma: <ecrã>.<en|pt>.<light|dark>.webp (2880 px) e .1440.webp
assets/brand/          logótipo (SVG e PNG, fundo claro e escuro), marca e ícones
favicon.svg, favicon.ico, apple-touch-icon.png, og-image.png, og-image-pt.png
customHttp.yml         cabeçalhos HTTP do Amplify (CSP, HSTS, etc.)
```

## Alterar o site

1. Editar `src/content.json` (texto) ou `src/build.py` (estrutura), `assets/site.css`, `assets/site.js`.
2. `python3 src/build.py`
3. Ver localmente: `python3 -m http.server 8089` e abrir http://localhost:8089/ e /pt/.
4. Commit e push para `main`: o Amplify publica em cerca de um minuto.

## Capturas

As capturas vêm da plataforma actual num ambiente de demonstração com dados neutros (VMs, regiões e
empresa inventadas; os tempos são de execuções reais). "Acme Cloud" é uma marca fictícia, usada para
mostrar o white-label. Cada ecrã existe em EN e PT, claro e escuro, em 2880 px e 1440 px; a página
escolhe a variante pela língua, pelo tema e pelo ecrã do visitante.

## Marca (logótipo e favicon)

O Z desenhado como uma rota: o anel é a estação de origem, a diagonal é a mudança e o ponto cheio é o
destino, no verde da plataforma (#0A7A63). A palavra é IBM Plex Sans SemiBold convertida em contornos,
com o hífen em verde (#0A7A63) em fundo claro e em menta (#3DC2A3) em fundo escuro. A plataforma
(https://copy.zmove.click) usa a mesma marca e o mesmo favicon desde 14/10/2026.

| Ficheiro | Uso |
|---|---|
| `assets/brand/zmove-logo.svg` / `.png` | logótipo para fundo claro |
| `assets/brand/zmove-logo-on-dark.svg` / `.png` | logótipo para fundo escuro |
| `assets/brand/zmove-mark.svg` | só o símbolo |
| `assets/brand/icon-192.png`, `icon-512.png` | ícones do `site.webmanifest` |
| `favicon.svg`, `favicon.ico` | favicon (traço mais grosso, legível a 16 px) |
| `apple-touch-icon.png` | ícone para iPhone e iPad (quadrado inteiro; o iOS arredonda os cantos) |
| `og-image.png`, `og-image-pt.png` | imagem de partilha (LinkedIn, WhatsApp) em EN e PT, 1200 x 630 |

No cabeçalho e no rodapé o símbolo está desenhado no próprio HTML (`mark()` em `src/build.py`) e a
palavra é texto em IBM Plex, para ficar nítida e sem pedidos extra.

## Verificar antes do push

Ver as duas línguas em desktop e telemóvel, nos temas claro e escuro, e confirmar que: não há scroll
horizontal; as capturas correspondem à língua e ao tema; os passos, o seletor de rotas, o comparador de
marca, o tema e o menu funcionam; a consola do browser não mostra erros nem violações de CSP; as
páginas antigas (`/blog/`, `/case-studies/...`, `/compare/...`) redireccionam. Não submeter o
formulário em testes: vai para o Formspree real.

## Formulário e estatísticas

O pedido de demonstração vai para o Formspree (`https://formspree.io/f/mwvykwlq`), com campo-armadilha
`_gotcha` contra spam. Sem JavaScript, o formulário é enviado da forma normal. As estatísticas são do
Plausible (sem cookies).

## Segurança

CSP sem `unsafe-inline` (nem scripts nem estilos inline), fontes e imagens só do próprio domínio,
`frame-ancestors 'none'`, HSTS com preload. A mesma CSP vai em `<meta>` em cada página, como reserva.
