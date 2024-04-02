"""
    LivePy bootstraps 'live.js' into a http server, so it automatically
    reloads your browser, if you did any file changes.

    Copyright (C) 2023  worstprgr <adam@seishin.io> GPG Key: key.seishin.io

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import pathlib
import sys
import socketserver
import argparse

from http.server import SimpleHTTPRequestHandler


class ArgumentParser:
    def __init__(self) -> None:
        description: str = 'LivePy bootstraps "live.js" into a http server, '\
                'so it automatically reloads your browser, '\
                'if you did any file changes.'
        html_help: str = 'The file name of your html. '\
                'You can omit the file extension ".html" if you want.'
        port_help: str = 'Custom port. [Optional] (Default: 9005)'

        parser = argparse.ArgumentParser(description=description)
        parser.add_argument('html', type=str, help=html_help)
        parser.add_argument('-p', '--port', default=9005, type=int, help=port_help)

        args = parser.parse_args()
        self.html_filename: str = args.html
        self.port_value: int = args.port


class HTTPRequestHandler(SimpleHTTPRequestHandler):
    """
    Turning off the logs. Use the `SimpleHTTPRequestHandler` as a handler,
    if you need some http logging.
    """
    def log_message(self, format, *args) -> None:
        pass


class Core(ArgumentParser):
    def __init__(self) -> None:
        super().__init__()
        self.localhost: str = '127.0.0.1'
        self.port: int = self.port_value
        self.file: pathlib.Path = self.check_html_file(self.html_filename)
        self.live_js: str = 'live.js'
        self.livejs: str = f'<script src="{self.live_js}"></script>'

    def run(self):
        self.read_write_file(self.inject)

        try:
            self.run_server()
        except KeyboardInterrupt:
            print('Shutting down server')
        except ConnectionAbortedError as e:
            print(e)
        finally:
            self.read_write_file(self.remove)

    def run_server(self) -> None:
        handler = HTTPRequestHandler

        index_name: str = (self.file.name).rstrip('.html').rstrip('.htm')

        # Yeah, I shouldn't override class vars that way, and use a 
        # subclass instead. But things are easier that way and I'm happy.
        handler.index_pages = (index_name + '.html', index_name + '.htm')

        with socketserver.TCPServer((self.localhost, self.port), handler) as httpd:
            print('Server is running. Shutdown with Ctrl+c')
            print('Serving at port:', self.port)
            httpd.serve_forever()

    def read_write_file(self, func) -> None:
        with open(self.file, 'r', encoding='utf8') as rf:
            html_file = rf.readlines()

        new_buffer = func(html_file)

        with open(self.file, 'w', encoding='utf8') as wf:
            wf.writelines(new_buffer)

    def inject(self, html_content: list) -> list[str]:
        buffer: list[str] = []
        first_occurence: bool = False
        c_wspace: int = 0
        c_tab: int = 0
        char: str

        for line in html_content:
            buffer.append(line)

            if ('<head>' in line) and first_occurence is False:
                first_occurence = True
                for char in line:
                    if not char.isspace():
                        break
                    if char == ' ':
                        c_wspace += 1
                    if char == '\t':
                        c_tab += 1
                pre_ws_tab: str = (' '*c_wspace + '\t'*c_tab)*2
                line_to_inject: str = pre_ws_tab + self.livejs + '\n'
                buffer.append(line_to_inject)

        return buffer

    def remove(self, html_content: list) -> list[str]:
        buffer: list[str] = []

        for line in html_content:
            if not (self.livejs in line):
                buffer.append(line)

        return buffer

    @staticmethod
    def check_html_file(html_fn) -> pathlib.Path:
        if not html_fn.endswith('.html'):
            html_fn += '.html'

        html_file = pathlib.Path(html_fn)

        if not html_file.exists():
            print(f'File "{html_file}" does not exist.')
            sys.exit(1)

        return html_file


if __name__ == '__main__':
    Core().run()

