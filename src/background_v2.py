import svgwrite
import numpy as np
from moviepy import ColorClip, CompositeVideoClip, VideoClip, ImageClip
import io
from PIL import Image
import cairosvg
import math

VIDEO_WIDTH = 640
VIDEO_HEIGHT = 480
FPS = 15
SPEED_X = 0
SPEED_Y = -10
CUSTOM_SVG_PATH = "assets/svg/white.svg" # <--- The path to your SVG file
SVG_RENDER_SIZE = 50 
# def lighten_color(color_hex, factor=0.2):
#     color_hex = color_hex.lstrip('#')
#     r, g, b = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
#     r = int(min(255, r + (255 - r) * factor))
#     g = int(min(255, g + (255 - g) * factor))
#     b = int(min(255, b + (255 - b) * factor))
#     return f'#{r:02x}{g:02x}{b:02x}'

# variables
# https://www.svgrepo.com/collection/restaurant-glyphs-icons/
svg_paths = [
    "assets/svg/food-pizza-slice-svgrepo-com.svg",
    "assets/svg/food-meat-beef-stake-svgrepo-com.svg",
    "assets/svg/seafood-animal-fish-svgrepo-com.svg",
]
background_colors = [(85, 183, 63), (137, 100, 255) ]

def create_pattern_from_stamp(time):
    """
    Creates a frame by stamping a pre-rendered image in a moving,
    rotated pattern. Returns RGB and alpha channels for MoviePy.
    """
    # --- Stamp Rendering (same as your original code) ---
    stamp_images = []
    counter = 0
    for svg_path in svg_paths:
        png_bytes = cairosvg.svg2png(url=svg_path, 
                                     output_width=SVG_RENDER_SIZE, 
                                     output_height=SVG_RENDER_SIZE)
        stamp_image = Image.open(io.BytesIO(png_bytes))
        stamp_images.append(stamp_image)
        
    cell_size_x = stamp_image.width
    cell_size_y = stamp_image.height 
    
    # 1. Calculate diagonal to determine the size of a larger, temporary canvas
    diagonal = int(math.sqrt(VIDEO_WIDTH**2 + VIDEO_HEIGHT**2))
    
    # Create a canvas large enough to cover the final frame after rotation
    large_canvas = Image.new('RGBA', (diagonal, diagonal), (0, 0, 0, 0))

    # 2. Tile the stamps onto this larger canvas
    num_x = int(diagonal / cell_size_x) + 2
    num_y = int(diagonal / cell_size_y) + 2
    total_offset_x = time * SPEED_X
    total_offset_y = time * SPEED_Y

    for i in range(num_x):
        counter = (counter + 1) % len(stamp_images)
        for j in range(num_y):
            px = int((i * cell_size_x + total_offset_x) % (num_x * cell_size_x) - cell_size_x)
            py = int((j * cell_size_y + total_offset_y) % (num_y * cell_size_y) - cell_size_y)
            large_canvas.paste(stamp_images[counter], (px, py))
            counter = (counter + 1) % len(stamp_images)

    # 3. Rotate the entire tiled canvas
    rotated_canvas = large_canvas.rotate(45, resample=Image.BICUBIC, expand=False)

    # 4. Crop the center of the rotated canvas to the final video size
    left = (diagonal - VIDEO_WIDTH) / 2
    top = (diagonal - VIDEO_HEIGHT) / 2
    right = (diagonal + VIDEO_WIDTH) / 2
    bottom = (diagonal + VIDEO_HEIGHT) / 2
    final_canvas = rotated_canvas.crop((left, top, right, bottom))

    # --- Conversion to NumPy array (same as your original code) ---
    rgba = np.array(final_canvas, dtype=np.uint8)
    rgb = rgba[:, :, :3]
    alpha = rgba[:, :, 3] / 255.0
    return rgb, alpha

def make_frame_rgb(t):
    rgb, _ = create_pattern_from_stamp(t)
    return rgb

def make_frame_mask(t):
    _, alpha = create_pattern_from_stamp(t)
    return alpha

def to_rgb_if_needed(clip):
    return clip.set_color([255, 255, 255]) if clip.ismask else clip

def safe_color_clip(size, color, duration):
    frame = np.ones((size[1], size[0], 3), dtype=np.uint8) * np.array(color, dtype=np.uint8)
    clip = ColorClip(size=size, color=color, duration=duration)
    clip = clip.set_make_frame(lambda t: frame)
    return clip

def create_background_clip(duration):
    # background_clip = safe_color_clip((VIDEO_WIDTH, VIDEO_HEIGHT), background_colors[0], duration)
    background_clip = ColorClip(size=(VIDEO_WIDTH, VIDEO_HEIGHT), color=background_colors[0], duration=duration)
    moving_svg_rgb_clip = VideoClip(lambda t: make_frame_rgb(t), duration=duration)
    moving_svg_mask_clip = VideoClip(lambda t: make_frame_mask(t), duration=duration).with_is_mask(True)
    moving_svg_clip = moving_svg_rgb_clip.with_mask(moving_svg_mask_clip)
    return CompositeVideoClip([background_clip, moving_svg_clip.with_opacity(0.2)])

if __name__ == '__main__':
    print("Creating background...")
    duration = 3
    svg_color = '#ffffff'  # White

    background_clip = safe_color_clip((VIDEO_WIDTH, VIDEO_HEIGHT), background_colors[0], duration)

    # Create RGB and mask clips from separate frame functions
    moving_svg_rgb_clip = VideoClip(lambda t: make_frame_rgb(t), duration=duration)
    moving_svg_mask_clip = VideoClip(lambda t: make_frame_mask(t), duration=duration).with_is_mask(True)
     

    # Apply the mask to the visual clip
    moving_svg_clip = moving_svg_rgb_clip.with_mask(moving_svg_mask_clip)

    # Composite with transparency
    final_clip = CompositeVideoClip([background_clip, moving_svg_clip.with_opacity(0.2)])
    final_clip.write_videofile("moving_svg_background.mp4", fps=FPS)

    print("Generated moving_svg_background.mp4")
