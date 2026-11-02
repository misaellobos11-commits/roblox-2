"""Generate overview and six-machine close-up of the polished authored geometry."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from expansion.content import MACHINES
from expansion.polish_822 import MODELS
from expansion.preview import main

CLOSE_IDS=('RollingMill','ChemicalReactor','GearPress','CircuitAssembler','RoboticsAssembler','CoreAssembler')
CLOSE=[next(m for m in MACHINES if m['id']==key) for key in CLOSE_IDS]
if __name__=='__main__':
    main(MODELS,'build/Expansion_822_Preview.rbxmx')
    main(MODELS,'build/Expansion_822_Close.rbxmx',CLOSE,3)
