"""Generate the Redmi Watch 5 Lite 12-hour variant; Pillow required.
Run with --font pointing to DejaVuSans-Bold.ttf if not on Linux.
"""
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import xml.etree.ElementTree as E
import argparse,io,base64,zipfile
args=argparse.ArgumentParser();args.add_argument('--font',default='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf');args.add_argument('--output',default='watchface/v2/DaiCaMinimal');a=args.parse_args()
P=Path(a.output);I=P/'images';I.mkdir(parents=True,exist_ok=True)
def textimg(text,size,w,h):
 f=ImageFont.truetype(a.font,size);b=f.getbbox(text);ink=Image.new('L',(b[2]-b[0],b[3]-b[1]),0);ImageDraw.Draw(ink).text((-b[0],-b[1]),text,font=f,fill=255)
 if ink.width>w-2:ink=ink.resize((w-2,ink.height),Image.Resampling.LANCZOS)
 assert ink.height<=h
 im=Image.new('L',(w,h),0);im.paste(ink,((w-ink.width)//2,(h-ink.height)//2));return im
ims={}
def save(im,name):ims[name]=im.convert('L');ims[name].convert('P').save(I/name)
save(Image.new('L',(410,502),0),'background.png')
for n in range(10):
 save(textimg(str(n),166,92,180),f'large{n}.png');save(textimg(str(n),28,22,36),f'small{n}.png');save(textimg(str(n),26,20,34),f'battery{n}.png')
save(textimg(':',130,22,180),'colon.png');save(textimg('/',28,18,36),'slash.png');save(textimg('%',26,28,34),'percent.png')
# Render a 24-entry hour lookup: data source remains reliable 0..23;
# displayed hour becomes 12,01,...11,12,01,...11, independent of phone format.
for hour in range(12):
 hh=hour%12 or 12; im=Image.new('L',(184,180),0)
 for i,c in enumerate(f'{hh:02d}'):im.paste(ims[f'large{c}.png'],(i*92,0))
 save(im,f'hour{hour}.png')
for n,t in enumerate(['CN','THỨ 2','THỨ 3','THỨ 4','THỨ 5','THỨ 6','THỨ 7']):save(textimg(t,26,110,36),f'week{n}.png')
for t in ['AM','PM']:save(textimg(t,24,62,34),f'{t}.png')
# One indexed image per integer percentage keeps the complete battery tile centered.
for pct in range(101):
 label=f'{pct}%';f=ImageFont.truetype(a.font,26);box=f.getbbox(label);tw=box[2]-box[0]
 im=Image.new('L',(134,34),0);d=ImageDraw.Draw(im);x=(134-(36+8+tw))//2
 d.rounded_rectangle((x,8,x+29,25),radius=3,outline=210,width=2);d.rectangle((x+30,13,x+33,20),fill=210)
 if pct:d.rectangle((x+4,12,x+4+max(1,round(21*pct/100))-1,21),fill=210)
 d.text((x+42-box[0],(34-(box[3]-box[1]))//2-box[1]),label,font=f,fill=255)
 save(im,f'power{pct}.png')
root=E.Element('FaceProject',DeviceType='3652',Id='928105002');screen=E.SubElement(root,'Screen',Title='Dai Ca 12H V2',Bitmap='preview.png')
def widget(shape,name,x,y,w,h,**kw):
 at=dict(Shape=str(shape),Name=name,X=str(x),Y=str(y),Width=str(w),Height=str(h),Alpha='255',Visible_Src='0');at.update({k:str(v) for k,v in kw.items()});return E.SubElement(screen,'Widget',at)
def image(name,x,y,w,h,file):widget(30,name,x,y,w,h,Bitmap=file)
def number(name,x,y,w,h,source,prefix,digits=2,blank=0,align=0):widget(32,name,x,y,w,h,BitmapList='|'.join([f'{prefix}{n}.png' for n in range(10)]+[f'{prefix}0.png']),Digits=digits,Alignment=align,Value_Src=source,Spacing=0,Blanking=blank)
def imagelist(name,x,y,w,h,source,files):widget(31,name,x,y,w,h,BitmapList='|'.join(f'({i}):{f}' for i,f in enumerate(files)),Alignment=0,DefaultIndex=0,Value_Src=source,Index_Src=source,Spacing=0,Blanking=0)
image('Background',0,0,410,502,'background.png')
imagelist('BatteryPercent',138,92,134,34,'0841',[f'power{n}.png' for n in range(101)])
imagelist('Hour12',10,156,184,180,'0811',[f'hour{h%12}.png' for h in range(24)])
image('Colon',194,156,22,180,'colon.png');number('Minute',216,156,184,180,'1011','large')
imagelist('AMPM',174,329,62,34,'0811',['AM.png']*12+['PM.png']*12)
imagelist('Weekday',83,383,110,36,'2012',[f'week{i}.png' for i in range(7)])
number('Day',207,383,44,36,'1812','small');image('Slash',251,383,18,36,'slash.png');number('Month',269,383,44,36,'1012','small')
E.indent(root);E.ElementTree(root).write(P/'DaiCaMinimal.fprj',encoding='utf-8',xml_declaration=True)
def preview(hour,minute=49,battery=87,week=3,day=28,month=10):
 im=ims['background.png'].copy()
 def paste(file,x,y):im.paste(ims[file],(x,y))
 paste(f'power{battery}.png',138,92);paste(f'hour{hour%12}.png',10,156);paste('colon.png',194,156)
 for i,c in enumerate(f'{minute:02d}'):paste(f'large{c}.png',216+i*92,156)
 paste('AM.png' if hour<12 else 'PM.png',174,329);paste(f'week{week}.png',83,383)
 for i,c in enumerate(f'{day:02d}'):paste(f'small{c}.png',207+i*22,383)
 paste('slash.png',251,383)
 for i,c in enumerate(f'{month:02d}'):paste(f'small{c}.png',269+i*22,383)
 return im.convert('RGB')
preview(23).save(P/'preview-full.png');save(preview(23).resize((244,298),Image.Resampling.LANCZOS),'preview.png')
sheet=Image.new('RGB',(410*3,502*2),'#222222')
for i,(h,m,b) in enumerate([(0,0,100),(11,59,87),(12,0,9),(13,8,50),(23,49,1),(22,22,0)]):sheet.paste(preview(h,m,b),((i%3)*410,(i//3)*502))
sheet.save(P/'preview-checks.png')
# Verify all lookup indexes, sources and PNGs before compilation.
assert len(list(screen))==10
for w in screen:
 x,y,ww,hh=[int(w.get(k)) for k in ['X','Y','Width','Height']];assert x>=0 and y>=0 and x+ww<=410 and y+hh<=502
for f in I.glob('*.png'):
 with Image.open(f) as im:assert im.mode=='P'
buf=io.BytesIO()
with zipfile.ZipFile(buf,'w',zipfile.ZIP_DEFLATED) as z:
 for f in sorted(P.rglob('*')):
  if f.is_file() and f.name!='preview-checks.png' and not (f.stem.startswith('hour') and int(f.stem[4:])>=12):z.write(f,Path('DaiCaMinimal')/f.relative_to(P))
Path('redmi5lite/assets/watchface.zip.b64').write_text(base64.b64encode(buf.getvalue()).decode()+'\n')
print('Created',P,'packaged',len(buf.getvalue()),'bytes')
