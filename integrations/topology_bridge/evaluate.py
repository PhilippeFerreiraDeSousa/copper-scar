import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'placement_bridge'))
from verify_incremental_fixture import check
if __name__=='__main__':
    check(Path(sys.argv[1]))
