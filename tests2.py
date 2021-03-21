import unittest
from repository import Repository, Stack
from service import ServiceRentals, ServiceMovies, ServiceClients
from undo import ServiceUndo
from valid import ValidRental, ValidMovie, ValidClient
from entities import Movie, Date, Rental, Client
from exceptions import RentingError, RepositoryError, ValidationError, DateError, TimelineError, UndoError


class TestsFirstFunctionality(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def test_init_movie_getProperties(self):
        movie = Movie(1, 'Frozen', 'Ice queen with magical powers', 'Animation')
        self.__valid_movie = movie
        self.assertEqual(movie.get_id(),1)
        self.assertEqual (movie.get_title(), 'Frozen')
        self.assertEqual (movie.get_description(), 'Ice queen with magical powers')
        self.assertEqual (movie.get_genre(), 'Animation')

    def test_setters_movie_changedProperties(self):
        movie = Movie(1, 'Frozen', 'Ice queen with magical powers', 'Animation')
        movie.set_title('Frozen 2')
        self.assertEqual(movie.get_title(), 'Frozen 2')
        movie.set_movieId(2)
        self.assertEqual(2,movie.get_id())

    def test_str_validMovie_string(self):
        movie = Movie(1,'a','b','c')
        self.assertEqual(str(movie),"Movie ID: 1" + "\n" + "Title: a"  + "\n" + "Description: b"  + "\n" + "Genre: c")

    def test_eq_moviesSameID_True(self):
        movie = Movie(1, 'Frozen', 'Ice queen with magical powers', 'Animation')
        self.__movie_sameID = Movie(1, 'Frozen 2', 'Ice queen with magical powers', 'Kids')
        self.assertEqual(movie, self.__movie_sameID)

    def test_specialReplace_elUpdateNonemptyFields_allFieldsReplaced(self):
        movie = Movie(1, 'Frozen', 'Ice queen with magical powers', 'Animation')
        self.__movieUpdate = Movie(1, 'Frozen 2', 'Story about sisters', 'Family')
        movie.special_replace(self.__movieUpdate)
        self.assertTrue(self.__movieUpdate.identical(movie))

    def test_specialReplace_elUpdate1EmptyField_1remainsUnchanged(self):
        movie = Movie(1, 'Frozen', 'Ice queen with magical powers', 'Animation')
        self.__movieUpdate_emptyField = Movie(1, 'Frozen 3', '', 'Family')
        movie.special_replace(self.__movieUpdate_emptyField)
        self.assertEqual(movie.get_title(),'Frozen 3' )
        self.assertEqual(movie.get_description(), 'Ice queen with magical powers')
        self.assertEqual(movie.get_genre(), 'Family')

    def test_identical_identicalMovies_True(self):
        movie = Movie(1, 'Frozen 2', 'Ice queen with magical powers', 'Animation')
        self.__valid_movie = movie
        self.assertTrue(self.__valid_movie.identical(movie))

    def test_identical_differentMovies_False(self):
        movie = Movie(1, 'Frozen', '-', 'Family')
        self.__valid_movie = Movie(1, 'Frozen 2', 'Ice queen with magical powers', 'Animation')
        self.assertFalse(self.__valid_movie.identical(movie))


    def test_validate_validMovie_None(self):
        self.__valid_movie = Movie(1,'a','a','a')
        validator = ValidMovie()
        validator.validate_movie(self.__valid_movie)

    def test_validate_invalidID_throwsException(self):
        validator = ValidMovie()
        self.__movie_invalidID = Movie(-2, 'Lion King', 'Hamlet for kids', 'Animation')
        with self.assertRaises(ValidationError):
            validator.validate_movie(self.__movie_invalidID)

    def test_validate_invalidTitle_throwsException(self):
        validator = ValidMovie()
        self.__movie_invalidTitle = Movie(1, '', 'No description', 'Horror')
        with self.assertRaises(ValidationError):
            validator.validate_movie(self.__movie_invalidTitle)

    def test_validate_invalidMovie_throwsException(self):
        validator = ValidMovie()
        self.__invalid_movie = Movie(-2, '', '-', 'Drama')
        with self.assertRaises(ValidationError):
            validator.validate_movie(self.__invalid_movie)

    def test_add_newMovie_movieIsAdded(self):
        movie = Movie(1, 'a','a','a')
        repo = Repository()
        repo.add(movie)
        self.assertEqual(repo.size(), 1)
        self.assertEqual(repo.get_all()[repo.size() - 1], movie)

    def test_add_movieSameID_throwsException(self):
        movie = Movie(1,'a','','')
        movie_sameID = Movie(1,'b','','')
        repository = Repository()
        repository.add(movie)
        with self.assertRaises(RepositoryError):
            repository.add(movie_sameID)

    def test_ServiceAdd_validMovie_isAdded(self):
        undo_stack = Stack()
        redo_stack = Stack()
        self.__movie_validator = ValidMovie()
        self.__movie_repository = Repository()
        self.__rental_repository = Repository
        self.__movie_service = ServiceMovies(self.__movie_repository, self.__movie_validator, undo_stack, redo_stack, self.__rental_repository)
        self.__valid_movie = Movie(1, 'Frozen', 'Ice queen with magical powers', 'Animation')
        self.__movie_service.add_movie(1, 'Frozen', 'Ice queen with magical powers', 'Animation')
        self.assertEqual(self.__movie_service.get_movies()[self.__movie_service.get_number() - 1],self.__valid_movie)

    def test_ServiceAdd_invalidId_throwsException(self):
        undo_stack = Stack()
        redo_stack = Stack()
        self.__movie_validator = ValidMovie()
        self.__movie_repository = Repository()
        self.__rental_repository = Repository
        self.__movie_service = ServiceMovies(self.__movie_repository, self.__movie_validator, undo_stack, redo_stack, self.__rental_repository)
        with self.assertRaises(ValidationError):
            self.__movie_service.add_movie(-1, '-', '-', '-')

    def test_ServiceAdd_invalidTitle_throwsException(self):
        undo_stack = Stack()
        redo_stack = Stack()
        self.__movie_validator = ValidMovie()
        self.__movie_repository = Repository()
        self.__rental_repository = Repository
        self.__movie_service = ServiceMovies(self.__movie_repository, self.__movie_validator, undo_stack, redo_stack,
                                             self.__rental_repository)
        with self.assertRaises(ValidationError):
            self.__movie_service.add_movie(2, '', '-', '-')

    def test_ServiceAdd_invalidMovie_throwsException(self):
        undo_stack = Stack()
        redo_stack = Stack()
        self.__movie_validator = ValidMovie()
        self.__movie_repository = Repository()
        self.__rental_repository = Repository
        self.__movie_service = ServiceMovies(self.__movie_repository, self.__movie_validator, undo_stack, redo_stack,
                                             self.__rental_repository)
        with self.assertRaises(ValidationError):
            self.__movie_service.add_movie(-1, '', '-', '-')

    def test_ServiceAdd_existingId_throwsException(self):
        undo_stack = Stack()
        redo_stack = Stack()
        self.__movie_validator = ValidMovie()
        self.__movie_repository = Repository()
        self.__rental_repository = Repository
        self.__movie_service = ServiceMovies(self.__movie_repository, self.__movie_validator, undo_stack, redo_stack, self.__rental_repository)
        self.__movie_service.add_movie(1,'a','','')
        with self.assertRaises(RepositoryError):
            self.__movie_service.add_movie(1, '-', '-', '-')


    def test_remove_movie_isRemoved(self):
        repository = Repository()
        movie = Movie(1, '-','-','-')
        repository.add(movie)
        repository.remove(movie)
        self.assertEqual(repository.size(), 0)


    def test_ServiceRemove_existingMovie_isRemoved(self):
        undo_stack = Stack()
        redo_stack = Stack()
        self.__rental_repository = Repository()
        self.__movie_validator = ValidMovie()
        self.__movie_repository = Repository()
        self.__movie_service = ServiceMovies(self.__movie_repository, self.__movie_validator, undo_stack, redo_stack, self.__rental_repository)
        self.__movie_service.add_movie(1, '-','-','-')
        self.__movie_service.remove_movie(1)
        self.assertEqual(self.__movie_service.get_number(), 0)

    def test_ServiceRemove_inexistentMovie_throwsException(self):
        undo_stack = Stack()
        redo_stack = Stack()
        self.__movie_validator = ValidMovie()
        self.__movie_repository = Repository()
        rental_repository = Repository()
        self.__movie_service = ServiceMovies(self.__movie_repository, self.__movie_validator, undo_stack, redo_stack, rental_repository)
        self.__movie_service.add_movie(1, '-', '-', '-')
        with self.assertRaises(RepositoryError):
            self.__movie_service.remove_movie(2)


    def test_updateElement_withAllFields_elementUpdated(self):
        repository = Repository()
        movie = Movie(1, 'Frozen', 'Ice queen with magical powers', 'Animation')
        repository.add(movie)
        movieUpdate = Movie(1, '-','-','-')
        repository.update(movie, movieUpdate)
        self.assertTrue(repository.get_all()[0].identical(movieUpdate))

    def test_updateElement_with1emptyField_elementUpdated1fieldUnchanged(self):
        repository = Repository()
        movie = Movie(1, 'Frozen', 'Ice queen with magical powers', 'Animation')
        repository.add(movie)
        repository.update(movie, Movie(1,'','a','b'))
        expected_result = Movie(1, 'Frozen', 'a', 'b')
        self.assertTrue(repository.get_all()[0].identical(expected_result))


    def test_ServiceUpdate_movieWithAllFields_allFieldsUpdated(self):
        undo_stack = Stack()
        redo_stack = Stack()
        self.__movie_validator = ValidMovie()
        self.__movie_repository = Repository()
        self.__rental_repository = Repository
        self.__movie_service = ServiceMovies(self.__movie_repository, self.__movie_validator, undo_stack, redo_stack, self.__rental_repository)
        self.__movie_service.add_movie(1, 'Harry Potter', 'Witchcraft', 'Adventure')
        self.__movie_service.update_movie(1, 'Harry Potter 2', 'Wizardry', 'Action')
        expected = Movie(1, 'Harry Potter 2', 'Wizardry', 'Action')
        self.assertTrue(self.__movie_service.get_movies()[0].identical(expected))

    def test_ServiceUpdate_movieWith1emptyField_thatFieldIsUnchanged(self):
        undo_stack = Stack()
        redo_stack = Stack()
        self.__movie_validator = ValidMovie()
        self.__movie_repository = Repository()
        self.__rental_repository = Repository
        self.__movie_service = ServiceMovies(self.__movie_repository, self.__movie_validator, undo_stack, redo_stack,
                                             self.__rental_repository)
        self.__movie_service.add_movie(1, 'Harry Potter', 'Witchcraft', 'Adventure')
        self.__movie_service.update_movie(1, '', '-', '-')
        expected = Movie(1, 'Harry Potter', '-', '-')
        self.assertTrue( self.__movie_service.get_movies()[0].identical(expected) )

    def test_ServiceUpdate_inexistentId_throwsException(self):
        undo_stack = Stack()
        redo_stack = Stack()
        self.__movie_validator = ValidMovie()
        self.__movie_repository = Repository()
        self.__rental_repository = Repository
        self.__movie_service = ServiceMovies(self.__movie_repository, self.__movie_validator, undo_stack, redo_stack,
                                             self.__rental_repository)
        self.__movie_service.add_movie(1, 'Harry Potter', 'Witchcraft', 'Adventure')
        with self.assertRaises(RepositoryError):
            self.__movie_service.update_movie(2, '', '', '')


    def test_init_client_getProperties(self):
        client = Client(1, 'Jonn Doe')
        self.assertEqual(client.get_id(),1)
        self.assertEqual (client.get_name(), 'Jonn Doe')

    def test_setters_client_changedProperties(self):
        self.__valid_client = Client(1,'-')
        self.__valid_client.set_name('John Doe')
        self.assertEqual( self.__valid_client.get_name() , 'John Doe')
        self.__valid_client.set_clientId(2)
        self.assertEqual(self.__valid_client.get_id(),2)

    def test_str_validClient_string(self):
        client = Client(1,'o')
        self.assertEqual(str(client), "Client ID: 1"+'\n'+'Name: o')

    def test_eq_clientsSameID_True(self):
        self.__valid_client = Client(1, '-')
        self.__client_sameID = Client(1, 'Jane Doe')
        self.assertEqual( self.__valid_client , self.__client_sameID)

    def test_identical_identicalClients_True(self):
        client = Client(1, 'John Doe')
        self.__valid_client = Client(1, 'John Doe')
        self.assertTrue( self.__valid_client.identical(client) )

    def test_identical_differentClients_False(self):
        self.__valid_client = Client(1, '-')
        client = Client(1, 'Billy')
        self.assertFalse( self.__valid_client.identical(client) )


    def test_validate_validClient_None(self):
        validator = ValidClient()
        self.__valid_client = Client(1,'a')
        validator.validate_client(self.__valid_client)

    def test_validate_invalidClientID_throwsException(self):
        validator = ValidClient()
        self.__client_invalidID = Client(-2, 'Elsa')
        with self.assertRaises(ValidationError):
            validator.validate_client(self.__client_invalidID)

    def test_validate_invalidName_throwsException(self):
        validator = ValidClient()
        self.__client_invalidName = Client(1, '')
        with self.assertRaises(ValidationError):
            validator.validate_client(self.__client_invalidName)

    def test_validate_invalidClient_throwsException(self):
        validator = ValidClient()
        self.__invalid_client = Client(-2, '')
        with self.assertRaises(ValidationError):
            validator.validate_client(self.__invalid_client)

    def test_ServiceAdd_validClient_isAdded(self):
        undo_stack = Stack()
        redo_stack = Stack()
        self.__rental_repository = Repository()
        self.__client_validator = ValidClient()
        self.__client_repository = Repository()
        self.__client_service = ServiceClients(self.__client_repository, self.__client_validator, undo_stack, redo_stack, self.__rental_repository)
        self.__client_service.add_client(1, 'John Doe')
        self.assertEqual( self.__client_service.get_clients()[self.__client_service.get_number() - 1] , Client(1, 'John Doe'))

    def test_ServiceAdd_invalidClientId_throwsException(self):
        undo_stack = Stack()
        redo_stack = Stack()
        self.__rental_repository = Repository()
        self.__client_validator = ValidClient()
        self.__client_repository = Repository()
        self.__client_service = ServiceClients(self.__client_repository, self.__client_validator, undo_stack, redo_stack, self.__rental_repository)
        with self.assertRaises(ValidationError):
            self.__client_service.add_client(-1, '-')

    def test_ServiceAdd_invalidName_throwsException(self):
        undo_stack = Stack()
        redo_stack = Stack()
        self.__rental_repository = Repository()
        self.__client_validator = ValidClient()
        self.__client_repository = Repository()
        self.__client_service = ServiceClients(self.__client_repository, self.__client_validator, undo_stack, redo_stack, self.__rental_repository)
        with self.assertRaises(ValidationError):
            self.__client_service.add_client(2, '')

    def test_ServiceAdd_invalidClient_throwsException(self):
        undo_stack = Stack()
        redo_stack = Stack()
        self.__rental_repository = Repository()
        self.__client_validator = ValidClient()
        self.__client_repository = Repository()
        self.__client_service = ServiceClients(self.__client_repository, self.__client_validator, undo_stack, redo_stack, self.__rental_repository)
        with self.assertRaises(ValidationError):
            self.__client_service.add_client(-1, '')

    def test_ServiceAdd_existingClientId_throwsException(self):
        undo_stack = Stack()
        redo_stack = Stack()
        self.__rental_repository = Repository()
        self.__client_validator = ValidClient()
        self.__client_repository = Repository()
        self.__client_service = ServiceClients(self.__client_repository, self.__client_validator, undo_stack, redo_stack, self.__rental_repository)
        self.__client_service.add_client(1,'o')
        with self.assertRaises(RepositoryError):
            self.__client_service.add_client(1, '-')


    def test_ServiceRemove_existingClient_isRemoved(self):
        undo_stack = Stack()
        redo_stack = Stack()
        self.__rental_repository = Repository()
        self.__client_validator = ValidClient()
        self.__client_repository = Repository()
        self.__client_service = ServiceClients(self.__client_repository, self.__client_validator, undo_stack, redo_stack, self.__rental_repository)
        self.__client_service.add_client(1, '-')

        self.__client_service.remove_client(1)
        self.assertEqual( self.__client_service.get_number() , 0)

    def test_ServiceRemove_inexistentClient_throwsException(self):
        undo_stack = Stack()
        redo_stack = Stack()
        self.__rental_repository = Repository()
        self.__client_validator = ValidClient()
        self.__client_repository = Repository()
        self.__client_service = ServiceClients(self.__client_repository, self.__client_validator, undo_stack, redo_stack, self.__rental_repository)
        self.__client_service.add_client(1, '-')
        with self.assertRaises(RepositoryError):
            self.__client_service.remove_client(2)


    def test_ServiceUpdate_client_isUpdated(self):
        undo_stack = Stack()
        redo_stack = Stack()
        self.__rental_repository = Repository()
        self.__client_validator = ValidClient()
        self.__client_repository = Repository()
        self.__client_service = ServiceClients(self.__client_repository, self.__client_validator, undo_stack, redo_stack, self.__rental_repository)
        self.__client_service.add_client(1, 'Bob')

        self.__client_service.update_client(1, 'Billy')
        self.assertEqual( self.__client_service.get_clients()[0].get_name() , 'Billy')

    def test_ServiceUpdate_inexistentClientId_throwsException(self):
        undo_stack = Stack()
        redo_stack = Stack()
        self.__rental_repository = Repository()
        self.__client_validator = ValidClient()
        self.__client_repository = Repository()
        self.__client_service = ServiceClients(self.__client_repository, self.__client_validator, undo_stack, redo_stack, self.__rental_repository)
        self.__client_service.add_client(1, 'Bob')
        with self.assertRaises(RepositoryError):
            self.__client_service.update_client(2, '-')




class TestsSecondFunctionality(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def initialize(self):
        undoStack = Stack()
        redoStack = Stack()
        self.__rental_validator = ValidRental()
        self.__movies_repository = Repository()
        self.__clients_repository = Repository()
        self.__rentals_repository = Repository()
        self.__service_rentals = ServiceRentals(self.__movies_repository, self.__clients_repository,
                                                self.__rentals_repository, self.__rental_validator, undoStack, redoStack)

        self.__movies_repository.add(Movie(1, 'Frozen', 'Ice', 'Animation'))
        self.__movies_repository.add(Movie(2, 'Harry Potter', 'Wizard', 'Adventure'))
        self.__clients_repository.add(Client(1, 'John Doe'))
        self.__clients_repository.add(Client(2, 'Jane Doe'))

        self.assertEqual(self.__service_rentals.get_number(),0)

    def test_setters_rental_areSet(self):
        rental = Rental(1,1,1,Date(1,1,1),Date(2,2,2),Date(0,0,0))
        rental.set_clientId(2)
        self.assertEqual(rental.get_clientId(),2)
        rental.set_movieId(2)
        self.assertEqual(rental.get_movieId(),2)
        rental.set_rentalId(2)
        self.assertEqual(rental.get_rentalId(),2)
        rental.set_rentDate(Date(2,1,1))
        self.assertEqual(rental.get_rentDate(),Date(2,1,1))
        rental.set_dueDate(Date(3,3,3))
        self.assertEqual(rental.get_dueDate(),Date(3,3,3))

    def test_str_rental_string(self):
        rental = Rental(1,1,1,Date(1,1,1),Date(2,2,2),Date(0,0,0))
        self.assertEqual(str(rental), "Rental ID: 1" + "\n" + "Movie ID: 1" + '\n' +"Client ID: 1"+'\n'+"   Rented:   1/1/1"+ '\n' + "   Due date: 2/2/2" + '\n' + "   Returned: - \n")
        rental = Rental(1,1,1,Date(1,1,1),Date(2,2,2),Date(3,3,3))
        self.assertEqual(str(rental),"Rental ID: 1" + "\n" + "Movie ID: 1" + '\n' + "Client ID: 1" + '\n' + "   Rented:   1/1/1" + '\n' + "   Due date: 2/2/2" + '\n' + "   Returned: 3/3/3"+"\n")

    def test_identical_sameRentals_True(self):
        rental = Rental(1, 1, 1, Date(1, 1, 1), Date(2, 2, 2), Date(0, 0, 0))
        rental1 = Rental(1, 1, 1, Date(1, 1, 1), Date(2, 2, 2), Date(0, 0, 0))
        self.assertTrue(rental.identical(rental1))

    def test_daysRented_rental_returnsNrOfDays(self):
        rental = Rental(1, 1, 1, Date(1, 1, 1), Date(2, 2, 2), Date(4, 1, 1))
        self.assertEqual(rental.number_of_days_rented(),4)

    def test_invalidDate(self):
        with self.assertRaises(DateError):
            d = Date(111,111,11)

    def test_getDate_invalidForm_ThrowsException(self):
        self.initialize()
        with self.assertRaises(DateError):
            self.__service_rentals.get_date('1234')

    def test_validateRental_validRental_none(self):
        self.initialize()
        rentals = self.__service_rentals.get_rentals()
        rental = Rental(1,1,1,Date(2,1,1), Date(2,2,2), Date(3,3,3))
        self.__rental_validator.validate_rental(rental, rentals)

    def test_validateRental_unavailableMovie_throwsException(self):
        self.initialize()
        self.__service_rentals.rent_movie(1,1,1,'1/1/1','2/2/2')
        rentals = self.__service_rentals.get_rentals()
        rental = Rental(2,1,2,Date(2,1,1), Date(2,2,2), Date(3,3,3))
        with self.assertRaises(ValidationError):
            self.__rental_validator.validate_rental(rental, rentals)

    def test_validateRental_lateClient_throwsException(self):
        self.initialize()
        self.__service_rentals.rent_movie(1, 1, 1, '1/1/1', '2/2/1')
        rentals = self.__service_rentals.get_rentals()
        rental = Rental(2, 2, 1, Date(2,1,2), Date(2,2,2), Date(3,3,3))
        with self.assertRaises(ValidationError):
            self.__rental_validator.validate_rental(rental, rentals)


    def test_rent_validMovieAndClient_rentalIsCreated(self):
        self.initialize()
        self.__service_rentals.rent_movie(1, 1, 1, '1/1/2000', '1/1/2001')
        rental = Rental(1, 1, 1, Date(1, 1, 2000), Date(1, 1, 2001), Date(0, 0, 0))
        self.assertEqual(self.__service_rentals.get_rentals()[0], rental)

    def test_rent_unavailableMovie_throwsException(self):
        self.initialize()
        self.__service_rentals.rent_movie(1, 1, 1, '1/1/2000', '1/1/2001')
        with self.assertRaises(RentingError):
            self.__service_rentals.rent_movie(2, 1, 2, '2/2/2000', '3/3/2000')

    def test_rent_clientPassedDueDate_throwsException(self):
        self.initialize()
        self.__service_rentals.rent_movie(1, 1, 1, '1/1/2000', '1/1/2001')
        with self.assertRaises(RentingError):
            self.__service_rentals.rent_movie(2, 2, 1, '2/1/2001', '2/2/2001')

    def test_rent_existingRentalId_throwsException(self):
        self.initialize()
        self.__service_rentals.rent_movie(1, 1, 1, '1/1/2000', '1/1/2001')
        with self.assertRaises(RepositoryError):
            self.__service_rentals.rent_movie(1, 2, 2, '2/1/2001', '2/2/2001')

    def test_rent_inexistentMovieClientId_throwsException(self):
        self.initialize()
        with self.assertRaises(RepositoryError):
            self.__service_rentals.rent_movie(1, 3, 2, '2/1/2001', '2/2/2001')

    def test_rent_timelineError_exception(self):
        self.initialize()
        with self.assertRaises(TimelineError):
            self.__service_rentals.rent_movie(1,1,1,'2/2/2','1/1/1')

    def testRent(self):
        self.test_rent_validMovieAndClient_rentalIsCreated()
        self.test_rent_unavailableMovie_throwsException()
        self.test_rent_clientPassedDueDate_throwsException()
        self.test_rent_existingRentalId_throwsException()
        self.test_rent_inexistentMovieClientId_throwsException()

    def test_return_rentedMovie_returnDateIsAdded(self):
        self.initialize()
        self.__service_rentals.rent_movie(1, 1, 1, '1/1/2000', '1/1/2001')
        self.__service_rentals.return_movie(1, '2/2/2000')
        self.assertEqual(Date(2, 2, 2000),
                         self.__rentals_repository.search(Rental(1, '', '', '', '', '')).get_returnDate())

    def test_return_notrentedMovie_throwsException(self):
        self.initialize()
        with self.assertRaises(RepositoryError):
            self.__service_rentals.return_movie(1, '1/1/1')

    def test_return_returnedMovie_throwsException(self):
        self.initialize()
        self.__service_rentals.rent_movie(1, 1, 1, '1/1/2000', '1/1/2001')
        self.__service_rentals.return_movie(1, '2/2/2000')
        with self.assertRaises(RentingError):
            self.__service_rentals.return_movie(1, '9/9/9999')

    def test_return_timelineError_exception(self):
        self.initialize()
        self.__service_rentals.rent_movie(1,1,1,'1/1/2','2/2/2')
        with self.assertRaises(TimelineError):
            self.__service_rentals.return_movie(1,'1/1/1')

    def testReturn(self):
        self.test_return_rentedMovie_returnDateIsAdded()
        self.test_return_notrentedMovie_throwsException()
        self.test_return_returnedMovie_throwsException()


class TestsThirdFunctionality(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def initialize(self):
        self.__valid_movie = ValidMovie()
        self.__valid_client = ValidClient()
        self.__movies_repository = Repository()
        self.__clients_repository = Repository()
        self.__rentals_repository = Repository()
        undoStack = Stack()
        redoStack = Stack()
        self.__service_movies = ServiceMovies(self.__movies_repository, self.__valid_movie, undoStack, redoStack, self.__rentals_repository)
        self.__service_clients = ServiceClients(self.__clients_repository, self.__valid_client, undoStack, redoStack, self.__rentals_repository)

        self.__movies_repository.add(Movie(1, 'Frozen', 'Ice', 'Animation'))
        self.__movies_repository.add(Movie(2, 'Harry Potter', 'Wizard', 'Adventure'))
        self.__clients_repository.add(Client(1, 'John Doe'))
        self.__clients_repository.add(Client(2, 'Jane Doe'))

    def test_searchMovie_validKey_returnsMovies(self):
        self.initialize()
        found_movies = self.__service_movies.search_movie('otter')
        expected_result = Movie(2, 'Harry Potter', 'Wizard', 'Adventure')
        self.assertEqual(expected_result, found_movies[0])

    def test_searchClient_validKey_returnsClients(self):
        self.initialize()
        found_clients = self.__service_clients.search_client('doe')
        found_client1 = Client(1, 'John Doe')
        found_client2 = Client(2, 'Jane Doe')
        self.assertEqual(found_client1, found_clients[0])
        self.assertEqual(found_client2, found_clients[1])



class TestsFourthFunctionality(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def initialize(self):
        undoStack = Stack()
        redoStack = Stack()
        self.__valid_movie = ValidMovie()
        self.__valid_client = ValidClient()
        self.__valid_rental = ValidRental()
        self.__movies_repository = Repository()
        self.__clients_repository = Repository()
        self.__rentals_repository = Repository()
        self.__service_movies = ServiceMovies(self.__movies_repository, self.__valid_movie, undoStack, redoStack, self.__rentals_repository)
        self.__service_clients = ServiceClients(self.__clients_repository, self.__valid_client, undoStack, redoStack, self.__rentals_repository)
        self.__service_rentals = ServiceRentals(self.__movies_repository, self.__clients_repository, self.__rentals_repository, self.__valid_rental, undoStack, redoStack)
        self.__service_movies.generate_movies()
        self.__service_clients.generate_client()

        self.__service_rentals.rent_movie(1,1,1,'1/1/1','2/1/1')
        self.__service_rentals.return_movie(1,'3/1/1')
        self.__service_rentals.rent_movie(3,1,1,'5/1/1','10/1/1')
        self.__service_rentals.return_movie(3,'15/1/1')
        self.__service_rentals.rent_movie(2,2,2,'2/2/2','3/3/3')
        self.__service_rentals.return_movie(2,'7/2/2')
        self.__service_rentals.rent_movie(4,3,4,'1/1/1','2/1/1')
        self.__service_rentals.return_movie(4,'2/1/1')

    def test_most_rented(self):
        self.initialize()
        result = self.__service_rentals.most_rented()
        self.assertEqual(result[0].movie.get_id(), 1)
        self.assertEqual(result[1].movie.get_id(), 2)
        self.assertEqual(result[2].movie.get_id(), 3)

    def test_most_active(self):
        self.initialize()
        result = self.__service_rentals.most_active()
        self.assertEqual(result[0].client.get_id(), 1)
        self.assertEqual(result[1].client.get_id(), 2)
        self.assertEqual(result[2].client.get_id(), 4)

    def test_late_rentals(self):
        self.initialize()
        self.__service_rentals.rent_movie(11,1,1,'4/4/4','5/5/5')
        self.__service_rentals.rent_movie(12, 2, 2, '4/4/4', '5/5/5')
        result = self.__service_rentals.late_rentals()
        print(result)
        self.assertEqual(result[0].movie_id, 1)
        self.assertEqual(result[1].movie_id, 2)


class TestUndoRedo(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def test(self):

        valid_movie = ValidMovie()
        valid_client = ValidClient()
        valid_rental = ValidRental()
        repository_movie = Repository()
        repository_client = Repository()
        repository_rental = Repository()
        undo_stack = Stack()
        redo_stack = Stack()
        service_movie = ServiceMovies(repository_movie, valid_movie, undo_stack, redo_stack, repository_rental)
        service_client = ServiceClients(repository_client, valid_client, undo_stack, redo_stack, repository_rental)
        service_rental = ServiceRentals(repository_movie, repository_client, repository_rental, valid_rental, undo_stack, redo_stack)
        service_undo = ServiceUndo(undo_stack, redo_stack)
        service_undo.clear()

        service_movie.add_movie(1,'a','a','a')
        service_undo.undo()
        self.assertEqual(0,service_movie.get_number())
        service_undo.redo()
        self.assertEqual(service_movie.get_movies()[0],Movie(1,'a','a','a'))

        service_client.add_client(1, 'a')
        service_undo.undo()
        self.assertEqual(0, service_client.get_number())
        service_undo.redo()
        self.assertEqual(service_client.get_clients()[0], Client(1, 'a'))
        with self.assertRaises(UndoError):
            service_undo.redo()

        service_client.update_client(1,'b')
        service_undo.undo()
        self.assertEqual(service_client.get_clients()[0].get_name(), 'a')
        service_undo.redo()
        self.assertEqual(service_client.get_clients()[0].get_name(), 'b')

        service_rental.rent_movie(1,1,1,'1/1/1','2/2/2')
        service_client.remove_client(1)
        self.assertEqual(service_rental.get_number(),0)
        self.assertEqual(service_client.get_number(),0)
        service_undo.undo()
        self.assertEqual(service_rental.get_number(), 1)
        self.assertEqual(service_client.get_number(), 1)
        service_undo.redo()
        self.assertEqual(service_rental.get_number(), 0)
        self.assertEqual(service_client.get_number(), 0)

        service_client.add_client(1,'a')
        service_rental.rent_movie(1,1,1,'1/1/1','2/2/2')
        service_undo.undo()
        self.assertEqual(service_rental.get_number(), 0)
        service_undo.redo()
        self.assertEqual(service_rental.get_rentals()[0], Rental(1,1,1,Date(1,1,1), Date(2,2,2), Date(0,0,0)))

        service_rental.return_movie(1,'3/3/3')
        service_undo.undo()
        self.assertEqual(service_rental.get_rentals()[0].get_returnDate(), Date(0,0,0))
        service_undo.redo()
        self.assertEqual(service_rental.get_rentals()[0].get_returnDate(), Date(3,3,3))