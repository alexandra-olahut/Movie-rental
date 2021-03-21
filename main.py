from entities import Client, Rental, Movie
from valid import ValidMovie, ValidClient, ValidRental
from repository import Repository, Stack
from service import ServiceMovies, ServiceClients, ServiceRentals
from undo import ServiceUndo
from ui import Console



''' Validators '''
valid_movie = ValidMovie()
valid_client = ValidClient()
valid_rental = ValidRental()

''' Undo Controller '''
undo_stack = Stack()
redo_stack = Stack()


''' Repositories '''
# loading settings.properties

filepath = "settings_binary.properties"

try:
    file = open(filepath, "r")
    line = file.readline().strip()  # reading repository = ...
    line = line.split(" ")
    if line[2] == "inmemory":
        repository_movie = Repository()
        repository_client = Repository()
        repository_rental = Repository()
        ''' Services '''
        service_movie = ServiceMovies(repository_movie, valid_movie, undo_stack, redo_stack, repository_rental)
        service_client = ServiceClients(repository_client, valid_client, undo_stack, redo_stack, repository_rental)
        service_rental = ServiceRentals(repository_movie, repository_client, repository_rental, valid_rental, undo_stack, redo_stack)
        service_undo = ServiceUndo(undo_stack, redo_stack)

        ''' Initializing '''
        service_movie.generate_movies()
        service_client.generate_client()


    elif line[2] == "text":
        from text_files import FileRepo

        line = file.readline().strip()
        line = line.split(" ")
        repository_movie = FileRepo(line[2], Movie.read_movie, Movie.write_movie)

        line = file.readline().strip()
        line = line.split(" ")
        repository_client = FileRepo(line[2], Client.read_client, Client.write_client)

        line = file.readline().strip()
        line = line.split(" ")
        repository_rental = FileRepo(line[2], Rental.read_rental, Rental.write_rental)

        ''' Services '''
        service_movie = ServiceMovies(repository_movie, valid_movie, undo_stack, redo_stack, repository_rental)
        service_client = ServiceClients(repository_client, valid_client, undo_stack, redo_stack, repository_rental)
        service_rental = ServiceRentals(repository_movie, repository_client, repository_rental, valid_rental, undo_stack, redo_stack)
        service_undo = ServiceUndo(undo_stack, redo_stack)




    elif line[2] == "binary":
        from binary_files import BinaryRepository

        line = file.readline().strip()
        line = line.split(" ")
        repository_movie = BinaryRepository(line[2])

        line = file.readline().strip()
        line = line.split(" ")
        repository_client = BinaryRepository(line[2])

        line = file.readline().strip()
        line = line.split(" ")
        repository_rental = BinaryRepository(line[2])

        ''' Services '''
        service_movie = ServiceMovies(repository_movie, valid_movie, undo_stack, redo_stack, repository_rental)
        service_client = ServiceClients(repository_client, valid_client, undo_stack, redo_stack, repository_rental)
        service_rental = ServiceRentals(repository_movie, repository_client, repository_rental, valid_rental, undo_stack, redo_stack)
        service_undo = ServiceUndo(undo_stack, redo_stack)

    file.close()

except IOError as error:
    print(str(error))


'''
service_rental.rent_movie(1, 1, 1, '1/1/2018', '2/2/2018')
service_rental.return_movie(1, '9/1/2018')
service_rental.rent_movie(2, 5, 6, '3/3/2018','3/3/2019')
service_rental.rent_movie(4, 7, 8,'11/11/2018', '11/11/2019')
service_rental.return_movie(2, '4/3/2019')
service_rental.rent_movie(3, 1, 7, '4/4/2018', '5/5/2018')
service_rental.return_movie(3,'8/8/2018')
service_rental.rent_movie(5, 9, 8, '1/1/2019', '6/6/2019')
service_rental.rent_movie(6, 6, 4, '11/11/2019', '1/1/2020')
service_rental.rent_movie(7, 1, 2, '13/11/2019', '23/11/2019')
service_rental.rent_movie(8, 8, 3, '12/9/2019', '13/1/2020')
service_rental.return_movie(8, '23/10/2019')
service_rental.rent_movie(9, 10, 10, '12/11/2019', '1/1/2020')
'''
service_undo.clear()

''' UI '''
ui = Console(service_movie, service_client, service_rental, service_undo)
ui.run()