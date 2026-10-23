#!/usr/bin/env python3
"""Serve only approved website files on loopback, under the real Pages subpath."""
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote,urlsplit
import argparse,mimetypes
ROOT=Path(__file__).resolve().parents[1]/'docs'
class Preview(BaseHTTPRequestHandler):
    def do_GET(self):
        path=unquote(urlsplit(self.path).path);base='/nj-name-atlas/'
        if path=='/':self.send_response(302);self.send_header('Location',base);self.end_headers();return
        if not path.startswith(base):self.send_error(404);return
        rel=path[len(base):]
        if not rel or rel.endswith('/'):rel+='index.html'
        target=(ROOT/rel).resolve()
        if ROOT.resolve() not in target.parents or not target.is_file() or any(p.startswith('.') for p in Path(rel).parts):self.send_error(404);return
        data=target.read_bytes();self.send_response(200);self.send_header('Content-Type',mimetypes.guess_type(str(target))[0] or 'application/octet-stream');self.send_header('Content-Length',str(len(data)));self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(data)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--port',type=int,default=8780);a=ap.parse_args()
    print(f'Local preview: http://127.0.0.1:{a.port}/nj-name-atlas/',flush=True)
    try:ThreadingHTTPServer(('127.0.0.1',a.port),Preview).serve_forever()
    except KeyboardInterrupt:pass
