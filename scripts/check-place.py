"""Check the built artifact's actual script hierarchy and entry points, not source text."""
import sys
import xml.etree.ElementTree as ET

root = ET.parse(sys.argv[1]).getroot()
instances = {}

def visit(item, path):
    name = item.find('./Properties/string[@name="Name"]')
    path += '/' + (name.text if name is not None else item.attrib['class'])
    instances[path] = item
    for child in item.findall('Item'):
        visit(child, path)

for item in root.findall('Item'):
    visit(item, '')

expected = {
    '/ReplicatedStorage/Shared/Construction': 'ModuleScript',
    '/ReplicatedStorage/Shared/MachineVisual': 'ModuleScript',
    '/ServerScriptService/Server': 'Script',
    '/ServerScriptService/Server/BuildServer': 'ModuleScript',
    '/StarterPlayer/StarterPlayerScripts/Client': 'LocalScript',
    '/StarterPlayer/StarterPlayerScripts/Client/BuildController': 'ModuleScript',
    '/StarterPlayer/StarterPlayerScripts/Client/BuildUI': 'ModuleScript',
    '/StarterPlayer/StarterPlayerScripts/Client/PointerRay': 'ModuleScript',
}
for path, kind in expected.items():
    item = instances[path]
    assert item.attrib['class'] == kind, (path, item.attrib)
    source = item.find('./Properties/*[@name="Source"]')
    assert source is not None and source.text and source.text.strip(), path
    disabled = item.find('./Properties/bool[@name="Disabled"]')
    assert disabled is None or disabled.text == 'false', path

print(f'PASS Rojo artifact: {len(expected)} expected scripts with source in their runtime paths')
