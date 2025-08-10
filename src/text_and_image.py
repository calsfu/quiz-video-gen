# import openai
from pydoc import text
import numpy as np
from PIL import Image  # Ensure this is imported for resampling
from moviepy import TextClip, ImageClip, VideoClip, CompositeVideoClip, ColorClip, concatenate_videoclips
# from moviepy.config import change_settings
# from moviepy.video.tools.drawing import color_split
from background_v2 import create_background_clip
from config import PADDING, QUESTION_FONT_SIZE, QUESTION_FONT_COLOR, QUESTION_FONT_NAME, NUMBER_FONT_SIZE, NUMBER_FONT_COLOR, NUMBER_FONT_NAME, MAX_IMAGE_WIDTH, MAX_IMAGE_HEIGHT, VIDEO_HEIGHT, VIDEO_WIDTH
# Set your OpenAI API key
# openai.api_key = 'your-api-key'



def bounce_y(duration, center_y, freq=2, amplitude=50):
    # This formula creates a sine wave bounce
    return center_y + amplitude * np.sin(freq * np.pi * duration)

def create_number_clip(q_num, duration=3):
    # question number
    question_num_clip = TextClip(text=f"{q_num}", font_size=NUMBER_FONT_SIZE, color=NUMBER_FONT_COLOR, font=NUMBER_FONT_NAME).with_duration(duration)
    question_num_clip = question_num_clip.with_position(lambda t: (VIDEO_WIDTH * .1, bounce_y(t, VIDEO_HEIGHT * .1, freq=.75, amplitude=4)))

    return question_num_clip

def create_text_clip(question, duration=3):
    # Create question text clip
    question_clip = TextClip(text=question, font_size=QUESTION_FONT_SIZE, color=QUESTION_FONT_COLOR, font=QUESTION_FONT_NAME).with_duration(duration)
    question_clip = question_clip.with_position(lambda t: ('center', bounce_y(t, VIDEO_HEIGHT * .1, freq=.75, amplitude=4)))
    # question_clip = question_clip.with_font_size(QUESTION_FONT_SIZE)

    return question_clip

def create_image_clip(image_path="assets/images/test.jpg", duration=3):
    image_clip = ImageClip(image_path)
    image_clip = image_clip.resized(width=MAX_IMAGE_WIDTH, height=MAX_IMAGE_HEIGHT)
    # image_clip = image_clip.with_position(('center', 'bottom'), relative=True).with_duration(duration)
    image_clip =image_clip.with_position(('center', 'center'), relative=True).with_duration(duration)
    
    return image_clip

def create_text_and_image_clip(question, q_num, image_path="assets/images/test.jpg", duration=3):
    number_clip = create_number_clip(q_num, duration)
    text_clip = create_text_clip(question, duration)
    image_clip = create_image_clip(image_path, duration)
    return number_clip, text_clip, image_clip

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