"use client";

import { useEffect, useState } from "react";
import FramerSpectacular from "@/components/FramerSpectacular";

export default function Home() {
  const [intenseEnabled, setIntenseEnabled] = useState<boolean>(false);
  const [ack, setAck] = useState<boolean>(false);

  useEffect(() => {
    const saved = localStorage.getItem("your-mind:intense");
    const savedAck = localStorage.getItem("your-mind:ack");
    if (saved) setIntenseEnabled(saved === "1");
    if (savedAck) setAck(savedAck === "1");
  }, []);

  useEffect(() => {
    localStorage.setItem("your-mind:intense", intenseEnabled ? "1" : "0");
    localStorage.setItem("your-mind:ack", ack ? "1" : "0");
  }, [intenseEnabled, ack]);

  return (
    <div className="min-h-screen w-full p-6 sm:p-10 grid gap-6">
      <header className="grid gap-2">
        <h1 className="text-2xl font-extrabold tracking-tight">your-mind-app</h1>
        <p className="text-sm text-slate-400">Projeto baseado em Framer Motion + player de máscaras. Atenção a animações intensas.</p>
      </header>

      <section className="rounded-xl border border-white/10 bg-white/5 p-4 grid gap-3">
        <div className="text-yellow-300 font-bold">Aviso de Segurança</div>
        <p className="text-sm text-yellow-100/90">
          Esta página pode exibir flashes e movimentos rápidos. Use com cautela e evite frequências acima de 3Hz.
          Se você for sensível (ex.: epilepsia fotossensível), mantenha o modo intenso desativado.
        </p>
        <div className="flex items-center gap-3 flex-wrap">
          <label className="flex items-center gap-2">
            <input type="checkbox" checked={ack} onChange={(e) => setAck(e.target.checked)} />
            <span>Li e compreendo o aviso</span>
          </label>
          <label className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={intenseEnabled}
              onChange={(e) => setIntenseEnabled(e.target.checked)}
              disabled={!ack}
            />
            <span>Habilitar animações intensas (pulsos rápidos, flashes)</span>
          </label>
        </div>
      </section>

      <section className="grid gap-3">
        <h2 className="text-lg font-bold">SPA: Animação “Excitantemente Espetacular”</h2>
        <FramerSpectacular enabled={true} intense={ack && intenseEnabled} />
      </section>
    </div>
  );
}
