from exceptions import RepositoryError, UndoError


class Repository(object):
    def __init__(self):
        self._entities = []

    def get_all(self):
        # Function that returns the list of entities
        return self._entities[:]

    def size(self):
        # Function that returns the number of entities
        return len(self._entities)

    def search(self, key):
        # Function that search an element (given as key) in the collection of entities
        if key not in self._entities:
            raise RepositoryError("The element (movie/client/rental) doesn't exist \n")
        for element in self._entities:
            if element == key:
                return element

    def search_by_all_fields(self, key):
        # Function that returns a list of entities having the search_key in at least one of its fields
        matching_entities = []
        for entity in self.get_all():
            if entity.contains_key(key):
                matching_entities.append(entity)
        return matching_entities

    def add(self, element):
        '''
        Function that adds element to the list of entities
        * Raises exception if element is already in the list (verified by the ID)
        '''
        if element in self._entities:
            raise RepositoryError('Id already exists \n')
        self._entities.append(element)

    def remove(self, element):
        '''
        Function that removes a given element, from the list of entities
        '''
        self._entities.remove(element)

    def update(self, element, element_update):
        '''
        Function that replaces a given element with a second given element
        '''
        for entity in self._entities:
            if entity == element:
                entity.special_replace(element_update)


class Stack():

    def __init__(self):
        self.__operations = []


    def push_op(self, operation):
        self.__operations.append(operation)

    def pop_op(self):
        if len(self.__operations) == 0:
            raise UndoError("No more undo's")
        return self.__operations.pop()

    def clear(self):
        self.__operations = []

