# Deploy e Hospedagem

## Onde o site roda

O projeto é hospedado no **Firebase Hosting** (projeto `guia-lancamentos-2026`, definido em `.firebaserc`), com **Firestore** como banco de dados. O domínio customizado `guiadelancamentos.com.br` é apontado para o Hosting (o arquivo `CNAME` na raiz é resquício/uso auxiliar de GitHub Pages e não afeta o Firebase Hosting).

## Configuração (`firebase.json`)

- `"hosting.public": "."` — a **raiz inteira do repositório** é publicada como site estático (exceto os arquivos listados em `hosting.ignore`: os próprios arquivos de config do Firebase, `.gitignore` e arquivos ocultos).
- `"rewrites"` — qualquer rota (`"source": "**"`) cai em `/index.htm`, já que é uma SPA de arquivo único sem roteador de servidor.
- `"headers"` — por padrão todo arquivo é servido com `Cache-Control: no-cache, no-store, must-revalidate` (útil durante o desenvolvimento ativo dos dados/JS embutidos em `index.htm`); imagens (`png|jpg|jpeg|gif|webp|svg`) recebem `Cache-Control: public, max-age=604800` (7 dias).
- `"firestore"` aponta para `firestore.rules` e `firestore.indexes.json`.

## Deploy automático (`.github/workflows/deploy.yml`)

Todo push nas branches `main` ou `master` dispara:

1. Checkout do repositório
2. `npm install -g firebase-tools`
3. `firebase deploy --token "$FIREBASE_TOKEN"` — publica Hosting **e** Firestore (regras + índices)

O `FIREBASE_TOKEN` é um secret do repositório GitHub (`Settings → Secrets and variables → Actions`). Sem ele configurado, o workflow falha na etapa de deploy.

## Deploy manual (local)

```bash
npm install -g firebase-tools
firebase login
firebase deploy   # publica hosting + firestore do projeto configurado em .firebaserc
```

## Coisas a saber antes de mexer na estrutura de pastas

- Como `hosting.public` é `"."`, **qualquer arquivo novo na raiz do repo (inclusive este `docs/`) fica publicamente acessível pela URL do site**, a menos que seja explicitamente adicionado a `hosting.ignore`. Não é um problema de segurança por si só (nada aqui é secreto), mas é bom ter em mente antes de colocar algo sensível no repositório.
- `index.htm` precisa continuar acessível em `/index.htm` na raiz publicada, por causa do rewrite acima.
- Caminhos de imagem/ícone referenciados em `index.htm` são relativos ao próprio `index.htm`; ao mover assets, atualize os `href`/`src` correspondentes (ver [`ESTRUTURA_DE_ARQUIVOS.md`](./ESTRUTURA_DE_ARQUIVOS.md)).
