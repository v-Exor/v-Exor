"""Generate original monochrome profile graphics using Pillow."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
ASSETS.mkdir(exist_ok=True)
FONT = Path('C:/Windows/Fonts')
def font(size, weight='regular'):
    return ImageFont.truetype(str(FONT / {'regular':'segoeui.ttf', 'bold':'segoeuib.ttf', 'light':'segoeuil.ttf', 'mono':'consola.ttf'}[weight]), size)
def background(w,h):
    im=Image.new('RGB',(w,h))
    im.putdata([(int(8+24*(x/w)**1.8),)*3 for x in range(w)]*h)
    return im
def text(d,xy,value,size,fill='#ffffff',weight='regular'):
    d.text(xy,value,font=font(size,weight),fill=fill)
def header(phase=0):
    im=background(1280,380); d=ImageDraw.Draw(im); cx,cy=1090,185
    for r in [73,113,153,195]: d.ellipse((cx-r,cy-r,cx+r,cy+r),outline='#3b3b3b')
    for angle in range(0,360,45):
        a=math.radians(angle)
        d.line((cx+math.cos(a)*48,cy+math.sin(a)*48,cx+math.cos(a)*195,cy+math.sin(a)*195),fill='#303030')
    d.rounded_rectangle((1055,150,1125,220),radius=15,fill='#161616',outline='#a3a3a3',width=2)
    text(d,(1070,159),'KR',28,weight='bold')
    a=phase*math.tau-math.pi/2; x,y=cx+math.cos(a)*153,cy+math.sin(a)*153
    for r,gray in [(11,42),(7,70),(3,225)]: d.ellipse((x-r,y-r,x+r,y+r),fill=(gray,)*3)
    for a,r in [(2.5,113),(5.7,195)]:
        x,y=cx+math.cos(a)*r,cy+math.sin(a)*r
        d.ellipse((x-3,y-3,x+3,y+3),fill='#888888')
    text(d,(54,38),'V-EXOR  /  DEVELOPER PORTFOLIO',17,'#b8b8b8','mono')
    text(d,(49,100),'Keanne Rosario',66,weight='bold')
    text(d,(54,199),'Computer Science student. Curious builder.',27,'#d0d0d0','light')
    d.line((54,268,740,268),fill='#484848')
    text(d,(54,294),'WEB EXPERIENCES   /   GAMES   /   COMPUTER VISION',17,'#b8b8b8','mono')
    d.line((0,379,1279,379),fill='#626262')
    return im
header().save(ASSETS/'profile-header.png',optimize=True)
frames=[header(i/48).quantize(colors=96) for i in range(48)]
frames[0].save(ASSETS/'profile-header.gif',save_all=True,append_images=frames[1:],duration=125,loop=0,optimize=True,disposal=1)
def card(number,category,title,subtitle,tags,kind,filename):
    im=background(1280,300); d=ImageDraw.Draw(im)
    text(d,(46,30),f'{number}  /  {category}',17,'#b5b5b5','mono')
    text(d,(43,85),title,49,weight='bold')
    text(d,(46,163),subtitle,23,'#cccccc')
    text(d,(46,238),tags,16,'#acacac','mono')
    d.line((44,213,820,213),fill='#404040'); d.line((0,299,1279,299),fill='#575757')
    if kind=='os':
        d.rounded_rectangle((945,59,1217,239),radius=15,fill='#111111',outline='#777777',width=2)
        d.line((945,90,1217,90),fill='#444444')
        for x in [963,976,989]:d.ellipse((x,72,x+4,76),fill='#999999')
        for y,values in [(111,[65,38,80]),(141,[36,86,54]),(171,[76,48,29])]:
            x=963
            for w in values:
                d.rounded_rectangle((x,y,x+w,y+19),radius=3,fill='#454545' if x<1050 else '#999999'); x+=w+7
        text(d,(964,210),'FCFS  RR  SJF',12,'#999999','mono')
    elif kind=='game':
        d.rounded_rectangle((949,89,1210,218),radius=48,fill='#181818',outline='#9b9b9b',width=2)
        d.rounded_rectangle((980,135,1040,153),radius=3,fill='#bcbcbc')
        d.rounded_rectangle((1001,114,1019,174),radius=3,fill='#bcbcbc')
        for x,y in [(1143,119),(1166,143),(1120,143),(1143,167)]:d.ellipse((x-8,y-8,x+8,y+8),outline='#bcbcbc',width=2)
        for x in [1064,1085]:d.rounded_rectangle((x,176,x+10,181),radius=2,fill='#696969')
    else:
        for x in range(954,1215,29):d.line((x,49,x,249),fill='#363636')
        for y in range(49,250,29):d.line((954,y,1215,y),fill='#363636')
        d.ellipse((1003,71,1169,237),outline='#bcbcbc',width=2)
        d.ellipse((1034,102,1138,206),outline='#6f6f6f',width=2)
        d.ellipse((1065,133,1107,175),fill='#a8a8a8')
        for x,y,dx,dy in [(975,69,1,1),(1196,69,-1,1),(975,233,1,-1),(1196,233,-1,-1)]:
            d.line((x,y,x+dx*25,y),fill='#dedede',width=3); d.line((x,y,x,y+dy*25),fill='#dedede',width=3)
    im.save(ASSETS/filename,optimize=True)
card('01','SYSTEMS & INTERACTION','RTX-6767-Pro-Max','A Windows-inspired desktop simulation in the browser.','JAVASCRIPT  /  HTML  /  CSS','os','project-os.png')
card('02','PLAY & PROBLEM SOLVING','Mini-Game Hub','Seven games. One place to play.','JAVASCRIPT  /  GAME LOGIC  /  LOCAL STORAGE','game','project-games.png')
card('03','LEARNING & EXPLORATION','Computer Vision Lab','A central home for seven independent laboratory activities.','REACT  /  TYPESCRIPT  /  VITE  /  TAILWIND CSS','vision','project-vision.png')
print('Generated', ', '.join(p.name for p in ASSETS.iterdir()))
