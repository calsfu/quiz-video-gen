import svgwrite
import numpy as np
from moviepy.editor import ColorClip, VideoClip
import io
from PIL import Image
import cairosvg
import os
import shutil

# --- CONFIGURATION ---
VIDEO_WIDTH = 640
VIDEO_HEIGHT = 480
FPS = 24
DURATION = 5
SVG_SIZE = 30
SPEED_X = -40
SPEED_Y = -30
TEMP_FRAME_DIR = "temp_frames"

# --- HELPER FUNCTIONS (Unchanged) ---
def lighten_color(color_hex, factor=0.2):
    color_hex = color_hex.lstrip('#')
    r, g, b = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
    r = int(min(255, r + (255 - r) * factor))
    g = int(min(255, g + (255 - g) * factor))
    b = int(min(255, b + (255 - b) * factor))
    return f'#{r:02x}{g:02x}{b:02x}'

def create_svg_frame(time, base_color):
    dwg = svgwrite.Drawing(size=(f"{VIDEO_WIDTH}px", f"{VIDEO_HEIGHT}px"))
    light_color = lighten_color(base_color)
    cell_size_x = SVG_SIZE * 1.5
    cell_size_y = SVG_SIZE * 1.5
    num_x = int(VIDEO_WIDTH / cell_size_x) + 2
    num_y = int(VIDEO_HEIGHT / cell_size_y) + 2
    total_offset_x = time * SPEED_X
    total_offset_y = time * SPEED_Y
    for i in range(num_x):
        for j in range(num_y):
            base_x = i * cell_size_x
            base_y = j * cell_size_y
            cx = (base_x + total_offset_x) % (num_x * cell_size_x)
            cy = (base_y + total_offset_y) % (num_y * cell_size_y)
            cx -= cell_size_x
            cy -= cell_size_y
            dwg.add(dwg.circle(center=(cx, cy), r=SVG_SIZE / 2, 
                               fill=light_color, fill_opacity=0.8))
    png_bytes = io.BytesIO()
    cairosvg.svg2png(bytestring=dwg.tostring().encode('utf-8'),
                       write_to=png_bytes,
                       output_width=VIDEO_WIDTH,
                       output_height=VIDEO_HEIGHT)
    png_bytes.seek(0)
    img = Image.open(png_bytes)
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    return np.array(img)

# --- MAIN EXECUTION ---
if __name__ == '__main__':
    # 1. SETUP
    if os.path.exists(TEMP_FRAME_DIR):
        shutil.rmtree(TEMP_FRAME_DIR)
    os.makedirs(TEMP_FRAME_DIR)
    
    print("Step 1: Pre-rendering all animation frames...")
    frame_filenames = []
    total_frames = int(DURATION * FPS)
    for i in range(total_frames):
        t = i / FPS
        frame_array = create_svg_frame(t, '#6495ED')
        img = Image.fromarray(frame_array)
        filename = os.path.join(TEMP_FRAME_DIR, f"frame_{i:04d}.png")
        img.save(filename)
        frame_filenames.append(filename)
    print(f"Step 1 Complete: {len(frame_filenames)} frames rendered.")

    print("Step 2: Building video with manual composition...")
    
    # 2. CREATE BACKGROUND CLIP
    background_clip = ColorClip(size=(VIDEO_WIDTH, VIDEO_HEIGHT),
                                color=(100, 149, 237), 
                                duration=DURATION)
                                
    # 3. MANUAL COMPOSITION FUNCTION
    # This function now loads the correct frame from disk for each moment in time.
    def make_final_frame(t):
        # Get the background frame
        bg_frame = background_clip.get_frame(t)
        bg_pil = Image.fromarray(bg_frame.astype('uint8'))

        # Determine which foreground frame to load
        frame_index = int(t * FPS)
        # Ensure we don't go past the last frame
        frame_index = min(len(frame_filenames) - 1, frame_index)
        fg_path = frame_filenames[frame_index]
        
        # Load the foreground frame directly from the file system
        # This guarantees we get the original, uncorrupted RGBA image
        fg_pil = Image.open(fg_path)

        # Paste the foreground (with its alpha channel) onto the background
        bg_pil.paste(fg_pil, (0, 0), mask=fg_pil)
        
        # Convert back to a numpy array for MoviePy
        return np.array(bg_pil)

    # 4. CREATE FINAL CLIP using our new robust function
    final_clip = VideoClip(make_final_frame, duration=DURATION)

    # 5. WRITE VIDEO
    final_clip.write_videofile("moving_svg_background.mp4", fps=FPS, codec="libx264")

    # 6. CLEANUP
    print("Step 3: Cleaning up temporary files...")
    shutil.rmtree(TEMP_FRAME_DIR)

    print("\nSuccessfully generated moving_svg_background.mp4")