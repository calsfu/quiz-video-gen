import svgwrite
import numpy as np
from moviepy.editor import ColorClip, CompositeVideoClip, VideoClip, ImageClip
import io
from PIL import Image
import cairosvg

VIDEO_WIDTH = 640
VIDEO_HEIGHT = 480
FPS = 24
DURATION = 3
SVG_SIZE = 30
SPEED_X = -10
SPEED_Y = -10

# def lighten_color(color_hex, factor=0.2):
#     color_hex = color_hex.lstrip('#')
#     r, g, b = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
#     r = int(min(255, r + (255 - r) * factor))
#     g = int(min(255, g + (255 - g) * factor))
#     b = int(min(255, b + (255 - b) * factor))
#     return f'#{r:02x}{g:02x}{b:02x}'

def create_svg_frame(time, base_color):
    """Returns (RGB image, mask) tuple."""
    dwg = svgwrite.Drawing(size=(f"{VIDEO_WIDTH}px", f"{VIDEO_HEIGHT}px"))
    # light_color = lighten_color(base_color)

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
            cx = (base_x + total_offset_x) % (num_x * cell_size_x) - cell_size_x
            cy = (base_y + total_offset_y) % (num_y * cell_size_y) - cell_size_y
            dwg.add(dwg.circle(center=(cx, cy), r=SVG_SIZE / 2, fill=base_color))

    png_bytes = io.BytesIO()
    cairosvg.svg2png(
        bytestring=dwg.tostring().encode('utf-8'),
        write_to=png_bytes,
        output_width=VIDEO_WIDTH,
        output_height=VIDEO_HEIGHT,
        background_color='none'
    )
    png_bytes.seek(0)

    img = Image.open(png_bytes).convert('RGBA')
    rgba = np.array(img, dtype=np.uint8)
    
    rgb = rgba[:, :, :3]
    alpha = rgba[:, :, 3] / 255.0  # Normalize alpha to [0, 1] for MoviePy mask
    return rgb, alpha

def make_frame_rgb(t, base_color):
    rgb, _ = create_svg_frame(t, base_color)
    return rgb

def make_frame_mask(t, base_color):
    _, alpha = create_svg_frame(t, base_color)
    return alpha

def to_rgb_if_needed(clip):
    return clip.set_color([255, 255, 255]) if clip.ismask else clip

def safe_color_clip(size, color, duration):
    frame = np.ones((size[1], size[0], 3), dtype=np.uint8) * np.array(color, dtype=np.uint8)
    clip = ColorClip(size=size, color=color, duration=duration)
    clip = clip.set_make_frame(lambda t: frame)
    return clip

if __name__ == '__main__':
    print("Creating background...")
    background_colors = [(85, 183, 63), (137, 100, 255) ]
    svg_color = '#ffffff'  # White

    background_clip = safe_color_clip((VIDEO_WIDTH, VIDEO_HEIGHT), background_colors[0], DURATION)

    # Create RGB and mask clips from separate frame functions
    moving_svg_rgb_clip = VideoClip(lambda t: make_frame_rgb(t, svg_color), duration=DURATION)
    moving_svg_mask_clip = VideoClip(lambda t: make_frame_mask(t, svg_color), duration=DURATION).set_ismask(True)

    # Apply the mask to the visual clip
    moving_svg_clip = moving_svg_rgb_clip.set_mask(moving_svg_mask_clip)

    # Composite with transparency
    final_clip = CompositeVideoClip([background_clip, moving_svg_clip.set_opacity(0.05)])
    final_clip.write_videofile("moving_svg_background.mp4", fps=FPS)

    print("Generated moving_svg_background.mp4")
