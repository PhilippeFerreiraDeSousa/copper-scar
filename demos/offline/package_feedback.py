#!/usr/bin/env python3
"""Freeze the owner's measured feedback/proposal chain after checking source hashes."""
import argparse,hashlib,json,shutil
from pathlib import Path

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def build(source,output):
 chain=json.loads((source/'chain.json').read_text());dst=output/'feedback-chain';dst.mkdir(parents=True,exist_ok=True)
 bindings={k:chain[k] for k in ['prior_attempt','native_effects','persisted_feedback','following_attempt','following_proposal']}
 bindings['automatic_exclusion_proposal']=chain['automatic_same_parent_exclusion']['proposal']
 copied={}
 for role,receipt in bindings.items():
  src=Path(receipt['path']);assert sha(src)==receipt['sha256'],role
  target=dst/(role+'.json');shutil.copy2(src,target);copied[role]={'path':'feedback-chain/'+target.name,'sha256':sha(target)}
 for name in ['chain.json','chain.md']:shutil.copy2(source/name,dst/name)
 prior=json.loads((dst/'prior_attempt.json').read_text());following=json.loads((dst/'following_attempt.json').read_text());proposal=json.loads((dst/'following_proposal.json').read_text());feedback=json.loads((dst/'persisted_feedback.json').read_text())
 assert feedback['attempt']==prior['attempt']
 assert prior['attempt'] in proposal['feedback_used']
 assert following['status']=='completed' and prior['status']=='completed'
 for field,key in [('prior_outcome',prior),('following_outcome',following)]:
  for metric,value in chain[field].items():assert key['after'][metric]==value,(field,metric)
 assert proposal['parent_board_sha256']==chain['parent_board_sha256']
 payload={'scope':'Measured feedback mechanism; no retained placement benefit','prior_id':prior['attempt'],'following_id':following['attempt'],'prior_outcome':chain['prior_outcome'],'following_outcome':chain['following_outcome'],'parent_board_sha256':chain['parent_board_sha256'],'following_pose':chain['following_pose'],'qualification':chain['qualification'],'automatic_exclusion':chain['automatic_same_parent_exclusion'],'files':copied,'original_chain':'feedback-chain/chain.json','narrative':'feedback-chain/chain.md'}
 (dst/'portable.json').write_text(json.dumps(payload,indent=2)+'\n');(output/'feedback-data.js').write_text('window.FEEDBACK='+json.dumps(payload)+';\n')
 print(json.dumps({'feedback_chain_verified':True,'prior':prior['attempt'],'following':following['attempt'],'native_after':[chain['prior_outcome'],chain['following_outcome']]}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();build(a.source,a.output)
