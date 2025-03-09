

# importing editor from movie py 
from moviepy.editor import TextClip
  
# text 
text = "Hello"
  
# creating a text clip 
# having font arial-bold 
# with font size = 50 
# and color = black 
clip = TextClip(text, font ="Arial-Bold", fontsize = 50, color ="black") 
  
# showing  clip  
clip.ipython_display()  
