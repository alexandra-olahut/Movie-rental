from repository import Repository


class FileRepo(Repository):

    def __init__(self, filename, read_object, write_object):
        self.__filename = filename
        self.__read_object = read_object
        self.__write_object = write_object
        Repository.__init__(self)

    def __read_all_from_file(self):
        self._entities = []
        with open(self.__filename, "r") as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line != "":
                    _object = self.__read_object(line)
                    self._entities.append(_object)
        file.close()

    def __write_all_to_file(self):
        with open(self.__filename, "w") as file:
            for _object in self._entities:
                line = self.__write_object(_object)
                file.write(line + "\n")
        file.close()

    def add(self, element):
        self.__read_all_from_file()
        Repository.add(self, element)
        self.__write_all_to_file()

    def update(self, element, element_update):
        self.__read_all_from_file()
        Repository.update(self, element, element_update)
        self.__write_all_to_file()

    def remove(self, element):
        self.__read_all_from_file()
        Repository.remove(self, element)
        self.__write_all_to_file()


    def get_all(self):
        self.__read_all_from_file()
        return Repository.get_all(self)
    def size(self):
        self.__read_all_from_file()
        return Repository.size()
    def search(self, search_key):
        self.__read_all_from_file()
        return Repository.search(self, search_key)

    def search_by_all_fields(self, search_string):
        self.__read_all_from_file()
        return Repository.search_by_all_fields(self, search_string)