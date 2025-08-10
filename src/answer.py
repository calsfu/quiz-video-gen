# import openai
from pydoc import text
import numpy as np
from PIL import Image  # Ensure this is imported for resampling
from moviepy import TextClip, ImageClip, VideoClip, CompositeVideoClip, ColorClip, concatenate_videoclips
# from moviepy.config import change_settings
# from moviepy.video.tools.drawing import color_split
from config import ANSWER_FONT_COLOR, ANSWER_FONT_NAME, ANSWER_FONT_SIZE

def create_answer(answer, duration=3):
    # Create question text clip
    answer_clip = TextClip(text=f"{answer}", font_size=ANSWER_FONT_SIZE, color=ANSWER_FONT_COLOR, font=ANSWER_FONT_NAME).with_position(('center', 'center'), relative=True).with_duration(duration)
    
    return answer_clip