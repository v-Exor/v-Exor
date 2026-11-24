"""Build the profile's code-drawn blue/black artwork and seamless GIF loops.
Requires Pillow and NumPy. Text stays still while decorative layers animate.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import math
import argparse
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
ASSETS.mkdir(exist_ok=True)
FONT = Path('C:/Windows/Fonts')
W = 1280
TAU = math.tau

def font(size, weight='regular'):
    return ImageFont.truetype(str(FONT / {'regular':'segoeui.ttf', 'bold':'segoeuib.ttf', 'light':'segoeuil.ttf', 'mono':'consola.ttf'}[weight]), size)

def text(d, xy, value, size, fill='#edf7ff', weight='regular'):
    d.text(xy, value, font=font(size, weight), fill=fill)

def blend(a,b,t):
    return tuple(round(x+(y-x)*t) for x,y in zip(a,b))

def background(h, hero=False):
    y,x=np.mgrid[0:h,0:W]
    glow=np.exp(-(((x-1090)/470)**2+((y-h*.45)/(h*.88))**2)*1.7)
    glow2=np.exp(-(((x-655)/500)**2+((y-h)/(h*.9))**2)*2)
    rgb=np.stack([5+glow*7+glow2*1,10+glow*49+glow2*10,20+glow*121+glow2*28],axis=-1)
    return Image.fromarray(np.uint8(np.clip(rgb,0,255)))

HEADER_HEIGHT=540
BASE_HEADER=background(HEADER_HEIGHT,True)
PORTRAIT=ImageOps.fit(Image.open(ASSETS/'profile-portrait.png').convert('RGB'),(310,310),method=Image.Resampling.LANCZOS)
PORTRAIT_MASK=Image.new('L',(310,310))
ImageDraw.Draw(PORTRAIT_MASK).ellipse((0,0,309,309),fill=255)
BASE_CARD=background(260)

def ambient(im, phase, center, radius=130):
    layer=Image.new('RGBA',im.size)
    d=ImageDraw.Draw(layer)
    pulse=(1-math.cos(TAU*phase))/2
    x,y=center
    d.ellipse((x-radius,y-radius,x+radius,y+radius),fill=(20,123,255,round(10+13*pulse)))
    layer=layer.filter(ImageFilter.GaussianBlur(42))
    return Image.alpha_composite(im.convert('RGBA'),layer).convert('RGB')

def glow_lines(im,draw_fn):
    layer=Image.new('RGBA',im.size)
    draw_fn(ImageDraw.Draw(layer))
    bloom=layer.filter(ImageFilter.GaussianBlur(7))
    im=Image.alpha_composite(im.convert('RGBA'),bloom)
    return Image.alpha_composite(im,layer).convert('RGB')

def header(phase=0):
    im=ambient(BASE_HEADER,phase,(1050,270),200)
    d=ImageDraw.Draw(im)
    # Fine flowing lines stay behind the portrait and clear of the name.
    for i in range(25):
        points=[]
        for x in range(770,W+1,5):
            y=50+i*9+math.sin((x-770)/185+phase*TAU)*35+(x-770)*.25
            points.append((x,y))
        d.line(points,fill=blend((12,31,62),(28,86,157),i/32),width=1)
    for i in range(11):
        points=[(x,505+i*9+math.sin(x/210+phase*TAU)*15) for x in range(0,760,5)]
        d.line(points,fill=(12,34+i,66+i*2),width=1)
    d.rounded_rectangle((60,36,103,79),radius=12,fill='#103569',outline='#397cbd')
    text(d,(68,44),'KR',18,'#d4edff','bold')
    text(d,(119,39),'KEANNE ROSARIO',17,'#d5e9fc','bold')
    text(d,(120,63),'DEVELOPMENT PORTFOLIO',11,'#76a5d4','mono')
    text(d,(1020,48),'v-Exor / PH',15,'#9fc5ed','mono')
    d.line((60,103,1220,103),fill='#1b385c')
    text(d,(61,148),'COMPUTER SCIENCE STUDENT',16,'#7abfff','mono')
    text(d,(56,185),'Keanne Jericho',64,weight='bold')
    text(d,(56,259),'M. Rosario',64,weight='bold')
    text(d,(61,357),'Web Development & Computer Vision',25,'#adcfee')
    d.line((61,425,695,425),fill='#24466f')
    text(d,(61,447),'LAGUNA STATE POLYTECHNIC UNIVERSITY',15,'#b2cce7','mono')
    text(d,(61,475),'Philippines',17,'#7c9fbe')
    cx,cy=1030,292
    d.ellipse((cx-166,cy-166,cx+166,cy+166),fill='#0b2547',outline='#285d94',width=1)
    im.paste(PORTRAIT,(cx-155,cy-155),PORTRAIT_MASK)
    d=ImageDraw.Draw(im)
    d.ellipse((cx-156,cy-156,cx+156,cy+156),outline='#63aeec',width=2)
    # A slow highlight follows the portrait frame; the photo and text stay still.
    angle=phase*TAU-math.pi/2
    x,y=cx+166*math.cos(angle),cy+166*math.sin(angle)
    d.ellipse((x-3,y-3,x+3,y+3),fill='#a3dcff')
    text(d,(926,480),'WEB  /  VISION',15,'#8cbae4','mono')
    d.line((0,HEADER_HEIGHT-1,W-1,HEADER_HEIGHT-1),fill='#2a5d94',width=2)
    return im

CARDS=[
 ('01','EXPERIMENTAL RESEARCH / THESIS','JUSTICE-KP','Transcription-assisted decision support.','NEXT.JS  /  FASTAPI  /  LOCAL TRANSCRIPTION','justice'),
 ('02','COMPUTER VISION','GestureDeck','Hand-gesture control for PowerPoint.','PYTHON  /  MEDIAPIPE  /  OPENCV','gesture'),
 ('03','WEB APPLICATION','RTX-6767-Pro-Max','Browser-based desktop & OS simulation.','JAVASCRIPT  /  HTML  /  CSS','os'),
 ('04','LABORATORY PORTAL','Computer Vision Lab','Seven CSST106 laboratory activities.','REACT  /  TYPESCRIPT  /  VITE  /  TAILWIND CSS','vision'),
 ('05','BROWSER GAMES','Mini-Game Hub','Seven games with local score storage.','JAVASCRIPT  /  GAME LOGIC  /  LOCAL STORAGE','games'),
]

def card(spec,phase=0):
    number,category,title,subtitle,tags,kind=spec
    im=ambient(BASE_CARD,phase,(1090,130),106)
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((42,25,80,55),radius=11,fill='#123d75',outline='#2367ac')
    text(d,(50,31),number,15,'#9cddff','mono')
    text(d,(95,32),category,15,'#70bfff','mono')
    text(d,(40,75),title,49,weight='bold')
    text(d,(43,144),subtitle,24,'#afcce8')
    d.line((43,199,802,199),fill='#193e63')
    text(d,(43,220),tags,16,'#65b9ef','mono')
    pulse=(math.sin(phase*TAU)+1)/2
    if kind=='os':
        d.rounded_rectangle((948,43,1212,220),radius=16,fill='#061a33',outline='#3d96e4',width=2)
        d.line((948,77,1212,77),fill='#1b4a78')
        for i,x in enumerate([965,979,993]):d.ellipse((x,57,x+5,62),fill=['#42cfff','#328cf5','#3a5eaa'][i])
        for row,values in enumerate([[57,42,87],[37,81,61],[70,40,38]]):
            x=968
            for col,width in enumerate(values):
                t=(math.sin(phase*TAU-row*.9-col*.65)+1)/2
                c=blend((19,65,116),(56,176,255),t)
                d.rounded_rectangle((x,94+row*28,x+width,112+row*28),radius=4,fill=c)
                x+=width+7
        text(d,(968,193),'FCFS / RR / SJF',12,'#6ba7d3','mono')
    elif kind=='games':
        d.rounded_rectangle((948,75,1213,202),radius=48,fill='#081f3f',outline='#4eabfa',width=2)
        d.rounded_rectangle((977,120,1043,138),radius=4,fill='#46acff')
        d.rounded_rectangle((1001,96,1019,162),radius=4,fill='#46acff')
        for i,(x,y) in enumerate([(1147,103),(1170,127),(1124,127),(1147,151)]):
            t=(math.sin(phase*TAU-i*math.pi/2)+1)/2
            c=blend((30,74,137),(106,233,255),t)
            d.ellipse((x-8,y-8,x+8,y+8),fill=c)
        for x in [1064,1085]:d.rounded_rectangle((x,165,x+11,170),radius=2,fill='#387ac5')
    elif kind=='vision':
        for x in range(966,1215,28):d.line((x,37,x,229),fill='#15385d')
        for y in range(37,230,28):d.line((966,y,1215,y),fill='#15385d')
        d.ellipse((1006,54,1170,218),outline='#4a9fe9',width=2)
        d.ellipse((1037,85,1139,187),outline='#2572b8',width=2)
        d.ellipse((1070,118,1106,154),fill=blend((25,102,185),(106,216,255),pulse))
        for x,y,dx,dy in [(976,49,1,1),(1200,49,-1,1),(976,221,1,-1),(1200,221,-1,-1)]:
            d.line((x,y,x+dx*24,y),fill='#74d3ff',width=3)
            d.line((x,y,x,y+dy*24),fill='#74d3ff',width=3)
        scan_y=64+(1-math.cos(phase*TAU))/2*142
        for off in range(-9,10):
            strength=(1-abs(off)/10)*.65
            d.line((989,scan_y+off,1187,scan_y+off),fill=blend((9,37,70),(72,175,236),strength))
        d.line((989,scan_y,1187,scan_y),fill='#93edff',width=2)
    elif kind=='justice':
        # A hearing waveform feeds a reviewable document and workflow.
        d.rounded_rectangle((1038,40,1186,181),radius=12,fill='#081f3f',outline='#4eabfa',width=2)
        text(d,(1056,53),'KP / REVIEW',14,'#8edbff','mono')
        for row,width in enumerate([104,82,94]):
            d.rounded_rectangle((1056,88+row*20,1056+width,93+row*20),radius=2,fill='#25649f')
        d.line((971,115,1022,115),fill='#368bd0',width=2)
        d.line((1015,109,1022,115,1015,121),fill='#74d3ff',width=2)
        for i in range(9):
            x=963+i*7
            height=5+19*(math.sin(phase*TAU-i*.7)+1)/2
            d.line((x,75-height,x,75+height),fill='#65cbff',width=3)
        nodes=[(990,210),(1080,210),(1170,210)]
        d.line(nodes,fill='#25649f',width=2)
        for i,(x,y) in enumerate(nodes):
            intensity=(math.cos(phase*TAU-i*TAU/3)+1)/2
            d.ellipse((x-9,y-9,x+9,y+9),fill=blend((18,61,112),(93,217,255),intensity))
        d.line((1084,158,1091,165,1107,149),fill='#82e4ff',width=3)
    elif kind=='gesture':
        # Stylized hand landmarks and a slideshow; the illustration is decorative.
        d.rounded_rectangle((1101,57,1225,146),radius=10,fill='#081f3f',outline='#4eabfa',width=2)
        d.line((1117,82,1208,82),fill='#28639d',width=4)
        d.line((1117,96,1184,96),fill='#28639d',width=4)
        d.line((1163,146,1163,164),fill='#4eabfa',width=2)
        d.line((1145,164,1181,164),fill='#4eabfa',width=2)
        squeeze=.82+.18*math.cos(phase*TAU)
        points=[(1013,212),(981,174),(965,156),(953,145),(944,132),
                (987,134),(984,108),(983,86),(982,65),
                (1007,128),(1006,94),(1006,67),(1006,45),
                (1027,132),(1030,102),(1032,79),(1034,60),
                (1044,143),(1054,120),(1063,103),(1071,88)]
        points=[(1013+(x-1013)*squeeze,y) for x,y in points]
        chains=[(0,1,2,3,4),(0,5,6,7,8),(5,9,10,11,12),
                (9,13,14,15,16),(13,17,18,19,20),(0,17),(5,9,13,17)]
        for chain in chains:d.line([points[i] for i in chain],fill='#3e9ae0',width=2)
        for x,y in points:d.ellipse((x-3,y-3,x+3,y+3),fill='#92e7ff')
        for direction,x in [(-1,1127),(1,1198)]:
            c=blend((38,105,169),(135,230,255),(math.sin(phase*TAU+direction)+1)/2)
            d.line((x-direction*10,192,x+direction*10,192),fill=c,width=3)
            d.line((x+direction*3,185,x+direction*10,192,x+direction*3,199),fill=c,width=3)
    d.line((0,259,1279,259),fill='#1b4b7b')
    return im

# One shared palette prevents color flicker across GIF frames.
preview=Image.new('RGB',(W,HEADER_HEIGHT+260*len(CARDS)))
preview.paste(header(),(0,0))
for i,spec in enumerate(CARDS):preview.paste(card(spec,.35),(0,HEADER_HEIGHT+i*260))
palette=preview.quantize(colors=256,method=Image.Quantize.MEDIANCUT)
preview.save(ROOT.parent/'design-preview-blue.png')

def save_loop(name,render,count=72,duration=90):
    still=render(0)
    still.save(ASSETS/(name+'.png'),optimize=True)
    frames=[render(i/count).quantize(palette=palette,dither=Image.Dither.FLOYDSTEINBERG) for i in range(count)]
    frames[0].save(ASSETS/(name+'.gif'),save_all=True,append_images=frames[1:],duration=duration,loop=0,optimize=True,disposal=1)
    print(name, (ASSETS/(name+'.gif')).stat().st_size,flush=True)

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--only',nargs='+',choices=['profile-header']+['project-'+s[-1] for s in CARDS],
                        help='Build selected assets; omit to rebuild everything.')
    selected=parser.parse_args().only
    if selected is None or 'profile-header' in selected:
        save_loop('profile-header',header)
    for spec in CARDS:
        name='project-'+spec[-1]
        if selected is None or name in selected:
            save_loop(name,lambda phase,spec=spec:card(spec,phase))
