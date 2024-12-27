import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { SamplerComponent } from './components/sampler/sampler.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, RouterOutlet, SamplerComponent],
  template: `<router-outlet></router-outlet>`
})
export class AppComponent {
  title = 'musicdatagenerator';
}