import React, { useState, useEffect, useRef } from 'react';
import { MousePointer2 } from 'lucide-react';
import { Canvas } from '@react-three/fiber';
import ArcPuzzlePiece from './ARC/ArcPuzzlePiece';
import { PerspectiveCamera, Environment } from '@react-three/drei';

type PointerState = {
  x: number;
  y: number;
  inside: boolean;
};

const CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+[]{}<>/\\|';
const POST_REVEAL_DELAY_MS = 5000; // Exatos 5s APÓS o preloader
const POST_REVEAL_DURATION_MS = 1800;

function clamp(value: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, value));
}

function easeOutCubic(t: number): number {
  const p = 1 - t;
  return 1 - p * p * p;
}

function createShader(gl: WebGLRenderingContext, type: number, source: string): WebGLShader {
  const shader = gl.createShader(type);
  if (!shader) throw new Error('Falha ao criar shader.');
  gl.shaderSource(shader, source);
  gl.compileShader(shader);
  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
    const log = gl.getShaderInfoLog(shader) ?? 'Sem log';
    gl.deleteShader(shader);
    throw new Error(`Erro ao compilar shader: ${log}`);
  }
  return shader;
}

function createProgram(gl: WebGLRenderingContext, vertexSource: string, fragmentSource: string): WebGLProgram {
  const vertexShader = createShader(gl, gl.VERTEX_SHADER, vertexSource);
  const fragmentShader = createShader(gl, gl.FRAGMENT_SHADER, fragmentSource);
  const program = gl.createProgram();
  if (!program) throw new Error('Falha ao criar programa WebGL.');
  gl.attachShader(program, vertexShader);
  gl.attachShader(program, fragmentShader);
  gl.linkProgram(program);
  return program;
}

function createTexture(gl: WebGLRenderingContext): WebGLTexture {
  const texture = gl.createTexture();
  if (!texture) throw new Error('Falha ao criar textura.');
  gl.bindTexture(gl.TEXTURE_2D, texture);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
  gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
  return texture;
}

function updateTextureFromCanvas(gl: WebGLRenderingContext, texture: WebGLTexture, canvas: HTMLCanvasElement): void {
  if (!canvas || canvas.width === 0 || canvas.height === 0) return;
  gl.bindTexture(gl.TEXTURE_2D, texture);
  gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, 1);
  gl.pixelStorei(gl.UNPACK_PREMULTIPLY_ALPHA_WEBGL, 1);
  gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, canvas);
}

function setupCanvasForDpr(canvas: HTMLCanvasElement, width: number, height: number): CanvasRenderingContext2D | null {
  if (width <= 0 || height <= 0) return null;
  const dpr = window.devicePixelRatio || 1;
  canvas.width = Math.floor(width * dpr);
  canvas.height = Math.floor(height * dpr);
  const ctx = canvas.getContext('2d');
  if (!ctx) return null;
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.scale(dpr, dpr);
  return ctx;
}

function drawBackground(ctx: CanvasRenderingContext2D, width: number, height: number): void {
  const bg = ctx.createRadialGradient(
    width * 0.5, height * 0.08, 0,
    width * 0.5, height * 0.12,
    Math.max(width, height)
  );
  bg.addColorStop(0, '#000000');
  bg.addColorStop(0.35, '#050505');
  bg.addColorStop(1, '#000000');
  ctx.fillStyle = bg;
  ctx.fillRect(0, 0, width, height);
}

function drawScrambleScreen(canvas: HTMLCanvasElement, width: number, height: number): void {
  const ctx = setupCanvasForDpr(canvas, width, height);
  if (!ctx) return;

  ctx.clearRect(0, 0, width, height);
  drawBackground(ctx, width, height);

  const charWidth = 9;
  const charHeight = 15;
  const cols = Math.max(1, Math.floor(width / charWidth));
  const rows = Math.max(1, Math.floor(height / charHeight));

  ctx.font = '10px ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace';
  ctx.textBaseline = 'top';

  for (let row = 0; row < rows; row += 1) {
    for (let col = 0; col < cols; col += 1) {
      if (Math.random() < 0.88) continue; 
      const x = col * charWidth;
      const y = row * charHeight;
      const char = CHARS.charAt(Math.floor(Math.random() * CHARS.length));
      const alpha = clamp(0.08 + Math.random() * 0.2, 0.08, 0.35);
      ctx.fillStyle = `rgba(0,255,239,${alpha.toFixed(3)})`;
      ctx.fillText(char, x, y);
    }
  }
}

function drawTextScreen(canvas: HTMLCanvasElement, width: number, height: number, puzzleImage?: HTMLImageElement | null): void {
  const ctx = setupCanvasForDpr(canvas, width, height);
  if (!ctx) return;

  ctx.clearRect(0, 0, width, height);

  if (puzzleImage && puzzleImage.complete && puzzleImage.naturalWidth > 0) {
    const areaX = width * 0.60;
    const areaW = width * 0.35;
    const areaH = height * 0.85;
    const areaY = height * 0.07;

    const imgRatio = puzzleImage.naturalWidth / puzzleImage.naturalHeight;
    const areaRatio = areaW / areaH;
    let drawW: number, drawH: number;
    if (imgRatio > areaRatio) {
      drawW = areaW; drawH = areaW / imgRatio;
    } else {
      drawH = areaH; drawW = areaH * imgRatio;
    }
    const drawX = areaX + (areaW - drawW) / 2;
    const drawY = areaY + (areaH - drawH) / 2;

    ctx.globalAlpha = 0.65;
    ctx.drawImage(puzzleImage, drawX, drawY, drawW, drawH);
    ctx.globalAlpha = 1.0;
  }

  const left = width * 0.05;
  const baselineY = height * 0.52;
  const titleSize = clamp(width * 0.14, 64, 180);
  const subtitleSize = clamp(width * 0.0135, 14, 20);
  const indexSize = clamp(width * 0.08, 48, 128);

  ctx.fillStyle = 'rgba(255,255,255,0.48)';
  ctx.font = '500 10px ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace';
  ctx.textBaseline = 'top';
  ctx.fillText('PROTOCOLO ELYSIAN // 01 // AUDITORIA FORENSE', left, baselineY - 80);

  ctx.fillStyle = 'rgba(255,255,255,0.12)';
  ctx.fillRect(left, baselineY - 24, Math.min(width * 0.32, 220), 1);

  ctx.fillStyle = '#FFFFFF';
  ctx.font = `900 ${titleSize}px "Lay Grotesk", Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`;
  ctx.textBaseline = 'alphabetic';
  // Adiciona um pequeno padding à esquerda para evitar clipping de glifos largos
  ctx.fillText('Elysian', left + 4, baselineY + titleSize * 0.35);

  ctx.fillStyle = 'rgba(255,255,255,0.68)';
  ctx.font = `400 ${subtitleSize}px "Lay Grotesk", Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`;
  ctx.textBaseline = 'top';
  ctx.fillText('A inteligência sob o seu controle', left, baselineY + titleSize * 0.52 + 10);

  const right = width * 0.95;
  const bottom = height * 0.94;
  ctx.textAlign = 'right';
  ctx.textBaseline = 'alphabetic';
  ctx.fillStyle = 'rgba(255,255,255,0.15)';
  ctx.font = `900 ${indexSize}px "Lay Grotesk", Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`;
  ctx.fillText('01', right, bottom - 20);
  ctx.fillRect(right - 100, bottom, 100, 1);
  ctx.textAlign = 'start';
}

const vertexShaderSource = `
attribute vec2 a_position;
attribute vec2 a_uv;
varying vec2 v_uv;
void main() {
  v_uv = a_uv;
  gl_Position = vec4(a_position, 0.0, 1.0);
}
`;

const fragmentShaderSource = `
precision mediump float;
uniform sampler2D u_scramble_tex;
uniform sampler2D u_text_tex;
uniform vec2 u_resolution;
uniform vec2 u_mouse;
uniform float u_mouse_inside;
uniform float u_post_reveal;
varying vec2 v_uv;

float random(vec2 st) {
    return fract(sin(dot(st.xy, vec2(12.9898,78.233))) * 43758.5453123);
}

void main() {
  vec4 scramble = texture2D(u_scramble_tex, v_uv);
  vec4 texColor  = texture2D(u_text_tex, v_uv);
  vec2 fragCoord = v_uv * u_resolution;

  float mouseReveal = 0.0;
  if (u_mouse_inside > 0.5) {
    float dist = distance(fragCoord, u_mouse);
    mouseReveal = 1.0 - smoothstep(100.0, 380.0, dist);
  }

  bool isImageZone = v_uv.x > 0.55;

  float textReveal = max(mouseReveal, u_post_reveal);
  float imageReveal = mouseReveal;
  float finalReveal = isImageZone ? imageReveal : textReveal;

  float noise = random(v_uv * u_resolution.xy) * 0.08;
  vec3 scrambleLayer = scramble.rgb + vec3(noise * 0.5);
  
  float contentAlpha = texColor.a * finalReveal;
  vec3 color = mix(scrambleLayer, texColor.rgb, contentAlpha);
  
  gl_FragColor = vec4(color, 1.0);
}
`;

const SovereignHeroWebGL: React.FC = () => {
  // Estados do Preloader
  const [loadProgress, setLoadProgress] = useState(0);
  const [isPreloaderDone, setIsPreloaderDone] = useState(false);
  
  // Refs para controle de tempo do WebGL
  const isReadyRef = useRef(false);
  const startTimeRef = useRef(0);

  const sectionRef = useRef<HTMLElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const offscreenScramble = useRef<HTMLCanvasElement | null>(null);
  const offscreenText = useRef<HTMLCanvasElement | null>(null);
  const pointerRef = useRef<PointerState>({ x: 0, y: 0, inside: false });
  const postRevealRef = useRef(0);
  const rafRef = useRef<number | null>(null);
  const puzzleImageRef = useRef<HTMLImageElement | null>(null);

  const [mouseHintVisible, setMouseHintVisible] = useState(true);

  // Lógica do Preloader Independente
  useEffect(() => {
    let start = performance.now();
    const duration = 2400; // 2.4 segundos de loading fake
    let animationFrame: number;

    const step = (now: number) => {
      const progress = Math.min((now - start) / duration, 1);
      setLoadProgress(Math.floor(easeOutCubic(progress) * 100));

      if (progress < 1) {
        animationFrame = requestAnimationFrame(step);
      } else {
        // Pausa dramática no 100% antes de liberar
        setTimeout(() => {
          setIsPreloaderDone(true);
          isReadyRef.current = true;
          startTimeRef.current = performance.now(); // AGORA o cronômetro WebGL começa!
          
          // Dica do mouse some após 4s DO FIM do preloader
          setTimeout(() => setMouseHintVisible(false), 4000);
        }, 500); 
      }
    };
    animationFrame = requestAnimationFrame(step);

    return () => cancelAnimationFrame(animationFrame);
  }, []);

  // Inicialização WebGL
  useEffect(() => {
    const section = sectionRef.current;
    const canvas = canvasRef.current;
    if (!section || !canvas) return;

    if (!offscreenScramble.current) offscreenScramble.current = document.createElement('canvas');
    if (!offscreenText.current) offscreenText.current = document.createElement('canvas');

    const gl = canvas.getContext('webgl', { alpha: true, antialias: true, powerPreference: 'high-performance' }) || canvas.getContext('experimental-webgl');
    if (!gl || !(gl instanceof WebGLRenderingContext)) return;

    const program = createProgram(gl, vertexShaderSource, fragmentShaderSource);
    gl.useProgram(program);

    const positionLocation  = gl.getAttribLocation(program, 'a_position');
    const uvLocation        = gl.getAttribLocation(program, 'a_uv');
    const resolutionLocation  = gl.getUniformLocation(program, 'u_resolution');
    const mouseLocation       = gl.getUniformLocation(program, 'u_mouse');
    const mouseInsideLocation = gl.getUniformLocation(program, 'u_mouse_inside');
    const postRevealLocation  = gl.getUniformLocation(program, 'u_post_reveal');
    const scrambleTexLocation = gl.getUniformLocation(program, 'u_scramble_tex');
    const textTexLocation     = gl.getUniformLocation(program, 'u_text_tex');

    const quadBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, quadBuffer);
    gl.bufferData(
      gl.ARRAY_BUFFER,
      new Float32Array([-1, -1, 0, 0, 1, -1, 1, 0, -1, 1, 0, 1, -1, 1, 0, 1, 1, -1, 1, 0, 1, 1, 1, 1]),
      gl.STATIC_DRAW
    );
    gl.enableVertexAttribArray(positionLocation);
    gl.vertexAttribPointer(positionLocation, 2, gl.FLOAT, false, 16, 0);
    gl.enableVertexAttribArray(uvLocation);
    gl.vertexAttribPointer(uvLocation, 2, gl.FLOAT, false, 16, 8);

    const scrambleTexture = createTexture(gl);
    const textTexture     = createTexture(gl);

    let viewportWidth  = window.innerWidth;
    let viewportHeight = window.innerHeight;

    const redrawTextCanvas = () => {
      if (offscreenText.current) {
        drawTextScreen(offscreenText.current, viewportWidth, viewportHeight, puzzleImageRef.current);
        updateTextureFromCanvas(gl, textTexture, offscreenText.current);
      }
    };

    const img = new Image();
    img.onload = () => {
      puzzleImageRef.current = img;
      redrawTextCanvas();
    };
    img.src = '/assets/puzzle-pb.png';

    const resize = () => {
      viewportWidth  = window.innerWidth;
      viewportHeight = window.innerHeight;
      const dpr = window.devicePixelRatio || 1;
      canvas.width  = Math.floor(viewportWidth  * dpr);
      canvas.height = Math.floor(viewportHeight * dpr);
      canvas.style.width  = `${viewportWidth}px`;
      canvas.style.height = `${viewportHeight}px`;

      gl.viewport(0, 0, canvas.width, canvas.height);
      gl.uniform2f(resolutionLocation, viewportWidth, viewportHeight);

      if (offscreenScramble.current) {
        drawScrambleScreen(offscreenScramble.current, viewportWidth, viewportHeight);
        updateTextureFromCanvas(gl, scrambleTexture, offscreenScramble.current);
      }
      redrawTextCanvas();
    };

    const render = () => {
      if (offscreenScramble.current) {
        drawScrambleScreen(offscreenScramble.current, viewportWidth, viewportHeight);
        updateTextureFromCanvas(gl, scrambleTexture, offscreenScramble.current);
      }

      gl.activeTexture(gl.TEXTURE0);
      gl.bindTexture(gl.TEXTURE_2D, scrambleTexture);
      gl.uniform1i(scrambleTexLocation, 0);

      gl.activeTexture(gl.TEXTURE1);
      gl.bindTexture(gl.TEXTURE_2D, textTexture);
      gl.uniform1i(textTexLocation, 1);

      const pointer = pointerRef.current;
      gl.uniform2f(mouseLocation, pointer.x, viewportHeight - pointer.y);
      gl.uniform1f(mouseInsideLocation, pointer.inside ? 1 : 0);
      gl.uniform1f(postRevealLocation, postRevealRef.current);

      gl.drawArrays(gl.TRIANGLES, 0, 6);
    };

    const loop = (now: number) => {
      // O Relógio do Shader só conta se isReadyRef for verdadeiro
      if (isReadyRef.current) {
        const elapsed = performance.now() - startTimeRef.current;
        const postElapsed = Math.max(0, elapsed - POST_REVEAL_DELAY_MS);
        postRevealRef.current = easeOutCubic(clamp(postElapsed / POST_REVEAL_DURATION_MS, 0, 1));
      }

      render();
      rafRef.current = window.requestAnimationFrame(loop);
    };

    const handleMouseMove = (e: MouseEvent) => {
      const r = section.getBoundingClientRect();
      pointerRef.current = { x: e.clientX - r.left, y: e.clientY - r.top, inside: true };
      if (isPreloaderDone) setMouseHintVisible(false);
    };

    const handleWheel = (e: WheelEvent) => {
      // Se o usuário tenta rolar para baixo e o reveal não acabou, acelera drasticamente
      if (e.deltaY > 0 && isReadyRef.current) {
        startTimeRef.current -= 200; // Avança o relógio interno em 200ms por tick de scroll
      }
    };

    window.addEventListener('resize', resize);
    section.addEventListener('mousemove', handleMouseMove);
    section.addEventListener('mouseleave', () => { pointerRef.current.inside = false; });
    window.addEventListener('wheel', handleWheel, { passive: true });

    resize();
    rafRef.current = window.requestAnimationFrame(loop);

    return () => {
      window.removeEventListener('resize', resize);
      window.removeEventListener('wheel', handleWheel);
      if (rafRef.current) window.cancelAnimationFrame(rafRef.current);
      gl.deleteTexture(scrambleTexture);
      gl.deleteTexture(textTexture);
      gl.deleteBuffer(quadBuffer);
      gl.deleteProgram(program);
    };
  }, [isPreloaderDone]);

  return (
    <section
      ref={sectionRef}
      className="relative w-full overflow-hidden bg-black-piano text-white-absolute"
      style={{ height: '100dvh', minHeight: '100dvh', margin: 0, padding: 0 }}
    >
      {/* 1 - PRELOADER BRUTALISTA AURORA */}
      <div 
        className={`absolute inset-0 z-50 flex flex-col items-center justify-center bg-[#050505] transition-opacity duration-1000 ease-in-out ${isPreloaderDone ? 'opacity-0 pointer-events-none' : 'opacity-100'}`}
      >
        <div className="flex flex-col items-center gap-4">
          <span className="font-mono text-[10px] uppercase tracking-[0.5em] text-white/40">Estabelecendo Conexão</span>
          <span className="font-headline text-8xl font-black text-white/90 tabular-nums tracking-tighter">
            {loadProgress.toString().padStart(3, '0')}
            <span className="text-4xl text-cyan-aqua/80">%</span>
          </span>
          <div className="w-48 h-px bg-white/10 relative overflow-hidden mt-4">
            <div 
              className="absolute top-0 left-0 h-full bg-cyan-aqua shadow-[0_0_10px_rgba(0,255,239,0.5)] transition-all duration-100 ease-out"
              style={{ width: `${loadProgress}%` }}
            />
          </div>
        </div>
      </div>

      {/* 2 - O EFEITO 3D ARC (Substituindo o antigo WebGL 2D) */}
      <div className="absolute inset-0 z-10 pointer-events-none">
        <Canvas dpr={[1, 2]} gl={{ antialias: true, alpha: true }}>
          <PerspectiveCamera makeDefault position={[0, 0, 5]} fov={15} />
          <Environment preset="city" />
          
          <React.Suspense fallback={null}>
            <ArcPuzzlePiece 
              url="/assets/models/puzzle_v8_ktx2.glb" 
              progress={isPreloaderDone ? postRevealRef.current : 0} 
            />
          </React.Suspense>

          <ambientLight intensity={0.2} />
          <pointLight position={[10, 10, 10]} intensity={1} />
        </Canvas>
      </div>

      {/* ELEMENTOS DA INTERFACE (Só aparecem após o preloader terminar) */}
      <div className={`transition-opacity duration-1000 delay-500 ${isPreloaderDone ? 'opacity-100' : 'opacity-0'}`}>
        
        <div
          className="absolute z-20 pointer-events-none select-none"
          style={{
            top: '50%', right: '7%', transform: 'translateY(-50%)',
            opacity: mouseHintVisible ? 1 : 0, transition: 'opacity 800ms ease',
          }}
        >
          <span className="font-mono text-[9px] uppercase tracking-[0.5em] text-white/30">← mova o mouse</span>
        </div>

        <div className="absolute inset-x-0 bottom-0 z-20 p-12 flex justify-between items-end pointer-events-none">
          <div className="flex flex-col gap-4 max-w-sm pointer-events-auto">
            <div className="flex items-center gap-3">
              <span className="w-2 h-2 bg-cyan-aqua cyan-glow animate-pulse"></span>
              <span className="font-mono text-[9px] uppercase tracking-[0.4em] text-cyan-aqua">Protocolo Ativo</span>
            </div>
            <h3 className="text-xl font-headline font-bold uppercase leading-tight">Auditoria Soberana em tempo real</h3>
          </div>

          <div className="flex flex-col items-end gap-12 pointer-events-auto">
            <div className="flex flex-col items-end gap-2 text-right">
              <span className="font-mono text-[8px] uppercase tracking-[0.5em] text-white/20">Deslize para navegar</span>
              <div className="w-px h-12 bg-white/20"></div>
            </div>

            <button
              className="group flex items-center gap-4 border border-white/10 bg-white/5 py-4 px-10 font-medium uppercase tracking-[0.25em] text-[10px] text-white backdrop-blur-xl transition-all duration-500 hover:bg-white/10 hover:border-white/30 active:scale-95"
              onClick={() => window.scrollTo({ top: window.innerHeight, behavior: 'smooth' })}
            >
              Acessar Auditoria
              <MousePointer2 className="h-4 w-4 transition-transform duration-500 group-hover:translate-x-1" />
            </button>
          </div>
        </div>

        <div className="absolute top-1/2 left-8 -translate-y-1/2 flex flex-col gap-32 pointer-events-none opacity-20">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="flex flex-col gap-4">
              <div className="w-4 h-px bg-white"></div>
              <span className="font-mono text-[8px] [writing-mode:vertical-lr] uppercase tracking-[0.8em]">0x7F49_SYS_{i+1}</span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default SovereignHeroWebGL;
