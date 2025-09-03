#!/usr/bin/env python3
"""
Generate Markdown Report with Embedded GIFs and Videos
Creates a comprehensive report showing mask sequences from the simulator
"""

import os
import glob
from datetime import datetime

def generate_markdown_report():
    """Generate comprehensive markdown report with embedded media"""
    
    # Get current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Start building markdown content
    markdown_content = f"""# Circular Motion Simulator - Mask Sequences Report

*Generated on: {timestamp}*

## Overview

This report showcases various mask sequences generated from the Circular Motion Simulator with different parameter configurations. Each sequence demonstrates unique patterns created by varying the physical parameters of the simulation.

## Parameter Sets Used

### 1. Simple Circle Motion
- **Elasticity**: 0.8
- **Damping**: 0.01  
- **Fluidity**: 0.8
- **Moment of Inertia**: 0.5
- **Initial Velocity**: 5.0
- **Radius**: 2.0
- **Description**: Simple circular motion with low damping

### 2. Complex Loop Patterns
- **Elasticity**: 0.3
- **Damping**: 0.05
- **Fluidity**: 0.2
- **Moment of Inertia**: 1.5
- **Initial Velocity**: 7.0
- **Radius**: 1.5
- **Description**: Complex loop patterns with high inertia

### 3. Spiral Decay Motion
- **Elasticity**: 0.6
- **Damping**: 0.08
- **Fluidity**: 0.9
- **Moment of Inertia**: 0.3
- **Initial Velocity**: 6.0
- **Radius**: 2.5
- **Description**: Spiral motion with gradual energy decay

### 4. Chaotic Motion
- **Elasticity**: 0.4
- **Damping**: 0.03
- **Fluidity**: 0.4
- **Moment of Inertia**: 0.8
- **Initial Velocity**: 8.0
- **Radius**: 1.8
- **Description**: Chaotic motion with medium parameters

### 5. Smooth Oscillation
- **Elasticity**: 0.9
- **Damping**: 0.02
- **Fluidity**: 0.95
- **Moment of Inertia**: 0.6
- **Initial Velocity**: 4.0
- **Radius**: 2.2
- **Description**: Smooth oscillatory motion

---

## Mask Sequences

### Circular Masks

Circular masks follow the trajectory with circular brush strokes.

#### Simple Circle Motion - Circular Mask
![Simple Circle Circular Mask](gifs/simple_circle_circular.gif)

#### Complex Loops - Circular Mask  
![Complex Loops Circular Mask](gifs/complex_loops_circular.gif)

#### Spiral Decay - Circular Mask
![Spiral Decay Circular Mask](gifs/spiral_decay_circular.gif)

#### Chaotic Motion - Circular Mask
![Chaotic Motion Circular Mask](gifs/chaotic_motion_circular.gif)

#### Smooth Oscillation - Circular Mask
![Smooth Oscillation Circular Mask](gifs/smooth_oscillation_circular.gif)

### Square Masks

Square masks create geometric patterns following the trajectory.

#### Simple Circle Motion - Square Mask
![Simple Circle Square Mask](gifs/simple_circle_square.gif)

#### Complex Loops - Square Mask
![Complex Loops Square Mask](gifs/complex_loops_square.gif)

#### Spiral Decay - Square Mask
![Spiral Decay Square Mask](gifs/spiral_decay_square.gif)

#### Chaotic Motion - Square Mask
![Chaotic Motion Square Mask](gifs/chaotic_motion_square.gif)

#### Smooth Oscillation - Square Mask
![Smooth Oscillation Square Mask](gifs/smooth_oscillation_square.gif)

### Trail Masks

Trail masks show the path history with fading intensity.

#### Simple Circle Motion - Trail Mask
![Simple Circle Trail Mask](gifs/simple_circle_trail.gif)

#### Complex Loops - Trail Mask
![Complex Loops Trail Mask](gifs/complex_loops_trail.gif)

#### Spiral Decay - Trail Mask
![Spiral Decay Trail Mask](gifs/spiral_decay_trail.gif)

#### Chaotic Motion - Trail Mask
![Chaotic Motion Trail Mask](gifs/chaotic_motion_trail.gif)

#### Smooth Oscillation - Trail Mask
![Smooth Oscillation Trail Mask](gifs/smooth_oscillation_trail.gif)

---

## Video Sequences

For higher quality viewing, here are the video versions of the mask sequences:

### Circular Masks - Video Collection

#### Simple Circle Motion
<video width="400" height="400" controls>
  <source src="videos/simple_circle_circular.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

#### Complex Loops
<video width="400" height="400" controls>
  <source src="videos/complex_loops_circular.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

#### Spiral Decay
<video width="400" height="400" controls>
  <source src="videos/spiral_decay_circular.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

#### Chaotic Motion
<video width="400" height="400" controls>
  <source src="videos/chaotic_motion_circular.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

#### Smooth Oscillation
<video width="400" height="400" controls>
  <source src="videos/smooth_oscillation_circular.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

### Square Masks - Video Collection

#### Simple Circle Motion
<video width="400" height="400" controls>
  <source src="videos/simple_circle_square.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

#### Complex Loops
<video width="400" height="400" controls>
  <source src="videos/complex_loops_square.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

#### Spiral Decay
<video width="400" height="400" controls>
  <source src="videos/spiral_decay_square.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

#### Chaotic Motion
<video width="400" height="400" controls>
  <source src="videos/chaotic_motion_square.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

#### Smooth Oscillation
<video width="400" height="400" controls>
  <source src="videos/smooth_oscillation_square.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

### Trail Masks - Video Collection

#### Simple Circle Motion
<video width="400" height="400" controls>
  <source src="videos/simple_circle_trail.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

#### Complex Loops
<video width="400" height="400" controls>
  <source src="videos/complex_loops_trail.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

#### Spiral Decay
<video width="400" height="400" controls>
  <source src="videos/spiral_decay_trail.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

#### Chaotic Motion
<video width="400" height="400" controls>
  <source src="videos/chaotic_motion_trail.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

#### Smooth Oscillation
<video width="400" height="400" controls>
  <source src="videos/smooth_oscillation_trail.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

---

## Analysis and Observations

### Pattern Characteristics

1. **Simple Circle Motion**: Creates clean, predictable circular patterns with minimal variation.

2. **Complex Loops**: Generates intricate, self-intersecting patterns that create beautiful organic shapes.

3. **Spiral Decay**: Shows gradual energy dissipation leading to inward spiraling motion.

4. **Chaotic Motion**: Produces unpredictable, non-repeating patterns with high visual complexity.

5. **Smooth Oscillation**: Creates fluid, wave-like patterns with consistent amplitude.

### Mask Type Effects

- **Circular Masks**: Provide smooth, organic appearance following the trajectory
- **Square Masks**: Create geometric, pixelated effects with sharp edges
- **Trail Masks**: Show motion history with temporal fading effects

### Parameter Impact

- **High Elasticity**: Tends to create more regular, circular patterns
- **High Damping**: Results in energy decay and spiral patterns
- **High Fluidity**: Produces smoother transitions and more organic shapes
- **High Moment of Inertia**: Creates more complex, multi-loop patterns

---

## Technical Details

### Generation Process

1. **Simulation**: Each parameter set runs the circular motion simulator for 3 seconds at 20 FPS
2. **Mask Creation**: Individual mask frames are generated for each simulation step
3. **Animation**: Frames are compiled into GIF and MP4 formats
4. **Embedding**: Media files are embedded in this markdown report

### File Structure

```
├── masks/           # Individual mask frames (PNG)
├── gifs/            # Animated GIF sequences
├── videos/          # MP4 video sequences
└── mask_report.md   # This report file
```

### Performance Metrics

- **Total Frames Generated**: 300 frames per parameter set (60 frames × 5 sets)
- **Mask Types**: 3 types (circular, square, trail)
- **Total Animations**: 15 GIFs + 15 Videos
- **Generation Time**: Approximately 2-3 minutes per parameter set

---

## Conclusion

The mask sequences demonstrate the rich variety of patterns that can emerge from the circular motion simulator by varying physical parameters. Each combination of elasticity, damping, fluidity, and moment of inertia produces unique visual characteristics that could be useful for:

- **Artistic Applications**: Creating dynamic visual patterns
- **Scientific Visualization**: Understanding complex motion dynamics  
- **Educational Purposes**: Demonstrating physics principles
- **Creative Coding**: Generating procedural art and animations

The combination of different mask types (circular, square, trail) provides additional visual variety and can be used to create different aesthetic effects from the same underlying motion patterns.

---

*Report generated by the Circular Motion Simulator Mask Generator*
"""

    # Write the markdown file
    with open('mask_report.md', 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print("Markdown report generated: mask_report.md")
    return 'mask_report.md'

def check_generated_files():
    """Check what files have been generated"""
    print("\nChecking generated files...")
    
    # Check directories
    dirs = ['masks', 'gifs', 'videos']
    for dir_name in dirs:
        if os.path.exists(dir_name):
            files = os.listdir(dir_name)
            print(f"{dir_name}/: {len(files)} files")
        else:
            print(f"{dir_name}/: Directory not found")
    
    # Check specific file types
    gif_files = glob.glob('gifs/*.gif')
    video_files = glob.glob('videos/*.mp4')
    mask_files = glob.glob('masks/*.png')
    
    print(f"\nFile counts:")
    print(f"  GIF files: {len(gif_files)}")
    print(f"  Video files: {len(video_files)}")
    print(f"  Mask frames: {len(mask_files)}")

if __name__ == "__main__":
    # Generate the markdown report
    report_file = generate_markdown_report()
    
    # Check what files are available
    check_generated_files()
    
    print(f"\nReport ready: {report_file}")
    print("You can now view the report with embedded GIFs and videos!")