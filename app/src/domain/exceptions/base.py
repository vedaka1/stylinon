class ApplicationException(Exception):
    def __init__(
        self,
        status_code: int = 500,
        message: str = "Unknown error occured",
        *args: object,
    ) -> None:
        self.status_code = status_code
        self.message = message
        super().__init__(status_code, message, *args)
