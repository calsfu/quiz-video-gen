import svgwrite
import numpy as np
from moviepy.editor import ColorClip, ImageClip, CompositeVideoClip, VideoClip
import io
from PIL import Image

VIDEO_WIDTH = 640
VIDEO_HEIGHT = 480
FPS = 24
DURATION = 5  # Duration of the background animation in seconds
SVG_SIZE = 30  # Size of each SVG circle
SPEED_X = -20  # Pixels per second to the left
SPEED_Y = -20  # Pixels per second upwards

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
    dwg = svgwrite.Drawing(filename='temp.svg', size=(VIDEO_WIDTH, VIDEO_HEIGHT))
    light_color = lighten_color(base_color)
    num_x = VIDEO_WIDTH // (SVG_SIZE * 1.5) + 2
    num_y = VIDEO_HEIGHT // (SVG_SIZE * 1.5) + 2

    for i in range(int(num_x)):
        for j in range(int(num_y)):
            x_offset = time * SPEED_X
            y_offset = time * SPEED_Y
            cx = i * SVG_SIZE * 1.5 + SVG_SIZE // 2 + x_offset % (SVG_SIZE * 1.5)
            cy = j * SVG_SIZE * 1.5 + SVG_SIZE // 2 + y_offset % (SVG_SIZE * 1.5)
            dwg.add(dwg.circle(center=(cx, cy), r=SVG_SIZE // 2, fill=light_color))

    # Save the SVG to a BytesIO object to avoid file I/O
    svg_bytes = io.BytesIO(dwg.tostring().encode('utf-8'))
    img = Image.open(svg_bytes)
    return np.array(img)

def make_frame(t, base_color):
    """Creates a frame for the MoviePy VideoClip."""
    return create_svg_frame(t, base_color)

if __name__ == '__main__':
    base_color_hex = '#%02x%02x%02x' % (100, 149, 237) # Cornflower Blue as an example

    # Create a solid color background
    background_clip = ColorClip(size=(VIDEO_WIDTH, VIDEO_HEIGHT), color=base_color_hex, duration=DURATION)

    # Create the moving SVG pattern layer
    moving_svg_clip = VideoClip(lambda t: make_frame(t, base_color_hex), duration=DURATION)

    # Overlay the moving SVG pattern on the background
    final_clip = CompositeVideoClip([background_clip, moving_svg_clip.set_opacity(0.8)]) # Adjust opacity as needed

    final_clip.write_videofile("moving_svg_background.mp4", fps=FPS)

    print("Generated moving_svg_background.mp4")