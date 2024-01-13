
class NoCacheMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Cache-Control'] = "max-age=0, no-cache, no-store, must-revalidate"
        response['Pragma'] = 'no-cache'
        response['Expires'] = '"Mon, 01 Jan 1970 00:00:00 GMT"'
        return response