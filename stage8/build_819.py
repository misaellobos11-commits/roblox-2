#!/usr/bin/env python3
"""Restyle distant canyon and sky while retaining the clear-night lighting and game."""
import copy
import xml.etree.ElementTree as ET
from build import BASE,replace_once
from build_818 import main as build_previous,OUTPUT as PREVIOUS
from build_812 import set_prop
from world.scene import prop
from world.horizon_819 import generate
OUTPUT=BASE.parent/'build'/'Matterloom_8_19_Canon_Estratificado_y_Cielo.rbxlx'
WORLD=OUTPUT.parent/'Matterloom_Canyon_World_819.rbxmx'

def name(i):return i.findtext("Properties/string[@name='Name']")
def main():
    build_previous();original=ET.parse(PREVIOUS).getroot();root=copy.deepcopy(original)
    workspace=next(i for i in root if i.get('class')=='Workspace')
    world=next(i for i in workspace if name(i)=='MatterloomWorld')
    landscape=next(i for i in world if name(i)=='Landscape')
    old=next(i for i in landscape if name(i)=='CanyonRockFormations')
    old_index=list(landscape).index(old);landscape.remove(old)
    landscape.insert(old_index,generate())
    lighting=next(i for i in root if i.get('class')=='Lighting')
    assert not any(i.get('class')=='Sky' for i in lighting)
    sky=ET.SubElement(lighting,'Item',{'class':'Sky','referent':'RBX_SKY819'})
    ET.SubElement(sky,'Properties');prop(sky,'string','Name','MatterloomDesertSky')
    # Roblox bundled sky assets need no external uploads or permissions.
    for face,suffix in (('Bk','bk'),('Dn','dn'),('Ft','ft'),('Lf','lf'),('Rt','rt'),('Up','up')):
        p=ET.SubElement(sky.find('Properties'),'Content',{'name':'Skybox'+face})
        ET.SubElement(p,'url').text=f'rbxasset://textures/sky/sky512_{suffix}.tex'
    for kind,key,val in [('bool','CelestialBodiesShown',True),('float','SunAngularSize',8),
                         ('float','MoonAngularSize',6),('int','StarCount',2200),
                         ('Vector3','SkyboxOrientation',(0,25,0))]:prop(sky,kind,key,val)
    terrain=next(i for i in workspace if i.get('class')=='Terrain')
    clouds=next(i for i in terrain if i.get('class')=='Clouds')
    for kind,key,val in [('bool','Enabled',True),('float','Cover',.58),('float','Density',.68),
                         ('Color3','Color',(244,242,237))]:set_prop(clouds,kind,key,val)
    old_workspace_props=copy.deepcopy(workspace.find('Properties'))
    set_prop(workspace,'Vector3','GlobalWind',(7,0,2))
    touched={clouds.get('referent')}
    for i in root.iter('Item'):
        source=i.find("Properties/ProtectedString[@name='Source']")
        if source is None:continue
        s=source.text or '';before=s
        if name(i)=='MatterloomDayNightClient':
            s=replace_once(s,"local lamps = {}",'''local terrain = workspace:FindFirstChildOfClass('Terrain')
local clouds = terrain and terrain:FindFirstChildOfClass('Clouds')
local lamps = {}''')
            s=replace_once(s,'    if correction then', '''    if clouds then
        clouds.Cover = .58 - .14 * look.night
        clouds.Density = .68 - .12 * look.night
        clouds.Color = Color3.fromRGB(244 - 104 * look.night, 242 - 88 * look.night, 237 - 63 * look.night)
    end
    if correction then''')
        if 'PRUEBAS · 8.18' in s:s=replace_once(s,'PRUEBAS · 8.18','PRUEBAS · 8.19')
        if before!=s:source.text=s;touched.add(i.get('referent'))
    normalized=copy.deepcopy(root)
    originals={i.get('referent'):i for i in original.iter('Item')}
    def restore(parent):
        for i in list(parent):
            ref=i.get('referent','')
            if ref=='RBX_SKY819':parent.remove(i)
            elif name(i)=='StratifiedCanyon':
                index=list(parent).index(i);parent.remove(i);parent.insert(index,copy.deepcopy(old))
            elif ref in touched:
                index=list(parent).index(i);parent.remove(i);parent.insert(index,copy.deepcopy(originals[ref]))
            else:restore(i)
    restore(normalized)
    ws=next(i for i in normalized if i.get('class')=='Workspace')
    ws.remove(ws.find('Properties'));ws.insert(0,old_workspace_props)
    assert ET.tostring(normalized)==ET.tostring(original),'Unrelated gameplay/environment changed'
    refs=[i.get('referent') for i in root.iter('Item')];assert len(refs)==len(set(refs))
    ET.ElementTree(root).write(OUTPUT,encoding='utf-8',xml_declaration=True)
    model=ET.Element('roblox',{'version':'4'});model.append(world)
    ET.ElementTree(model).write(WORLD,encoding='utf-8',xml_declaration=True)
    print('PASS changes limited to distant rock formations, sky/clouds/wind and version tag')
    print('Built',OUTPUT)
if __name__=='__main__':main()
