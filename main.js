/*
  Criador de loops: movimento circular com mola torsional, amortecimento e inércia.
  - A posição angular do objeto (theta) segue uma referência periódica phi(t) = w0 * t
  - Dinâmica: I * theta_ddot = -k_eff * erro - c * (theta_dot - w0)
  - k_eff usa um termo de amolecimento dependente da velocidade relativa
  - Gera frames de um período no regime permanente para garantir loop sem emendas
*/

// Utilidades matemáticas
function wrapToPi(angle) {
  let a = ((angle + Math.PI) % (2 * Math.PI));
  if (a < 0) a += 2 * Math.PI;
  return a - Math.PI;
}

function lerp(a, b, t) {
  return a + (b - a) * t;
}

// Conversão de parâmetros de UI -> físicos
function computeDampingFromFluidity(k, I, fluidity01) {
  const clamped = Math.min(1, Math.max(0, fluidity01));
  // Mapear para razão de amortecimento zeta em [0.1, 2.0]
  const zeta = lerp(0.1, 2.0, clamped);
  const cCrit = 2 * Math.sqrt(Math.max(1e-9, k) * Math.max(1e-9, I));
  return zeta * cCrit;
}

class PhysicsLoopGenerator {
  constructor() {
    this.state = {
      theta: 0,
      thetaDot: 0,
      time: 0,
    };
  }

  reset(theta = 0, thetaDot = 0, time = 0) {
    this.state.theta = theta;
    this.state.thetaDot = thetaDot;
    this.state.time = time;
  }

  // Integra um pequeno passo de tempo dt
  step(dt, params) {
    const { I, k, c, w0, softness } = params;
    const time = this.state.time + dt;

    // Ângulo de referência (âncora do acoplamento mola/amortecedor)
    const phi = w0 * time;

    // Erro angular embrulhado (-pi..pi) e velocidade relativa
    const error = wrapToPi(this.state.theta - phi);
    const relVel = this.state.thetaDot - w0;

    // Amolecimento: reduz k conforme cresce a velocidade relativa
    const kEff = k / (1 + softness * Math.abs(relVel));

    // Torque resultante e aceleração angular
    const torque = -kEff * error - c * relVel;
    const thetaDDot = torque / Math.max(1e-9, I);

    // Integração semi-implícita (estável p/ dt pequeno)
    const thetaDot = this.state.thetaDot + thetaDDot * dt;
    const theta = this.state.theta + thetaDot * dt;

    this.state.theta = theta;
    this.state.thetaDot = thetaDot;
    this.state.time = time;
  }

  // Simula até regime permanente e coleta exatamente um período em N amostras
  generateFrames(input) {
    const {
      durationSec,
      numFrames,
      radiusPx,
      inertia,
      stiffness,
      fluidity01,
      softness01,
      warmupPeriods,
      canvasCenter,
    } = input;

    const w0 = (2 * Math.PI) / Math.max(1e-6, durationSec);
    const c = computeDampingFromFluidity(stiffness, inertia, fluidity01);
    const params = { I: inertia, k: stiffness, c, w0, softness: softness01 };

    // Escolha de dt: pequeno o suficiente p/ estabilidade e suavidade
    const targetFps = 240;
    const dt1 = 1 / targetFps;
    const dt2 = durationSec / (numFrames * 8);
    const dt = Math.min(dt1, dt2);

    // Aquecimento
    this.reset(0, 0, 0);
    const warmupTime = durationSec * Math.max(0, warmupPeriods);
    let t = 0;
    while (t < warmupTime) {
      const stepDt = Math.min(dt, warmupTime - t);
      this.step(stepDt, params);
      t += stepDt;
    }

    // Reiniciar o tempo da referência sem mexer no estado relativo
    const theta0 = this.state.theta;
    const thetaDot0 = this.state.thetaDot;
    this.reset(theta0, thetaDot0, 0);

    // Coleta um período
    const frames = [];
    const T = durationSec;
    const sampleTimes = [];
    for (let i = 0; i < numFrames; i++) {
      sampleTimes.push((i / numFrames) * T);
    }

    // Integra e amostra com busca do ponto de amostragem seguinte
    let currentSampleIndex = 0;
    let accumulatedTime = 0;
    const centerX = canvasCenter.x;
    const centerY = canvasCenter.y;

    while (currentSampleIndex < sampleTimes.length) {
      const nextSampleTime = sampleTimes[currentSampleIndex];
      const stepDt = Math.min(dt, nextSampleTime - accumulatedTime);

      if (stepDt > 1e-9) {
        this.step(stepDt, params);
        accumulatedTime += stepDt;
        continue;
      }

      const theta = this.state.theta;
      const x = centerX + radiusPx * Math.cos(theta);
      const y = centerY + radiusPx * Math.sin(theta);
      frames.push({
        t: nextSampleTime,
        theta,
        x,
        y,
      });
      currentSampleIndex += 1;
    }

    // Para CSS, adicionamos ponto de 100% idêntico ao 0%
    const thetaFirst = frames[0].theta;
    const xFirst = frames[0].x;
    const yFirst = frames[0].y;
    const cssFrames = frames.slice();
    cssFrames.push({ t: T, theta: thetaFirst, x: xFirst, y: yFirst });

    return { frames, cssFrames, params, T };
  }
}

// UI e Preview
const els = {
  duration: document.getElementById('duration'),
  frames: document.getElementById('frames'),
  radius: document.getElementById('radius'),
  inertia: document.getElementById('inertia'),
  stiffness: document.getElementById('stiffness'),
  fluidity: document.getElementById('fluidity'),
  fluidityValue: document.getElementById('fluidityValue'),
  softness: document.getElementById('softness'),
  softnessValue: document.getElementById('softnessValue'),
  warmup: document.getElementById('warmup'),
  canvas: document.getElementById('preview'),
  btnGenerate: document.getElementById('btn-generate'),
  btnPlay: document.getElementById('btn-play'),
  btnExportCss: document.getElementById('btn-export-css'),
  btnExportJson: document.getElementById('btn-export-json'),
  output: document.getElementById('output'),
  readoutTime: document.getElementById('readout-time'),
  readoutTheta: document.getElementById('readout-theta'),
};

const ctx = els.canvas.getContext('2d');
const center = { x: els.canvas.width / 2, y: els.canvas.height / 2 };
const generator = new PhysicsLoopGenerator();

let lastGenerated = null;
let isPlaying = true;
let playTime = 0; // 0..T

function getParamsFromUI() {
  const durationSec = Math.max(0.05, parseFloat(els.duration.value || '2'));
  const numFrames = Math.max(3, parseInt(els.frames.value || '60', 10));
  const radiusPx = Math.max(1, parseFloat(els.radius.value || '120'));
  const inertia = Math.max(0.0001, parseFloat(els.inertia.value || '1'));
  const stiffness = Math.max(0.0001, parseFloat(els.stiffness.value || '20'));
  const fluidity01 = Math.min(1, Math.max(0, parseFloat(els.fluidity.value || '0.8')));
  const softness01 = Math.min(1, Math.max(0, parseFloat(els.softness.value || '0.3')));
  const warmupPeriods = Math.max(0, parseInt(els.warmup.value || '6', 10));

  return {
    durationSec,
    numFrames,
    radiusPx,
    inertia,
    stiffness,
    fluidity01,
    softness01,
    warmupPeriods,
    canvasCenter: center,
  };
}

function drawBackground(radiusPx) {
  ctx.clearRect(0, 0, els.canvas.width, els.canvas.height);

  // Grade leve
  ctx.save();
  ctx.strokeStyle = 'rgba(120, 140, 200, 0.1)';
  ctx.lineWidth = 1;
  const step = 50;
  for (let x = step; x < els.canvas.width; x += step) {
    ctx.beginPath();
    ctx.moveTo(x + 0.5, 0);
    ctx.lineTo(x + 0.5, els.canvas.height);
    ctx.stroke();
  }
  for (let y = step; y < els.canvas.height; y += step) {
    ctx.beginPath();
    ctx.moveTo(0, y + 0.5);
    ctx.lineTo(els.canvas.width, y + 0.5);
    ctx.stroke();
  }
  ctx.restore();

  // Círculo de trajetória
  ctx.beginPath();
  ctx.arc(center.x, center.y, radiusPx, 0, 2 * Math.PI);
  ctx.strokeStyle = 'rgba(122, 162, 255, 0.5)';
  ctx.lineWidth = 2;
  ctx.stroke();
}

function drawFrame(frame) {
  drawBackground(parseFloat(els.radius.value || '120'));

  // Sombra do objeto
  ctx.beginPath();
  ctx.arc(frame.x + 6, frame.y + 6, 12, 0, 2 * Math.PI);
  ctx.fillStyle = 'rgba(0, 0, 0, 0.25)';
  ctx.fill();

  // Objeto
  const gradient = ctx.createRadialGradient(frame.x - 6, frame.y - 6, 6, frame.x, frame.y, 14);
  gradient.addColorStop(0, '#55d3c8');
  gradient.addColorStop(1, '#1e265f');
  ctx.beginPath();
  ctx.arc(frame.x, frame.y, 12, 0, 2 * Math.PI);
  ctx.fillStyle = gradient;
  ctx.fill();
}

function renderPlay(timeSec) {
  if (!lastGenerated) return;
  const { cssFrames, T } = lastGenerated;
  const t = timeSec % T;

  // Encontrar intervalo [i, i+1]
  let i = 0;
  while (i + 1 < cssFrames.length && cssFrames[i + 1].t < t) i++;
  const a = cssFrames[i];
  const b = cssFrames[(i + 1) % cssFrames.length];
  const span = (b.t >= a.t) ? (b.t - a.t) : ((T - a.t) + b.t);
  const tt = span > 0 ? ((t - a.t + (a.t <= t ? 0 : T)) / span) : 0;

  const x = lerp(a.x, b.x, tt);
  const y = lerp(a.y, b.y, tt);
  const theta = lerp(a.theta, b.theta, tt);

  drawFrame({ x, y, theta });
  els.readoutTime.textContent = `t=${t.toFixed(2)}s`;
  els.readoutTheta.textContent = `θ=${theta.toFixed(2)} rad`;
}

function updateOutputCSS() {
  if (!lastGenerated) return;
  const { cssFrames, T } = lastGenerated;
  const name = 'loopCircularElastico';
  const durationMs = Math.round(T * 1000);

  const keyframes = cssFrames.map((f, idx) => {
    const pct = (100 * (f.t / T));
    const x = f.x - center.x;
    const y = f.y - center.y;
    const pcStr = idx === cssFrames.length - 1 ? '100%' : `${pct.toFixed(5)}%`;
    return `  ${pcStr} { transform: translate(${x.toFixed(3)}px, ${y.toFixed(3)}px); }`;
  }).join('\n');

  const css = `@keyframes ${name} {\n${keyframes}\n}\n\n/* Uso sugerido: */\n.mover {\n  animation: ${name} ${durationMs}ms linear infinite;\n  will-change: transform;\n}`;

  els.output.value = css;
}

function updateOutputJSON() {
  if (!lastGenerated) return;
  const { frames, params, T } = lastGenerated;
  const payload = {
    meta: {
      generator: 'loop-circular-elastico',
      version: 1,
      durationSec: T,
      center,
    },
    params,
    frames: frames.map(f => ({ t: Number(f.t.toFixed(6)), x: Number(f.x.toFixed(6)), y: Number(f.y.toFixed(6)), theta: Number(f.theta.toFixed(6)) })),
  };
  els.output.value = JSON.stringify(payload, null, 2);
}

function generate() {
  const p = getParamsFromUI();
  lastGenerated = generator.generateFrames(p);
  playTime = 0;
  updateOutputCSS();
}

function animate(ts) {
  if (animate.prevTs === undefined) animate.prevTs = ts;
  const dt = Math.max(0, Math.min(0.05, (ts - animate.prevTs) / 1000));
  animate.prevTs = ts;
  if (isPlaying && lastGenerated) {
    playTime += dt;
  }
  renderPlay(playTime);
  requestAnimationFrame(animate);
}

// Eventos UI
function wireUI() {
  const syncRangeLabel = (rangeEl, labelEl) => {
    const v = parseFloat(rangeEl.value || '0');
    labelEl.textContent = v.toFixed(2);
  };

  els.fluidity.addEventListener('input', () => syncRangeLabel(els.fluidity, els.fluidityValue));
  els.softness.addEventListener('input', () => syncRangeLabel(els.softness, els.softnessValue));
  syncRangeLabel(els.fluidity, els.fluidityValue);
  syncRangeLabel(els.softness, els.softnessValue);

  els.btnGenerate.addEventListener('click', () => {
    generate();
  });

  els.btnPlay.addEventListener('click', () => {
    isPlaying = !isPlaying;
    els.btnPlay.textContent = isPlaying ? 'Pausar' : 'Tocar';
  });

  els.btnExportCss.addEventListener('click', () => {
    updateOutputCSS();
    els.output.focus();
    els.output.select();
  });

  els.btnExportJson.addEventListener('click', () => {
    updateOutputJSON();
    els.output.focus();
    els.output.select();
  });

  // Regerar ao alterar parâmetros principais
  [els.duration, els.frames, els.radius, els.inertia, els.stiffness, els.fluidity, els.softness, els.warmup]
    .forEach(el => el.addEventListener('change', generate));
}

// Inicialização
wireUI();
generate();
requestAnimationFrame(animate);

