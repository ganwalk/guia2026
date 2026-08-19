# Estrutura de Arquivos

Mapa de diretórios do repositório e o que cada parte contém.

```
guia2026/
├── index.htm                  # Aplicação inteira (HTML + CSS + JS), servida na raiz do site
├── firebase-config.js         # Config pública do Firebase + lista de e-mails admin
├── firebase.json              # Config do Firebase Hosting/Firestore
├── firestore.rules            # Regras de segurança do Firestore
├── firestore.indexes.json     # Índices compostos do Firestore
├── .firebaserc                # Projeto Firebase padrão (guia-lancamentos-2026)
├── CNAME                      # Domínio customizado (guiadelancamentos.com.br)
│
├── assets/
│   ├── icons/                 # Favicons e ícones de app (referenciados no <head>)
│   ├── images/                # Imagens usadas pelo site (og:image, logos parceiros)
│   │   └── originals/         # Versões originais/alta-resolução, não referenciadas no HTML
│   └── video/                 # Vídeos (atualmente sem referência ativa no index.htm)
│
├── docs/                      # Esta documentação
│
└── .github/workflows/
    └── deploy.yml              # CI: deploy automático para Firebase no push em main/master
```

## Observações

- **`index.htm` precisa continuar na raiz.** O `firebase.json` reescreve todas as rotas (`"source": "**"`) para `/index.htm`, então mover esse arquivo exige atualizar a config de hosting.
- **Arquivos de config do Firebase (`firebase.json`, `.firebaserc`, `firestore.*`) ficam na raiz** porque o Firebase CLI (usado no workflow de deploy) os procura ali por padrão, sem flags extras.
- **`assets/images/originals/`** guarda `mi2.png`, `hits2.png` e `Lançamentos da música br 2026.png` — arquivos maiores/alternativos que não são carregados pelo site hoje (o site usa as versões menores `mi.png`/`hits.png`, e `og-image.png` é o mesmo conteúdo de `Lançamentos da música br 2026.png` já com o nome esperado pelas metatags Open Graph). Ficam preservados aqui como material-fonte em vez de serem apagados.
- **`assets/video/`** contém `5bandas.mp4` e `GANWALK.mp4`, usados anteriormente nos banners promocionais rotativos removidos do topo/rodapé do site. Não há mais nenhuma referência a eles em `index.htm`; foram apenas realocados, não removidos, caso sejam reaproveitados no futuro.
- **`mi.png`/`hits.png`** (logos dos parceiros no rodapé) são carregados via URL absoluta do `raw.githubusercontent.com` apontando para a branch `main`, não por caminho relativo — provavelmente para evitar os headers de `no-cache` que o `firebase.json` aplica a `**`. Isso significa que qualquer mudança de caminho desses dois arquivos só "aparece" no site depois que a branch `main` for atualizada.
