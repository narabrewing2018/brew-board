from PIL import Image, ImageDraw
S=1024
def glyph(d, cx, top, scale, color):
    # conical fermenter: dome, cylinder, cone, legs
    w=380*scale; h_cyl=360*scale; h_cone=200*scale; dome=90*scale
    x0=cx-w/2; x1=cx+w/2
    y_dome=top; y_cyl=top+dome; y_cone=y_cyl+h_cyl; y_tip=y_cone+h_cone
    d.pieslice([x0,y_dome,x1,y_dome+2*dome],180,360,fill=color)
    d.rectangle([x0,y_cyl-1,x1,y_cone],fill=color)
    d.polygon([(x0,y_cone),(x1,y_cone),(cx+40*scale,y_tip),(cx-40*scale,y_tip)],fill=color)
    lw=34*scale
    for sx in (-1,1):
        lx=cx+sx*(w/2-30*scale)
        d.rectangle([lx-lw/2,y_cone-10,lx+lw/2,y_tip+90*scale],fill=color)
    d.rectangle([cx-lw/2,y_tip-2,cx+lw/2,y_tip+40*scale],fill=color)  # valve
    # sight-glass band
    return (x0,y_cyl,x1,y_cone)
def make(bg,fg,rounded,scale,path,size):
    im=Image.new('RGBA',(S,S),(0,0,0,0))
    d=ImageDraw.Draw(im)
    if rounded: d.rounded_rectangle([0,0,S-1,S-1],radius=220,fill=bg)
    else: d.rectangle([0,0,S,S],fill=bg)
    total=(90+360+200+90)*scale
    top=(S-total)/2
    x0,y0,x1,y1=glyph(d,S/2,top,scale,fg)
    # liquid level line (beer) inside cylinder: a darker band
    d.rectangle([x0+40*scale,y0+130*scale,x1-40*scale,y0+150*scale],fill=bg)
    im.resize((size,size),Image.LANCZOS).save(path)
amber=(168,96,14,255); cream=(250,246,236,255)
make(amber,cream,False,1.0,'app/icons/icon-512.png',512)
make(amber,cream,False,1.0,'app/icons/icon-192.png',192)
make(amber,cream,False,0.78,'app/icons/maskable-512.png',512)
make(amber,cream,False,0.95,'app/icons/apple-touch-icon.png',180)
make(amber,cream,True,1.0,'app/icons/favicon-64.png',64)
