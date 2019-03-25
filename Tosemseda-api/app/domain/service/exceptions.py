class InvalidSMSIdentificator(Exception):
    pass


class OfferChosenExpired(Exception):
    pass


class InvalidStepProcess(Exception):
    pass


class CantCreateAQuote(Exception):
    pass


class RepositoryError(Exception):

    def __init__(self, message):
        self.internal_code = 'unknow-error'
        self.status_code = 500
        if 'id_number' in message and 'already exists' in message:
            self.internal_code = 'id-number'
            self.status_code = 400
            self.message = 'The id-number is already in use'
        if 'email' in message and 'already exists' in message:
            self.internal_code = 'email'
            self.status_code = 400
            self.message = 'The email is already in use'
