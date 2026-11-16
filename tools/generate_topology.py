#!/usr/bin/env python3
"""Generate editable Draw.io and DOT/SVG conceptual topology files.

Exact interface-to-interface wiring is in docs/interface_matrix.csv.
"""
from __future__ import annotations
from pathlib import Path
import subprocess
import xml.etree.ElementTree as ET
from html import escape
from validate_plan import load_plan

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs'


def main():
    root = ET.Element('mxfile', host='app.diagrams.net', modified='2026-11-13T00:00:00Z',
                      agent='TVI lab build', version='24.1.0', type='device')
    diag = ET.SubElement(root, 'diagram', name='TVI logical topology', id='tvi-main')
    model = ET.SubElement(diag, 'mxGraphModel', dx='1400', dy='850', grid='1', gridSize='10',
                           guides='1', tooltips='1', connect='1', arrows='1', fold='1',
                           page='1', pageScale='1', pageWidth='1500', pageHeight='1020', math='0', shadow='0')
    layer = ET.SubElement(model, 'root')
    ET.SubElement(layer, 'mxCell', id='0')
    ET.SubElement(layer, 'mxCell', id='1', parent='0')

    def box(key, label, x, y, w, h, *, fill='#EDF3FA', stroke='#64748B', font=13, round=True, parent='1'):
        attrs = {'id':key, 'value': label, 'style': f'rounded={int(round)};whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};fontSize={font};fontColor=#1E293B;align=center;verticalAlign=middle;',
                 'vertex':'1', 'parent':parent}
        cell = ET.SubElement(layer, 'mxCell', **attrs)
        ET.SubElement(cell, 'mxGeometry', x=str(x), y=str(y), width=str(w), height=str(h), **{'as':'geometry'})
    def edge(key, src, dst, label='', dashed=False, color='#70839A'):
        style = f'edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=none;strokeColor={color};strokeWidth=2;'
        if dashed: style += 'dashed=1;dashPattern=8 4;'
        cell = ET.SubElement(layer, 'mxCell', id=key, value=label,
                             style=style, edge='1', parent='1', source=src, target=dst)
        ET.SubElement(cell, 'mxGeometry', relative='1', **{'as':'geometry'})

    box('ispa', 'ISP-A\nAS 64501', 480, 55, 160, 60, fill='#FDECCB', font=14)
    box('ispb', 'ISP-B\nAS 64502', 815, 55, 160, 60, fill='#FDECCB', font=14)
    box('internet', 'TEST INTERNET\n192.0.2.18', 310, 55, 145, 60, fill='#DAF5E6')
    edge('isp-peer', 'ispa', 'ispb', 'eBGP inter-provider', color='#B88722')
    edge('inet-conn', 'internet', 'ispa')
    positions = {'hcmc': 30, 'hanoi': 485, 'danang': 940}
    plan = load_plan()
    for name, x in positions.items():
        spec = plan['sites'][name]
        box('zone-'+name, f'{spec["label"]}\n{spec["base"]}.0.0/16  |  AS {spec["asn"]}',
            x, 285, 415, 435, fill='#FAFCFF', stroke='#94A3B8', font=15)
        for idx in (1, 2):
            router = f'{name}-r{idx}'
            switch = f'{name}-sw{idx}'
            box(router, f'{name.upper()}-R{idx}\nHSRP | OSPF | BGP', x + 30 + (idx-1)*195, 350,
                165, 65, fill='#DDEAFE')
            box(switch, f'{name.upper()}-SW{idx}\nRSTP | LACP', x + 30 + (idx-1)*195, 475,
                165, 65, fill='#DBF3E6')
            edge(f'wan-{router}', router, 'ispa' if idx == 1 else 'ispb',
                 'WAN / eBGP', color='#AA7740')
            edge(f'access-{router}', router, switch, '802.1Q', color='#3D6F94')
        edge(f'site-igp-{name}', f'{name}-r1', f'{name}-r2', 'OSPF / iBGP')
        edge(f'ether-{name}', f'{name}-sw1', f'{name}-sw2', '2 x LACP')
        box(f'{name}-corp', f'CORP\nVLAN {10 if name == "hcmc" else 20 if name == "hanoi" else 30}',
            x+40, 585, 135, 50, fill='#EEE9FA')
        box(f'{name}-guest', 'GUEST\nVLAN 50', x+240, 585, 135, 50, fill='#FCE9EF')
        edge(f'client-{name}', f'{name}-corp', f'{name}-sw1')
        edge(f'guest-{name}', f'{name}-guest', f'{name}-sw2')
        if name == 'hcmc':
            box('dhcp', 'HQ DHCP + DNS\n10.10.60.10', x+45, 655, 140, 42, fill='#FFF3CB', font=11)
            box('automation', 'AUTOMATION\n10.10.99.50', x+232, 655, 145, 42, fill='#FFF3CB', font=11)
            edge('dhcp-edge', 'dhcp', f'{name}-sw1')
            edge('automation-edge', 'automation', f'{name}-sw1')
    for site in ('hanoi', 'danang'):
        edge(f'overlayA-{site}', 'hcmc-r1', f'{site}-r1', 'GRE + IPsec / BGP', True, '#7C3AED')
        edge(f'overlayB-{site}', 'hcmc-r2', f'{site}-r2', 'GRE + IPsec / BGP', True, '#7C3AED')
    box('legend', 'DASHED PURPLE: IPsec GRE overlays    |    ORANGE: ISP/eBGP    |    BLUE: LAN/routing\nSee interface_matrix.csv for exact cables and port names.',
        390, 760, 690, 65, fill='#F8FAFC', font=12)
    ET.indent(root, space='  ')
    (OUT / 'TVI_Logical_Topology.drawio').write_bytes(ET.tostring(root, encoding='utf-8', xml_declaration=True))

    # Also supply a universally viewable SVG. Draw.io is the editable source.
    dot = ['graph TVI {', 'graph [rankdir=TB, bgcolor=white, pad=0.4, splines=polyline];',
           'node [shape=box, style="rounded,filled", fillcolor="#EAF0F7", fontname="DejaVu Sans"];',
           'edge [color="#718096", fontname="DejaVu Sans", fontsize=9];',
           '"ISP-A" [fillcolor="#FFF0C7"]; "ISP-B" [fillcolor="#FFF0C7"];',
           '"ISP-A" -- "ISP-B" [label="eBGP"];',
           '"INTERNET-TEST" -- "ISP-A";']
    for site in plan['sites']:
        s = site.upper()
        dot += [f'subgraph cluster_{site} {{', f'label="{plan["sites"][site]["label"]}";',
                'style="rounded"; color="#94A3B8";']
        for n in (1, 2):
            dot += [f'"{s}-R{n}" [fillcolor="#D8E7FC"];',
                    f'"{s}-SW{n}" [fillcolor="#DCF4E6"];',
                    f'"{s}-R{n}" -- "{s}-SW{n}" [label="trunk"];']
        dot += [f'"{s}-R1" -- "{s}-R2" [label="OSPF/iBGP"];',
                f'"{s}-SW1" -- "{s}-SW2" [label="LACP x2"];', '}']
        dot += [f'"{s}-R1" -- "ISP-A";', f'"{s}-R2" -- "ISP-B";']
    for site in ('HANOI', 'DANANG'):
        dot += [f'"HCMC-R1" -- "{site}-R1" [style=dashed, color=purple, label="IPsec GRE"];',
                f'"HCMC-R2" -- "{site}-R2" [style=dashed, color=purple, label="IPsec GRE"];']
    dot += ['"HQ-DHCP-DNS" -- "HCMC-SW1";', '"AUTOMATION" -- "HCMC-SW1";', '}']
    (OUT / 'TVI_Logical_Topology.dot').write_text('\n'.join(dot), encoding='utf-8')
    subprocess.run(['dot', '-Tsvg', str(OUT / 'TVI_Logical_Topology.dot'),
                    '-o', str(OUT / 'TVI_Logical_Topology.svg')], check=True)
    print('Generated editable Draw.io topology and SVG.')


if __name__ == '__main__':
    main()
