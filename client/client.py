# ============================
# client/client.py
# ============================

def send_filters(filtros):
    from server.server import handle_request
    return handle_request(filtros)