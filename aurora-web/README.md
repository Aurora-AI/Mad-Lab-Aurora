# Aurora Web

Site institucional e brand site do ecossistema Aurora, governado pelo braco criativo `MadLabAurora`.

## Papel

- propriedade web institucional da marca Aurora
- laboratorio de experiencia, narrativa e posicionamento
- ativo criativo do portfolio, nao produto da fabrica

## Localizacao canonica

`C:\Aurora\MadLabAurora\aurora-web`

## Execucao local

Pre-requisito: Node.js

1. Instalar dependencias com `npm install`
2. Configurar variaveis locais conforme `.env.example`
3. Subir em desenvolvimento com `npm run dev`
4. Gerar build com `npm run build`
5. Validar o pacote com `npm run check`

## Variaveis de ambiente

- `VITE_GEMINI_API_KEY`: chave Gemini usada pelo chat institucional no cliente
- `VITE_GEMINI_MODEL`: modelo do Gemini usado pelo chat
- `APP_URL`: URL publica da aplicacao

## Deploy no Vercel

O projeto esta preparado como app Vite estatico.

1. Importar o repositorio no Vercel
2. Configurar a variavel `VITE_GEMINI_API_KEY`
3. Opcionalmente configurar `VITE_GEMINI_MODEL`
4. Fazer o deploy com build command `npm run build` e output `dist`

## Observacao

O projeto nasceu de export inicial do AI Studio e foi internalizado na topologia oficial do portfolio Aurora.
