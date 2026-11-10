import sys, xml.etree.ElementTree as ET, textwrap
src, out = sys.argv[1], sys.argv[2]
root = ET.parse(src).getroot()
lines = []
def txt(e): return ' '.join(''.join(e.itertext()).split())
def walk(e, depth):
    tag = e.tag
    if tag == 'title':
        lines.append(''); lines.append('#'*min(depth,6)+' '+txt(e)); return
    if tag in ('p',):
        t = txt(e)
        if t: lines.extend(textwrap.wrap(t, 110)); lines.append('')
        return
    if tag == 'table-wrap':
        lab = e.find('label'); cap = e.find('caption')
        lines.append('[TABLE] '+(txt(lab) if lab is not None else '')+' '+(txt(cap) if cap is not None else ''))
        for tr in e.iter('tr'):
            lines.append(' | '.join(txt(c) for c in tr if c.tag in ('td','th')))
        for fn in e.iter('table-wrap-foot'): lines.append('[foot] '+txt(fn))
        lines.append(''); return
    if tag == 'fig':
        lab = e.find('label'); cap = e.find('caption')
        lines.append('[FIGURE] '+(txt(lab) if lab is not None else '')+' '+(txt(cap) if cap is not None else '')); lines.append(''); return
    if tag == 'list-item':
        t = txt(e); lines.extend(textwrap.wrap('- '+t,110, subsequent_indent='  ')); return
    if tag == 'ref':
        lines.append('REF: '+txt(e)); return
    if tag == 'sec': depth += 1
    for c in e: walk(c, depth)
front = root.find('front')
if front is not None:
    am = front.find('.//abstract')
    if am is not None: lines.append('# ABSTRACT'); walk(am,1)
for part in ('body','back'):
    p = root.find(part)
    if p is not None: lines.append('');lines.append('==== '+part.upper()+' ===='); walk(p,1)
open(out,'w').write('\n'.join(lines))
