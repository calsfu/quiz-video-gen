# import openai
from pydoc import text
import numpy as np
from PIL import Image  # Ensure this is imported for resampling
from moviepy import TextClip, ImageClip, VideoClip, CompositeVideoClip, ColorClip, concatenate_videoclips
# from moviepy.config import change_settings
# from moviepy.video.tools.drawing import color_split

TRANSITION_FONT_SIZE = 30
TRANSITION_FONT_COLOR = 'white'
TRANSITION_FONT_NAME = 'fonts/vag-rounded-bold_gEBUv/VAG Rounded Bold/VAG Rounded Bold.ttf'

def create_transition(q_num, duration=3):
    # Create question text clip
    transition_clip = TextClip(text=f"Question {q_num}", font_size=TRANSITION_FONT_SIZE, color=TRANSITION_FONT_COLOR, font=TRANSITION_FONT_NAME)
    transition_clip = transition_clip.with_position(('center', 'center'), relative=True).with_duration(duration)
    
    return transition_clip

def main():
    transition_clip = create_transition(1, 3)
    transition_clip.write_videofile("videos/transition_clip.mp4", fps=24)

if __name__ == "__main__":
    main()