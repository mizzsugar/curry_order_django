class CurryAppError(Exception):
    pass


class FormError(CurryAppError):
    def __init__(self, form):
        self.form = form
