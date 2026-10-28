"""Stacked 12h face + outline AOD for Redmi Watch 5 Lite.
Pillow required. Font: Barlow Condensed Bold, SIL OFL.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageChops
import xml.etree.ElementTree as E
import io,zipfile,base64
R=Path(__file__).resolve().parents[1];P=R.parent/'watchface/v3/DaiCaMinimal';F=R/'design/fonts/BarlowCondensed-Bold.ttf'
P.mkdir(parents=True,exist_ok=True)
W,H=410,502;cw,ch=132,218

def text(text,size,w,h,color=255):
 f=ImageFont.truetype(str(F),size);b=f.getbbox(text);assert b[2]-b[0]<=w and b[3]-b[1]<=h,(text,b,w,h)
 im=Image.new('L',(w,h),0);ImageDraw.Draw(im).text(((w-(b[2]-b[0]))//2-b[0],(h-(b[3]-b[1]))//2-b[1]),text,font=f,fill=color);return im

def project(aod=False):
 path=P/'AOD' if aod else P;ip=path/'images';ip.mkdir(parents=True,exist_ok=True);ims={}
 def save(im,name):ims[name]=im;im.convert('P').save(ip/name,optimize=True)
 save(Image.new('L',(W,H),0),'black.png')
 for n in range(10):
  im=text(str(n),270,cw,ch)
  if aod:
   # A one-pixel inner contour: no solid digit fills or animation.
   im=ImageChops.subtract(im,im.filter(ImageFilter.MinFilter(3))).point(lambda v:round(v*0.5))
  save(im,f'digit{n}.png')
 for h in range(12):
  im=Image.new('L',(cw*2,ch),0)
  for j,c in enumerate(f'{h or 12:02d}'):im.paste(ims[f'digit{c}.png'],(j*cw,0))
  save(im,f'hour{h}.png')
 root=E.Element('FaceProject',DeviceType='3652',Id='928105003');s=E.SubElement(root,'Screen',Title='Dai Ca Stacked V3',Bitmap='preview.png')
 def add(shape,name,x,y,w,h,**kw):
  at={k:str(v) for k,v in dict(Shape=shape,Name=name,X=x,Y=y,Width=w,Height=h,Alpha=255,Visible_Src=0,**kw).items()};return E.SubElement(s,'Widget',at)
 def image(name,x,y,w,h,f):add(30,name,x,y,w,h,Bitmap=f)
 def il(name,x,y,w,h,src,files):add(31,name,x,y,w,h,BitmapList='|'.join(f'({i}):{f}' for i,f in enumerate(files)),Alignment=0,DefaultIndex=0,Value_Src=src,Index_Src=src,Spacing=0,Blanking=0)
 def num(name,x,y,w,h,src,prefix):add(32,name,x,y,w,h,BitmapList='|'.join([f'{prefix}{i}.png' for i in range(10)]+[f'{prefix}0.png']),Digits=2,Alignment=0,Value_Src=src,Spacing=0,Blanking=0)
 image('Background',0,0,W,H,'black.png')
 x=73 if aod else 20
 il('Hour12',x,34,cw*2,ch,'0811',[f'hour{h%12}.png' for h in range(24)])
 num('Minutes',x,250,cw*2,ch,'1011','digit')
 if not aod:
  for n in range(10):save(text(str(n),29,16,38),f'small{n}.png')
  save(text('/',29,12,38),'slash.png')
  for n,t in enumerate(['CN','THỨ 2','THỨ 3','THỨ 4','THỨ 5','THỨ 6','THỨ 7']):save(text(t,29,90,40),f'week{n}.png')
  for pct in range(101):save(text(f'{pct}%',32,90,42),f'power{pct}.png')
  il('Weekday',297,202,90,40,'2012',[f'week{n}.png' for n in range(7)])
  num('Day',303,244,32,38,'1812','small');image('DateSlash',335,244,12,38,'slash.png');num('Month',347,244,32,38,'1012','small')
  il('BatteryPercent',297,364,90,42,'0841',[f'power{n}.png' for n in range(101)])
 def render(hour,minute,day=29,month=10,week=4,pct=59):
  im=ims['black.png'].copy();im.paste(ims[f'hour{hour%12}.png'],(x,34))
  for j,c in enumerate(f'{minute:02d}'):im.paste(ims[f'digit{c}.png'],(x+j*cw,250))
  if not aod:
   im.paste(ims[f'week{week}.png'],(297,202));im.paste(ims[f'power{pct}.png'],(297,364))
   for j,c in enumerate(f'{day:02d}'):im.paste(ims[f'small{c}.png'],(303+j*16,244))
   im.paste(ims['slash.png'],(335,244))
   for j,c in enumerate(f'{month:02d}'):im.paste(ims[f'small{c}.png'],(347+j*16,244))
  return im
 preview=render(0,0);save(preview.resize((244,298),Image.Resampling.LANCZOS),'preview.png')
 preview.convert('RGB').save(path/'preview-full.png')
 E.indent(root);E.ElementTree(root).write(path/('AOD.fprj' if aod else 'DaiCaMinimal.fprj'),encoding='utf-8',xml_declaration=True)
 for e in s:
  assert int(e.get('X'))+int(e.get('Width'))<=W;assert int(e.get('Y'))+int(e.get('Height'))<=H
 assert not any(e.get('Name')=='AMPM' for e in s)
 if aod:
  assert len(s)==3
  # Broad coverage of 12-hour displays, including midnight/noon.
  most=0
  for h in range(12):
   for m in range(60):
    im=render(h,m);hist=im.histogram();most=max(most,(W*H-hist[0])/(W*H))
  print('AOD maximum lit pixel ratio:',round(most*100,2),'percent')
  assert most<0.08
 return render
normal=project(False);aod=project(True)
board=Image.new('RGB',(820,502),'black');board.paste(normal(0,0).convert('RGB'),(0,0));board.paste(aod(0,0).convert('RGB'),(410,0));board.save(P.parent/'compare-active-aod.png')
sheet=Image.new('RGB',(1230,1004),'black')
for i,(h,m,p) in enumerate([(0,0,100),(11,59,87),(12,0,9),(13,8,50),(23,49,1),(22,22,0)]):sheet.paste(normal(h,m,pct=p).convert('RGB'),(i%3*410,i//3*502))
sheet.save(P.parent/'checks.png')
b=io.BytesIO()
with zipfile.ZipFile(b,'w',zipfile.ZIP_DEFLATED) as z:
 for f in sorted(P.rglob('*')):
  if f.is_file():z.write(f,Path('DaiCaMinimal')/f.relative_to(P))
(R/'assets/watchface.zip.b64').write_text(base64.b64encode(b.getvalue()).decode()+'\n')
print('Packaged',len(b.getvalue()),'bytes')
