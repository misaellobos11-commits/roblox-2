from pathlib import Path
import xml.etree.ElementTree as ET
import sys
original=ET.parse(sys.argv[1]).getroot()
updated=ET.parse(sys.argv[2]).getroot()
changes=[]
allowed={
 '/ReplicatedStorage/Shared/MachineCatalog',
 '/ReplicatedStorage/Shared/MachineVisual',
 '/StarterPlayer/StarterPlayerScripts/Client/BuildUI',
}
if '--86' in sys.argv:
    allowed.add('/StarterPlayer/StarterPlayerScripts/Client/BuildController')
if '--87-delta' in sys.argv:
    allowed.remove('/ReplicatedStorage/Shared/MachineCatalog')
if '--88' in sys.argv or '--88-delta' in sys.argv:
    allowed.update({'/ServerScriptService/Server/BuildServer','/ServerScriptService/Server/FactorySimulation'})
    if '--88' in sys.argv:
        allowed.add('/StarterPlayer/StarterPlayerScripts/Client/BuildController')
def compare(a,b,path=''):
    assert a.tag==b.tag and a.attrib==b.attrib,(path,a.tag,b.tag)
    if a.tag=='Item': path+='/'+a.findtext("Properties/string[@name='Name']",'')
    if a.text!=b.text:
        assert a.attrib.get('name')=='Source' and path in allowed,('Unexpected content change',path,a.attrib)
        changes.append(path)
    assert len(a)==len(b),path
    for x,y in zip(a,b):compare(x,y,path)
compare(original,updated)
assert set(changes)==allowed and len(changes)==len(allowed),changes
print(f'PASS place preservation: exactly {len(allowed)} active scripts changed; original assets and backups intact')
