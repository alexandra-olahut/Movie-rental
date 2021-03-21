from exceptions import ValidationError, RepositoryError, InputError, UndoError


class Console(object):

    def __read_id(self):
        while True:
            number = input('ID: ')
            try:
                number = int(number)
                return number
            except ValueError:
                print('ID must be an integer')

    def __print_list(self, list_):
        for element in list_:
            print(element)
            print('')

    def __undo(self):
        self.__serviceUndo.undo()

    def __redo(self):
        self.__serviceUndo.redo()

    def __statistics(self):
        print('Type: ')
        print('1 - for most rented movies')
        print('2 - for most active clients')
        print('3 - for late rentals')
        task = input('>>')
        if task == '1':
            self.__print_list(self.__serviceRentals.most_rented())
        elif task == '2':
            self.__print_list(self.__serviceRentals.most_active())
        elif task == '3':
            self.__print_list(self.__serviceRentals.late_rentals())
        else:
            print(' ! Invalid command')

    def __search(self):
        print('Choose what you wish to search for')
        print('m - for movies /n', 'c - for clients')
        entity = input('>>')
        if entity != 'm' and entity != 'c':
            raise InputError('invalid input')
        search_key = input('Search:  ')
        if entity == 'm':
            movies_found = self.__serviceMovies.search_movie(search_key)
            self.__print_list(movies_found)
        if entity == 'c':
            clients_found = self.__serviceClients.search_client(search_key)
            self.__print_list(clients_found)

    def __ui_rent(self):
        try:
            rentalId = int(input('Rental ID: '))
            movieId = int(input('Movie ID: '))
            clientId = int(input('Client ID: '))
        except ValueError:
            raise InputError('ID must be an integer')

        print('  * Insert date as day/month/year (00/00/0000) format')
        rentDate = input('Rented date: ')
        dueDate = input('Due date: ')
        self.__serviceRentals.rent_movie(rentalId, movieId, clientId, rentDate, dueDate)

    def __ui_return(self):
        try:
            rentalId = int(input('Rental ID: '))
        except ValueError:
            raise InputError('ID must be an integer')

        print('  * Insert date as day/month/year (00/00/0000) format')
        returnDate = input('Returned date: ')
        self.__serviceRentals.return_movie(rentalId, returnDate)

    def __ui_list_rentals(self):
        for rental in self.__serviceRentals.get_rentals():
            print(rental)

    def __rent_return(self):
        print('Insert the action you wish to proceed (rent/return)')
        print(" * type 'back' to return to app menu")
        print(" * type 'list' to list all rentals")
        action = input('> ')
        if action == 'back':
            return
        if action == 'list':
            self.__ui_list_rentals()
        elif action == 'rent':
            self.__ui_rent()
        elif action == 'return':
            self.__ui_return()
        else:
            print(' ! Invalid command')

    def __manage(self):
        print('Choose which list you wish to manage:')
        print('   Type: m - for movies  /  c - for clients')

        command = input('> ')
        if command == 'm':
            self.__manage_movies()
        elif command == 'c':
            self.__manage_clients()
        else:
            print(' ! Invalid command')

    def __manage_movies(self):
        print('a - add \n u - update \n r - remove \n l - list')
        command = input(' > ')
        if command in self.__movie_commands:
            self.__movie_commands[command]()
        else:
            print(' ! Invalid command')

    def __manage_clients(self):
        print(' a - add \n u - update \n r - remove \n l - list')
        command = input(' > ')
        if command in self.__client_commands:
            self.__client_commands[command]()
        else:
            print(' ! Invalid command')

    def __ui_add_movie(self):
        movieId = self.__read_id()
        title = input('Title: ')
        description = input('Description: ')
        genre = input('Genre: ')
        self.__serviceMovies.add_movie(movieId, title, description, genre)

    def __ui_remove_movie(self):
        print('Movie of given Id will be deleted')
        movieId = self.__read_id()
        self.__serviceMovies.remove_movie(movieId)

    def __ui_update_movie(self):
        print('For given Id, you can update its title, description and genre')
        print('  * If you wish to keep a certain field unchaged, just press enter')
        movieId = self.__read_id()
        title = input('Title: ')
        description = input('Description: ')
        genre = input('Genre: ')
        self.__serviceMovies.update_movie(movieId, title, description, genre)

    def __ui_list_movie(self):
        for movie in self.__serviceMovies.get_movies():
            print(movie)
            print('')

    def __ui_add_client(self):
        clientId = self.__read_id()
        name = input('Name: ')
        self.__serviceClients.add_client(clientId, name)

    def __ui_remove_client(self):
        print('Client of given Id will be deleted')
        clientId = self.__read_id()
        self.__serviceClients.remove_client(clientId)

    def __ui_update_client(self):
        clientId = self.__read_id()
        name = input('New name: ')
        self.__serviceClients.update_client(clientId, name)

    def __ui_list_client(self):
        for client in self.__serviceClients.get_clients():
            print(client)
            print('')

    def __init__(self, serviceMovies, serviceClients, serviceRentals, serviceUndo):
        self.__serviceMovies = serviceMovies
        self.__serviceClients = serviceClients
        self.__serviceRentals = serviceRentals
        self.__serviceUndo = serviceUndo
        self.__commands = {
            '1': self.__manage,
            '2': self.__rent_return,
            '3': self.__search,
            '4': self.__statistics,
            'u': self.__undo,
            'r': self.__redo}
        self.__movie_commands = {
            'a': self.__ui_add_movie,
            'r': self.__ui_remove_movie,
            'u': self.__ui_update_movie,
            'l': self.__ui_list_movie}
        self.__client_commands = {
            'a': self.__ui_add_client,
            'r': self.__ui_remove_client,
            'u': self.__ui_update_client,
            'l': self.__ui_list_client}

    def menu(self):
        print('App menu')
        print('  Insert:  ')
        print('1 - to manage the lists of movies and clients')
        print('2 - to rent or return a movie')
        print('3 - to search for clients or movies')
        print('4 - to create statistics')
        print('u - undo')
        print('r - redo')
        print('x - exit')
        print('')

    def run(self):
        self.menu()
        while True:
            task = input('>>> ')
            if task == 'x':
                return
            elif task in self.__commands:
                try:
                    self.__commands[task]()
                except InputError as text:
                    print(' ! Input error: ' + str(text))
                except ValidationError as text:
                    print(' ! Validity error: ' + str(text))
                except RepositoryError as text:
                    print(' ! Repository error: ' + str(text))
                except UndoError as text:
                    print(' ! Undo Error: ' + str(text))

            else:
                print(' ! Invalid command')



