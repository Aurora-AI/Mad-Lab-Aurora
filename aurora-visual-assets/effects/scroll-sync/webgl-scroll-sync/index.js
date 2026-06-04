/**
 * WebGL Scroll Sync — Aurora Visual Assets
 * Asset ID: webgl-scroll-sync-001
 * Categoria: effects/scroll-sync
 * Origem: Lusion Ltd — github.com/lusionltd/WebGL-Scroll-Sync
 * Licença: MIT
 * Ingerido em: 2026-04-18
 * OS: OS-ANTIGRAVITY-AURORA-VISUAL-ASSETS-20260418-012
 *
 * Padrões: P046, P047, P048, P049, P050, P051, P052
 *
 * COMO USAR:
 * 1. Criar canvas#canvas dentro de div#wrapper (position: relative)
 * 2. Adicionar classe .image nos elementos DOM a serem ancorados
 * 3. Fornecer texturas via textureLoader (adaptar createImageMeshes)
 * 4. Substituir fragmentShader por shader de profundidade se necessário
 *
 * IMPORTANTE: CSS do canvas deve ser position: absolute (não fixed)
 */

import * as THREE from 'three'
import imgVertexShader from './shaders/img.vert'
import imgFragmentShader from './shaders/img.frag'

const textureLoader = new THREE.TextureLoader()

let canvas
let renderer
let scene
let camera
let planeGeometry
let scrollOffset = new THREE.Vector2()
let sceneOffset = new THREE.Vector2()

let imageMeshes = []

let strength = 0
let lastScrollY = typeof window !== 'undefined' ? window.scrollY : 0
let isReducedMotion = false

const padding = 0.25

export function init() {
  canvas = document.querySelector('#canvas')
  if (!canvas) return

  renderer = new THREE.WebGLRenderer({
    canvas,
    antialias: true,
    alpha: true,
  })
  renderer.setPixelRatio(window.devicePixelRatio)

  scene = new THREE.Scene()
  camera = new THREE.OrthographicCamera(-0.5, 0.5, 0.5, -0.5, 0, 1000)
  camera.position.z = 2
  
  planeGeometry = new THREE.PlaneGeometry(1, 1)

  // Accessibility check
  isReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches

  createImageMeshes()
  onResize()

  window.addEventListener('resize', onResize)
  window.addEventListener('scroll', onScroll)

  update()
}

/**
 * Cleanup function to prevent memory leaks in SPAs
 * Seal: AURORA_TRUSTWARE
 */
export function dispose() {
  window.removeEventListener('resize', onResize)
  window.removeEventListener('scroll', onScroll)
  
  if (renderer) {
    renderer.dispose()
  }

  imageMeshes.forEach((item) => {
    item.mesh.geometry.dispose()
    item.mesh.material.dispose()
    if (item.material.uniforms.u_texture.value) {
      item.material.uniforms.u_texture.value.dispose()
    }
  })

  scene = null
  camera = null
  imageMeshes = []
}

function createImageMeshes() {
  const imageElements = document.querySelectorAll('.image')

  imageElements.forEach((el, i) => {
    const texture = new THREE.Texture() // Placeholder

    const material = new THREE.ShaderMaterial({
      uniforms: {
        u_texture: { value: texture },
        u_res: { value: new THREE.Vector2() },
        u_imgRes: { value: new THREE.Vector2() },
        u_domXY: { value: new THREE.Vector2() },
        u_domWH: { value: new THREE.Vector2() },
        u_strength: { value: 0 },
        u_viewportWH: { value: new THREE.Vector2() },
        u_scrollOffset: { value: scrollOffset },
        u_rands: { value: new THREE.Vector4() },
      },
      vertexShader: imgVertexShader,
      fragmentShader: imgFragmentShader,
      transparent: true,
    })

    const mesh = new THREE.Mesh(planeGeometry, material)
    scene.add(mesh)

    imageMeshes.push({
      el,
      mesh,
      material,
    })
  })
}

function onResize() {
  if (!canvas) return
  const width = window.innerWidth
  const height = window.innerHeight

  const canvasWidth = width
  const canvasHeight = height * (1 + padding * 2)

  canvas.style.width = `${canvasWidth}px`
  canvas.style.height = `${canvasHeight}px`

  renderer.setSize(canvasWidth, canvasHeight, false)

  imageMeshes.forEach((item) => {
    const rect = item.el.getBoundingClientRect()
    item.material.uniforms.u_domWH.value.set(rect.width, rect.height)
    item.material.uniforms.u_viewportWH.value.set(width, height)
  })
}

function onScroll() {
  const currentScrollY = window.scrollY
  const delta = currentScrollY - lastScrollY
  
  // Suppression for accessibility
  if (!isReducedMotion) {
    strength += delta * 0.05
    strength = Math.min(Math.max(strength, -2), 2)
  } else {
    strength = 0
  }
  
  lastScrollY = currentScrollY
}

function update() {
  if (!scene || !camera) return
  requestAnimationFrame(update)

  const dt = 0.016
  strength *= Math.exp(-dt * 10)

  scrollOffset.set(window.scrollX, window.scrollY)
  
  // P046 — Absolute Canvas Scroll Sync
  const canvasY = scrollOffset.y - window.innerHeight * padding
  canvas.style.transform = `translate(${scrollOffset.x}px, ${canvasY}px)`

  imageMeshes.forEach((item) => {
    const rect = item.el.getBoundingClientRect()
    
    // P048 — Anchoring
    item.material.uniforms.u_domXY.value.set(
      rect.left + scrollOffset.x,
      rect.top + scrollOffset.y
    )
    
    item.material.uniforms.u_strength.value = strength
    
    // Randoms para glitch estocástico (desativado se reduced motion)
    if (!isReducedMotion) {
      item.material.uniforms.u_rands.value.set(
        Math.random(),
        Math.random(),
        Math.random(),
        Math.random()
      )
    }

    // P052 — Frustum Culling Manual
    const canvasTop = scrollOffset.y - window.innerHeight * padding
    const canvasBottom = canvasTop + window.innerHeight * (1 + padding * 2)
    const itemTop = rect.top + scrollOffset.y
    const itemBottom = itemTop + rect.height

    item.mesh.visible = itemTop < canvasBottom && itemBottom > canvasTop
  })

  renderer.render(scene, camera)
}
