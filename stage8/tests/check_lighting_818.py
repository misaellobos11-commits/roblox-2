"""Regression checks for visible lanterns without illumination and retained fog."""
import sys
import xml.etree.ElementTree as ET
root=ET.parse(sys.argv[1]).getroot()
def name(i):return i.findtext("Properties/string[@name='Name']")
def value(i,key):return i.findtext(f"Properties/*[@name='{key}']")
world=next(i for i in root.iter('Item') if name(i)=='MatterloomWorld')
lighting=next(i for i in root if i.get('class')=='Lighting')
lanterns=[i for i in world.iter('Item') if name(i)=='CyanLantern']
assert len(lanterns)==124
missing=[i for i in lanterns if not any(c.get('class')=='PointLight' for c in i)]
assert not missing,f'{len(missing)} of {len(lanterns)} visible lanterns still have no real light'
for bulb in lanterns:
    lights=[i for i in bulb if i.get('class')=='PointLight']
    assert len(lights)==1,'Duplicate light source on same fixture'
    lamp=lights[0]
    assert float(value(lamp,'Brightness'))>=.8
    assert 35<=float(value(lamp,'Range'))<=60
    assert value(lamp,'Shadows')=='false'
    assert value(lamp,'Enabled')=='false','Daytime fixtures should not spend light budget'
assert len([i for i in world.iter('Item') if i.get('class')=='PointLight'])==136
for a in lighting:
    if a.get('class')=='Atmosphere':
        for key in ('Density','Haze','Glare'):assert float(value(a,key))==0,(key,value(a,key))
assert float(value(lighting,'FogStart'))>=10000
assert float(value(lighting,'FogEnd'))>float(value(lighting,'FogStart'))
print('PASS clear atmosphere and 124 existing lanterns fitted with one real unshadowed light each; 136 total')
