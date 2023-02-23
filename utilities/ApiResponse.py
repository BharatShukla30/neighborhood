class ApiResponse:
    def __init__(self, data, status=200, message=None, headers=None):
        self.data = data
        self.status = status
        self.message = message
        self.headers = headers or {}