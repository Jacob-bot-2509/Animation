"""Print an already verified static HTML using an owned, hidden Edge CDP session.
Protocol reference: https://chromedevtools.github.io/devtools-protocol/
Only loopback sockets and our private browser profile are used.
"""
from pathlib import Path
import base64,hashlib,json,os,socket,struct,subprocess,tempfile,time,urllib.request,urllib.parse

class CDP:
    def __init__(self,url,timeout=180):
        u=urllib.parse.urlsplit(url)
        if u.scheme!='ws' or u.hostname not in ('127.0.0.1','localhost'):raise ValueError('CDP must be local loopback')
        self.socket=socket.create_connection((u.hostname,u.port),timeout=timeout);self.buffer=b'';self.serial=0;self.timeout=timeout
        key=base64.b64encode(os.urandom(16)).decode();target=u.path+('?' + u.query if u.query else '')
        self.socket.sendall((f'GET {target} HTTP/1.1\r\nHost: {u.hostname}:{u.port}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n').encode())
        while b'\r\n\r\n' not in self.buffer:
            chunk=self.socket.recv(4096)
            if not chunk:raise OSError('CDP closed during handshake')
            self.buffer+=chunk
            if len(self.buffer)>65536:raise ValueError('CDP handshake too large')
        header,self.buffer=self.buffer.split(b'\r\n\r\n',1);expected=base64.b64encode(hashlib.sha1((key+'258EAFA5-E914-47DA-95CA-C5AB0DC85B11').encode()).digest())
        if not header.startswith(b'HTTP/1.1 101') or expected.lower() not in header.lower():raise ValueError('WebSocket handshake rejected')
    def read(self,n):
        while len(self.buffer)<n:
            chunk=self.socket.recv(max(4096,n-len(self.buffer)))
            if not chunk:raise OSError('CDP socket closed')
            self.buffer+=chunk
        out,self.buffer=self.buffer[:n],self.buffer[n:];return out
    def send(self,payload,opcode=1):
        data=payload if isinstance(payload,bytes) else payload.encode();n=len(data);mask=os.urandom(4)
        size=bytes([0x80|opcode,0x80|n]) if n<126 else (bytes([0x80|opcode,0x80|126])+struct.pack('!H',n) if n<65536 else bytes([0x80|opcode,0x80|127])+struct.pack('!Q',n))
        self.socket.sendall(size+mask+bytes(b^mask[i%4] for i,b in enumerate(data)))
    def receive(self):
        parts=[]
        while True:
            first,second=self.read(2);op=first&15;n=second&127
            if n==126:n=struct.unpack('!H',self.read(2))[0]
            elif n==127:n=struct.unpack('!Q',self.read(8))[0]
            if n>64*1024*1024:raise ValueError('CDP frame too large')
            mask=self.read(4) if second&128 else None;data=self.read(n)
            if mask:data=bytes(b^mask[i%4] for i,b in enumerate(data))
            if op==8:raise OSError('CDP closed')
            if op==9:self.send(data,10);continue
            if op==10:continue
            if op not in (0,1):raise ValueError('unexpected binary CDP frame')
            parts.append(data)
            if first&128:return json.loads(b''.join(parts).decode())
    def call(self,method,params=None):
        self.serial+=1;serial=self.serial;self.send(json.dumps({'id':serial,'method':method,'params':params or {}}));deadline=time.monotonic()+self.timeout
        while True:
            remaining=deadline-time.monotonic()
            if remaining<=0:raise TimeoutError('CDP timed out: '+method)
            self.socket.settimeout(remaining);reply=self.receive()
            if reply.get('id')==serial:
                if 'error' in reply:raise ValueError(method+': '+str(reply['error']))
                return reply.get('result',{})
    def close(self):self.socket.close()


def print_static_to_pdf(html_path,output,edge,expected_inline,expected_display):
    output=Path(output)
    if output.exists():raise ValueError('fresh CDP output must not exist')
    with tempfile.TemporaryDirectory(prefix='.edge-print-',dir=output.parent,ignore_cleanup_errors=True) as profile:
        proc=subprocess.Popen([edge,'--headless=new','--disable-gpu','--no-first-run','--disable-extensions',
            '--remote-debugging-address=127.0.0.1','--remote-debugging-port=0','--allow-file-access-from-files',
            '--user-data-dir='+profile,'about:blank'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,
            creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        page=browser=None
        try:
            port_file=Path(profile)/'DevToolsActivePort';deadline=time.monotonic()+30
            while not port_file.is_file():
                if time.monotonic()>deadline:raise TimeoutError('owned Edge CDP endpoint unavailable')
                time.sleep(0.1)
            lines=port_file.read_text('utf-8').splitlines();port=int(lines[0]);browser=CDP(f'ws://127.0.0.1:{port}{lines[1]}',timeout=180)
            with urllib.request.urlopen(f'http://127.0.0.1:{port}/json/list',timeout=10) as response:targets=json.load(response)
            target=next(t for t in targets if t['type']=='page');page=CDP(target['webSocketDebuggerUrl'],timeout=180)
            page.call('Page.enable');nav=page.call('Page.navigate',{'url':Path(html_path).resolve().as_uri()})
            if nav.get('errorText'):raise ValueError(nav['errorText'])
            result=page.call('Runtime.evaluate',{'expression':"new Promise(resolve=>{const done=()=>document.fonts.ready.then(()=>resolve({title:document.title,inline:document.querySelectorAll('span.math').length,display:document.querySelectorAll('div.math-block').length,containers:document.querySelectorAll('mjx-container').length,scripts:document.scripts.length}));if(document.readyState==='complete')done();else window.addEventListener('load',done,{once:true});})",'awaitPromise':True,'returnByValue':True})
            value=result.get('result',{}).get('value',{})
            if value!={'title':'MJDONE','inline':expected_inline,'display':expected_display,'containers':expected_inline+expected_display,'scripts':0}:raise ValueError('CDP static document changed or incomplete: '+str(value))
            result=page.call('Page.printToPDF',{'printBackground':True,'preferCSSPageSize':True,'displayHeaderFooter':False,'transferMode':'ReturnAsStream'})
            handle=result.get('stream')
            if not handle:raise ValueError('CDP did not provide a PDF stream')
            with output.open('xb') as stream:
                while True:
                    chunk=page.call('IO.read',{'handle':handle,'size':65536});data=chunk.get('data','')
                    stream.write(base64.b64decode(data,validate=True) if chunk.get('base64Encoded') else data.encode())
                    if chunk.get('eof'):break
            page.call('IO.close',{'handle':handle})
        finally:
            if browser:
                try:browser.timeout=5;browser.call('Browser.close')
                except (OSError,ValueError,TimeoutError):pass
            if page:page.close()
            if browser:browser.close()
            try:proc.wait(timeout=10)
            except subprocess.TimeoutExpired:proc.terminate();proc.wait(timeout=10)
