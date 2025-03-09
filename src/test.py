# importing editor from movie py 
from moviepy.editor import TextClip
from moviepy.config import change_settings
change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})
# C:\Program Files\ImageMagick-7.1.1-Q16-HDRI/magick.exe
# text
text = "Hello"
  
# creating a text clip
# having font arial-bold
# with font size = 50
# and color = black
clip = TextClip(text, font ="Arial-Bold", fontsize = 50, color ="black") 
  
# showing  clip
clip.ipython_display()  
