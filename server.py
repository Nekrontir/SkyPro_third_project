from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    """
        Специальный класс, который отвечает за
        обработку входящих запросов от клиентов
    """
    def do_GET(self):
        """ Метод для обработки входящих GET-запросов """
        path = self.path.lstrip('/')

        if path == '' or path == 'index.html':
            self.serve_file('index.html', 'text/html')
        elif path in ['orders.html', 'category.html', 'contacts.html']:
            self.serve_file(path, 'text/html')
        elif path.startswith('css/') and path.endswith('.css'):
            self.serve_file(path, 'text/css')
        elif path.startswith('js/') and path.endswith('.js'):
            self.serve_file(path, 'application/javascript')
        else:
            self.send_error(404, "File not found")

    def serve_file(self, filepath, content_type):
        """Вспомогательный метод для чтения и отправки файла"""
        try:
            with open(filepath, 'rb') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, "File not found")


    def do_POST(self):
        """Обработка POST-запросов: читаем данные, печатаем в консоль, отвечаем."""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        data_str = post_data.decode('utf-8')
        parsed = parse_qs(data_str)
        print("=== ПОЛУЧЕН POST-ЗАПРОС ===")
        print("Данные от пользователя:", parsed)
        print("============================")

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        response = "<h1>Данные успешно получены!</h1><p>Спасибо, мы обработали ваш запрос.</p>"
        self.wfile.write(response.encode("utf-8"))

if __name__ == "__main__":
    # noinspection PyTypeChecker
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Сервер запущен: http://{hostName}:{serverPort}")
    print("Для остановки нажмите Ctrl+C")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Сервер остановлен.")