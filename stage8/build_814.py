#!/usr/bin/env python3
"""Five visual cleanup fixes requested after the 8.13 Studio screenshot."""
import xml.etree.ElementTree as ET
from build import BASE,replace_once
from build_813 import main as build_previous,OUTPUT as PREVIOUS,between
from build_812 import set_prop
from ui_814 import patch_ui
from world.canyon import generate
from world.refine_814 import refine

OUTPUT=BASE.parent/'build'/'Matterloom_8_14_Entorno_y_HUD.rbxlx'
WORLD=OUTPUT.parent/'Matterloom_Canyon_World_814.rbxmx'

def patch(name,s):
    if name=='BuildUI':return patch_ui(s)
    if name=='BuildController':
        s=replace_once(s,'    local function redrawMarkers()',
            (BASE/'patches/local-build-grid.luau').read_text()+'\n    local function redrawMarkers()')
        s=replace_once(s,'        ui:setMode(mode,selectedId,pending,chosen,count,confirmDelete)',
            '''        updateBuildGrid()
        local selection=selectedId and state and state.buildings[selectedId]
        ui:setMode(mode,selectedId,pending,if mode=='select' and selection then selection.machineType else chosen,count,confirmDelete)''')
        s=replace_once(s,'    local function previewAt()\n', '    local function previewAt()\n        updateBuildGrid()\n')
        s=replace_once(s,'        ui:setCatalogOpen(catalogOpen)','        ui:setCatalogOpen(catalogOpen)\n        updateBuildGrid()')
        s=replace_once(s,"    plot=workspace:WaitForChild('MatterloomPlots'):WaitForChild('Plot_'..player.UserId)",
            """    plot=workspace:WaitForChild('MatterloomPlots'):WaitForChild('Plot_'..player.UserId)
    for _,edge in ipairs(plot:GetChildren()) do
        if edge.Name=='BordeCian' then
            edge.Color=Color3.fromRGB(65,205,216);edge.Material=Enum.Material.Neon
        end
    end""")
    elif name=='BuildServer':
        s=replace_once(s,"local p=slab(parent,'BordeCian',size,at,CYAN,Enum.Material.Neon)",
            "local p=slab(parent,'BordeCian',size,at,Color3.fromRGB(48,97,102),Enum.Material.Metal)")
        s=between(s,'    for i=0,Construction.GRID_SIZE do','    addEdge(plot,',
            '    -- Grid lines are local to the owner and visible only while building.\n')
        s=between(s,"    local signPost=slab(plot,'PosteCartel'",'    local label=Instance.new',
            """    local signAt=entrance+tangent*23+Vector3.new(0,5,0)
    slab(plot,'PosteCartel',Vector3.new(1,5,1),entrance+tangent*23+Vector3.new(0,2.5,0),Color3.fromRGB(31,46,53),Enum.Material.Metal)
    local signBoard=slab(plot,'PlacaParcela',Vector3.new(14,4,.7),signAt,Color3.fromRGB(26,39,49),Enum.Material.Metal)
    signBoard.CFrame=CFrame.lookAt(signAt,signAt+entryDirection)
    local sign=Instance.new('SurfaceGui')
    sign.Name='CartelParcela'
    sign.Face=Enum.NormalId.Front
    sign.AlwaysOnTop=false
    sign.CanvasSize=Vector2.new(512,160)
    sign.SizingMode=Enum.SurfaceGuiSizingMode.FixedSize
    sign.LightInfluence=.4
    sign.MaxDistance=72
    sign.Parent=signBoard
""")
        s=replace_once(s,'    label.BackgroundTransparency=.05','    label.BackgroundTransparency=1')
        s=replace_once(s,'    label.TextSize=18','    label.TextSize=18\n    label.TextScaled=true\n    label.TextWrapped=true')
    return s

def main():
    build_previous();root=ET.parse(PREVIOUS).getroot();changed=[]
    targets={'/StarterPlayer/StarterPlayerScripts/Client/BuildController',
             '/StarterPlayer/StarterPlayerScripts/Client/BuildUI','/ServerScriptService/Server/BuildServer'}
    def visit(item,path=''):
        name=item.findtext("Properties/string[@name='Name']",'');path+='/'+name
        if path in targets:
            source=item.find("Properties/ProtectedString[@name='Source']")
            source.text=patch(name,source.text);changed.append(path)
        for child in item.findall('Item'):visit(child,path)
    for item in root.findall('Item'):visit(item)
    assert set(changed)==targets
    workspace=next(i for i in root if i.get('class')=='Workspace')
    old=next(i for i in workspace.findall('Item') if i.findtext("Properties/string[@name='Name']")=='MatterloomWorld')
    scene=refine(generate())
    for item in scene.world.iter('Item'):item.set('referent',item.get('referent').replace('RBX_CANYON_','RBX_CANYON814_'))
    index=list(workspace).index(old);workspace.remove(old);workspace.insert(index,scene.world)
    lighting=next(i for i in root if i.get('class')=='Lighting')
    for kind,name,value in [
        ('token','Technology',4),('token','LightingStyle',0),('bool','PrioritizeLightingQuality',True),
        ('string','TimeOfDay','16:12:00'),('float','ClockTime',16.2),('float','Brightness',2.5),
        ('Color3','Ambient',(64,57,52)),('Color3','OutdoorAmbient',(117,106,93)),
        ('Color3','ColorShift_Top',(33,19,8)),('float','EnvironmentDiffuseScale',.45),
        ('float','EnvironmentSpecularScale',.45),('float','ExposureCompensation',0),
        ('Color3','FogColor',(206,172,131)),('float','FogStart',300),('float','FogEnd',2500),
    ]:set_prop(lighting,kind,name,value)
    for item in lighting.findall('Item'):
        cls=item.get('class')
        if cls=='Atmosphere':
            for kind,name,value in [('float','Density',.16),('float','Haze',.6),('float','Glare',.04),
                ('Color3','Color',(232,200,158)),('Color3','Decay',(159,130,107))]:set_prop(item,kind,name,value)
        elif cls=='ColorCorrectionEffect':
            set_prop(item,'float','Contrast',.13);set_prop(item,'float','Saturation',.08)
            set_prop(item,'Color3','TintColor',(255,244,226))
        elif cls=='BloomEffect':set_prop(item,'float','Intensity',.08)
    ET.ElementTree(root).write(OUTPUT,encoding='utf-8',xml_declaration=True)
    standalone=ET.Element('roblox',{'version':'4'});standalone.append(scene.world)
    ET.ElementTree(standalone).write(WORLD,encoding='utf-8',xml_declaration=True)
    print('Built',OUTPUT)

if __name__=='__main__':main()
