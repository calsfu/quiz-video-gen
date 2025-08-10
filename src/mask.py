from moviepy import TextClip, ImageClip, VideoClip, CompositeVideoClip, ColorClip, concatenate_videoclips
from background_v2 import create_background_clip
from config import VIDEO_WIDTH, VIDEO_HEIGHT
import numpy as np

def create_rounded_corner_mask(size, radius):
    w, h = size
    
    # Create a full white mask (the base for the rounded rectangle)
    mask = ColorClip(size, color=255, is_mask=True)

    # Create transparent circles for each corner
    circle_mask = ColorClip((radius * 2, radius * 2), color=0, is_mask=True)

    # Place the transparent circles at the corners
    # The circles are black (0), which will make those areas transparent in the mask
    mask = CompositeVideoClip([
        mask,
        circle_mask.with_position((0, 0)),
        circle_mask.with_position((w - radius * 2, 0)),
        circle_mask.with_position((0, h - radius * 2)),
        circle_mask.with_position((w - radius * 2, h - radius * 2))
    ], size=size).with_duration(1).with_fps(1).with_is_mask(True)

    return mask

def make_circle_mask(size):
    Y, X = np.ogrid[:size, :size]
    center = size / 2
    distance_from_center = np.sqrt((X - center)**2 + (Y - center)**2)
    mask = 255 * (distance_from_center <= size / 2)/255
    return mask.astype(np.uint8)

def main():
    background = create_background_clip(3)
    color = ColorClip(size=(100, 100), color=(255, 0, 0), duration=3).with_position(('center', 'center'))
    mask = make_circle_mask(color.size[0])
    circle_mask = ImageClip(mask, is_mask=True)

    color = color.with_mask(circle_mask)
    final_clip = CompositeVideoClip([background, color])
    final_clip.write_videofile("videos/test_mask.mp4", fps=24)
 
if __name__ == "__main__":
    main()