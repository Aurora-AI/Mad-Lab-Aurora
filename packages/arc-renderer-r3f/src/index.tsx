import {
  memo,
  useEffect,
  useMemo,
  useRef,
  useState,
  Suspense,
  type CSSProperties,
} from "react";
import { Canvas, useFrame, useLoader } from "@react-three/fiber";
import * as THREE from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import type { ArtifactManifest } from "@aurora/arc-schema";
import {
  resolveRendererRuntimeSnapshot,
  sceneSpecForProfile,
  shouldShowRendererDiagnostics,
  type ArcRendererDiagnostics,
  type RendererDeviceHints,
} from "./runtime";

type ShapePrimitive = "torus" | "torusKnot" | "sphere" | "icosahedron" | "nautilus";

export interface AgentRenderedShapeProps {
  artifact: ArtifactManifest | null;
  style?: CSSProperties;
  className?: string;
  diagnostics?: boolean;
  onDiagnostics?: (diagnostics: ArcRendererDiagnostics) => void;
  sceneTone?: "dark" | "paper";
}

function useReducedMotionPreference() {
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(false);

  useEffect(() => {
    if (typeof window === "undefined" || typeof window.matchMedia !== "function") {
      return;
    }

    const mediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
    const update = () => setPrefersReducedMotion(mediaQuery.matches);
    update();

    if (typeof mediaQuery.addEventListener === "function") {
      mediaQuery.addEventListener("change", update);
      return () => mediaQuery.removeEventListener("change", update);
    }

    mediaQuery.addListener(update);
    return () => mediaQuery.removeListener(update);
  }, []);

  return prefersReducedMotion;
}

function useRendererDeviceHints(): RendererDeviceHints {
  const prefersReducedMotion = useReducedMotionPreference();
  const [hints, setHints] = useState<RendererDeviceHints>({
    hardwareConcurrency: 4,
    deviceMemoryGb: 4,
    maxTouchPoints: 0,
    pixelRatio: 1,
    viewportWidth: 1280,
    prefersReducedMotion,
  });

  useEffect(() => {
    const readHints = () => {
      const navigatorWithMemory = navigator as Navigator & {
        deviceMemory?: number;
      };

      setHints({
        hardwareConcurrency: navigator.hardwareConcurrency,
        deviceMemoryGb: navigatorWithMemory.deviceMemory,
        maxTouchPoints: navigator.maxTouchPoints,
        pixelRatio: window.devicePixelRatio,
        viewportWidth: window.innerWidth,
        prefersReducedMotion,
      });
    };

    readHints();
    window.addEventListener("resize", readHints);
    return () => window.removeEventListener("resize", readHints);
  }, [prefersReducedMotion]);

  return hints;
}

function buildGeometry(primitive: ShapePrimitive, complexity: number) {
  const detail = Math.max(2, Math.round(2 + complexity * 4));
  switch (primitive) {
    case "torus":
      return new THREE.TorusGeometry(0.96, 0.26, 32 + detail * 4, 96 + detail * 18);
    case "torusKnot":
      return new THREE.TorusKnotGeometry(0.78, 0.22, 180 + detail * 24, 22 + detail * 4);
    case "sphere":
      return new THREE.IcosahedronGeometry(1, detail + 2);
    case "icosahedron":
      return new THREE.IcosahedronGeometry(1.02, detail);
    case "nautilus":
    default:
      return new THREE.TorusKnotGeometry(0.88, 0.18, 220 + detail * 20, 24 + detail * 4, 2, 3);
  }
}

function detectWebGLSupport() {
  if (typeof document === "undefined") {
    return false;
  }

  try {
    const canvas = document.createElement("canvas");
    return Boolean(
      canvas.getContext("webgl2") ||
        canvas.getContext("webgl") ||
        canvas.getContext("experimental-webgl"),
    );
  } catch {
    return false;
  }
}

function ArtifactMesh({
  artifact,
  diagnostics,
}: {
  artifact: ArtifactManifest;
  diagnostics: ArcRendererDiagnostics;
}) {
  const meshRef = useRef<THREE.Mesh>(null);
  const geometryRecipe = artifact.shapeDNA.geometry;
  const motionRecipe = artifact.shapeDNA.motion;
  const materialRecipe = artifact.shapeDNA.material;
  const sceneSpec = sceneSpecForProfile(
    diagnostics.effectiveProfile ?? artifact.renderProfile,
  );

  const geometry = useMemo(
    () => buildGeometry(geometryRecipe.primitive as ShapePrimitive, geometryRecipe.complexity),
    [geometryRecipe.complexity, geometryRecipe.primitive],
  );

  useEffect(() => () => geometry.dispose(), [geometry]);

  useFrame(({ clock, pointer }) => {
    const mesh = meshRef.current;
    if (!mesh) return;

    const elapsed = clock.getElapsedTime();
    const reducedMotion = diagnostics.prefersReducedMotion;
    const degraded = diagnostics.effectiveProfile === "DEGRADED";
    const rotationSpeed = reducedMotion
      ? motionRecipe.rotationSpeed * 0.18
      : degraded
        ? motionRecipe.rotationSpeed * 0.42
        : motionRecipe.rotationSpeed;
    const floatAmplitude = reducedMotion
      ? motionRecipe.floatAmplitude * 0.2
      : degraded
        ? motionRecipe.floatAmplitude * 0.45
        : motionRecipe.floatAmplitude;
    const mouseStrength = reducedMotion || degraded ? 0 : motionRecipe.mouseStrength;
    const turbulence = reducedMotion
      ? motionRecipe.turbulence * 0.08
      : degraded
        ? motionRecipe.turbulence * 0.25
        : motionRecipe.turbulence;

    mesh.rotation.y += rotationSpeed * 0.018;
    mesh.rotation.x = Math.sin(elapsed * (0.32 + turbulence * 0.2)) * (0.1 + turbulence * 0.1);
    mesh.position.y = Math.sin(elapsed * (0.65 + motionRecipe.floatFrequency)) * floatAmplitude;
    mesh.position.x = pointer.x * mouseStrength;
    mesh.position.z = pointer.y * mouseStrength * 0.5;

    const pulse =
      1 +
      Math.sin(elapsed * (0.52 + motionRecipe.floatFrequency)) *
        geometryRecipe.deformation *
        (degraded ? 0.04 : 0.08);
    mesh.scale.setScalar(sceneSpec.scale * pulse);
  });

  return (
    <mesh ref={meshRef} geometry={geometry}>
      <meshPhysicalMaterial
        color={materialRecipe.colorA}
        emissive={materialRecipe.colorB}
        emissiveIntensity={diagnostics.effectiveProfile === "DEGRADED" ? 0.08 : 0.18}
        metalness={materialRecipe.metalness}
        roughness={materialRecipe.roughness}
        clearcoat={materialRecipe.clearcoat}
        transmission={
          diagnostics.effectiveProfile === "DEGRADED"
            ? Math.min(materialRecipe.transmission, 0.02)
            : materialRecipe.transmission
        }
        ior={materialRecipe.ior}
        iridescence={
          diagnostics.effectiveProfile === "DEGRADED"
            ? Math.min(materialRecipe.iridescence, 0.08)
            : materialRecipe.iridescence
        }
        reflectivity={0.6}
      />
    </mesh>
  );
}

function BlenderMesh({
  modelPath,
  artifact,
  diagnostics,
}: {
  modelPath: string;
  artifact: ArtifactManifest;
  diagnostics: ArcRendererDiagnostics;
}) {
  const gltf = useLoader(GLTFLoader, modelPath);
  const groupRef = useRef<THREE.Group>(null);
  const motionRecipe = artifact.shapeDNA.motion;
  const geometryRecipe = artifact.shapeDNA.geometry;
  const sceneSpec = sceneSpecForProfile(
    diagnostics.effectiveProfile ?? artifact.renderProfile,
  );

  useFrame(({ clock, pointer }) => {
    const group = groupRef.current;
    if (!group) return;

    const elapsed = clock.getElapsedTime();
    const reducedMotion = diagnostics.prefersReducedMotion;
    const degraded = diagnostics.effectiveProfile === "DEGRADED";
    const rotationSpeed = reducedMotion
      ? motionRecipe.rotationSpeed * 0.18
      : degraded
        ? motionRecipe.rotationSpeed * 0.42
        : motionRecipe.rotationSpeed;
    const floatAmplitude = reducedMotion
      ? motionRecipe.floatAmplitude * 0.2
      : degraded
        ? motionRecipe.floatAmplitude * 0.45
        : motionRecipe.floatAmplitude;
    const mouseStrength = reducedMotion || degraded ? 0 : motionRecipe.mouseStrength;
    const turbulence = reducedMotion
      ? motionRecipe.turbulence * 0.08
      : degraded
        ? motionRecipe.turbulence * 0.25
        : motionRecipe.turbulence;

    group.rotation.y += rotationSpeed * 0.018;
    group.rotation.x = Math.sin(elapsed * (0.32 + turbulence * 0.2)) * (0.1 + turbulence * 0.1);
    group.position.y = Math.sin(elapsed * (0.65 + motionRecipe.floatFrequency)) * floatAmplitude;
    group.position.x = pointer.x * mouseStrength;
    group.position.z = pointer.y * mouseStrength * 0.5;

    const pulse =
      1 +
      Math.sin(elapsed * (0.52 + motionRecipe.floatFrequency)) *
        geometryRecipe.deformation *
        (degraded ? 0.04 : 0.08);
    group.scale.setScalar(sceneSpec.scale * pulse);
  });

  const clonedScene = useMemo(() => gltf.scene.clone(), [gltf.scene]);

  useEffect(() => {
    clonedScene.traverse((child) => {
      if (child instanceof THREE.Mesh && child.material) {
        if (child.material instanceof THREE.MeshPhysicalMaterial || child.material instanceof THREE.MeshStandardMaterial) {
          child.material.envMapIntensity = 1.0;
        }
      }
    });
  }, [clonedScene]);

  return <primitive ref={groupRef} object={clonedScene} />;
}

function ArtifactScene({
  artifact,
  diagnosticsEnabled,
  runtimeDiagnostics,
  sceneTone,
}: {
  artifact: ArtifactManifest;
  diagnosticsEnabled: boolean;
  runtimeDiagnostics: ArcRendererDiagnostics;
  sceneTone: "dark" | "paper";
}) {
  const environmentRecipe = artifact.shapeDNA.environment;
  const sceneSpec = sceneSpecForProfile(
    runtimeDiagnostics.effectiveProfile ?? artifact.renderProfile,
  );
  const degraded = runtimeDiagnostics.effectiveProfile === "DEGRADED";
  const backgroundColor = sceneTone === "paper" ? "#f4f1ec" : "#000000";
  const fogColor = sceneTone === "paper" ? "#ebe6df" : "#000000";
  const ambientBase = sceneTone === "paper" ? (degraded ? 0.68 : 0.86) : degraded ? 0.52 : 0.7;
  const directionalBase =
    sceneTone === "paper" ? (degraded ? 0.88 : 1.18) : degraded ? 0.72 : 1.1;
  const pointBase = sceneTone === "paper" ? (degraded ? 0.58 : 0.94) : degraded ? 0.42 : 0.8;
  const modelPath = artifact.outputs.modelPath;

  return (
    <>
      <color attach="background" args={[backgroundColor]} />
      <fog attach="fog" args={[fogColor, 4, sceneSpec.fogFar]} />
      <ambientLight intensity={ambientBase * environmentRecipe.hdriIntensity} />
      <directionalLight
        position={[3.4, 3.6, 4.8]}
        intensity={directionalBase * environmentRecipe.hdriIntensity}
        color={artifact.shapeDNA.material.colorRim}
      />
      <pointLight
        position={[-3.6, -2.4, 2.2]}
        intensity={pointBase}
        color={artifact.shapeDNA.material.colorB}
      />
      {modelPath && !degraded ? (
        <Suspense fallback={<ArtifactMesh artifact={artifact} diagnostics={runtimeDiagnostics} />}>
          <BlenderMesh modelPath={modelPath} artifact={artifact} diagnostics={runtimeDiagnostics} />
        </Suspense>
      ) : (
        <ArtifactMesh artifact={artifact} diagnostics={runtimeDiagnostics} />
      )}
      {diagnosticsEnabled && (
        <group position={[0, -1.85, 0]}>
          <mesh>
            <planeGeometry args={[2.4, 0.24]} />
            <meshBasicMaterial
              color={artifact.shapeDNA.material.colorRim}
              transparent
              opacity={0.08}
            />
          </mesh>
        </group>
      )}
    </>
  );
}

function EmptyArtifactLayer() {
  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        background:
          "radial-gradient(circle at 50% 42%, rgba(255,255,255,0.05), transparent 42%)",
      }}
    />
  );
}

function DiagnosticsOverlay({
  diagnostics,
}: {
  diagnostics: ArcRendererDiagnostics;
}) {
  return (
    <div
      style={{
        position: "absolute",
        left: 16,
        bottom: 16,
        zIndex: 2,
        padding: "10px 12px",
        borderRadius: 12,
        border: "1px solid rgba(255,255,255,0.12)",
        background: "rgba(0,0,0,0.4)",
        color: "rgba(255,255,255,0.76)",
        fontFamily: "monospace",
        fontSize: 11,
        lineHeight: 1.45,
        letterSpacing: "0.01em",
      }}
    >
      <div>{diagnostics.deviceTier}</div>
      <div>{diagnostics.requestedProfile} -&gt; {diagnostics.effectiveProfile}</div>
      <div>reduced_motion={String(diagnostics.prefersReducedMotion)}</div>
      <div>dpr={diagnostics.pixelRatio.toFixed(2)}</div>
    </div>
  );
}

export const AgentRenderedShape = memo(function AgentRenderedShape({
  artifact,
  style,
  className,
  diagnostics = false,
  onDiagnostics,
  sceneTone = "dark",
}: AgentRenderedShapeProps) {
  const hints = useRendererDeviceHints();
  const webglSupported = useMemo(() => detectWebGLSupport(), []);

  const runtimeSnapshot = useMemo(
    () => resolveRendererRuntimeSnapshot(artifact, hints),
    [artifact, hints],
  );
  const showDiagnostics = shouldShowRendererDiagnostics(diagnostics, {
    nodeEnv: process.env.NODE_ENV,
  });

  useEffect(() => {
    if (onDiagnostics) {
      onDiagnostics(runtimeSnapshot.diagnostics);
    }
  }, [onDiagnostics, runtimeSnapshot]);

  if (!runtimeSnapshot.artifact || !runtimeSnapshot.sceneSpec || !webglSupported) {
    return <EmptyArtifactLayer />;
  }

  return (
    <div
      className={className}
      style={{
        position: "absolute",
        inset: 0,
        pointerEvents: "none",
        ...style,
      }}
    >
      <Canvas
        dpr={runtimeSnapshot.sceneSpec.dpr}
        gl={{ alpha: true, antialias: true, powerPreference: "high-performance" }}
        camera={{ position: [0, 0, runtimeSnapshot.sceneSpec.cameraZ], fov: 34 }}
      >
        <ArtifactScene
          artifact={runtimeSnapshot.artifact}
          diagnosticsEnabled={showDiagnostics}
          runtimeDiagnostics={runtimeSnapshot.diagnostics}
          sceneTone={sceneTone}
        />
      </Canvas>
      {showDiagnostics && runtimeSnapshot.diagnostics.renderable && (
        <DiagnosticsOverlay diagnostics={runtimeSnapshot.diagnostics} />
      )}
    </div>
  );
});

export type {
  ArcRendererDiagnostics,
  RendererDeviceHints,
  RendererDeviceTier,
} from "./runtime";
export {
  buildRendererDiagnostics,
  detectRendererDeviceTier,
  resolveEffectiveRenderProfile,
  resolveRendererRuntimeSnapshot,
  sceneSpecForProfile,
  shouldShowRendererDiagnostics,
} from "./runtime";
