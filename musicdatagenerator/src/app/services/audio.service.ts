import { Injectable } from '@angular/core';
import { Sample } from '../models/sample.model';

@Injectable({
  providedIn: 'root'
})
export class AudioService {
  private audioContext: AudioContext;
  private samples: Sample[] = [];
  private currentSource: AudioBufferSourceNode | null = null;

  constructor() {
    this.audioContext = new AudioContext();
  }

  getSamples(): Sample[] {
    return this.samples;
  }

  saveSample(sample: Sample): void {
    this.samples.push(sample);
  }

  async loadAudioFile(file: File): Promise<AudioBuffer> {
    const arrayBuffer = await file.arrayBuffer();
    return this.audioContext.decodeAudioData(arrayBuffer);
  }

  async cutSample(audioBuffer: AudioBuffer, startTime: number, endTime: number): Promise<AudioBuffer> {
    const sampleLength = endTime - startTime;
    const sampleRate = audioBuffer.sampleRate;
    const channels = audioBuffer.numberOfChannels;

    const newBuffer = this.audioContext.createBuffer(
      channels,
      Math.floor(sampleLength * sampleRate),
      sampleRate
    );

    for (let channel = 0; channel < channels; channel++) {
      const newData = newBuffer.getChannelData(channel);
      const originalData = audioBuffer.getChannelData(channel);

      for (let i = 0; i < newBuffer.length; i++) {
        newData[i] = originalData[i + Math.floor(startTime * sampleRate)];
      }
    }

    return newBuffer;
  }

  playBuffer(buffer: AudioBuffer, startTime: number = 0, endTime?: number): void {
    if (this.currentSource) {
      this.currentSource.stop();
    }

    this.currentSource = this.audioContext.createBufferSource();
    this.currentSource.buffer = buffer;
    this.currentSource.connect(this.audioContext.destination);

    const duration = endTime ? endTime - startTime : buffer.duration - startTime;
    this.currentSource.start(0, startTime, duration);
  }

  stopPlayback(): void {
    if (this.currentSource) {
      this.currentSource.stop();
      this.currentSource = null;
    }
  }
}