#!/usr/bin/env python3
"""
Complete Mask Generation Pipeline
Runs the entire process: simulation -> masks -> GIFs -> videos -> markdown report
"""

import os
import sys
import subprocess
import time
from mask_generator import MaskGenerator, generate_parameter_sets
from generate_markdown_report import generate_markdown_report, check_generated_files

def check_dependencies():
    """Check if required dependencies are installed"""
    print("Checking dependencies...")
    
    try:
        import numpy
        import matplotlib
        from PIL import Image
        print("✓ All Python dependencies are available")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False

def check_ffmpeg():
    """Check if ffmpeg is available for video generation"""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        print("✓ FFmpeg is available for video generation")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠ FFmpeg not found - videos will not be generated")
        print("  Install ffmpeg for video support: https://ffmpeg.org/download.html")
        return False

def run_mask_generation():
    """Run the complete mask generation process"""
    print("=" * 60)
    print("CIRCULAR MOTION SIMULATOR - MASK GENERATION")
    print("=" * 60)
    
    start_time = time.time()
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    ffmpeg_available = check_ffmpeg()
    
    print("\n" + "=" * 60)
    print("STARTING MASK GENERATION")
    print("=" * 60)
    
    # Initialize generator
    generator = MaskGenerator()
    
    # Get parameter sets
    param_sets = generate_parameter_sets()
    mask_types = ['circular', 'square', 'trail']
    
    total_combinations = len(param_sets) * len(mask_types)
    current_combination = 0
    
    print(f"Generating {total_combinations} mask sequences...")
    print(f"Parameter sets: {len(param_sets)}")
    print(f"Mask types: {len(mask_types)}")
    print()
    
    # Generate all combinations
    for i, params in enumerate(param_sets):
        print(f"[{i+1}/{len(param_sets)}] Processing: {params['name']}")
        print(f"  Description: {params['description']}")
        
        for j, mask_type in enumerate(mask_types):
            current_combination += 1
            print(f"  [{current_combination}/{total_combinations}] {mask_type} masks...")
            
            try:
                # Generate mask sequence
                mask_paths, trajectory_x, trajectory_y = generator.generate_mask_sequence(
                    params, duration=3.0, fps=20, mask_type=mask_type
                )
                
                # Create GIF
                gif_path = f"gifs/{params['name']}_{mask_type}.gif"
                generator.create_gif(mask_paths, gif_path, duration=100)
                
                # Create video (if ffmpeg is available)
                if ffmpeg_available:
                    try:
                        video_path = f"videos/{params['name']}_{mask_type}.mp4"
                        generator.create_video(mask_paths, video_path, fps=20)
                    except Exception as e:
                        print(f"    ⚠ Video creation failed: {e}")
                else:
                    print(f"    ⚠ Skipping video generation (ffmpeg not available)")
                
                print(f"    ✓ Completed {mask_type} sequence")
                
            except Exception as e:
                print(f"    ✗ Error generating {mask_type} sequence: {e}")
        
        print()
    
    # Generate markdown report
    print("=" * 60)
    print("GENERATING MARKDOWN REPORT")
    print("=" * 60)
    
    try:
        report_file = generate_markdown_report()
        print(f"✓ Report generated: {report_file}")
    except Exception as e:
        print(f"✗ Error generating report: {e}")
        return False
    
    # Final summary
    end_time = time.time()
    duration = end_time - start_time
    
    print("\n" + "=" * 60)
    print("GENERATION COMPLETE")
    print("=" * 60)
    
    print(f"Total time: {duration:.1f} seconds")
    print(f"Report file: mask_report.md")
    
    # Check generated files
    check_generated_files()
    
    print("\n" + "=" * 60)
    print("NEXT STEPS")
    print("=" * 60)
    print("1. Open 'mask_report.md' to view the generated report")
    print("2. The report contains embedded GIFs and videos")
    print("3. All media files are stored in their respective directories:")
    print("   - gifs/ - Animated GIF sequences")
    print("   - videos/ - MP4 video sequences") 
    print("   - masks/ - Individual mask frames")
    
    return True

def main():
    """Main function"""
    try:
        success = run_mask_generation()
        if success:
            print("\n🎉 Mask generation completed successfully!")
            sys.exit(0)
        else:
            print("\n❌ Mask generation failed!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠ Generation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()