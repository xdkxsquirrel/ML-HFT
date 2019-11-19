
import os
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
 
text = (("This is a test to see how long this will be willing to run for ", (255, 0, 0)),
        ("Wow this is running for quite a while ", (0, 255, 0)),
        ("MSFT ^ $135", (0, 0, 255)))
 
 
font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 16)
all_text = ""
for text_color_pair in text:
    t = text_color_pair[0]
    all_text = all_text + t
 
print(all_text)
width, ignore = font.getsize(all_text)
print(width)
 
 
im = Image.new("RGB", (width + 30, 16), "black")
draw = ImageDraw.Draw(im)
 
x = 0;
for text_color_pair in text:
    t = text_color_pair[0]
    c = text_color_pair[1]
    print("t=" + t + " " + str(c) + " " + str(x))
    draw.text((x, 0), t, c, font=font)
    x = x + font.getsize(t)[0]
 
im.save("test.ppm")
 
os.system("./demo -t 1000 --led-cols=32 --led-rows=16 --led-chain=3 -D 1 test.ppm")

