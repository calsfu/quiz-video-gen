from moviepy import VideoClip, CompositeVideoClip, ColorClip
from PIL import Image, ImageDraw
import numpy as np
from config import VIDEO_WIDTH, VIDEO_HEIGHT, FPS
from background_v2 import create_background_clip

TRANSPARENT = (255, 255, 255, 0)
BAR_WIDTH = int(VIDEO_WIDTH * .5)

def draw_rounded_rectangle(draw, xy, radius, fill):
    """
    Draws a rounded rectangle on an ImageDraw object by combining a rectangle
    with two circles on the ends.

    Args:
        draw (ImageDraw.ImageDraw): The ImageDraw object to draw on.
        xy (tuple): A tuple of (x1, y1, x2, y2) defining the bounding box.
        radius (int): The radius of the rounded ends (circles).
        fill (any): The fill color for the shapes.
    """
    x1, y1, x2, y2 = xy
    
    # Ensure the width is at least twice the radius for the circles to fit
    if x2 - x1 < 2 * radius:
        # If the rectangle is too narrow, just draw an ellipse
        draw.ellipse(xy, fill=fill)
        return
    
    # Draw the central rectangle portion
    # The rectangle starts after the left circle and ends before the right one
    rect_coords = [x1 + radius, y1, x2 - radius, y2]
    draw.rectangle(rect_coords, fill=fill)
    
    # Draw the left semicircle (full circle in this case)
    # Its bounding box is from x1 to x1 + 2*radius
    left_circle_coords = [x1, y1, x1 + 2 * radius, y2]
    draw.ellipse(left_circle_coords, fill=fill)
    
    # Draw the right semicircle (full circle in this case)
    # Its bounding box is from x2 - 2*radius to x2
    right_circle_coords = [x2 - 2 * radius, y1, x2, y2]
    draw.ellipse(right_circle_coords, fill=fill)

def draw_rounded_rectangle_outside(draw, xy, radius, fill):
  x1, y1, x2, y2 = xy
  draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
  draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
  draw.pieslice([x1, y1, x1 + 2 * radius, y1 + 2 * radius], 180, 270, fill=fill)
  draw.pieslice([x2 - 2 * radius, y1, x2, y1 + 2 * radius], 270, 360, fill=fill)
  draw.pieslice([x1, y2 - 2 * radius, x1 + 2 * radius, y2], 90, 180, fill=fill)
  draw.pieslice([x2 - 2 * radius, y2 - 2 * radius, x2, y2], 0, 90, fill=fill)

def draw_rounded_rectangle_inside(draw, xy, radius, fill):
  x1, y1, x2, y2 = xy
  draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
  draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
  draw.pieslice([x1, y1, x1 + 2 * radius, y1 + 2 * radius], 180, 270, fill=fill)
  draw.pieslice([x2 - 2 * radius, y1, x2, y1 + 2 * radius], 270, 360, fill=fill)
  draw.pieslice([x1, y2 - 2 * radius, x1 + 2 * radius, y2], 90, 180, fill=fill)
  draw.pieslice([x2 - 2 * radius, y2 - 2 * radius, x2, y2], 0, 90, fill=fill)
 

def make_bar_frame(t, duration=3, bar_height=20):
  # Create a transparent base image
  
  img = Image.new('RGBA', (BAR_WIDTH, bar_height), (0, 0, 0, 0))
  draw = ImageDraw.Draw(img)
 

  # Bar properties
  radius = 10
  bar_color = (255, 128, 0) # Orange color
  bg_bar_color = (255, 255, 255) # White background with full opacity

  # Draw the background bar
  draw_rounded_rectangle_outside(draw, (0, 0, BAR_WIDTH, bar_height), radius, bg_bar_color)

#   Calculate the current width of the progress bar
  progress_width = int(BAR_WIDTH * (t / duration))

#   Draw the progress bar
  if progress_width > 2 * radius:
    draw_rounded_rectangle_inside(draw, [0, 0, progress_width, bar_height], radius, fill=bar_color)
 

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