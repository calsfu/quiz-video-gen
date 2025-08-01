# import openai
from pydoc import text
import numpy as np
from PIL import Image  # Ensure this is imported for resampling
from moviepy import TextClip, ImageClip, VideoClip, CompositeVideoClip, ColorClip, concatenate_videoclips
# from moviepy.config import change_settings
# from moviepy.video.tools.drawing import color_split
from background_v2 import create_background_clip

# Set your OpenAI API key
# openai.api_key = 'your-api-key'

VIDEO_WIDTH = 640
VIDEO_HEIGHT = 480
VIDEO_RESOLUTION = (VIDEO_WIDTH, VIDEO_HEIGHT)
PADDING = 10
QUESTION_FONT_SIZE = 30
QUESTION_FONT_COLOR = 'white'
QUESTION_FONT_NAME = 'fonts/vag-rounded-bold_gEBUv/VAG Rounded Bold/VAG Rounded Bold.ttf'
NUMBER_FONT_SIZE = 30
NUMBER_FONT_COLOR = 'white'
NUMBER_FONT_NAME = 'fonts/vag-rounded-bold_gEBUv/VAG Rounded Bold/VAG Rounded Bold.ttf'
MAX_IMAGE_WIDTH = 100
MAX_IMAGE_HEIGHT = 100

# def generate_quiz_questions(topic, num_questions=5):
#     prompt = f"Generate {num_questions} quiz questions with answers about {topic}."
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=prompt,
#         max_tokens=500
#     )
#     return response.choices[0].text.strip().split('\n')

def make_frame(t, duration=3):
    # Define the bar height, color, and other properties
    bar_height = 20
    bar_color = (255, 0, 0)  # Red bar
    bar_width = (VIDEO_WIDTH - 2 ) * (t / duration)  # Bar width increases over time
    
    # Create a frame with transparent background (all zeros means transparent)
    frame = np.ones((bar_height, VIDEO_WIDTH, 3), dtype=np.uint8) * 255
    
    # Draw the red bar on the frame
    frame[:, :int(bar_width)] = bar_color
    
    return frame

def create_number_clip(q_num, duration=3):
    # question number
    question_num_clip = TextClip(text=f"{q_num}", font_size=NUMBER_FONT_SIZE, color=NUMBER_FONT_COLOR, font=NUMBER_FONT_NAME)
    question_num_clip = question_num_clip.with_position(('center', 'center')).with_duration(duration)
    width, height = question_num_clip.size
    # box = ColorClip(size=(width + PADDING, height + PADDING * 2), color=(255, 255, 255))
    # question_num_clip = CompositeVideoClip([box, question_num_clip])
    question_num_clip = question_num_clip.with_position((.05, .05), relative=True).with_duration(duration)

    return question_num_clip

def create_text_clip(question, duration=3):
    # Create question text clip
    question_clip = TextClip(text=question, font_size=QUESTION_FONT_SIZE, color=QUESTION_FONT_COLOR, font=QUESTION_FONT_NAME)
    question_clip = question_clip.with_position(('center', .05), relative=True).with_duration(duration)
    
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