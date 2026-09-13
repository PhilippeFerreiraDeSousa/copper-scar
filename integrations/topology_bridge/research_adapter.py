"""Hash/pose-bound adapter from KRT group translations to source placement moves."""
import hashlib
import math

def moves_from_research(proposal,board,components,export_poses):
    if proposal.get('kind')!='group_pose' or hashlib.sha256(board.read_bytes()).hexdigest()!=proposal['parent_board_sha256']:
        raise ValueError('Stale or unsupported research parent')
    if set(proposal['from_poses'])!=set(proposal['refs']):raise ValueError('Incomplete group poses')
    dx,dy=proposal['translation_mm'];moves={}
    if not all(math.isfinite(x) for x in (dx,dy)):raise ValueError('Invalid translation')
    for ref in proposal['refs']:
        old=proposal['from_poses'][ref];actual=export_poses[ref]
        if any(abs(old[k]-v)>1e-6 for k,v in zip(('x_mm','y_mm','angle_deg'),actual)):
            raise ValueError('Research pose does not match native parent')
        # Fixture is front-side only with source Y increasing up, export Y down.
        x,y=components[ref]['xy'];moves[ref]=[x+dx,y-dy]
    return moves
