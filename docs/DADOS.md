# Modelo de Dados

## Coleção Firestore: `submissions2026_v4`

Cada documento representa um lançamento musical (disco, EP ou single). Campos usados pela aplicação (ver `index.htm`, parsing do CSV e formulário de submissão):

| Campo | Tipo | Descrição |
|---|---|---|
| `artist` | string | Nome do artista |
| `uf` | string | Sigla da UF (calculada a partir da localização, ex.: "SP", ou `"Sem UF"`) |
| `type` | string | `"Disco"` ou `"EP"` (ou outro valor livre) |
| `date` | string | Data/previsão de lançamento em texto livre (ex.: `"24/02"`, `"Segundo semestre"`, `"Não Revelada"`) |
| `title` | string | Título do lançamento (ou `"Não Revelado"`) |
| `label` | string | Selo/gravadora ou `"Independente"` |
| `fonte` | string | Fonte da informação (pessoa/veículo que divulgou) |
| `link` | string | Link do release (Spotify, etc.), opcional |
| `month` / `semester` | string | Derivados de `date` por `parseDateInfo`, usados nos gráficos/filtros |
| `status` | string | `"pending"` \| `"approved"` |
| `timestamp` | number/Timestamp | Data de criação, exigido pelas regras do Firestore |
| `requestType` | string | Presente apenas em pedidos de alteração: `"change"` |
| `originalId` | string | Presente apenas em pedidos de alteração: id do lançamento original |
| `motivo` | string | Presente apenas em pedidos de alteração: justificativa da mudança |

Documentos vindos do seed estático (`RAW_CSV_DATA` em `index.htm`) usam o mesmo formato de objeto em memória, mas nunca são persistidos no Firestore — existem só no `state.releases` do navegador, com `id: "seed_<índice>"`.

## Fluxo de status

```
Usuário anônimo           Admin
     │                       │
     │  submete (pending)    │
     ├──────────────────────►│
     │                       │  aprova → status = "approved"
     │                       │  ou exclui (delete)
     │                       │
     │◄──── passa a aparecer para todo mundo (onSnapshot com status == "approved")
```

Pedidos de **alteração** (`requestType == "change"`) também nascem como `pending` e seguem o mesmo fluxo; a diferença é que carregam `originalId` apontando para o documento que o admin deve revisar/atualizar manualmente.

## Regras de segurança (`firestore.rules`)

- **Leitura**: qualquer pessoa pode ler documentos com `status == "approved"`. Documentos `pending` só são legíveis por admins.
- **Criação**: admins podem criar com qualquer status; usuários anônimos só podem criar com `status == "pending"` e, dependendo do tipo (novo lançamento vs. pedido de alteração), precisam preencher um conjunto mínimo de campos (`hasAll([...])`).
- **Atualização/exclusão**: restritas a admins.
- **Quem é admin**: `request.auth.token.email` precisa estar na lista fixa dentro da própria regra (duplicada de `firebase-config.js` → `window.ADMIN_EMAILS`, veja a nota de manutenção abaixo).

> **Atenção ao manter:** a lista de e-mails admin existe em **dois lugares** — `firebase-config.js` (`window.ADMIN_EMAILS`, usada só para mostrar/esconder botões na UI) e `firestore.rules` (`isAdmin()`, a autorização que de fato vale). Adicionar um admin exige editar as duas.

## Índices (`firestore.indexes.json`)

Dois índices compostos sobre `submissions2026_v4`, para as queries usadas nos filtros/gráficos:
- `status` + `artist` (ordenação alfabética dentro do conjunto aprovado/pendente)
- `status` + `month` (agrupamento por mês na timeline)
