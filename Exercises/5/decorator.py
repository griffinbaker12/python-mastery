class API:
    def __init__(self) -> None:
        self.routes = {}

    def get(self, path):
        def decorator(func):
            self.routes[(path, "GET")] = func
            return func

        return decorator

    def post(self, path):
        def decorator(func):
            self.routes[(path, "POST")] = func
            return func

        return decorator


api = API()


@api.get("/home")
def hello():
    return "Hello World"


def _hello():
    return "_Hello World"


_hello = api.get("home")(_hello)


def simulate_request(path, method):
    key = (path, method)
    if key in api.routes:
        return api.routes[key]()
    else:
        return 404, "Not found"


print(api.routes)
print(simulate_request("/home", "GET"))
