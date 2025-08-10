# import openai
from pydoc import text
import numpy as np
from PIL import Image  # Ensure this is imported for resampling
from moviepy import TextClip, ImageClip, VideoClip, CompositeVideoClip, ColorClip, concatenate_videoclips
from moviepy.video.fx import Rotate
# from moviepy.config import change_settings
# from moviepy.video.tools.drawing import color_split
from background_v2 import create_background_clip
from config import QUESTION_FONT_SHADOW_COLOR, QUESTION_FONT_SIZE, QUESTION_FONT_COLOR, QUESTION_FONT_NAME, NUMBER_FONT_SIZE, NUMBER_FONT_COLOR, NUMBER_FONT_NAME, MAX_IMAGE_WIDTH, MAX_IMAGE_HEIGHT, VIDEO_HEIGHT, VIDEO_WIDTH, IMAGE_ROTATE_AMPLITUDE, IMAGE_ROTATE_FREQUENCY
from movement import bounce_y

def create_number_clip(q_num, duration=3):
    # question number
    question_num_clip = TextClip(text=f"{q_num}", font_size=NUMBER_FONT_SIZE, color=NUMBER_FONT_COLOR, font=NUMBER_FONT_NAME).with_duration(duration)
    question_num_clip = question_num_clip.with_position(lambda t: (VIDEO_WIDTH * .1, bounce_y(t, VIDEO_HEIGHT * .1, freq=.75, amplitude=4)))

    return question_num_clip

def create_text_clip(question, duration=3):
    # Create question text clip
    question_clip = TextClip(text=question, font_size=QUESTION_FONT_SIZE, color=QUESTION_FONT_COLOR, font=QUESTION_FONT_NAME).with_duration(duration)
    question_clip = question_clip.with_position(lambda t: ('center', bounce_y(t, VIDEO_HEIGHT * .1, freq=.75, amplitude=4)))
    question_clip_shadow = TextClip(text=question, font_size=QUESTION_FONT_SIZE, color=QUESTION_FONT_SHADOW_COLOR, font=QUESTION_FONT_NAME).with_duration(duration)
    question_clip_shadow = question_clip_shadow.with_position(lambda t: ('center', bounce_y(t, VIDEO_HEIGHT * .1+3, freq=.75, amplitude=4)))

    # question_clip = question_clip.with_font_size(QUESTION_FONT_SIZE)

    return question_clip, question_clip_shadow

def create_rounded_corner_mask(size, radius):
    w, h = size
    
    # Create a full white mask (the base for the rounded rectangle)
    mask = ColorClip(size, color=1, is_mask=True)

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
    ], size=size).with_is_mask(True)

    return mask

def create_image_clip(image_path="assets/images/test.jpg", duration=3):
    image_clip = ImageClip(image_path)
    image_clip = image_clip.resized(width=MAX_IMAGE_WIDTH, height=MAX_IMAGE_HEIGHT)
    image_clip =image_clip.with_position(('center', 'center'), relative=True).with_duration(duration)
    # image_clip = image_clip.with_mask(create_rounded_corner_mask(image_clip.size, 50)).with_effects([Rotate(lambda t: IMAGE_ROTATE_AMPLITUDE * np.sin(np.pi * IMAGE_ROTATE_FREQUENCY * t))])
    mask = create_rounded_corner_mask(image_clip.size, 20)
    image_clip = image_clip.with_mask(mask)
    return image_clip

def create_text_and_image_clip(question, q_num, image_path="assets/images/test.jpg", duration=3):
    number_clip = create_number_clip(q_num, duration)
    text_clip, text_clip_shadow = create_text_clip(question, duration)
    image_clip = create_image_clip(image_path, duration)
    return number_clip, text_clip, text_clip_shadow, image_clip

def main():
    # topic = input("Enter quiz topic: ")

    # Static questions for testing
    questions = ["WHAT IS THE CAPITAL OF FRANCE", "What is the capital of France? - Paris", "What is 2 + 2? - 4", "What is the largest ocean? - Pacific Ocean"]  # generate_quiz_questions(topic)
    # text = "Hello"
    DURATION = 1
    background_clip = create_background_clip(DURATION)

    number_clip = create_number_clip(1, DURATION)
    text_clip = create_text_clip(questions[0], DURATION)
    image_clip = create_image_clip(duration=DURATION)

    clips = [background_clip, number_clip, text_clip, image_clip]

    final_video = CompositeVideoClip(clips)
    final_video.write_videofile("videos/quiz_video.mp4", fps=24)

if __name__ == "__main__":
    main()