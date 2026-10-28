"""Compact recognizable cargo, 3–6 parts each, within the existing belt envelope."""
from visuals.cargo_shapes import piece
from .content import expanded_items,lua

def shapes(data):
    parts=[];c=data['color'];dark=(53,68,78);silver=(186,203,209);gold=(201,152,81)
    def b(n,s,p,color=c,mat='Metal',rot=(0,0,0)):parts.append(piece(n,s,p,color,mat,rot=rot))
    def cyl(n,p,length,diam,color=c,axis='Y'):
        parts.append(piece(n,(length,diam,diam),p,color,shape='Cylinder',rot={'X':(0,0,0),'Y':(0,0,90),'Z':(0,90,0)}[axis]))
    kind=data['shape']
    if kind in ('plates','tiles','shield','bar'):
        for i in range(3):b('Capa'+str(i),(1.1-i*.1,.14,.8-i*.06),(0,.07+i*.17,0),c if i!=1 else silver)
        if kind=='shield':b('Refuerzo',(.18,.13,1),(0,.55,0),dark)
    elif kind in ('spool','coil'):
        cyl('Devanado',(0,.4,0),.72,.65,c,'X')
        for x in (-.42,.42):cyl('Brida',(x,.42,0),.12,.82,dark,'X')
        cyl('Eje',(0,.42,0),1.08,.16,silver,'X')
        if kind=='coil':b('Nucleo',(.24,.88,.24),(0,.44,0),silver)
    elif kind=='gear':
        cyl('Disco',(0,.2,0),.3,.78)
        for x,z in ((.45,0),(-.45,0),(0,.45),(0,-.45)):b('Diente',(.23,.3,.23),(x,.2,z))
        cyl('Buje',(0,.39,0),.15,.25,dark)
    elif kind=='tubes':
        for x in (-.28,.28):
            cyl('Tubo',(x,.22,0),1.1,.36,c,'Z')
            cyl('Hueco',(x,.22,.56),.025,.24,dark,'Z')
        b('Fleje',(.94,.11,.17),(0,.43,0),silver)
    elif kind=='pellets':
        b('Bandeja',(1.05,.12,.85),(0,.06,0),dark)
        for x,z in ((-.24,-.2),(.24,-.2),(-.24,.2),(.24,.2)):
            parts.append(piece('Granulo',(.4,.38,.35),(x,.3,z),c,'SmoothPlastic',shape='Ball'))
    elif kind in ('canister','cell'):
        cyl('Cuerpo',(0,.43,0),.72,.62)
        cyl('Tapa',(0,.84,0),.12,.65,dark)
        cyl('Terminal',(0,.96,0),.12,.22,gold)
        b('Etiqueta',(.32,.3,.04),(0,.43,.32),silver)
    elif kind in ('crystal','prism'):
        b('BaseCristal',(.85,.12,.72),(0,.06,0),dark)
        b('Cristal',(.45,.7,.45),(0,.49,0),c,'Glass',rot=(0,35,0))
        parts.append(piece('Punta',(.45,.25,.45),(0,.965,0),c,'Glass','WedgePart',rot=(0,35,0)))
    elif kind=='lens':
        cyl('Montura',(0,.18,0),.2,1,dark)
        cyl('Lente',(0,.3,0),.15,.8)
        b('Estuche',(1.1,.11,.95),(0,.055,0),silver)
    elif kind in ('circuit','chip'):
        b('Placa',(1.04,.12,.86),(0,.06,0),(61,129,111) if kind=='circuit' else c)
        b('Chip',(.5,.16,.48),(0,.2,0),dark)
        for x in (-.4,.4):b('Contactos',(.12,.06,.75),(x,.15,0),gold)
        b('Pista',(.65,.03,.05),(0,.14,.32),silver)
    elif kind=='motor':
        b('PieMotor',(1.05,.13,.75),(0,.065,0),dark)
        cyl('CuerpoMotor',(0,.44,0),.75,.58,c,'X')
        cyl('TapaMotor',(-.42,.44,0),.1,.64,silver,'X')
        cyl('EjeMotor',(.5,.44,0),.3,.17,silver,'X')
    elif kind=='battery':
        b('Bateria',(.88,.7,.68),(0,.35,0))
        b('TapaBateria',(.92,.12,.72),(0,.76,0),dark)
        for x in (-.25,.25):cyl('Borne',(x,.88,0),.14,.15,gold)
        b('Indicador',(.45,.16,.025),(0,.43,.35),silver)
    elif kind=='sensor':
        b('CajaSensor',(.8,.6,.7),(0,.3,0),dark)
        cyl('Objetivo',(0,.4,.4),.25,.45,c,'Z')
        cyl('CristalSensor',(0,.4,.54),.04,.33,silver,'Z')
        b('Conector',(.5,.16,.16),(0,.15,-.4),gold)
    elif kind=='frame':
        for x in (-.45,.45):b('Larguero',(.15,.17,1),(x,.085,0))
        for z in (-.43,.43):b('Travesano',(.9,.17,.15),(0,.085,z))
        b('Diagonal',(.12,.12,1.12),(0,.22,0),silver,rot=(0,43,0))
    elif kind=='actuator':
        cyl('Cilindro',(0,.3,0),.8,.5,c,'Z')
        cyl('Vastago',(0,.3,.5),.4,.17,silver,'Z')
        for z in (-.35,.35):b('Soporte',(.8,.13,.16),(0,.065,z),dark)
    elif kind=='robot':
        cyl('Peana',(0,.12,0),.24,.7,dark)
        b('Brazo',(.23,.6,.24),(-.15,.5,0),c,rot=(0,0,-20))
        b('Antebrazo',(.6,.18,.22),(.15,.81,0))
        for z in (-.17,.17):b('Pinza',(.13,.28,.09),(.43,.66,z),silver)
    elif kind in ('core','stabilizer'):
        b('Cuna',(.9,.14,.8),(0,.07,0),dark)
        parts.append(piece('Nucleo',(.55,.65,.55),(0,.52,0),c,'Glass',shape='Ball'))
        for x in (-.38,.38):b('Soporte',(.12,.75,.18),(x,.51,0),silver)
        b('Corona',(.9,.1,.65),(0,.94,0),gold)
    else:raise ValueError(kind)
    return parts

SHAPES={item:shapes(data) for item,data in expanded_items().items()}

def source():return '\nlocal expansionCargo='+lua(SHAPES)+'\nfor item,shape in pairs(expansionCargo) do cargoShapes[item]=shape end\n'
