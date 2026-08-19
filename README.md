# Guia de Lançamentos 2026

Site que reúne discos, EPs e singles mais esperados da música brasileira em 2026 — timeline, mapa por estado, listagem filtrável e um fluxo de submissão/moderação para a comunidade sugerir e corrigir lançamentos.

🔗 [guiadelancamentos.com.br](https://guiadelancamentos.com.br)

## Como o projeto funciona

É uma SPA de arquivo único: todo o HTML, CSS e JavaScript da aplicação está em [`index.htm`](./index.htm), sem etapa de build. As dependências (Tailwind, Lucide, Google Charts, Firebase) são carregadas via CDN.

Para rodar localmente, basta servir a raiz do repositório com qualquer servidor estático, por exemplo:

```bash
python3 -m http.server 8000
# depois abra http://localhost:8000/index.htm
```

> Como não há build, editar `index.htm` e recarregar o navegador já é o ciclo de desenvolvimento.

## Documentação

- [`docs/ARQUITETURA.md`](./docs/ARQUITETURA.md) — stack, views, estado, fluxo de renderização
- [`docs/DADOS.md`](./docs/DADOS.md) — schema dos lançamentos, fluxo pending/approved, regras do Firestore
- [`docs/DEPLOY.md`](./docs/DEPLOY.md) — Firebase Hosting/Firestore, CI de deploy, domínio customizado
- [`docs/ESTRUTURA_DE_ARQUIVOS.md`](./docs/ESTRUTURA_DE_ARQUIVOS.md) — mapa de diretórios do repositório

## Estrutura resumida

```
index.htm            aplicação (HTML + CSS + JS)
firebase-config.js    config pública do Firebase + lista de admins
firebase.json / .firebaserc / firestore.*   config de Hosting e Firestore
assets/               ícones, imagens e vídeos do site
docs/                 esta documentação
.github/workflows/    deploy automático para Firebase
```

Veja o detalhamento completo em [`docs/ESTRUTURA_DE_ARQUIVOS.md`](./docs/ESTRUTURA_DE_ARQUIVOS.md).

## Créditos

Inspirado na curadoria de Alexandre Giglio e Rafael Chioccarello. Desenvolvido por [@ganwalk](https://ganwalk.github.io/2026/).
