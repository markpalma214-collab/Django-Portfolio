from vercel.headers import set_headers


class VercelOIDCMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        set_headers(request.headers)
        return self.get_response(request)
