class MockAPIResponse:
    def __init__(self, data=None):
        if isinstance(data, list):
            self.data = data
            self.count = len(data)
        elif data is None:
            self.data = None
            self.count = 0
        else:
            self.data = [data]
            self.count = 1


def execute_response_format(data):
    if data:
        return MockAPIResponse(data=data)
    else:
        return None
