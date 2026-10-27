#!/usr/bin/env python3
"""Remove atmospheric veil and make existing campus lanterns illuminate at night."""
import copy
import xml.etree.ElementTree as ET
from build import BASE,replace_once
from build_817 import main as build_previous,OUTPUT as PREVIOUS
from build_812 import set_prop
from world.scene import prop

OUTPUT=BASE.parent/'build'/'Matterloom_8_18_Noche_Clara_y_Focos.rbxlx'
WORLD=OUTPUT.parent/'Matterloom_Canyon_World_818.rbxmx'

def name(i):return i.findtext("Properties/string[@name='Name']")
def patch_client(s):
    s=replace_once(s,'    Lighting.ExposureCompensation = .08 * look.night',
        '''    Lighting.ExposureCompensation = .18 * look.night
    -- Keep both Roblox atmosphere and legacy distance fog clear all day.
    Lighting.FogStart = 100000
    Lighting.FogEnd = 1000000''')
    s=replace_once(s,'        atmosphere.Density = .16 + .025 * look.night',
        '        atmosphere.Density = 0\n        atmosphere.Haze = 0')
    s=replace_once(s,'        atmosphere.Glare = .04 * (1 - look.night)','        atmosphere.Glare = 0')
    s=replace_once(s,'    if correction then correction.TintColor = color(look.tint) end',
        '''    if correction then
        correction.TintColor = color(look.tint)
        -- Preserve shadow detail when the sun is below the horizon.
        correction.Contrast = .13 - .10 * look.night
    end''')
    s=replace_once(s,'        lamp.Brightness = base * (.15 + 2.35 * look.night)',
        '''        lamp.Brightness = base * (.15 + 2.35 * look.night)
        lamp.Enabled = look.night > .01''')
    return s

def main():
    build_previous();original=ET.parse(PREVIOUS).getroot();root=copy.deepcopy(original)
    world=next(i for i in root.iter('Item') if name(i)=='MatterloomWorld')
    lighting=next(i for i in root if i.get('class')=='Lighting')
    touched={lighting.get('referent')}
    for kind,key,val in [('float','FogStart',100000),('float','FogEnd',1000000)]:set_prop(lighting,kind,key,val)
    for i in lighting.findall('Item'):
        if i.get('class')=='Atmosphere':
            for key in ('Density','Haze','Glare','Offset'):set_prop(i,'float',key,0)
    lanterns=[i for i in world.iter('Item') if name(i)=='CyanLantern']
    assert len(lanterns)==124
    added=0
    for bulb in lanterns:
        lamps=[i for i in bulb if i.get('class')=='PointLight']
        assert len(lamps)<=1
        if lamps:
            lamp=lamps[0];touched.add(lamp.get('referent'))
        else:
            added+=1
            lamp=ET.SubElement(bulb,'Item',{'class':'PointLight','referent':f'RBX_LAMP818_{added}'})
            ET.SubElement(lamp,'Properties');prop(lamp,'string','Name','LampLight')
        # Broad, unshadowed pools from the existing luminous heads; no new posts/models.
        for kind,key,val in [('Color3','Color',(238,229,209)),('float','Brightness',.9),
                              ('float','Range',48),('bool','Shadows',False),('bool','Enabled',False)]:
            set_prop(lamp,kind,key,val)
    assert added==116
    for lamp in world.iter('Item'):
        if lamp.get('class')=='PointLight' and name(lamp)=='PerimeterLight':
            touched.add(lamp.get('referent'));set_prop(lamp,'bool','Enabled',False)
    changes=set()
    for i in root.iter('Item'):
        source=i.find("Properties/ProtectedString[@name='Source']")
        if source is None:continue
        old=source.text or '';new=old
        if name(i)=='MatterloomDayNightClient':new=patch_client(old)
        elif name(i)=='MatterloomDayNight':
            night='{67,79,106}, {88,99,126}, {115,139,176}, {222,233,255}'
            assert old.count(night)==4
            new=old.replace(night,'{108,116,134}, {130,138,155}, {115,139,176}, {238,244,255}')
        elif 'PRUEBAS · 8.17' in old:new=replace_once(old,'PRUEBAS · 8.17','PRUEBAS · 8.18')
        if new!=old:
            touched.add(i.get('referent'));source.text=new;changes.add(name(i))
    assert changes=={'MatterloomDayNight','MatterloomDayNightClient','BuildUI'},changes
    # Normalize only the documented modifications to verify the rest of the place exactly.
    originals={i.get('referent'):i for i in original.iter('Item')}
    normalized=copy.deepcopy(root)
    def restore(parent):
        for i in list(parent):
            ref=i.get('referent','')
            if ref.startswith('RBX_LAMP818_'):parent.remove(i)
            elif ref in touched:
                index=list(parent).index(i);parent.remove(i);parent.insert(index,copy.deepcopy(originals[ref]))
            else:restore(i)
    restore(normalized)
    assert ET.tostring(normalized)==ET.tostring(original),'Unrelated geometry/gameplay changed'
    refs=[i.get('referent') for i in root.iter('Item')];assert len(refs)==len(set(refs))
    ET.ElementTree(root).write(OUTPUT,encoding='utf-8',xml_declaration=True)
    standalone=ET.Element('roblox',{'version':'4'});standalone.append(world)
    ET.ElementTree(standalone).write(WORLD,encoding='utf-8',xml_declaration=True)
    scripts=OUTPUT.parent/'818-scripts';scripts.mkdir(exist_ok=True)
    for i in root.iter('Item'):
        if name(i) in ('MatterloomDayNight','MatterloomDayNightClient','MatterloomDayNightServer'):
            (scripts/(name(i)+'.luau')).write_text(i.findtext("Properties/ProtectedString[@name='Source']"))
    print('PASS only lighting, day/night visuals and version label changed; all geometry/gameplay preserved')
    print('Built',OUTPUT)
if __name__=='__main__':main()
