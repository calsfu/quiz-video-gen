import svgwrite
import numpy as np
from moviepy.editor import ColorClip, CompositeVideoClip, VideoClip
import io
from PIL import Image
import cairosvg

VIDEO_WIDTH = 640
VIDEO_HEIGHT = 480
FPS = 24
DURATION = 5  # Duration of the background animation in seconds
SVG_SIZE = 30  # Size of each SVG circle
SPEED_X = -40  # Pixels per second to the left
SPEED_Y = -30  # Pixels per second upwards

def lighten_color(color_hex, factor=0.2):
    """Lightens a given hex color."""
    color_hex = color_hex.lstrip('#')
    r, g, b = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
    r = int(min(255, r + (255 - r) * factor))
    g = int(min(255, g + (255 - g) * factor))
    b = int(min(255, b + (255 - b) * factor))
    return f'#{r:02x}{g:02x}{b:02x}'

def create_svg_frame(time, base_color):
    """Creates an SVG frame with moving circles."""
    dwg = svgwrite.Drawing(size=(f"{VIDEO_WIDTH}px", f"{VIDEO_HEIGHT}px"))
    light_color = lighten_color(base_color)

    # --- REFACTORED & SIMPLIFIED ANIMATION LOGIC ---
    # The cell_size determines the spacing of the repeating pattern.
    cell_size_x = SVG_SIZE * 1.5
    cell_size_y = SVG_SIZE * 1.5

    # Calculate how many cells we need to draw to cover the screen plus a buffer for wrapping.
    num_x = int(VIDEO_WIDTH / cell_size_x) + 2
    num_y = int(VIDEO_HEIGHT / cell_size_y) + 2

    # Calculate the total offset based on time and speed. This is how much the whole grid has moved.
    total_offset_x = time * SPEED_X
    total_offset_y = time * SPEED_Y

    for i in range(num_x):
        for j in range(num_y):
            # Base position for each circle in the grid.
            base_x = i * cell_size_x
            base_y = j * cell_size_y

            # Add the time-based offset and then use the modulo operator (%)
            # to make the pattern wrap around. This creates a seamless scroll.
            # The ( ... + cell_size) % cell_size ensures the result is always positive.
            cx = (base_x + total_offset_x) % (num_x * cell_size_x)
            cy = (base_y + total_offset_y) % (num_y * cell_size_y)

            # We shift the grid left/up by one cell size to hide the 'seam' where the wrapping happens.
            cx -= cell_size_x
            cy -= cell_size_y
            
            dwg.add(dwg.circle(center=(cx, cy), r=SVG_SIZE / 2, fill=light_color))
    # --- END OF REFACTOR ---

    # Convert SVG to PNG bytes using cairosvg
    png_bytes = io.BytesIO()
    cairosvg.svg2png(bytestring=dwg.tostring().encode('utf-8'),
                       write_to=png_bytes,
                       output_width=VIDEO_WIDTH,
                       output_height=VIDEO_HEIGHT)
    png_bytes.seek(0)

    img = Image.open(png_bytes)
    
    # --- THE FIX FOR THE VALUEERROR ---
    # Convert the image to 'RGB' to match the 3-channel format of the ColorClip background.
    # This prevents the `could not broadcast... (shape) into (shape,3)` error.
    if img.mode != 'RGB':
        img = img.convert('RGB')
    # --- END OF FIX ---
        
    return np.asarray(img.convert("RGB"), dtype=np.uint8)


def make_frame(t, base_color):
    """Creates a frame for the MoviePy VideoClip."""
    return create_svg_frame(t, base_color)

# Ensure all image arrays are RGB
def to_rgb_if_needed(clip):
    return clip.set_color([255, 255, 255]) if clip.ismask else clip

def safe_color_clip(size, color, duration):
    # Create constant RGB frame
    frame = np.ones((size[1], size[0], 3), dtype=np.uint8) * np.array(color, dtype=np.uint8)
    
    clip = ColorClip(size=size, color=color, duration=duration)
    # Override frame generation to ensure RGB output
    clip = clip.set_make_frame(lambda t: frame)
    return clip
    
if __name__ == '__main__':
    print("Creating background...")
    base_color_hex = '#%02x%02x%02x' % (100, 149, 237) # Cornflower Blue

    background_clip = safe_color_clip((640, 480), (100, 149, 237), DURATION)

    # Create the moving SVG pattern layer. make_frame will return 3-channel (RGB) frames.
    moving_svg_clip = VideoClip(lambda t: make_frame(t, base_color_hex), duration=DURATION)

    clips = [background_clip, moving_svg_clip.set_opacity(0.8)]
    final_clip = CompositeVideoClip([to_rgb_if_needed(c) for c in clips])
    final_clip = to_rgb_if_needed(final_clip)
    final_clip.write_videofile("moving_svg_background.mp4", fps=FPS)

    print("Generated moving_svg_background.mp4")