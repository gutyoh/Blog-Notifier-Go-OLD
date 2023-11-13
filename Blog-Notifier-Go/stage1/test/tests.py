import http.server
import logging
import socketserver
import threading
from pathlib import Path

from hstest.check_result import CheckResult
from hstest.stage_test import StageTest
from hstest.test_case import TestCase


class BlogNotifierTest(StageTest):
    ADDRESS = "127.0.0.1"
    PORT = 9090
    STATIC_FILES_DIRECTORY = Path(__file__).parent / "static"

    server_thread = None
    httpd = None

    @classmethod
    def start_server(cls):
        def handler(*args, **kwargs):
            return http.server.SimpleHTTPRequestHandler(*args, directory=cls.STATIC_FILES_DIRECTORY, **kwargs)

        try:
            cls.httpd = socketserver.TCPServer((cls.ADDRESS, cls.PORT), handler)
            cls.server_thread = threading.Thread(target=cls.httpd.serve_forever)
            cls.server_thread.start()
        except Exception as e:
            logging.error(f"Failed to start server: {e}")
            raise e

    @classmethod
    def stop_server(cls):
        if cls.httpd:
            cls.httpd.shutdown()
            cls.httpd.server_close()
        if cls.server_thread:
            cls.server_thread.join()

    def generate(self):
        self.start_server()
        return [TestCase(time_limit=10000)]

    def check(self, reply: str, attach):
        try:
            if "Welcome to the Test Blog!" in reply:
                return CheckResult.correct()
            self.stop_server()
            return CheckResult.wrong("The Go program did NOT fetch the expected content from the static page.")
        finally:
            self.stop_server()


if __name__ == '__main__':
    BlogNotifierTest().run_tests()
