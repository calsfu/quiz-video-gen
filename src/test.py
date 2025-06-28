import numpy as np
from moviepy.editor import VideoClip, ColorClip
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
TEMP_FRAME_DIR = "temp_frames"

# --- Custom SVG Configuration ---
CUSTOM_SVG_PATH = "assets/svg/white.svg" 
SVG_RENDER_SIZE = 50
SVG_OPACITY = 0.4  # <--- CONTROL OPACITY HERE (0.0 to 1.0)
SPEED_X = -10
SPEED_Y = -10

def create_pattern_from_stamp(time, stamp_image, stamp_mask):
    """
    Creates a frame by stamping a pre-rendered image in a moving pattern.
    Returns an RGBA numpy array.
    """
    canvas = Image.new('RGBA', (VIDEO_WIDTH, VIDEO_HEIGHT), (0, 0, 0, 0))

    cell_size_x = stamp_image.width * 1.5
    cell_size_y = stamp_image.height * 1.5
    num_x = int(VIDEO_WIDTH / cell_size_x) + 2
    num_y = int(VIDEO_HEIGHT / cell_size_y) + 2
    total_offset_x = time * SPEED_X
    total_offset_y = time * SPEED_Y

    for i in range(num_x):
        for j in range(num_y):
            px = int((i * cell_size_x + total_offset_x) % (num_x * cell_size_x) - cell_size_x)
            py = int((j * cell_size_y + total_offset_y) % (num_y * cell_size_y) - cell_size_y)
            canvas.paste(stamp_image, (px, py), stamp_mask)
            
    return np.array(canvas, dtype=np.uint8)

def safe_color_clip(size, color, duration):
    frame = np.ones((size[1], size[0], 3), dtype=np.uint8) * np.array(color, dtype=np.uint8)
    clip = ColorClip(size=size, color=color, duration=duration)
    clip = clip.set_make_frame(lambda t: frame)
    return clip

# --- MAIN EXECUTION ---
if __name__ == '__main__':
    # --- Step 1: Load SVG and create the stamp AND the mask once ---
    print(f"Step 1: Loading and rendering '{CUSTOM_SVG_PATH}'...")
    if not os.path.exists(CUSTOM_SVG_PATH):
        raise FileNotFoundError(f"Custom SVG not found at: {CUSTOM_SVG_PATH}")
    
    png_bytes = cairosvg.svg2png(url=CUSTOM_SVG_PATH, 
                                 output_width=SVG_RENDER_SIZE, 
                                 output_height=SVG_RENDER_SIZE)
    stamp_image = Image.open(io.BytesIO(png_bytes))
    if stamp_image.mode != 'RGBA':
        stamp_image = stamp_image.convert('RGBA')

    # ------------------- vvv NEW CODE BLOCK vvv -------------------
    # Modify the stamp's opacity
    rgba = np.array(stamp_image)
    # The 4th channel (index 3) is the alpha channel.
    # Multiply it by the opacity factor and convert back to an integer.
    rgba[:, :, 3] = (rgba[:, :, 3] * SVG_OPACITY).astype(np.uint8)
    # Create the new, semi-transparent stamp image
    stamp_image = Image.fromarray(rgba)
    # ------------------- ^^^ NEW CODE BLOCK ^^^ -------------------

    # Create the mask from the stamp's NEW alpha channel
    stamp_mask = stamp_image.getchannel('A')

    # --- Step 2: Pre-render frames using the new function ---
    if os.path.exists(TEMP_FRAME_DIR):
        shutil.rmtree(TEMP_FRAME_DIR)
    os.makedirs(TEMP_FRAME_DIR)
    
    print("Step 2: Pre-rendering all animation frames...")
    frame_filenames = []
    total_frames = int(DURATION * FPS)
    for i in range(total_frames):
        frame_array = create_pattern_from_stamp(i / FPS, stamp_image, stamp_mask)
        img = Image.fromarray(frame_array)
        filename = os.path.join(TEMP_FRAME_DIR, f"frame_{i:04d}.png")
        img.save(filename)
        frame_filenames.append(filename)
    print(f"Step 2 Complete: {len(frame_filenames)} frames rendered.")

    # --- Step 3: Build the final video (this part is now robust) ---
    print("Step 3: Building video with manual composition...")
    background_clip = safe_color_clip((VIDEO_WIDTH, VIDEO_HEIGHT), (100, 149, 237), DURATION)
            
    def make_final_frame(t):
        bg_frame = background_clip.get_frame(t)
        bg_pil = Image.fromarray(bg_frame)
        frame_index = min(int(t * FPS), len(frame_filenames) - 1)
        fg_path = frame_filenames[frame_index]
        fg_pil = Image.open(fg_path)
        bg_pil.paste(fg_pil, (0, 0), mask=fg_pil)
        return np.array(bg_pil)

    final_clip = VideoClip(make_final_frame, duration=DURATION)
    final_clip.write_videofile("custom_svg_background.mp4", fps=FPS, codec="libx264")

    # --- Step 4: Cleanup ---
    print("Step 4: Cleaning up temporary files...")
    shutil.rmtree(TEMP_FRAME_DIR)

    print("\nSuccessfully generated custom_svg_background.mp4")