from exceptions import DateError
import datetime

from repository import Repository


class Movie:
    '''
    We have a class for 'movie' entity, which contains movie id, title, description and genre
    '''

    def __init__(self, movieId, title, description, genre):
        self.__movieId = movieId
        self.__title = title
        self.__description = description
        self.__genre = genre

    # getters
    def get_id(self):
        return self.__movieId

    def get_title(self):
        return self.__title

    def get_description(self):
        return self.__description

    def get_genre(self):
        return self.__genre

    # setters
    def set_movieId(self, value):
        self.__movieId = value

    def set_title(self, value):
        self.__title = value

    def set_description(self, value):
        self.__description = value

    def set_genre(self, value):
        self.__genre = value

    # comparing 2 movies by their id's
    def __eq__(self, other):
        return self.__movieId == other.__movieId

    def __str__(self):
        return "Movie ID: " + str(self.__movieId) + "\n" + \
               "Title: " + self.__title + "\n" + \
               "Description: " + self.__description + "\n" + \
               "Genre: " + self.__genre

    def special_replace(self, other):
        '''
        The function replaces the fields of an element (title/description/genre) with those of a second element(other)
        If a certain field of 'other' is empty, the element keeps the initial value for that certain field
        '''
        if other.get_title() != '':
            self.set_title(other.get_title())
        if other.get_description() != '':
            self.set_description(other.get_description())
        if other.get_genre() != '':
            self.set_genre(other.get_genre())

    def identical(self, other):
        # function returns true if all fields are the same for two elements
        return self.get_id() == other.get_id() \
               and self.get_title() == other.get_title() \
               and self.get_description() == other.get_description() \
               and self.get_genre() == other.get_genre()

    def contains_key(self, other):
        # function that returns true if at least one field from self contains the corresponding field from other
        return other.get_id().lower() in str(self.get_id()).lower() \
               or other.get_title().lower() in self.get_title().lower() \
               or other.get_description().lower() in self.get_description().lower() \
               or other.get_genre().lower() in self.get_genre().lower()

    @staticmethod
    def read_movie (line):
        parts = line.split(",")
        return Movie(int(parts[0].strip()),parts[1].strip(), parts[2].strip(),parts[3].strip())

    @staticmethod
    def write_movie(movie):
        return str(movie.get_id())+","+movie.get_title()+','+movie.get_description()+','+movie.get_genre()


class Client:
    '''
    We have a class for 'client' entity which contains client id and name
    '''

    def __init__(self, clientId, name):
        self.__clientId = clientId
        self.__name = name

    # getters
    def get_id(self):
        return self.__clientId

    def get_name(self):
        return self.__name

    # setters
    def set_clientId(self, value):
        self.__clientId = value

    def set_name(self, value):
        self.__name = value

        # comparing 2 clients by their id's

    def __eq__(self, other):
        return self.__clientId == other.__clientId

    def __str__(self):
        return "Client ID: " + str(self.__clientId) + "\n" + \
               "Name: " + self.__name

    def special_replace(self, other):
        '''
        The function replaces the fields of an element (name) with those of a second element(other)
        If a certain field of 'other' is empty, the element keeps the initial value for that certain field
        '''
        if other.get_name() != '':
            self.set_name(other.get_name())

    def identical(self, other):
        # function returns true if all fields are the same for two elements
        return self.get_id() == other.get_id() and self.get_name() == other.get_name()

    def contains_key(self, other):
        # function that returns true if at least one field from self contains the corresponding field from other
        return other.get_id().lower() in str(self.get_id()).lower() \
               or other.get_name().lower() in self.get_name().lower()


    @staticmethod
    def read_client (line):
        parts = line.split(",")
        return Client(int(parts[0].strip()),parts[1].strip())

    @staticmethod
    def write_client(client):
        return str(client.get_id())+","+client.get_name()

class Rental:
    '''
    We have a class for 'rental' entity which contains rental id, client and movie ids, rental/due/returned dates
    '''

    def __init__(self, rentalId, movieId, clientId, rentDate, dueDate, returnDate):
        self.__rentalId = rentalId
        self.__movieId = movieId
        self.__clientId = clientId
        self.__rentDate = rentDate
        self.__dueDate = dueDate
        self.__returnDate = returnDate

    def get_rentalId(self):
        return self.__rentalId

    def get_movieId(self):
        return self.__movieId

    def get_clientId(self):
        return self.__clientId

    def get_rentDate(self):
        return self.__rentDate

    def get_dueDate(self):
        return self.__dueDate

    def get_returnDate(self):
        return self.__returnDate

    def set_rentalId(self, value):
        self.__rentalId = value

    def set_movieId(self, value):
        self.__movieId = value

    def set_clientId(self, value):
        self.__clientId = value

    def set_rentDate(self, value):
        self.__rentDate = value

    def set_dueDate(self, value):
        self.__dueDate = value

    def set_returnDate(self, value):
        self.__returnDate = value

    def __eq__(self, other):
        return self.get_rentalId() == other.get_rentalId()

    def __str__(self):
        if self.get_returnDate().empty() == False:
            return "Rental ID: " + str(self.__rentalId) + "\n" + \
                   "Movie ID: " + str(self.__movieId) + '\n' + \
                   "Client ID: " + str(self.__clientId) + '\n' + \
                   "   Rented:   " + str(self.get_rentDate()) + '\n' + \
                   "   Due date: " + str(self.get_dueDate()) + '\n' + \
                   "   Returned: " + str(self.get_returnDate()) + '\n'
        else:
            return "Rental ID: " + str(self.__rentalId) + "\n" + \
                   "Movie ID: " + str(self.__movieId) + '\n' + \
                   "Client ID: " + str(self.__clientId) + '\n' + \
                   "   Rented:   " + str(self.get_rentDate()) + '\n' + \
                   "   Due date: " + str(self.get_dueDate()) + '\n' + \
                   "   Returned: - \n"

    def identical(self, other):
        return self.get_rentalId() == other.get_rentalId() \
               and self.get_movieId() == other.get_movieId() \
               and self.get_clientId() == other.get_clientId() \
               and self.get_rentDate() == other.get_rentDate() \
               and self.get_dueDate() == other.get_dueDate() \
               and self.get_returnDate() == other.get_returnDate()

    def special_replace(self, other):
        self.set_returnDate(other.get_returnDate())

    def number_of_days_rented(self):
        # Function that returns the number of days for a certain rental, using rented date and returned date
        returned = self.get_returnDate()
        if returned == Date(0, 0, 0):
            returned = datetime.date.today()
        rented = self.get_rentDate()
        return (datetime.date(returned.year, returned.month, returned.day) - datetime.date(rented.year, rented.month,
                                                                                           rented.day)).days + 1

    def number_of_days_delayed(self):
        due = self.get_dueDate()
        current = datetime.date.today()
        return (current - datetime.date(due.year, due.month, due.day)).days + 1

    @staticmethod
    def read_rental(line):
        parts = line.split(",")
        date1 = parts[3].split('/')
        Date1 = Date(int(date1[0]), int(date1[1]), int(date1[2]))
        date2 = parts[4].split('/')
        Date2 = Date(int(date2[0]), int(date2[1]), int(date2[2]))
        date3 = parts[5].split('/')
        Date3 = Date(int(date3[0]), int(date3[1]), int(date3[2]))
        return Rental(int(parts[0].strip()),int(parts[1].strip()),int(parts[2].strip()), Date1, Date2, Date3)

    @staticmethod
    def write_rental(rental):
        return str(rental.get_rentalId())+","+str(rental.get_movieId())+','+str(rental.get_clientId())+","+str(rental.get_rentDate())+","+str(rental.get_dueDate())+","+str(rental.get_returnDate())




class Date:
    def __init__(self, day, month, year):
        self.__days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        self.day = day
        self.month = month
        self.year = year
        if year < 0 or month < 0 or month > 12 or day < 0 or day > self.__days[month - 1]:
            raise DateError('Date is not valid')

    def __str__(self):
        return str(self.day) + '/' + str(self.month) + '/' + str(self.year)

    def __eq__(self, other):
        return self.day == other.day and self.month == other.month and self.year == other.year

    def empty(self):
        return self.day == 0 and self.month == 0 and self.year == 0

    def __le__(self, other):
        return self.year < other.year or (self.year == other.year and self.month < other.month) or (
                    self.year == other.year and self.month == other.month and self.day <= other.day)





class Operation:

    def __init__(self, repository, action, reverse_action, object):
        self.__repository = repository
        self.__action = action
        self.__reverse_action = reverse_action
        self.__object = object

    def get_repo(self):
        return self.__repository
    def get_action(self):
        return self.__action
    def get_reverse(self):
        return self.__reverse_action
    def get_object(self):
        return self.__object

    def execute(self):
        #self.__action(self.__repository, self.__object)
        if self.get_action() == 'Repository.add':
            self.__repository.add(self.__object)
        elif self.get_action() == 'Repository.remove':
            self.__repository.remove(self.__object)

    def get_opposite_operation(self):
        return Operation(self.get_repo(), self.get_reverse(), self.get_action(), self.get_object())

class UpdateOperation:

    def __init__(self, repository, action, object, reverse_object):
        self.__repository = repository
        self.__action = action
        self.__object = object
        self.__reverse_object = reverse_object

    def get_repo(self):
        return self.__repository
    def get_action(self):
        return self.__action
    def get_reverse(self):
        return self.__reverse_object
    def get_object(self):
        return self.__object

    def execute(self):
        self.__repository.update(self.__object, self.__reverse_object)

    def get_opposite_operation(self):
        return UpdateOperation(self.get_repo(), self.get_action(), self.get_reverse(), self.get_object())


class ComplexOperation(Operation):

    def __init__(self):
        self.__operations = []

    def get_operation(self):
        return self.__operations

    def execute(self):
        for i in range(len(self.__operations) - 1, -1, -1):
            self.__operations[i].execute()

    def add_action(self, operation):
        self.__operations.append(operation)

    def get_opposite_operation(self):
        opposite = ComplexOperation()
        for i in range(len(self.__operations) - 1, -1, -1):
            operation = self.__operations[i]
            opposite.add_action(operation.get_opposite_operation())
        return opposite

