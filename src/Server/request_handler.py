import http.server

from Controllers.controller import ApiController


class RequestHandler(http.server.BaseHTTPRequestHandler):
    controller = ApiController()
    routes = {
        "transacoes": controller.post_transaction,
        "extrato": controller.get_extrato,
    }

    def extract_info(self, path):
        parts = path.split("/")[1:]  # Split the path. Ignore empty first element
        if len(parts) == 2:
            return parts[0], parts[1]
        else:
            return None, None

    async def handle_request(self, path: str) -> dict:
        if not path.startswith("/cliente/"):
            self.send_error(404, "Invalid path")

        client_id, operation = self.extract_info(self.path)

        try:
            self.routes[operation](client_id)
        except KeyError:
            self.send_error(404, "Invalid route")

    async def do_GET(self):
        await self.handle_request(self.path)

    async def do_POST(self):
        await self.handle_request(self.path)
