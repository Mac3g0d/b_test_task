from typing import Self


class ApiError(Exception):
    def __init__(self: Self) -> None:
        self.status_code = 500

    def __str__(self: Self) -> None:
        raise NotImplementedError()

