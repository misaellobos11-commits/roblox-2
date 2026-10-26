#!/usr/bin/env python3
"""Embed the editable canyon campus over 8.11, preserving factory gameplay."""
import math
import xml.etree.ElementTree as ET
from build import BASE, replace_once
from build_811 import main as build_previous, OUTPUT as PREVIOUS
from world.canyon import generate, config_source
from world.scene import prop

OUTPUT=BASE.parent/'build'/'Matterloom_8_12_Canon_Industrial.rbxlx'


def patch(name,source):
    if name=='MapConfig':return config_source()
    if name=='MapGenerator':return '''--!nonstrict
-- The editable environment is already embedded in the place.
local MapGenerator={}
function MapGenerator.build()
    local world=workspace:WaitForChild('MatterloomWorld')
    local preview=world:FindFirstChild('PreviewPlots')
    if preview then preview:Destroy() end
    return world:WaitForChild('Plaza'):WaitForChild('MatterloomLobbySpawn')
end
return MapGenerator
'''
    if name=='BuildServer':
        source=replace_once(source,'Color3.fromRGB(102,112,119)','Color3.fromRGB(82,91,99)')
        source=replace_once(source,'Color3.fromRGB(130,146,149) else Color3.fromRGB(115,126,132)',
                           'Color3.fromRGB(106,118,123) else Color3.fromRGB(93,103,110)')
        source=replace_once(source,'    local entrance=MapConfig.entryPoint(slot)',
                           '''    local entrance=MapConfig.entryPoint(slot)
    local entryDirection=MapConfig.entryDirection(slot)
    local tangent=Vector3.new(entryDirection.Z,0,-entryDirection.X)
    local entrySize=if entryDirection.X==0 then Vector3.new(28,1,24) else Vector3.new(24,1,28)''')
        source=replace_once(source,"slab(plot,'Entrada',Vector3.new(28,1,24)","slab(plot,'Entrada',entrySize")
        source=replace_once(source,'entrance+Vector3.new(18,3,0)','entrance+tangent*18+Vector3.new(0,3,0)')
        source=replace_once(source,'character:PivotTo(CFrame.new(session.spawn.Position+Vector3.new(0,4,0)) * CFrame.Angles(0,math.pi,0))',
                           '''local at=session.spawn.Position+Vector3.new(0,4,0)
            character:PivotTo(CFrame.lookAt(at,at-MapConfig.entryDirection(session.slot)))''')
    if name=='BuildUI':
        source=replace_once(source,'MATTERLOOM · 8.11 ASCENSORES','MATTERLOOM · 8.12 CAÑÓN')
        source=replace_once(source,'08.11 / CONEXIONES EN DOS ALTURAS','08.12 / COMPLEJO DEL CAÑÓN')
    return source


def set_prop(item,kind,name,value):
    for child in list(item.find('Properties')):
        if child.get('name')==name:item.find('Properties').remove(child)
    return prop(item,kind,name,value)


def main():
    build_previous()
    root=ET.parse(PREVIOUS).getroot();changed=[]
    targets={'/ReplicatedStorage/Shared/MapConfig',
             '/ServerScriptService/Server/MapGenerator',
             '/ServerScriptService/Server/BuildServer',
             '/StarterPlayer/StarterPlayerScripts/Client/BuildUI'}
    def visit(item,path=''):
        name=item.findtext("Properties/string[@name='Name']",'');path+='/'+name
        if path in targets:
            source=item.find("Properties/ProtectedString[@name='Source']")
            assert source is not None,path
            source.text=patch(name,source.text);changed.append(path)
        for child in item.findall('Item'):visit(child,path)
    for item in root.findall('Item'):visit(item)
    assert set(changed)==targets
    def service(name):
        return next(i for i in root.findall('Item') if i.attrib['class']==name)
    scene=generate();workspace=service('Workspace');workspace.append(scene.world)
    # These settings are visible in edit mode and remain in effect during Play.
    lighting=service('Lighting')
    for kind,name,value in [
        ('float','ClockTime',16.35),('float','Brightness',2.4),
        ('Color3','Ambient',(100,102,114)),('Color3','OutdoorAmbient',(143,133,119)),
        ('bool','GlobalShadows',True),('float','ShadowSoftness',.25),
        ('float','EnvironmentDiffuseScale',.7),('float','EnvironmentSpecularScale',.8),
        ('float','ExposureCompensation',.1),('float','FogEnd',4000),
    ]:set_prop(lighting,kind,name,value)
    atmosphere=scene.item(lighting,'Atmosphere','MatterloomAtmosphere')
    for kind,name,value in [('float','Density',.23),('float','Offset',.15),
                            ('Color3','Color',(224,201,172)),('Color3','Decay',(106,126,145)),
                            ('float','Glare',.12),('float','Haze',1.4)]:prop(atmosphere,kind,name,value)
    bloom=scene.item(lighting,'BloomEffect','MatterloomBloom')
    for name,val in [('Intensity',.13),('Size',20),('Threshold',1.4)]:prop(bloom,'float',name,val)
    correction=scene.item(lighting,'ColorCorrectionEffect','MatterloomColors')
    prop(correction,'float','Saturation',.03);prop(correction,'float','Contrast',.08)
    prop(correction,'Color3','TintColor',(255,246,232))
    terrain=next(i for i in workspace.findall('Item') if i.attrib['class']=='Terrain')
    clouds=scene.item(terrain,'Clouds','CanyonClouds')
    prop(clouds,'float','Cover',.42);prop(clouds,'float','Density',.55)
    prop(clouds,'Color3','Color',(245,230,211))
    camera=next(i for i in workspace.findall('Item') if i.attrib['class']=='Camera')
    # Elevated edit-mode overview; Roblox's normal player camera still takes over on Play.
    at=(680,530,780);target=(0,0,0)
    backward=[at[i]-target[i] for i in range(3)];mag=math.sqrt(sum(v*v for v in backward));backward=[v/mag for v in backward]
    right=[backward[2],0,-backward[0]];mag=math.hypot(right[0],right[2]);right=[v/mag for v in right]
    up=[backward[1]*right[2],backward[2]*right[0]-backward[0]*right[2],-backward[1]*right[0]]
    matrix=tuple(v for i in range(3) for v in (right[i],up[i],backward[i]))
    set_prop(camera,'CoordinateFrame','CFrame',(*at,*matrix))
    set_prop(camera,'CoordinateFrame','Focus',(*target,1,0,0,0,1,0,0,0,1))
    # Also emit the standalone world for schema round-trip checks and geometry previews.
    scene.root.remove(scene.world);standalone=ET.Element('roblox',{'version':'4'});standalone.append(scene.world)
    ET.ElementTree(standalone).write(OUTPUT.parent/'Matterloom_Canyon_World.rbxmx',encoding='utf-8',xml_declaration=True)
    ET.ElementTree(root).write(OUTPUT,encoding='utf-8',xml_declaration=True)
    print('Built',OUTPUT)


if __name__=='__main__':main()
