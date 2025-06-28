from moviepy.editor import TextClip, ColorClip, CompositeVideoClip, VideoFileClip, VideoClip

clip1 = ColorClip(size=(100, 100), color=(255, 0, 0), duration=10)
clip2 = ColorClip(size=(100, 100), color=(0, 255, 0), duration=10)

clips = [clip1, clip2]
final_clip = CompositeVideoClip(clips)
video_clip = VideoClip("test.mp4")

final_clip.write_videofile("test.mp4", fps=30)