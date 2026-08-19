# Arquitetura

## Visão geral

O **Guia de Lançamentos 2026** é uma SPA (single-page application) sem etapa de build: todo o HTML, CSS e JavaScript da aplicação vive em um único arquivo, `index.htm`. Não há `npm install`, bundler ou transpilação — o navegador executa o arquivo diretamente.

## Stack

Todas as dependências são carregadas via CDN, direto no `<head>` ou por `import` ES module dentro do `<script type="module">`:

| Dependência | Uso |
|---|---|
| [Tailwind CSS](https://cdn.tailwindcss.com) (CDN) | Estilização utilitária |
| [Lucide Icons](https://unpkg.com/lucide) | Ícones SVG |
| [Google Charts](https://www.gstatic.com/charts/loader.js) (`geochart`) | Mapa do Brasil por UF na home |
| [Firebase JS SDK 11.6.1](https://www.gstatic.com/firebasejs/) (`firebase-app`, `firebase-auth`, `firebase-firestore`) | Autenticação e banco de dados |
| Fonte "Garet" via `fonts.cdnfonts.com` | Tipografia de destaque |

## Renderização

Não há framework de componentes (React, Vue, etc.). A UI é manipulada diretamente via DOM (`document.getElementById`, `classList`, `innerHTML`) a partir de um objeto de estado global `state` (declarado por volta da linha 777 de `index.htm`). Funções são expostas em `window.*` (ex.: `window.switchTab`, `window.renderUI`, `window.toggleTheme`) para serem chamadas a partir de atributos `onclick` inline no HTML.

## Views

A aplicação tem três telas, alternadas por `window.switchTab(tab)` mostrando/escondendo divs (`display: none` via `.hidden`):

- **`#view-home`** — dashboard público: hero, gráfico de frequência de lançamentos (timeline), mapa por UF, listagem/grid filtrável de lançamentos.
- **`#view-submit`** — formulário público para sugerir um novo lançamento ou solicitar alteração em um já existente.
- **`#view-admin`** — painel de moderação (visível só para e-mails admin autenticados): aprovar/editar/excluir lançamentos pendentes.

## Dados: seed estático + Firestore

Os lançamentos exibidos vêm de duas fontes combinadas em tempo de execução:

1. **Seed estático (`RAW_CSV_DATA`)** — um bloco de texto CSV gigante, literalmente embutido em `index.htm` (a partir da linha ~848), com a base inicial de artistas/lançamentos. É parseado por `parseCSVLine`/o `.map()` logo abaixo (linha ~1251) e vira `state.releases` com `id` no formato `seed_<index>` e `status: 'approved'`.
2. **Firestore (`submissions2026_v4`)** — coleção onde ficam as submissões da comunidade (novos lançamentos ou pedidos de alteração) e onde admins podem também inserir/editar registros. Um listener `onSnapshot` (linha ~2007) mescla os documentos do Firestore com os itens do seed, dando prioridade ao Firestore quando o mesmo `id` existir nas duas fontes.

Ou seja: **editar dados definitivos não requer alterar o CSV** — o fluxo normal é o usuário público submeter pelo formulário (`#view-submit`), cair em `submissions2026_v4` com `status: 'pending'`, e um admin aprovar pelo painel (`#view-admin`). Editar o `RAW_CSV_DATA` só é necessário para alterar a base inicial "hardcoded".

Veja [`DADOS.md`](./DADOS.md) para o detalhamento do schema e das regras de segurança.

## Autenticação

- Usuários comuns não precisam logar para ver lançamentos aprovados nem para submeter sugestões.
- Login de admin é por e-mail/senha (`signInWithEmailAndPassword`), acessível por um "easter egg": 4 cliques rápidos no rodapé (`window.secretAdminLogin`, linha ~2152) abrem o modal de login.
- Um usuário é considerado admin se o e-mail autenticado estiver na lista `window.ADMIN_EMAILS` (definida em `firebase-config.js`) — a mesma lista é replicada em `firestore.rules` para a autorização real acontecer no servidor.

## Hospedagem

Ver [`DEPLOY.md`](./DEPLOY.md).
