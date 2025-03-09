# import openai
from moviepy.editor import TextClip, concatenate_videoclips
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})

# Set your OpenAI API key
# openai.api_key = 'your-api-key'

# def generate_quiz_questions(topic, num_questions=5):
#     prompt = f"Generate {num_questions} quiz questions with answers about {topic}."
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=prompt,
#         max_tokens=500
#     )
#     return response.choices[0].text.strip().split('\n')

def create_text_clip(text, duration=5, fontsize=50):
    return TextClip(text, color ="green") 

def main():
    # topic = input("Enter quiz topic: ")

    # Static questions for testing
    questions = ["What is the capital of France? - Paris", "What is 2 + 2? - 4", "What is the largest ocean? - Pacific Ocean"]  # generate_quiz_questions(topic)
    # text = "Hello"
    clip = TextClip("My Holidays 2013", fontsize=70, color='white').set_position('center').set_duration(10)

    clips = []
    clips.append(clip)
    # for qa in questions:
    #     clips.append(create_text_clip(qa))

    final_video = concatenate_videoclips(clips)
    final_video.write_videofile("videos/quiz_video.mp4", fps=24)

if __name__ == "__main__":
    main()