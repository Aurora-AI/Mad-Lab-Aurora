/**
 * ARC Stage Telemetry
 * Exposes internal metrics to the window for Chrome DevTools MCP consumption.
 */

export interface TelemetrySnapshot {
  fps: number;
  drawCalls: number;
  triangles: number;
  memory: number;
  assemblyProgress: number;
  status: 'IDLE' | 'ANIMATING' | 'CONVERGED';
  timestamp: number;
}

class TelemetrySystem {
  private static instance: TelemetrySystem;
  private currentSnapshot: TelemetrySnapshot = {
    fps: 0,
    drawCalls: 0,
    triangles: 0,
    memory: 0,
    assemblyProgress: 0,
    status: 'IDLE',
    timestamp: Date.now()
  };

  private constructor() {
    if (typeof window !== 'undefined') {
      (window as any).__AURORA_AUDIT__ = this;
    }
  }

  public static getInstance(): TelemetrySystem {
    if (!TelemetrySystem.instance) {
      TelemetrySystem.instance = new TelemetrySystem();
    }
    return TelemetrySystem.instance;
  }

  public update(snapshot: Partial<TelemetrySnapshot>) {
    this.currentSnapshot = {
      ...this.currentSnapshot,
      ...snapshot,
      timestamp: Date.now()
    };
  }

  public getSnapshot(): TelemetrySnapshot {
    return this.currentSnapshot;
  }

  // Diagnostic method for agents
  public scout(): string {
    return JSON.stringify(this.currentSnapshot, null, 2);
  }
}

export const telemetry = TelemetrySystem.getInstance();
