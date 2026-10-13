import json,sys
sys.path.insert(0, r'D:\Animation-Model-Training\src')
from animtrain import network_isolation as net
print('TOKEN=' + json.dumps(net.token_identity()))
