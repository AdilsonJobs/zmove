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

## Capturas e logótipo

As capturas vêm da plataforma actual num ambiente de demonstração com dados neutros (VMs, regiões e
empresa inventadas; os tempos são de execuções reais). "Acme Cloud" é uma marca fictícia, usada para
mostrar o white-label. O logótipo é o Z desenhado como uma rota: estação de origem, a mudança e o destino,
no verde da plataforma (#0A7A63); a palavra é IBM Plex Sans SemiBold convertida em contornos.

## Formulário e estatísticas

O pedido de demonstração vai para o Formspree (`https://formspree.io/f/mwvykwlq`), com campo-armadilha
`_gotcha` contra spam. Sem JavaScript, o formulário é enviado da forma normal. As estatísticas são do
Plausible (sem cookies).

## Segurança

CSP sem `unsafe-inline` (nem scripts nem estilos inline), fontes e imagens só do próprio domínio,
`frame-ancestors 'none'`, HSTS com preload. A mesma CSP vai em `<meta>` em cada página, como reserva.
