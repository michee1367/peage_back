class ExceptionService(Exception):
    """Exception personnalisée pour les erreurs spécifiques."""

    def __init__(self, message, code=None):
        super().__init__(message)
        self.code = code  # Vous pouvez ajouter des attributs supplémentaires ici
    def get_error_message(self) :
        return self.args[0]
    def __str__(self):
        return f"[Error {self.code}]: {self.args[0]}" if self.code else self.args[0]
