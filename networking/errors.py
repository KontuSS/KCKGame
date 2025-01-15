class PokerError(Exception):
    def __init__(self, message: str, status_code: int):            
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
            
        self.message = message
        self.status_code = status_code