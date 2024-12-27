import { CommonModule } from '@angular/common';
import { Component, OnInit, ViewChild, ElementRef, NgZone } from '@angular/core';
import { Sample } from '../../models/sample.model';
import { AudioService } from '../../services/audio.service';

@Component({
  selector: 'app-sampler',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="sampler-container">
      <div class="file-upload">
        <input type="file" (change)="onFileSelected($event)" accept="audio/*">
      </div>

      <div class="waveform-container" #waveformContainer
           (mousedown)="onWaveformClick($event)"
           (mousemove)="onWaveformMove($event)"
           (mouseup)="onWaveformRelease()">
        <canvas #waveformCanvas></canvas>
        <div class="playhead" [style.left.px]="playheadPosition"></div>
        <div class="marker start-marker" [style.left.px]="startMarkerPosition"></div>
        <div class="marker end-marker" [style.left.px]="endMarkerPosition"></div>
        <div class="time-markers">
          <span>{{currentTime | number:'1.2-2'}}s</span>
          <span>{{duration | number:'1.2-2'}}s</span>
        </div>
      </div>

      <div class="controls">
        <button (click)="togglePlay()" [disabled]="!audioBuffer">
          {{isPlaying ? 'Pause' : 'Play'}}
        </button>
        <button (click)="setStartMarker()" [disabled]="!audioBuffer">
          Set Start ({{currentStartTime | number:'1.2-2'}}s)
        </button>
        <button (click)="setEndMarker()" [disabled]="!audioBuffer">
          Set End ({{currentEndTime | number:'1.2-2'}}s)
        </button>
        <button (click)="saveSample()" [disabled]="!canSave()">
          Save Sample
        </button>
      </div>

      <div class="samples-list">
        <h3>Saved Samples</h3>
        <div class="sample-item" *ngFor="let sample of samples">
          <div class="sample-info">
            <span class="sample-name">{{sample.name}}</span>
            <span class="sample-duration">
              {{(sample.endTime - sample.startTime) | number:'1.2-2'}}s
            </span>
          </div>
          <button (click)="playSample(sample)">Play</button>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .sampler-container {
      padding: 20px;
      max-width: 800px;
      margin: 0 auto;
      font-family: Arial, sans-serif;
    }

    .file-upload {
      margin-bottom: 20px;
    }

    .waveform-container {
      position: relative;
      margin: 20px 0;
      border: 1px solid #ccc;
      height: 200px;
      cursor: pointer;
    }

    canvas {
      width: 100%;
      height: 100%;
    }

    .playhead {
      position: absolute;
      top: 0;
      width: 2px;
      height: 100%;
      background-color: #ff0000;
      pointer-events: none;
    }

    .marker {
      position: absolute;
      top: 0;
      width: 2px;
      height: 100%;
      pointer-events: none;
    }

    .start-marker {
      background-color: #00ff00;
    }

    .end-marker {
      background-color: #0000ff;
    }

    .controls {
      display: flex;
      gap: 10px;
      margin: 20px 0;
    }

    button {
      padding: 8px 16px;
      background-color: #2196F3;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }

    button:disabled {
      background-color: #ccc;
      cursor: not-allowed;
    }

    .samples-list {
      margin-top: 20px;
    }

    .sample-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 10px;
      border-bottom: 1px solid #eee;
    }

    .sample-info {
      display: flex;
      flex-direction: column;
    }

    .sample-name {
      font-weight: bold;
    }

    .sample-duration {
      color: #666;
      font-size: 0.9em;
    }
  `]
})
export class SamplerComponent implements OnInit {
  @ViewChild('waveformCanvas') waveformCanvas: ElementRef<HTMLCanvasElement>;

  audioBuffer: AudioBuffer | null = null;
  isPlaying = false;
  currentStartTime = 0;
  currentEndTime = 0;
  currentTime = 0;
  duration = 0;
  samples: Sample[] = [];
  playheadPosition = 0;
  startMarkerPosition = 0;
  endMarkerPosition = 0;
  private animationFrameId: number | null = null;
  private dragStart: number | null = null;
  private startTime = 0;

  constructor(
    private audioService: AudioService,
    private ngZone: NgZone
  ) {}

  ngOnInit() {
    // Inicialização do componente
  }

  async onFileSelected(event: Event) {
    const file = (event.target as HTMLInputElement).files?.[0];
    if (file) {
      this.audioBuffer = await this.audioService.loadAudioFile(file);
      this.duration = this.audioBuffer.duration;
      this.currentEndTime = this.duration;
      this.endMarkerPosition = this.waveformCanvas.nativeElement.width;
      this.drawWaveform();
    }
  }

  drawWaveform() {
    if (!this.audioBuffer) return;

    const canvas = this.waveformCanvas.nativeElement;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;
    const data = this.audioBuffer.getChannelData(0);

    // Configurar canvas para resolução adequada
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    ctx.scale(dpr, dpr);

    // Limpar canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Configurar estilo
    ctx.strokeStyle = '#2196F3';
    ctx.lineWidth = 1;

    // Desenhar forma de onda
    const step = Math.ceil(data.length / canvas.width);
    const amp = canvas.height / 2;

    ctx.beginPath();
    for (let i = 0; i < canvas.width; i++) {
      let min = 1.0;
      let max = -1.0;

      for (let j = 0; j < step; j++) {
        const datum = data[(i * step) + j];
        if (datum < min) min = datum;
        if (datum > max) max = datum;
      }

      ctx.moveTo(i, (1 + min) * amp);
      ctx.lineTo(i, (1 + max) * amp);
    }
    ctx.stroke();
  }

  togglePlay() {
    if (!this.audioBuffer) return;

    if (this.isPlaying) {
      this.stopPlayback();
    } else {
      this.startPlayback();
    }
  }

  startPlayback() {
    if (!this.audioBuffer) return;

    this.isPlaying = true;
    this.startTime = performance.now();
    this.audioService.playBuffer(this.audioBuffer, this.currentTime);
    this.animatePlayhead();
  }

  stopPlayback() {
    this.isPlaying = false;
    this.audioService.stopPlayback();
    if (this.animationFrameId !== null) {
      cancelAnimationFrame(this.animationFrameId);
      this.animationFrameId = null;
    }
  }

  animatePlayhead() {
    const animate = () => {
      if (!this.isPlaying) return;

      const elapsed = (performance.now() - this.startTime) / 1000;
      this.currentTime = this.currentStartTime + elapsed;

      if (this.currentTime >= this.duration) {
        this.stopPlayback();
        this.currentTime = 0;
      } else {
        this.updatePlayheadPosition();
        this.animationFrameId = requestAnimationFrame(animate);
      }
    };

    this.ngZone.runOutsideAngular(() => {
      this.animationFrameId = requestAnimationFrame(animate);
    });
  }

  updatePlayheadPosition() {
    const canvas = this.waveformCanvas.nativeElement;
    this.playheadPosition = (this.currentTime / this.duration) * canvas.width;
  }

  onWaveformClick(event: MouseEvent) {
    if (!this.audioBuffer) return;

    const rect = this.waveformCanvas.nativeElement.getBoundingClientRect();
    const x = event.clientX - rect.left;
    this.currentTime = (x / rect.width) * this.duration;
    this.updatePlayheadPosition();
    this.dragStart = x;
  }

  onWaveformMove(event: MouseEvent) {
    if (this.dragStart === null) return;

    const rect = this.waveformCanvas.nativeElement.getBoundingClientRect();
    const x = event.clientX - rect.left;
    this.currentTime = (x / rect.width) * this.duration;
    this.updatePlayheadPosition();
  }

  onWaveformRelease() {
    this.dragStart = null;
  }

  setStartMarker() {
    this.currentStartTime = this.currentTime;
    this.startMarkerPosition = this.playheadPosition;
  }

  setEndMarker() {
    this.currentEndTime = this.currentTime;
    this.endMarkerPosition = this.playheadPosition;
  }

  async saveSample() {
    if (!this.audioBuffer || !this.canSave()) return;

    const cutBuffer = await this.audioService.cutSample(
      this.audioBuffer,
      this.currentStartTime,
      this.currentEndTime
    );

    const sample: Sample = {
      id: `sample_${Date.now()}`,
      name: `Sample ${this.samples.length + 1}`,
      startTime: this.currentStartTime,
      endTime: this.currentEndTime,
      buffer: cutBuffer,
      createdAt: new Date()
    };

    this.audioService.saveSample(sample);
    this.samples = this.audioService.getSamples();
  }

  playSample(sample: Sample) {
    this.audioService.playBuffer(sample.buffer);
  }

  canSave(): boolean {
    return this.currentStartTime < this.currentEndTime;
  }
}
