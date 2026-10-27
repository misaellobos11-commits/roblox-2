"""Round-trip generated parts through Rojo's Roblox XML reader/writer."""
import math
from pathlib import Path
import json
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

source=Path(sys.argv[1]).resolve()
def geometry(path):
    records=[]
    for item in ET.parse(path).iter('Item'):
        if item.get('class')=='PointLight':
            props=item.find('Properties');record=['PointLight']
            for key,default in (('Brightness','1'),('Range','8')):
                record.append(float(props.findtext(f"*[@name='{key}']",default)))
            for axis in ('R','G','B'):
                record.append(float(props.findtext(f"Color3[@name='Color']/{axis}",'1')))
            for key,default in (('Enabled','true'),('Shadows','false')):
                record.append(props.findtext(f"*[@name='{key}']",default))
            records.append(tuple(record))
            continue
        if item.get('class') not in ('Part','WedgePart','SpawnLocation'):continue
        props=item.find('Properties');record=[item.get('class')]
        for name in ('size','CFrame'):
            value=props.find(f"*[@name='{name}']");assert value is not None,name
            record.extend(float(n.text) for n in value)
        for name in ('Color3uint8','Material','shape','Anchored','CanCollide','CanQuery'):
            record.append(props.findtext(f"*[@name='{name}']"))
        records.append(tuple(record))
    return records
with tempfile.TemporaryDirectory() as directory:
    folder=Path(directory);project=folder/'check.project.json';output=folder/'check.rbxlx'
    project.write_text(json.dumps({'name':'CanyonSchema','tree':{'$className':'DataModel',
                          'Workspace':{'World':{'$path':str(source)}}}}))
    subprocess.run(['/workspace/tools/bin/rojo','build',str(project),'-o',str(output)],check=True)
    original,normalized=geometry(source),geometry(output)
    assert len(original)==len(normalized)
    for index,(a,b) in enumerate(zip(original,normalized)):
        assert len(a)==len(b)
        for x,y in zip(a,b):
            equal=math.isclose(x,y,rel_tol=1e-6,abs_tol=1e-4) if isinstance(x,float) else x==y
            assert equal,('Geometry changed during Roblox schema round-trip',index,x,y)
print('PASS Roblox XML round-trip: geometry, collision/query flags and real light properties')
