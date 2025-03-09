# import openai
import numpy as np
from PIL import Image  # Ensure this is imported for resampling
from moviepy.editor import TextClip, ImageClip, VideoClip, CompositeVideoClip, ColorClip, concatenate_videoclips
from moviepy.config import change_settings
from moviepy.video.tools.drawing import color_split
change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})

# Set your OpenAI API key
# openai.api_key = 'your-api-key'

VIDEO_WIDTH = 640
VIDEO_HEIGHT = 480
VIDEO_RESOLUTION = (VIDEO_WIDTH, VIDEO_HEIGHT)
PADDING = 20

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
    frame = np.ones((20, VIDEO_WIDTH, 3), dtype=np.uint8) * 255
    
    # Draw the red bar on the frame
    frame[:, :int(bar_width)] = bar_color
    
    return frame

def create_quiz_clip(question, image_path, question_type='free_answer', duration=3):
    # Create a bright-colored background
    bg_clip = ColorClip(size=VIDEO_RESOLUTION, color=(205, 0, 255)).set_duration(duration)
    
    # Create question text clip
    question_clip = TextClip(question, fontsize=40, color='black', font='Arial-Bold')
    # question_clip = question_clip.set_position(('center', 'top')).set_duration(duration)
    width, height = question_clip.size
    box = ColorClip(size=(width + PADDING * 2, height + PADDING * 2), color=(255, 255, 255))
    question_clip = CompositeVideoClip([box, question_clip])
    question_clip = question_clip.set_position(('center', 'top')).set_duration(duration)
    
    # Add image clip with proper resampling
    image_clip = (ImageClip(image_path)
                  .set_duration(duration)
                  .set_position('center')).resize(height=VIDEO_HEIGHT/3)  # Resize image to fit the video
    # white box around the image
    width, height = image_clip.size
    box = ColorClip(size=(width + PADDING * 2, height + PADDING * 2), color=(255, 255, 255))
    image_clip = CompositeVideoClip([box, image_clip])    
    image_clip = image_clip.set_position('center').set_duration(duration)
    
    if question_type == 'multiple_choice':
        image_clip = image_clip.set_position(('left', 'center'))

    timer_clip = VideoClip(lambda t: make_frame(t, duration=duration), duration=duration).set_position('bottom')

    # Composite the clips together
    return CompositeVideoClip([bg_clip, question_clip, image_clip, timer_clip])

def main():
    # topic = input("Enter quiz topic: ")

    # Static questions for testing
    questions = ["What is the capital of France? - Paris", "What is 2 + 2? - 4", "What is the largest ocean? - Pacific Ocean"]  # generate_quiz_questions(topic)
    # text = "Hello"

    clips = []
    for qa in questions:
        clips.append(create_quiz_clip(qa, 'images/test.jpg'))

    final_video = concatenate_videoclips(clips)
    final_video.write_videofile("videos/quiz_video.mp4", fps=24)

if __name__ == "__main__":
    main()