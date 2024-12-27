export interface Sample {
  id: string;
  name: string;
  startTime: number;
  endTime: number;
  buffer: AudioBuffer;
  createdAt: Date;
}
