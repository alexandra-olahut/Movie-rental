import copy

from repository import Repository
from entities import Movie, Client, Date, Rental, Operation, UpdateOperation, ComplexOperation
from exceptions import TimelineError, DateError, RentingError
import random
import datetime

from text_files import FileRepo


class ServiceClients(object):
    '''
    Coordinates all actions involving clients, using the repository and the movie validator
    '''

    def __init__(self, repoClients, validClient, undoStack, redoStack, repoRentals):
        self.repoRentals = repoRentals
        self.repoClients = repoClients
        self.validClient = validClient
        self.undoStack = undoStack
        self.redoStack = redoStack

    def get_number(self):
        # Function that returns the number of clients currently existing in the application
        return self.repoClients.size()

    def get_clients(self):
        # Function that returns all clients existing in the application as a list of entities
        return self.repoClients.get_all()

    def add_client(self, clientId, name):
        '''
        Based on the parameters given (id/name)
         - it creates an object 'client' that belongs in 'Client' class
         - it validates the client
         - it adds it to the repository
        '''
        client = Client(clientId, name)
        self.validClient.validate_client(client)
        self.repoClients.add(client)
        ''' For undo '''
        operation = Operation(self.repoClients, "Repository.add", "Repository.remove", client)
        self.undoStack.push_op(operation)
        self.redoStack.clear()


    def remove_client(self, clientId):
        '''
        Function that removes from the list the client having the Id given from user
        '''
        complex_operation = ComplexOperation()
        rentals = self.repoRentals.get_all()
        for rental in reversed(rentals):
            if rental.get_clientId() == clientId:
                self.repoRentals.remove(rental)
                simple_operation = Operation(self.repoRentals, "Repository.remove", "Repository.add", rental)
                complex_operation.add_action(simple_operation)
        client = self.repoClients.search(Client(clientId, ''))
        self.repoClients.remove(client)
        operation = Operation(self.repoClients,  "Repository.remove", "Repository.add", client)
        complex_operation.add_action(operation)
        self.undoStack.push_op(complex_operation)
        self.redoStack.clear()

    def update_client(self, clientId, name):
        '''
        Function that, for the client of given Id, updates its fields with new values, if they are given by user
        '''
        client = self.repoClients.search(Client(clientId, ''))
        initial_client = copy.deepcopy(client)
        client_update = Client(clientId, name)
        self.repoClients.update(client, client_update)
        ''' For undo '''
        operation = UpdateOperation(self.repoClients, "Repository.update", initial_client, client_update)
        self.undoStack.push_op(operation)
        self.redoStack.clear()

    def generate_client(self):
        self.firstname = ['Jon', 'Peter', 'Ana', 'Emma', 'John', 'Jim', 'Eli', 'Billy', 'Ron', 'Roger', 'Jon', 'Betty',
                          'Ellen', 'James', 'Dan']
        self.lastname = ['Snow', 'Williams', 'Low', 'Carter', 'Weasley', 'Potter', 'Bay', 'Walker', 'Archibald', 'Bob',
                         'Doll', 'Thomas', 'Doe']
        for i in range(1, 11):
            name = str(random.choice(self.firstname)) + ' ' + str(random.choice(self.lastname))
            self.add_client(i, name)

    def search_client(self, key):
        key_client = Client(key, key)
        requested_clients = self.repoClients.search_by_all_fields(key_client)
        return requested_clients


class ServiceMovies(object):
    '''
    Coordinates all actions involving movies, using the repository and the movie validator
    '''

    def __init__(self, repoMovies, validMovie, undoStack, redoStack, repoRentals):
        self.repoRentals = repoRentals
        self.repoMovies = repoMovies
        self.validMovie = validMovie
        self.undoStack = undoStack
        self.redoStack = redoStack

    def get_number(self):
        # Function that returns the number of movies currently existing in the application
        return self.repoMovies.size()

    def get_movies(self):
        # Function that returns all movies existing in the application as a list of entities
        return self.repoMovies.get_all()

    def add_movie(self, movieId, title, description, genre):
        '''
        Based on the parameters given (id/title/description/genre)
         - it creates an object 'movie' that belongs in 'Movie' class
         - it validates the movie
         - it adds it to the repository
        '''
        movie = Movie(movieId, title, description, genre)
        self.validMovie.validate_movie(movie)
        self.repoMovies.add(movie)
        ''' For the undo'''
        operation = Operation(self.repoMovies, "Repository.add", "Repository.remove", movie)
        self.undoStack.push_op(operation)
        self.redoStack.clear()


    def remove_movie(self, movieId):
        '''
        Function that removes from the list the movie having the Id given from user
        '''
        complex_operation = ComplexOperation()
        rentals = self.repoRentals.get_all()
        for rental in reversed(rentals):
            if rental.get_movieId() == movieId:
                self.repoRentals.remove(rental)
                simple_operation = Operation(self.repoRentals, "Repository.remove", "Repository.add", rental)
                complex_operation.add_action(simple_operation)
        movie = self.repoMovies.search(Movie(movieId, '', '', ''))
        self.repoMovies.remove(movie)
        operation = Operation(self.repoMovies, "Repository.remove", "Repository.add", movie)
        complex_operation.add_action(operation)
        self.undoStack.push_op(complex_operation)
        self.redoStack.clear()

    def update_movie(self, movieId, title, description, genre):
        '''
        Function that, for the movie of given Id, updates its fields with new values, if they are given by user
        '''
        movie = self.repoMovies.search(Movie(movieId, '', '', ''))
        initial_movie = copy.deepcopy(movie)
        movie_update = Movie(movieId, title, description, genre)
        self.repoMovies.update(movie, movie_update)
        ''' For undo '''
        operation = UpdateOperation(self.repoMovies, "Repository.update", initial_movie, movie_update)
        self.undoStack.push_op(operation)
        self.redoStack.clear()

    def generate_movies(self):
        self.titles = ['In time', 'Eclipse', 'Lala Land', 'Scandal', 'Ben ten', 'Gone with the wind', 'Dear John',
                       'Frozen', 'Harry Potter', 'Titanic', 'Jurassic Park', 'Bad romance', 'Love actually',
                       'So this is Christmas', 'Hannah Montana', 'Percy Jackson', 'Forest Gump']
        self.genres = ['animation', 'comedy', 'family', 'drama', 'horror', 'adventure', 'action', 'thriller', 'rom-com',
                       'romantic', 'documentary', 'history']
        self.descriptions = ['Drama queen', 'Typical highschool drama', 'Story about family', 'Story about two friends',
                             'Best love story', 'Queen with magical powers', 'Wizards and witches',
                             'Story about best friends', 'Story about brothers', 'Main character goes on adventure',
                             'Main character falls in love']
        for i in range(1, 11):
            title = random.choice(self.titles)
            for j in self.titles:
                if j == title:
                    self.titles.remove(j)
            genre = random.choice(self.genres)
            description = random.choice(self.descriptions)
            self.add_movie(i, title, description, genre)

    def search_movie(self, key):
        key_movie = Movie(key, key, key, key)
        requested_movies = self.repoMovies.search_by_all_fields(key_movie)
        return requested_movies


class MovieRentalDays:  # DTO
    def __init__(self, movie, days_rented):
        self.movie = movie
        self.days_rented = days_rented

    def get_days(self):
        return self.days_rented

    def __str__(self):
        return str(self.movie) + '\n' + '   Rented for: ' + str(self.days_rented) + ' days'


class ClientRentalDays:  # DTO
    def __init__(self, client, rental_days):
        self.client = client
        self.rental_days = rental_days

    def get_days(self):
        return self.rental_days

    def __str__(self):
        return str(self.client) + '\n' + '   has ' + str(self.rental_days) + ' movie rental days'


class LateRentals:  # DTO
    def __init__(self, movie_id, name, delay):
        self.movie_id = movie_id
        self.name = name
        self.delay = delay

    def get_delay(self):
        return self.delay

    def __str__(self):
        return str(self.movie_id) + ': ' + self.name + '\n' + '   Late for ' + str(self.delay) + ' days'


class ServiceRentals(object):
    def __init__(self, repoMovies, repoClients, repoRentals, validRental, undoStack, redoStack):
        self.repoMovies = repoMovies
        self.repoClients = repoClients
        self.repoRentals = repoRentals
        self.validRental = validRental
        self.undoStack = undoStack
        self.redoStack = redoStack

    def get_number(self):
        return self.repoRentals.size()

    def get_rentals(self):
        return self.repoRentals.get_all()

    def get_date(self, inputDate):
        date = inputDate.split('/')
        if len(date) != 3:
            raise DateError('Date is not in valid format')
        return Date(int(date[0]), int(date[1]), int(date[2]))

    def rent_movie(self, rentalId, movieId, clientId, rentDate, dueDate):
        # it creates a rental - if movie and client exist
        # it validates and adds it to the repository for rentals
        # - the movie must not be already rented (and not returned)
        # - the client must not have any rented movies past their due date
        movie = self.repoMovies.search(Movie(movieId, '', '', ''))
        client = self.repoClients.search(Client(clientId, ''))
        rentDate = self.get_date(rentDate)
        dueDate = self.get_date(dueDate)
        returnDate = Date(0, 0, 0)
        if dueDate <= rentDate:
            raise TimelineError('Due date must be chronologically after rent-date')

        rental = Rental(rentalId, movie.get_id(), client.get_id(), rentDate, dueDate, returnDate)

        rentals = self.get_rentals()
        self.validRental.validate_rental(rental, rentals)
        self.repoRentals.add(rental)
        ''' For undo '''
        operation = Operation(self.repoRentals, "Repository.add", "Repository.remove", rental)
        self.undoStack.push_op(operation)
        self.redoStack.clear()


    def return_movie(self, rentalId, returnDate):
        # it searches for the rental id given
        # if it exists it adds the returned date
        returnDate = self.get_date(returnDate)
        rental = self.repoRentals.search(Rental(rentalId, '', '', '', '', ''))
        initial_rental = copy.deepcopy(rental)
        if rental.get_returnDate() != Date(0, 0, 0):
            raise RentingError('Movie was already returned')
        if returnDate <= rental.get_rentDate():
            raise TimelineError('Return-date must be chronologically after rent-date')
        self.repoRentals.update(rental, Rental(rentalId, '', '', '', '', returnDate))
        ''' For undo '''
        operation = UpdateOperation(self.repoRentals, "Repository.update", initial_rental, Rental(rentalId,'','','','',returnDate))
        self.undoStack.push_op(operation)
        self.redoStack.clear()


    def most_rented(self):
        situation_movies_rented = {}
        rentals = self.get_rentals()
        # Make a dictionary with the movie Id as key, and a list of the number of days rented for each rental of that movie
        for rental in rentals:
            movie_id = rental.get_movieId()
            if movie_id not in situation_movies_rented:
                situation_movies_rented[movie_id] = 0
            situation_movies_rented[movie_id] += rental.number_of_days_rented()

        result = []
        for item in situation_movies_rented.items():
            movie = self.repoMovies.search(Movie(item[0], '', '', ''))
            rented_days = item[1]
            result.append(MovieRentalDays(movie, rented_days))
        result.sort(key=lambda x: x.get_days(), reverse=True)
        return result

    def most_active(self):
        situation_clients_renting = {}
        rentals = self.get_rentals()
        # Make a dictionary with the client Id as key, and a list of the number of rental days for each rental they had
        for rental in rentals:
            client_id = rental.get_clientId()
            if client_id not in situation_clients_renting:
                situation_clients_renting[client_id] = 0
            situation_clients_renting[client_id] += rental.number_of_days_rented()

        result = []
        for item in situation_clients_renting.items():
            client = self.repoClients.search(Client(item[0], ''))
            rental_days = item[1]
            result.append(ClientRentalDays(client, rental_days))
        result.sort(key=lambda x: x.get_days(), reverse=True)
        return result

    def late_rentals(self):
        current_date = datetime.date.today()
        situation_late_rentals = []
        rentals = self.get_rentals()
        for rental in rentals:
            if rental.get_returnDate() == Date(0, 0, 0) and rental.get_dueDate() <= Date(current_date.day,
                                                                                         current_date.month,
                                                                                         current_date.year):
                # it means the movie hasn't been returned, and the due date passed
                movie_id = rental.get_movieId()
                movie = self.repoMovies.search(Movie(movie_id, '', '', ''))
                name = movie.get_title()
                delay = rental.number_of_days_delayed()
                situation_late_rentals.append(LateRentals(movie_id, name, delay))
        situation_late_rentals.sort(key=lambda x: x.get_delay(), reverse=True)
        return situation_late_rentals



