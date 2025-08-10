from tokenize import String
from moviepy import CompositeVideoClip, concatenate_videoclips, ColorClip
from moviepy.video.fx import FadeIn
from background_v2 import create_background_clip
from text_and_image import create_text_and_image_clip, create_number_clip, create_text_clip, create_image_clip
from bar_timer import create_bar_timer_clip
from answer import create_answer
from config import VIDEO_WIDTH, VIDEO_HEIGHT, QUESTION_DURATION, ANSWER_DURATION
QUESTIONS = {
    "What is the capital of France?" : "Paris",
    # "What is the capital of Germany?" : "Berlin",
    # "What is the capital of Italy?" : "Rome",
    # "What is the capital of Spain?" : "Madrid",
    # "What is the capital of Portugal?" : "Lisbon",
}
    
IMAGE_PATH = "assets/images/test.jpg"

def create_question_clip(question, q_num, image_path, duration):
    transparent_clip = create_transparent_clip(duration)
    number_clip, text_clip, image_clip = create_text_and_image_clip(question, q_num, image_path, duration)
    bar_timer_clip = create_bar_timer_clip(duration)
    return CompositeVideoClip([transparent_clip, number_clip, text_clip, image_clip, bar_timer_clip])

def create_answer_clip(answer, duration=3):
    transparent_clip = create_transparent_clip(duration)
    answer_clip = create_answer(answer, duration)
    return CompositeVideoClip([transparent_clip, answer_clip])

def create_constant_background_clip(duration):
    background_clip = create_background_clip(duration)
    return background_clip

def create_transparent_clip(duration):
    transparent_clip = ColorClip(size=(VIDEO_WIDTH, VIDEO_HEIGHT), color=(255, 255, 255, 0), duration=duration)
    return transparent_clip

def main():
    clips = []
    video_duration = len(QUESTIONS) * (QUESTION_DURATION + ANSWER_DURATION)
    background_clip = create_constant_background_clip(video_duration)
    
    for idx, question in enumerate(QUESTIONS, start=1):
        
        question_clip = create_question_clip(question, idx, IMAGE_PATH, QUESTION_DURATION)
        answer_clip = create_answer_clip(QUESTIONS[question], ANSWER_DURATION)

        
        clips.append(question_clip)
        clips.append(answer_clip)
        
    no_background_clips = concatenate_videoclips(clips)
    assert background_clip.duration == no_background_clips.duration
    
    final_clip = CompositeVideoClip([background_clip, concatenate_videoclips(clips)])
    final_clip.write_videofile("videos/quiz_video.mp4", fps=24) 


if __name__ == "__main__":
    main()