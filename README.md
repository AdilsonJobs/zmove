# Z-Move — Landing Page

> Move anything. Across any cloud.

Site de divulgação do **Z-Move**, a plataforma agentless de migração multi-cloud.

---

## Estrutura

```
zmove/
├── index.html       # Landing page completa (single-file, sem dependências)
└── assets/
    └── founder.jpg  # Foto de perfil do fundador
```

---

## Deploy

Ficheiro único — pode ser publicado em qualquer hosting estático:

- **Vercel** — `vercel deploy`
- **Netlify** — drag & drop da pasta
- **GitHub Pages** — push para branch `gh-pages`

### Headers HTTP obrigatórios no servidor

Configurar no `nginx.conf`, `netlify.toml`, `vercel.json` ou equivalente:

```nginx
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
Referrer-Policy: strict-origin-when-cross-origin
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; frame-ancestors 'none'; upgrade-insecure-requests;
```

---

## Pendências

### 🔴 Segurança — Backend do formulário de contacto

A implementar quando o backend estiver activo:

| # | O que aplicar | Porquê |
|---|---------------|--------|
| 1 | **Rate limiting** | Máx 5 submissions por IP por hora — bloqueia spam em massa |
| 2 | **CSRF token** | Token único por sessão no form — previne ataques cross-site request forgery |
| 3 | **Validação server-side** | Client-side é UX, server-side é segurança real |
| 4 | **reCAPTCHA v3 invisível** | Score-based, sem friction para o utilizador |
| 5 | **Sanitização de inputs** | Strip HTML antes de guardar ou enviar por email |

> Referência: análise de segurança realizada em 2026-04-17. O formulário actual faz `mailto:` como fallback — seguro para fase de lançamento.

### 🟡 Produto — A implementar

| # | Feature | Prioridade |
|---|---------|------------|
| 1 | **Vídeo demo 90s** | Alta — substituir placeholder na secção Live Demo |
| 2 | **Backend do formulário** | Alta — substituir mailto por API real (ex: Resend, Formspree) |
| 3 | **og-image.png** | Média — criar imagem 1200×630 para partilha em redes sociais |
| 4 | **favicon** | Média — adicionar `<link rel="icon">` |
| 5 | **Google Analytics / Plausible** | Média — medir tráfego e conversões |
| 6 | **Blog técnico** | Alta (SEO) — primeiro artigo: "AWS → Zadara in 15 minutes" |

---

## Segurança implementada (landing page)

| # | Medida | Onde |
|---|--------|------|
| 1 | Content-Security-Policy | `<meta http-equiv>` + headers servidor |
| 2 | Referrer-Policy `strict-origin-when-cross-origin` | meta tag |
| 3 | Permissions-Policy (câmara, mic, geo, payment desativados) | meta tag |
| 4 | `rel="noopener noreferrer"` em todos os links externos | HTML |
| 5 | Email obfuscado (reconstituído via JS em runtime) | JS |
| 6 | Honeypot anti-bot no formulário | HTML oculto |
| 7 | Validação client-side (nome, email regex) | JS |
| 8 | `frame-ancestors 'none'` — anti-clickjacking | CSP |
| 9 | `upgrade-insecure-requests` | CSP |
