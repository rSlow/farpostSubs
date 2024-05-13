class NotCreatedError(RuntimeError):
    def __init__(self):
        super().__init__("Connection was not created")


class RejectedError(RuntimeError):
    pass
