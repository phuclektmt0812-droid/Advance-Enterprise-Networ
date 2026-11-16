#!/usr/bin/env python3
"""Create a legible report graphic; editable source is the .drawio file."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math
R = Path(__file__).resolve().parents[1]
out = R / 'docs' / 'TVI_Logical_Topology.png'
W, H = 1900, 970
im = Image.new('RGB', (W,H), '#FFFFFF')
d = ImageDraw.Draw(im)
base = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
bold = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
font = ImageFont.truetype(base, 19)
small = ImageFont.truetype(base, 16)
tiny = ImageFont.truetype(base, 14)
fb = ImageFont.truetype(bold, 21)
ft = ImageFont.truetype(bold, 29)

def txt(x, y, s, f=font, fill='#233344', anchor='mm'):
    d.text((x, y), s, font=f, fill=fill, anchor=anchor)

def shape(x1,y1,x2,y2,text,fill='#EEF4FC',outline='#9BADC0',rad=13,ff=font):
    d.rounded_rectangle((x1,y1,x2,y2), radius=rad, fill=fill, outline=outline, width=2)
    txt((x1+x2)//2,(y1+y2)//2,text,ff)

def edge(x1,y1,x2,y2,color='#667788',width=4,dashed=False):
    if not dashed:
        d.line((x1,y1,x2,y2), fill=color, width=width)
    else:
        dist=math.hypot(x2-x1,y2-y1)
        if not dist: return
        ux,uy=(x2-x1)/dist,(y2-y1)/dist
        length=0
        while length<dist:
            end=min(length+13,dist)
            d.line((x1+ux*length,y1+uy*length,x1+ux*end,y1+uy*end),fill=color,width=width)
            length+=23

txt(W//2,44,'TECHVIET INNOVATIONS  |  THREE-SITE NETWORK LAB',ft)
# Underlay ISP at top
shape(470,100,680,184,'ISP-A  |  AS64501',fill='#FFF2D8',ff=fb)
shape(1220,100,1430,184,'ISP-B  |  AS64502',fill='#FFF2D8',ff=fb)
edge(680,142,1220,142,color='#BF913B',width=6)
txt(950,122,'eBGP ISP interconnect',small)
shape(140,109,374,174,'TEST HTTP / DNS',fill='#E9F7E8',ff=fb)
edge(374,142,470,142,color='#5C9761',width=4)
txt(257,193,'192.0.2.18',small)
positions=[('HCMC HQ','10.10.0.0/16','AS65010',70),('HANOI R&D','10.20.0.0/16','AS65020',730),('DA NANG LOGISTICS','10.30.0.0/16','AS65030',1390)]
for site,net,asn,x in positions:
    y=315
    d.rounded_rectangle((x,y,x+440,y+490),radius=19, fill='#FAFCFF',outline='#B9C4D3',width=3)
    txt(x+220,y+42,site,fb)
    txt(x+220,y+76,f'{net}  •  {asn}',small)
    shape(x+26,y+127,x+197,y+205,'R1 — ACTIVE',fill='#E1EDFF',ff=fb)
    shape(x+245,y+127,x+414,y+205,'R2 — STANDBY',fill='#E1EDFF',ff=fb)
    edge(x+197,y+162,x+245,y+162,width=3)
    txt(x+220,y+146,'OSPF',tiny)
    edge(x+110,y+205,x+110,y+283,color='#547BA0')
    edge(x+330,y+205,x+330,y+283,color='#547BA0')
    shape(x+26,y+283,x+197,y+363,'SW1 / VLANs',fill='#DEF5E7',ff=fb)
    shape(x+245,y+283,x+414,y+363,'SW2 / VLANs',fill='#DEF5E7',ff=fb)
    edge(x+197,y+323,x+245,y+323,color='#479875',width=6)
    txt(x+220,y+309,'LACP',tiny)
    shape(x+31,y+401,x+192,y+455,'CORP CLIENT',fill='#F1F2FB',ff=font)
    shape(x+250,y+401,x+409,y+455,'GUEST CLIENT',fill='#FEEDF0',ff=font)
    edge(x+110,y+363,x+110,y+401,width=3)
    edge(x+330,y+363,x+330,y+401,width=3)

# Explain provider connectivity without crossing the site cards.
txt(950,248,'WAN: each site R1 connects to ISP-A; each site R2 connects to ISP-B',small)
txt(330,829,'HQ DHCP/DNS 10.10.60.10   |   Automation 10.10.99.50',tiny)
# Overlay explained as visually distinct bottom banner.
shape(82,850,1815,924,'GRE over IPsec + BGP: HCMC-R1 ↔ HANOI-R1 and DANANG-R1   |   HCMC-R2 ↔ HANOI-R2 and DANANG-R2',
      fill='#EEE8FA',outline='#9C8ACA',ff=font)
txt(950,947,'Illustrative topology. Exact cable ports are documented in interface_matrix.csv; Draw.io file is editable.',tiny)
im.save(out, optimize=True)
print(out)
