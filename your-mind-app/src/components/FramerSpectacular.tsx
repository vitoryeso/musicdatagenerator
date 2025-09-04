"use client";

import { motion, useMotionValue, useSpring } from "framer-motion";
import React, { useEffect, useRef, useState } from "react";

type SequenceName =
  | "circular_complex_loops"
  | "square_complex_loops"
  | "trail_complex_loops"
  | "circular_simple_circle"
  | "circular_smooth_oscillation";

type SpectacularProps = {
  enabled?: boolean;
  intense?: boolean;
};

export default function FramerSpectacular({ enabled = true, intense = false }: SpectacularProps) {
  const [sequence, setSequence] = useState<SequenceName>("trail_complex_loops");
  const [fps, setFps] = useState<number>(30);
  const [frames, setFrames] = useState<number>(180); // Movimento mais suave e contemplativo do ∞
  const [loop, setLoop] = useState<boolean>(true);
  const [preload, setPreload] = useState<boolean>(true);
  const [index, setIndex] = useState<number>(0);
  const [playing, setPlaying] = useState<boolean>(true);

  const containerRef = useRef<HTMLDivElement | null>(null);
  const x = useMotionValue(0);
  const y = useMotionValue(0);
  const rotate = useMotionValue(0);
  const scaleX = useMotionValue(1);
  const scaleY = useMotionValue(1);

  // Springs em cadeia para criar rastro (trail) suave - foco nos segmentos próximos à cabeça
  const TRAIL = 12;
  const trail: { x: ReturnType<typeof useSpring>; y: ReturnType<typeof useSpring> }[] = [];
  let prevX = x;
  let prevY = y;
  for (let i = 0; i < TRAIL; i++) {
    // Maior elasticidade e massa para corpo mais responsivo
    const xi = useSpring(prevX, { stiffness: 120, damping: 18, mass: 1.2 });
    const yi = useSpring(prevY, { stiffness: 120, damping: 18, mass: 1.2 });
    trail.push({ x: xi, y: yi });
    prevX = xi;
    prevY = yi;
  }

  function computeLemniscatePoint(w: number, h: number, idx: number) {
    const cx = w / 2;
    const cy = h / 2;
    const base = Math.min(w, h) * 0.35; // Aumentado para símbolo mais proeminente
    const t = (idx / Math.max(1, frames)) * Math.PI * 2; // 0..2π para um loop completo

    // Lemniscata Perfeita de Bernoulli: forma matemática exata do símbolo ∞
    // x = (a * √2 * cos(t)) / (1 + sin²(t))
    // y = (a * √2 * sin(t) * cos(t)) / (1 + sin²(t))
    const a = base;
    const s = Math.sin(t);
    const c = Math.cos(t);
    const s2 = s * s;
    const denom = 1 + s2;

    // Fator √2 para simetria perfeita do símbolo do infinito
    const scaleFactor = Math.sqrt(2);
    let xLocal = (a * scaleFactor * c) / denom;
    let yLocal = (a * scaleFactor * s * c) / denom;

    // Variações por sequência - mantidas sutis para preservar a forma perfeita
    let rot = 0; // rad
    let ampMod = 0;
    switch (sequence) {
      case "square_complex_loops":
        rot = Math.PI / 12; // Rotação mais sutil
        ampMod = 0.04;
        break;
      case "trail_complex_loops":
        rot = 0;
        ampMod = 0.08; // Modulação mais suave
        break;
      case "circular_simple_circle":
        rot = Math.PI / 16;
        ampMod = 0.03;
        break;
      case "circular_smooth_oscillation":
        rot = -Math.PI / 14;
        ampMod = 0.025;
        break;
      default:
        rot = 0;
        ampMod = 0.06;
    }

    // Modulação de amplitude mais suave para preservar a simetria
    const mod = 1 + ampMod * Math.sin(2 * t); // Frequência reduzida
    xLocal *= mod;
    yLocal *= mod;

    // Rotação do caminho - mais sutil
    const xr = xLocal * Math.cos(rot) - yLocal * Math.sin(rot);
    const yr = xLocal * Math.sin(rot) + yLocal * Math.cos(rot);

    return { px: cx + xr, py: cy + yr };
  }

  // Precompute pontos se preload
  const pointsRef = useRef<Array<{ px: number; py: number }>>([]);
  useEffect(() => {
    if (!preload) {
      pointsRef.current = [];
      return;
    }
    const rect = containerRef.current?.getBoundingClientRect();
    const w = rect?.width ?? 800;
    const h = rect?.height ?? 600;
    const arr: Array<{ px: number; py: number }> = [];
    for (let i = 0; i < frames; i++) arr.push(computeLemniscatePoint(w, h, i));
    pointsRef.current = arr;
  }, [preload, sequence, frames]);

  useEffect(() => { setIndex(Math.max(0, Math.min(frames - 1, index))); }, [frames]);

  const idxRef = useRef<number>(0);
  const lastRef = useRef<{ x: number; y: number }>({ x: 0, y: 0 });
  const lastTickRef = useRef<number>(0);

  useEffect(() => {
    if (!enabled) return;
    let raf = 0;

    const tick = (ts: number) => {
      const rect = containerRef.current?.getBoundingClientRect();
      const w = rect?.width ?? 800;
      const h = rect?.height ?? 600;

      // Atualiza índice com base em FPS/loop/playing
      const interval = 1000 / Math.max(1, fps);
      if (playing) {
        if (!lastTickRef.current) lastTickRef.current = ts;
        if (ts - lastTickRef.current >= interval) {
          lastTickRef.current = ts;
          let next = idxRef.current + 1;
          if (next >= frames) {
            if (loop) next = 0; else next = frames - 1;
          }
          idxRef.current = next;
          setIndex(next);
        }
      }

      const idx = idxRef.current;
      let pt = pointsRef.current[idx];
      if (!pt) pt = computeLemniscatePoint(w, h, idx);
      const { px, py } = pt;

      // Atualiza Motion Values
      x.set(px);
      y.set(py);

      // Movimento estritamente 2D - sem cálculo de orientação/rotação
      const last = lastRef.current;
      const vx = px - last.x;
      const vy = py - last.y;

      // Squash & stretch proporcional à velocidade - maior elasticidade horizontal
      const v = Math.hypot(vx, vy);
      const stretch = Math.min(0.8, v / 300) * (intense ? 1.5 : 1.2); // Maior stretch
      scaleX.set(1 + stretch);
      scaleY.set(1 - 0.25 * stretch); // Menos compressão vertical para corpo mais alongado

      lastRef.current = { x: px, y: py };
      raf = requestAnimationFrame(tick);
    };

    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [enabled, intense, sequence, fps, frames, loop, playing, preload, x, y, rotate, scaleX, scaleY]);

  return (
    <div className="grid gap-4">
      {/* Controles */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        <div className="grid gap-1">
          <label className="font-semibold">Sequência</label>
          <select value={sequence} onChange={(e) => setSequence(e.target.value as SequenceName)} className="text-black rounded px-2 py-1">
            <option value="circular_complex_loops">circular_complex_loops</option>
            <option value="square_complex_loops">square_complex_loops</option>
            <option value="trail_complex_loops">trail_complex_loops</option>
            <option value="circular_simple_circle">circular_simple_circle</option>
            <option value="circular_smooth_oscillation">circular_smooth_oscillation</option>
          </select>
        </div>
        <div className="grid gap-1">
          <label className="font-semibold">FPS</label>
          <input type="number" min={1} max={60} value={fps} onChange={(e) => setFps(Number(e.target.value))} className="text-black rounded px-2 py-1" />
        </div>
        <div className="grid gap-1">
          <label className="font-semibold">Frames</label>
          <input type="number" min={1} max={600} value={frames} onChange={(e) => setFrames(Number(e.target.value))} className="text-black rounded px-2 py-1" />
        </div>
        <div className="grid gap-1">
          <label className="font-semibold">Pré-carregar</label>
          <select value={preload ? "1" : "0"} onChange={(e) => setPreload(e.target.value === "1")} className="text-black rounded px-2 py-1">
            <option value="1">Sim</option>
            <option value="0">Não</option>
          </select>
        </div>
        <div className="grid gap-1">
          <label className="font-semibold">Loop</label>
          <select value={loop ? "1" : "0"} onChange={(e) => setLoop(e.target.value === "1")} className="text-black rounded px-2 py-1">
            <option value="1">Sim</option>
            <option value="0">Não</option>
          </select>
        </div>
        <div className="grid gap-1">
          <label className="font-semibold">Índice</label>
          <input type="range" min={0} max={Math.max(0, frames - 1)} value={index} onChange={(e) => { setIndex(Number(e.target.value)); idxRef.current = Number(e.target.value); }} />
        </div>
      </div>

      <div className="flex gap-2 flex-wrap">
        <button className="px-4 py-2 rounded bg-emerald-400 text-emerald-950 font-bold" onClick={() => setPlaying(true)}>Reproduzir</button>
        <button className="px-4 py-2 rounded bg-slate-400 text-slate-900 font-bold" onClick={() => setPlaying(false)}>Pausar</button>
        <button className="px-4 py-2 rounded bg-slate-600 text-white" onClick={() => { setIndex((index - 1 + frames) % frames); idxRef.current = (index - 1 + frames) % frames; }}>Anterior</button>
        <button className="px-4 py-2 rounded bg-slate-600 text-white" onClick={() => { setIndex((index + 1) % frames); idxRef.current = (index + 1) % frames; }}>Próximo</button>
        <button className="px-4 py-2 rounded bg-slate-700 text-white" onClick={() => { setIndex(0); idxRef.current = 0; }}>Reiniciar</button>
      </div>

      {/* Canvas da animação */}
      <div ref={containerRef} className="relative w-full h-[70vh] overflow-hidden rounded-2xl bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
        {/* Fundo animado piscante */}
        <motion.div
          aria-hidden
          className="absolute inset-0"
          animate={{
            background: [
              "radial-gradient(1000px 800px at 50% 50%, #0ea5e9 0%, rgba(14,165,233,0.3) 40%, rgba(14,165,233,0) 80%)",
              "radial-gradient(1200px 1000px at 50% 50%, #0ea5e9 0%, rgba(14,165,233,0.6) 30%, rgba(14,165,233,0) 70%)",
              "radial-gradient(1000px 800px at 50% 50%, #0ea5e9 0%, rgba(14,165,233,0.3) 40%, rgba(14,165,233,0) 80%)",
            ],
            opacity: [0.8, 1, 0.8],
          }}
          transition={{
            background: { duration: 2, ease: "easeInOut", repeat: Infinity },
            opacity: { duration: 1.5, ease: "easeInOut", repeat: Infinity }
          }}
        />

        {/* Corpo da minhoca: apenas segmentos próximos à cabeça com opacidade alta */}
        {trail.slice(0, 8).map((mv, i) => (
          <motion.div
            key={i}
            className="absolute rounded-full"
            style={{
              x: mv.x,
              y: mv.y,
              width: 18,
              height: 18,
              marginLeft: -9,
              marginTop: -9,
              // Movimento estritamente 2D - sem rotação
              background: intense
                ? `rgba(239, 68, 68, ${Math.max(0.6, 0.95 - i * 0.02)})` // Opacidade maior
                : `rgba(34, 197, 94, ${Math.max(0.6, 0.95 - i * 0.02)})`,
              boxShadow: `0 0 10px ${intense ? 'rgba(239, 68, 68, 0.8)' : 'rgba(34, 197, 94, 0.8)'}`,
              border: "1px solid rgba(255,255,255,0.15)",
            }}
            aria-hidden
          />
        ))}

        {/* Cabeça da minhoca (elemento principal) - movimento estritamente 2D */}
        <motion.div
          className="absolute rounded-full shadow-2xl border border-white/10"
          style={{
            x,
            y,
            // Removida rotação para movimento estritamente 2D
            scaleX,
            scaleY,
            width: 26,
            height: 26,
            marginLeft: -13,
            marginTop: -13,
            background: intense
              ? "linear-gradient(to right, #ef4444, #dc2626)"
              : "linear-gradient(to right, #22c55e, #16a34a)",
            boxShadow: intense
              ? "0 0 20px rgba(239,68,68,0.8), 0 0 40px rgba(239,68,68,0.4)"
              : "0 0 15px rgba(34,197,94,0.8), 0 0 30px rgba(34,197,94,0.4)",
          }}
          whileHover={{ scaleX: 1.2, scaleY: 0.9 }}
          whileTap={{ x: [-8, 8, -8, 8], transition: { duration: 0.12 } }}
        />
      </div>
    </div>
  );
}


