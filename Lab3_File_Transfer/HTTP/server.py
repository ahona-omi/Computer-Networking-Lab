import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import os

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.client_address), str(self.path), str(self.headers))
        file_path = self.path[1:]

        if file_path == '':
            self._list_files()
        else:
            self._serve_file(file_path)

    def _list_files(self):
        files = '\n'.join(os.listdir())
        self._set_response()
        self.wfile.write(files.encode())

    def _serve_file(self, file_path):
        if os.path.exists(file_path):
            try:
                download_time = time.strftime('%Y-%m-%d %H:%M:%S')
                with open(file_path, "rb") as f:
                    file_content = f.read()
                print(f"[SENT] File '{file_path}' sent  at {download_time}.")
            except FileNotFoundError:
                logging.error("File not found: %s", file_path)
                self.send_error(404, "File not found")
                return

            self._set_response()
            self.wfile.write(file_content)
        else:
            logging.error("File not found: %s", file_path)
            self.send_error(404, "File not found")

    def do_POST(self):
        content_type = self.headers['Content-Type']
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        file_name = 'upload.in'
        if 'filename' in content_type:
            file_name = content_type.split('filename=')[1].strip('"')

        with open(file_name, 'wb') as local_file:
            local_file.write(post_data)

        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n", str(self.client_address),
                     str(self.path), str(self.headers))

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def start(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    # Set a larger value for max_size to handle larger file uploads
    httpd.max_size = 10 * 1024 * 1024  # 10 MB
    logging.info('Starting httpd...\n')
    try:
         httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        start(port=int(argv[1]))
    else:
        start()
