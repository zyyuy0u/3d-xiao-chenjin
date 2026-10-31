"""Validate public links, model downloads and the cartoon-only asset boundary."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import hashlib,json,re,zipfile

ROOT=Path(__file__).resolve().parents[1]
GROUPS={'hello_kitty_100mm','ghost_100mm','halloween_pumpkin_100mm','zongzi_assembly_3parts_color_100mm',
    'zongzi_assembly_3parts_100mm','zongzi_assembly_100mm','zongzi_multicolor_100mm','zongzi_100mm'}
class Links(HTMLParser):
    def __init__(self):super().__init__();self.values=[];self.articles=0
    def handle_starttag(self,tag,attrs):
        if tag=='article':self.articles+=1
        for key,value in attrs:
            if key in ('href','src') and value:self.values.append(value)

total_links=0
for page in ROOT.glob('*.html'):
    content=page.read_text();parser=Links();parser.feed(content)
    assert not any(p in content for p in ['/Users/','file://','actual_smile','actual_three_quarter','revision_2','revision_3','真人']),page
    if page.name in ['index.html','00_作品總覽.html']:assert 'store.js' in content
    for url in parser.values:
        u=urlsplit(url)
        if u.scheme or u.netloc or not u.path:continue
        assert not u.path.startswith('/'),(page.name,url,'must work below GitHub project path')
        target=(page.parent/unquote(u.path)).resolve()
        assert target.is_file(),(page.name,url)
        assert ROOT in target.parents,(page.name,url)
        total_links+=1

manifest=json.loads((ROOT/'models.json').read_text())['models'];assert len(manifest)==23
assert len(list(ROOT.glob('*.3mf')))==23
for model in manifest:
    p=ROOT/model['file'];data=p.read_bytes()
    assert len(data)==model['bytes'] and hashlib.sha256(data).hexdigest()==model['sha256'],p
    assert p.name.startswith(('萬聖節_','幽靈_','HelloKitty_','粽子'))
    with zipfile.ZipFile(p) as z:
        assert z.testzip() is None
        if 'Metadata/project_settings.config' in z.namelist():
            cfg=json.loads(z.read('Metadata/project_settings.config'))
            assert cfg['printer_settings_id']=='Bambu Lab X1 Carbon 0.4 nozzle'
            if 'extruder_variant_list' in cfg:
                count=len(cfg['filament_colour']);variants=cfg['filament_extruder_variant'];indices=cfg['filament_self_index']
                assert len(variants)==len(indices) and len(variants)>=count
                assert set(map(int,indices))==set(range(1,count+1)),p

images=list((ROOT/'assets').rglob('*'))
for p in images:
    if p.is_file():
        rel=p.relative_to(ROOT/'assets')
        assert len(rel.parts)==2 and rel.parts[0] in GROUPS and p.suffix=='.png',p
for p in ROOT.rglob('*'):
    if not p.is_file() or '.git' in p.parts:continue
    assert p.stat().st_size<100*1024*1024,p
    assert p.suffix.lower() not in ['.jpg','.jpeg','.heic','.log','.gcode','.blend','.stl'],p
    assert not any(s in p.name for s in ['真人','actual_smile','actual_three_quarter']),p
    if p.suffix in ['.html','.json','.txt','.md']:
        text=p.read_text()
        assert not re.search(r'(?:gh[pousr]_[A-Za-z0-9]{25,}|github_pat_[A-Za-z0-9_]{30,})',text),p
        assert '/Users/' not in text and 'file://' not in text,p
print(f'Passed: 4 product designs, 23 intact 3MFs, {total_links} relative links, no portrait-photo assets.')

products=json.loads((ROOT/'products.json').read_text())
assert len(products)==4 and {p['id'] for p in products}=={'ghost','pumpkin','zongzi','kitty'}
model_files={p['file'] for p in manifest}
for product in products:
    assert {v['construction'] for v in product['variants']}=={'一體成型','分件組裝'},product['id']
    assert any(v['id']=='solid-color' and v['construction']=='一體成型' for v in product['variants']),product['id']
    assert len({v['id'] for v in product['variants']})==len(product['variants'])
    for v in product['variants']:
        assert (ROOT/v['image']).is_file() and (ROOT/v['guide']).is_file()
        assert set(v['files'])<=model_files
        if v['id']=='solid-color':
            for name in v['files']:
                with zipfile.ZipFile(ROOT/name) as z:
                    cfg=json.loads(z.read('Metadata/project_settings.config'))
                    assert len(cfg['filament_colour'])==(6 if product['id']=='kitty' else 4)
                    assert cfg['enable_prime_tower']=='1'
                    from xml.etree import ElementTree as ET
                    c=ET.fromstring(z.read('Metadata/model_settings.config'))
                    obj=c.findall('object');assert len(obj)==1
                    parts=obj[0].findall('part');assert len(parts)==len(cfg['filament_colour'])
                    assignments=[next(m.get('value') for m in part.findall('metadata') if m.get('key')=='extruder') for part in parts]
                    assert set(map(int,assignments))==set(range(1,len(parts)+1))
        with zipfile.ZipFile(ROOT/v['bundle']) as z:
            assert z.testzip() is None
            assert {n for n in z.namelist() if n.endswith('.3mf')}==set(v['files'])
            for name in v['files']:
                assert hashlib.sha256(z.read(name)).digest()==hashlib.sha256((ROOT/name).read_bytes()).digest()
print('Passed: all four products expose both construction modes; every variant ZIP contains its exact selected model files.')
