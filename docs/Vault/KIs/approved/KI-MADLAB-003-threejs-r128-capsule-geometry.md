---
ki_id: KI-MADLAB-003
title: "Three.js r128 fixado — CapsuleGeometry indisponível, alternativas obrigatórias"
domain: webgl-stack
source_os: "ceo-effects SKILL.md + Stack canônico MadLab"
approved_at: "2026-05-30"
approved_by: "antigravity-sprint3"
status: approved
confidence: 0.99
evidence_type: "Verificação direta de changelog do Three.js — CapsuleGeometry introduzida em r142"
applicable_to: ["ceo-effects", "aurora-web", "ElysianCorp", "todo contexto com Three.js"]
---

# KI-MADLAB-003 — Three.js r128: CapsuleGeometry Indisponível

## O Aprendizado

O MadLab Aurora tem **Three.js r128 como versão fixa**.

A `THREE.CapsuleGeometry` foi introduzida em **r142**.

Em r128, o uso de `THREE.CapsuleGeometry` lança:
```
TypeError: THREE.CapsuleGeometry is not a constructor
```

**Este erro é silencioso em contextos onde o THREE global é importado por CDN.**
O código "funciona" até o momento de instanciar a geometria — e quebra em runtime.

## Alternativas Obrigatórias em r128

Para substituir CapsuleGeometry:

```javascript
// OPÇÃO 1 — Cilindro com esferas nas pontas (mais simples)
const body = new THREE.CylinderGeometry(radius, radius, height, 32);
const topCap = new THREE.SphereGeometry(radius, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2);
const bottomCap = new THREE.SphereGeometry(radius, 32, 16, 0, Math.PI * 2, Math.PI / 2, Math.PI / 2);

// OPÇÃO 2 — RoundedBoxGeometry (se a lib estiver disponível)
// Disponível via three/examples/jsm/geometries/RoundedBoxGeometry.js em r128

// OPÇÃO 3 — Geometria customizada via BufferGeometry
// Para formas orgânicas — máximo controle
```

## Por Que Isso É Um KI de Segurança Operacional

- Agentes e desenvolvedores que não sabem a versão fixada importarão `CapsuleGeometry` naturalmente
- O erro ocorre em runtime, não em build — passa em desenvolvimento com versão nova mas quebra em produção se a versão estiver fixada
- A causa raiz nunca é óbvia — o agente vai depurar por horas sem encontrar

## Regra de Atualização de Versão

Para atualizar o Three.js além do r128:
1. OS formal de nível Médio/Alto aprovada pelo Comandante
2. Auditoria de todos os usos de geometrias introduzidas em versões intermediárias
3. Verificação de todos os imports via `import { X } from 'three'` (tree-shaking)
4. Teste de performance em Intel Iris Xe (baseline de GPU do MadLab)
5. Evidência em OS-Evidence antes de qualquer commit

## Geometrias Introduzidas Entre r128 e r142 (Alta Atenção)

| Geometria | Versão de Entrada | Alternativa em r128 |
|---|---|---|
| `CapsuleGeometry` | r142 | CylinderGeometry + SphereGeometry |
| `TorusKnotGeometry` updates | r130+ | Usar parâmetros originais |

## Importação Correta (Tree-Shaking) em r128

```javascript
// CORRETO — tree-shaking
import { Scene, PerspectiveCamera, WebGLRenderer, Mesh } from 'three';
import { CylinderGeometry, SphereGeometry } from 'three';

// ERRADO em produção — importa o bundle completo
import * as THREE from 'three';
```

## Evidência de Origem

- `.aurora/skills/ceo-effects/SKILL.md` — Stack técnico canônico: "Three.js → r128 (FIXO)"
- `.aurora/skills/ceo-effects/references/effects-playbook.md` — Seção Stack Técnico Canônico
- Three.js changelog: CapsuleGeometry adicionada em r142 (verificável em github.com/mrdoob/three.js/releases)
