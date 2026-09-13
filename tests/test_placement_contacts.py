from copper_scar.tools.copperhead.placement_contacts import check

def board(path,number,name):
 path.write_text(f'(kicad_pcb (net {number} "{name}") (via (uuid "v") (net {number})))');return path

def test_semantic_renumbering_is_not_reassignment(tmp_path):
 assert check(board(tmp_path/'a',1,'A'),board(tmp_path/'b',2,'A'))['existing_via_net_attachments_preserved']

def test_native_net_reassignment_rejected(tmp_path):
 result=check(board(tmp_path/'a',1,'A'),board(tmp_path/'b',1,'B'));assert not result['existing_via_net_attachments_preserved'];assert result['changes']==[dict(uuid='v',before_net='A',after_net='B')]
