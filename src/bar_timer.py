from moviepy import VideoClip, CompositeVideoClip, ColorClip
from PIL import Image, ImageDraw
import numpy as np
from config import VIDEO_WIDTH, VIDEO_HEIGHT, FPS
from background_v2 import create_background_clip

TRANSPARENT = (255, 255, 255, 0)
BAR_WIDTH = int(VIDEO_WIDTH * .5)

def draw_rounded_rectangle_mask_with_border(width, height, radius, border_width=2):
    """
    Draws a rounded rectangle mask with a white border on a black background.

    Args:
        width: Width of the rectangle.
        height: Height of the rectangle.
        radius: Radius of the rounded corners.
        border_width: Width of the white border in pixels.

    Returns:
        A numpy array representing the grayscale image (mask).
    """
    # Create a new image that is completely black (for transparency).
    img = Image.new('RGBA', (100, 20), color = (255,255,255,0))
    draw = ImageDraw.Draw(img)


    full_bar = (0, 0, 100, 20)
    partial_bar = (0, 0, 50, 20)
    corner_radius = 30
    draw.rounded_rectangle(full_bar, radius=corner_radius, fill='white')
    draw.rounded_rectangle(partial_bar, radius=corner_radius, fill='red')

    # Draw the white border (slightly larger rounded rectangle).
    # border_radius = radius + border_width
    # draw.rounded_rectangle(
    #     (border_width // 2, border_width // 2, width - border_width // 2 - 1, height - border_width // 2 - 1),
    #     fill=255,
    #     radius=border_radius
    # )
    # # Draw the inner black rounded rectangle (the transparent part).
    # draw.rounded_rectangle(
    #     (border_width, border_width, width - border_width - 1, height - border_width - 1),
    #     fill=255,
    #     radius=radius
    # )

    return np.array(img)

# def draw_rounded_rectangle_outside(draw, xy, radius, fill):
#   x1, y1, x2, y2 = xy
#   draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
#   draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
#   draw.pieslice([x1, y1, x1 + 2 * radius, y1 + 2 * radius], 180, 270, fill=fill)
#   draw.pieslice([x2 - 2 * radius, y1, x2, y1 + 2 * radius], 270, 360, fill=fill)
#   draw.pieslice([x1, y2 - 2 * radius, x1 + 2 * radius, y2], 90, 180, fill=fill)
#   draw.pieslice([x2 - 2 * radius, y2 - 2 * radius, x2, y2], 0, 90, fill=fill)

# def draw_rounded_rectangle_inside(draw, xy, radius, fill):
#   x1, y1, x2, y2 = xy
#   draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
#   draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
#   draw.pieslice([x1, y1, x1 + 2 * radius, y1 + 2 * radius], 180, 270, fill=fill)
#   draw.pieslice([x2 - 2 * radius, y1, x2, y1 + 2 * radius], 270, 360, fill=fill)
#   draw.pieslice([x1, y2 - 2 * radius, x1 + 2 * radius, y2], 90, 180, fill=fill)
#   draw.pieslice([x2 - 2 * radius, y2 - 2 * radius, x2, y2], 0, 90, fill=fill)

def make_bar_frame(t, duration=3, bar_height=20):
  # Create a transparent base image
  
  img = Image.new('RGBA', (BAR_WIDTH, bar_height), color = (255,255,255,0))
  draw = ImageDraw.Draw(img)
 

  # Bar properties
  radius = 20
  bar_color = (255, 128, 0) # Orange color
  bg_bar_color = (255, 255, 255) # White background with full opacity

  draw.rounded_rectangle((0, 0, BAR_WIDTH, bar_height), radius=radius, fill='white')

  #   Calculate the current width of the progress bar
  progress_width = int(BAR_WIDTH * (1 - (t / duration)))

#   Draw the progress bar
  if progress_width >= 0:
    draw.rounded_rectangle((0, 0, progress_width, bar_height), radius=radius, fill=bar_color)

  # OLD
#   # Draw the background bar
#   draw_rounded_rectangle_outside(draw, (0, 0, BAR_WIDTH, bar_height), radius, bg_bar_color)


 

  # Convert the Pillow image to a NumPy array for MoviePy
  return np.array(img)
 

def create_bar_timer_clip(duration):
  timer_clip = VideoClip(lambda t: make_bar_frame(t, duration=duration), duration=duration)
 
  # Positioning with a slight margin from the bottom
  return timer_clip.with_position(('center', VIDEO_HEIGHT * .9))

def main():
  duration = 3
  background_clip = create_background_clip(duration=duration)
  timer_clip = create_bar_timer_clip(duration=duration)
  final_clip = CompositeVideoClip([background_clip, timer_clip], size=(VIDEO_WIDTH, VIDEO_HEIGHT))
  final_clip.write_videofile("videos/quiz_video_transparent.mp4", fps=FPS)
 

if __name__ == "__main__":
  main()