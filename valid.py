from exceptions import ValidationError, RentingError
from entities import Date


class ValidClient(object):
    def __init__(self):
        pass

    def validate_client(self, client):
        '''
        Function that validates a client
        Input: client
        Output: - , if client is valid
                raises Exception: 'invalid id', id<=0
                                  'invalid name', name - empty
        '''
        errors = ''
        if client.get_id() <= 0:
            errors += 'Invalid Id \n'
        if client.get_name() == '':
            errors += 'Invalid name \n'
        if len(errors) > 0:
            raise ValidationError(errors)


class ValidMovie():
    def __init__(self):
        pass

    def validate_movie(self, movie):
        '''
        Function that validates a movie
        Input: movie
        Output: - , if movie is valid
                raises Exception: 'invalid id', id<=0
                                  'invalid title', title - empty
        '''
        errors = ''
        if movie.get_id() <= 0:
            errors += 'Invalid Id \n'
        if movie.get_title() == '':
            errors += 'Invalid title \n'
        if len(errors) > 0:
            raise ValidationError(errors)


class ValidRental(object):
    def __init__(self):
        pass

    def validate_rental(self, rental, rentals):
        errors = ''
        # check if movie is available
        for existing_rental in rentals:
            if existing_rental.get_movieId() == rental.get_movieId() and existing_rental.get_returnDate() == Date(0, 0,
                                                                                                                  0):
                errors += 'Movie is not available at the moment \n'
        # check if client has unreturned movies past due date
        # (rent date (of new rental) > due date (old rental); return date - empty)
        for existing_rental in rentals:
            if existing_rental.get_clientId() == rental.get_clientId() and existing_rental.get_returnDate() == Date(0,
                                                                                                                    0,
                                                                                                                    0) and existing_rental.get_dueDate() <= rental.get_rentDate():
                errors += 'Client has not returned a movie that passed the due date and can not rent another one'
                break
        if len(errors) > 0:
            raise RentingError(errors)




