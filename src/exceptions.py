class ApiException(Exception):
    def __init__(self):
        self.status_code = 500

    def __str__(self):
        raise NotImplementedError()

