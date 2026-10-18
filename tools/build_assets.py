"""Build the profile's code-drawn blue/black artwork and seamless GIF loops.
Requires Pillow and NumPy. Text stays still while decorative layers animate.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
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

BASE_HEADER=background(400,True)
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
    im=ambient(BASE_HEADER,phase,(1082,194),145)
    d=ImageDraw.Draw(im)
    for i in range(3):
        points=[]
        for x in range(730,1281,4):
            y=195+i*35+math.sin((x-730)/190+phase*TAU+i*.8)*(49+i*11)
            points.append((x,y))
        d.line(points,fill=[(14,61,119),(17,83,165),(21,121,204)][i],width=2)
    cx,cy=1081,184
    for r in [69,112,157]:
        d.ellipse((cx-r,cy-r,cx+r,cy+r),outline='#19467b',width=1)
    for j in range(20):
        angle=j*TAU/20+phase*TAU
        strength=((j+1)/20)**2
        x,y=cx+math.cos(angle)*157,cy+math.sin(angle)*157
        color=blend((15,49,93),(96,221,255),strength)
        rr=2 if j<18 else 4
        d.ellipse((x-rr,y-rr,x+rr,y+rr),fill=color)
    for j in range(8):
        x=780+(j*137)%470
        y=30+(j*83)%310
        fade=(math.sin(phase*TAU+j*.9)+1)/2
        c=blend((13,37,70),(81,181,255),fade*.7)
        d.ellipse((x,y,x+2,y+2),fill=c)
    pulse=(math.sin(phase*TAU)+1)/2
    d.rounded_rectangle((1036,139,1126,229),radius=25,fill='#081d38',outline=blend((37,115,220),(111,219,255),pulse),width=2)
    text(d,(1051,152),'</>',31,'#a4e9ff','mono')
    d.rounded_rectangle((52,32,346,68),radius=18,fill='#0a2647',outline='#1a5891')
    d.ellipse((68,45,76,53),fill='#55d8ff')
    text(d,(89,39),'v-Exor / hello, world',15,'#9adaff','mono')
    text(d,(47,103),'Keanne Rosario',70,weight='bold')
    text(d,(52,204),'A little code. A lot of curiosity.',29,'#b8d8f4','light')
    text(d,(52,250),'Web experiments, games & computer vision.',21,'#83b3dc')
    x=52
    for label,width in [('BUILD',104),('PLAY',94),('EXPLORE',133)]:
        d.rounded_rectangle((x,316,x+width,351),radius=17,fill='#0a2444',outline='#19558a')
        text(d,(x+20,323),label,15,'#88d9ff','mono')
        x+=width+12
    d.line((0,398,1279,398),fill='#1b4b7b',width=2)
    return im

CARDS=[
 ('01','DESKTOP EXPERIMENT','RTX-6767-Pro-Max','A whole desktop. Inside your browser.','JAVASCRIPT  /  HTML  /  CSS','os'),
 ('02','PRESS PLAY','Mini-Game Hub','Seven games. One more round?','JAVASCRIPT  /  GAME LOGIC  /  LOCAL STORAGE','games'),
 ('03','EXPLORE THE VISUAL WORLD','Computer Vision Lab','Seven labs. One place to explore.','REACT  /  TYPESCRIPT  /  VITE  /  TAILWIND CSS','vision'),
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
    else:
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
    d.line((0,259,1279,259),fill='#1b4b7b')
    return im

# One shared palette prevents color flicker across GIF frames.
preview=Image.new('RGB',(1280,400+260*3))
preview.paste(header(),(0,0))
for i,spec in enumerate(CARDS):preview.paste(card(spec,.35),(0,400+i*260))
palette=preview.quantize(colors=256,method=Image.Quantize.MEDIANCUT)
preview.save(ROOT.parent/'design-preview-blue.png')

def save_loop(name,render,count=100,duration=60):
    still=render(0)
    still.save(ASSETS/(name+'.png'),optimize=True)
    frames=[render(i/count).quantize(palette=palette,dither=Image.Dither.FLOYDSTEINBERG) for i in range(count)]
    frames[0].save(ASSETS/(name+'.gif'),save_all=True,append_images=frames[1:],duration=duration,loop=0,optimize=True,disposal=1)
    print(name, (ASSETS/(name+'.gif')).stat().st_size,flush=True)

save_loop('profile-header',header,120,50)
for spec in CARDS:
    save_loop('project-'+spec[-1],lambda phase,spec=spec:card(spec,phase))
