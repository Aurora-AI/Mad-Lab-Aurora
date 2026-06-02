# Aurora Visual Assets

**Biblioteca canônica de ativos visuais da fábrica Aurora.**

> Sites vivos. Responsivos. Que respiram junto com o usuário. Que reagem a cada interação.  
> Explorar os limites da física e WebGPU — não replicar o que o mercado já faz.

---

## Filosofia

Esta biblioteca não é um design system no sentido convencional. Não é Storybook.
Não é uma coleção de botões e inputs.

É um **arsenal de física visual** — efeitos que fazem o usuário sentir que o site
está vivo. Que respira. Que tem peso, inércia, e reação.

Cada ativo aqui segue dois caminhos:
1. **Ativos externos curados** — importados de fontes de referência (21st.dev, Codrops,
   repositórios de ponta), dissecados e documentados para que a Aurora entenda *como*
   foram construídos, não apenas *o que* fazem.
2. **Ativos Aurora-native** — criados pela fábrica a partir dos padrões extraídos dos
   ativos externos. Esses são o diferencial real.

---

## Categorias

| Categoria | Descrição |
|---|---|
| `heroes/` | Componentes de hero section — primeira impressão do produto |
| `effects/` | Efeitos isolados reutilizáveis — shader, particle, distortion |
| `scenes/` | Cenas Three.js / WebGPU completas — imersão total |
| `interactions/` | Padrões de interação — mouse parallax, scroll physics, touch |
| `typography/` | Efeitos tipográficos animados — glitch, reveal, scramble |

---

## Como usar em um projeto Aurora

```tsx
// Importar diretamente pelo path relativo
import { HeroFuturistic } from '../../aurora-visual-assets/heroes/hero-futuristic'

// Ou via alias de path (configurar no vite.config / tsconfig)
import { HeroFuturistic } from '@aurora-visual/heroes/hero-futuristic'
```

Para configurar o alias no projeto consumidor, adicionar ao `vite.config.ts`:
```ts
resolve: {
  alias: {
    '@aurora-visual': path.resolve(__dirname, '../aurora-visual-assets')
  }
}
```

---

## Protocolo de Adição de Novo Ativo

1. Criar pasta em `[categoria]/[nome-do-ativo]/`
2. Copiar código-fonte para `index.tsx`
3. Criar `package.json` com deps específicas
4. **Obrigatório:** Criar `anatomy/[nome-do-ativo].md` com dissecação técnica completa
5. Adicionar entrada no `manifest.json`
6. Adicionar padrões técnicos ao `PATTERNS.md`
7. Adicionar entrada ao `CHANGELOG.md`

Sem `anatomy/`: o ativo não existe para o CEO-Design agent.

---

## CEO-Design Agent

O agente CEO-Design consome esta biblioteca como corpus de aprendizado.
Seu propósito: entender os padrões técnicos de cada ativo e gerar
variações Aurora-native.

**Status:** Pendente. Ativado quando o corpus tiver mínimo 3 ativos dissecados.

---

## Dependências Globais da Biblioteca

Os ativos desta biblioteca assumem que o projeto consumidor tem:

```json
{
  "three": "^0.183.0",
  "@react-three/fiber": "^9.0.0",
  "@react-three/drei": "^10.0.0",
  "framer-motion": "^12.0.0",
  "gsap": "^3.15.0"
}
```

Ativos com deps adicionais documentam em seu `package.json` local.
