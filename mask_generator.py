#!/usr/bin/env python3
"""
Mask Generator for Circular Motion Simulator
Generates mask sequences from trajectory patterns with different parameters
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image, ImageDraw
import os
import math
from circular_motion_simulator import CircularMotionSimulator

class MaskGenerator:
    def __init__(self, width=400, height=400, mask_size=50):
        self.width = width
        self.height = height
        self.mask_size = mask_size
        self.center_x = width // 2
        self.center_y = height // 2
        
        # Create output directories
        os.makedirs('masks', exist_ok=True)
        os.makedirs('gifs', exist_ok=True)
        os.makedirs('videos', exist_ok=True)
        
    def create_mask_from_trajectory(self, trajectory_x, trajectory_y, frame_idx, 
                                  mask_type='circular', intensity=1.0):
        """Create a mask image from trajectory data"""
        # Create blank image
        mask = Image.new('L', (self.width, self.height), 0)
        draw = ImageDraw.Draw(mask)
        
        if len(trajectory_x) == 0:
            return mask
            
        # Get current position
        x = trajectory_x[-1]
        y = trajectory_y[-1]
        
        # Convert to image coordinates
        img_x = int(self.center_x + x * 50)  # Scale factor
        img_y = int(self.center_y - y * 50)  # Flip Y axis
        
        # Create mask based on type
        if mask_type == 'circular':
            radius = int(self.mask_size * intensity)
            draw.ellipse([img_x - radius, img_y - radius, 
                         img_x + radius, img_y + radius], 
                        fill=int(255 * intensity))
        elif mask_type == 'square':
            size = int(self.mask_size * intensity)
            draw.rectangle([img_x - size, img_y - size, 
                           img_x + size, img_y + size], 
                          fill=int(255 * intensity))
        elif mask_type == 'trail':
            # Create trail effect
            trail_length = min(20, len(trajectory_x))
            for i in range(max(0, len(trajectory_x) - trail_length), len(trajectory_x)):
                alpha = (i - (len(trajectory_x) - trail_length)) / trail_length
                trail_x = int(self.center_x + trajectory_x[i] * 50)
                trail_y = int(self.center_y - trajectory_y[i] * 50)
                radius = int(self.mask_size * intensity * alpha * 0.3)
                if radius > 0:
                    draw.ellipse([trail_x - radius, trail_y - radius, 
                                 trail_x + radius, trail_y + radius], 
                                fill=int(255 * intensity * alpha))
        
        return mask
    
    def generate_mask_sequence(self, params, duration=5.0, fps=30, mask_type='circular'):
        """Generate a sequence of masks for given parameters"""
        # Create simulator with custom parameters
        simulator = CircularMotionSimulator()
        simulator.elasticity = params['elasticity']
        simulator.damping = params['damping']
        simulator.fluidity = params['fluidity']
        simulator.moment_of_inertia = params['moment_of_inertia']
        simulator.initial_velocity = params['initial_velocity']
        simulator.radius = params['radius']
        
        # Reset simulator
        simulator.reset_simulation(None)
        
        # Generate trajectory
        dt = 1.0 / fps
        total_frames = int(duration * fps)
        trajectory_x = []
        trajectory_y = []
        masks = []
        
        print(f"Generating {total_frames} frames for {mask_type} mask...")
        
        for frame in range(total_frames):
            # Calculate physics
            simulator.calculate_physics(dt)
            
            # Get position
            x, y = simulator.get_position()
            trajectory_x.append(x)
            trajectory_y.append(y)
            
            # Create mask
            intensity = 1.0 - (frame / total_frames) * 0.3  # Fade out slightly
            mask = self.create_mask_from_trajectory(trajectory_x, trajectory_y, frame, 
                                                  mask_type, intensity)
            
            # Save mask
            mask_path = f"masks/{mask_type}_{params['name']}_frame_{frame:04d}.png"
            mask.save(mask_path)
            masks.append(mask_path)
            
            if frame % 30 == 0:
                print(f"Generated frame {frame}/{total_frames}")
        
        return masks, trajectory_x, trajectory_y
    
    def create_gif(self, mask_paths, output_path, duration=100):
        """Create GIF from mask sequence"""
        images = []
        for path in mask_paths:
            if os.path.exists(path):
                img = Image.open(path)
                images.append(img)
        
        if images:
            images[0].save(
                output_path,
                save_all=True,
                append_images=images[1:],
                duration=duration,
                loop=0
            )
            print(f"GIF created: {output_path}")
    
    def create_video(self, mask_paths, output_path, fps=30):
        """Create video from mask sequence using matplotlib"""
        if not mask_paths:
            return
            
        # Create figure
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Load first image
        first_img = Image.open(mask_paths[0])
        im = ax.imshow(first_img, cmap='gray', vmin=0, vmax=255)
        
        def animate(frame):
            if frame < len(mask_paths) and os.path.exists(mask_paths[frame]):
                img = Image.open(mask_paths[frame])
                im.set_array(img)
            return [im]
        
        # Create animation
        anim = animation.FuncAnimation(fig, animate, frames=len(mask_paths), 
                                     interval=1000//fps, blit=True, repeat=True)
        
        # Save as video
        Writer = animation.writers['ffmpeg']
        writer = Writer(fps=fps, metadata=dict(artist='Mask Generator'), bitrate=1800)
        anim.save(output_path, writer=writer)
        plt.close(fig)
        print(f"Video created: {output_path}")

def generate_parameter_sets():
    """Generate different parameter sets for various mask patterns"""
    parameter_sets = [
        {
            'name': 'simple_circle',
            'elasticity': 0.8,
            'damping': 0.01,
            'fluidity': 0.8,
            'moment_of_inertia': 0.5,
            'initial_velocity': 5.0,
            'radius': 2.0,
            'description': 'Simple circular motion with low damping'
        },
        {
            'name': 'complex_loops',
            'elasticity': 0.3,
            'damping': 0.05,
            'fluidity': 0.2,
            'moment_of_inertia': 1.5,
            'initial_velocity': 7.0,
            'radius': 1.5,
            'description': 'Complex loop patterns with high inertia'
        },
        {
            'name': 'spiral_decay',
            'elasticity': 0.6,
            'damping': 0.08,
            'fluidity': 0.9,
            'moment_of_inertia': 0.3,
            'initial_velocity': 6.0,
            'radius': 2.5,
            'description': 'Spiral motion with gradual energy decay'
        },
        {
            'name': 'chaotic_motion',
            'elasticity': 0.4,
            'damping': 0.03,
            'fluidity': 0.4,
            'moment_of_inertia': 0.8,
            'initial_velocity': 8.0,
            'radius': 1.8,
            'description': 'Chaotic motion with medium parameters'
        },
        {
            'name': 'smooth_oscillation',
            'elasticity': 0.9,
            'damping': 0.02,
            'fluidity': 0.95,
            'moment_of_inertia': 0.6,
            'initial_velocity': 4.0,
            'radius': 2.2,
            'description': 'Smooth oscillatory motion'
        }
    ]
    return parameter_sets

def main():
    """Main function to generate all mask sequences"""
    print("Starting Mask Generation Process")
    print("=" * 50)
    
    # Initialize generator
    generator = MaskGenerator()
    
    # Get parameter sets
    param_sets = generate_parameter_sets()
    
    # Mask types to generate
    mask_types = ['circular', 'square', 'trail']
    
    # Generate all combinations
    for params in param_sets:
        print(f"\nProcessing parameter set: {params['name']}")
        print(f"Description: {params['description']}")
        
        for mask_type in mask_types:
            print(f"  Generating {mask_type} masks...")
            
            # Generate mask sequence
            mask_paths, trajectory_x, trajectory_y = generator.generate_mask_sequence(
                params, duration=3.0, fps=20, mask_type=mask_type
            )
            
            # Create GIF
            gif_path = f"gifs/{params['name']}_{mask_type}.gif"
            generator.create_gif(mask_paths, gif_path, duration=100)
            
            # Create video (if ffmpeg is available)
            try:
                video_path = f"videos/{params['name']}_{mask_type}.mp4"
                generator.create_video(mask_paths, video_path, fps=20)
            except Exception as e:
                print(f"    Video creation failed: {e}")
    
    print("\nMask generation completed!")
    print("Generated files:")
    print("- Individual mask frames in 'masks/' directory")
    print("- GIF animations in 'gifs/' directory") 
    print("- Video files in 'videos/' directory")

if __name__ == "__main__":
    main()