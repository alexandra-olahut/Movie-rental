from repository import Repository
import pickle
import os


class BinaryRepository(Repository):
    def __init__(self, fileName):
        Repository.__init__(self)
        self._fileName = fileName
        self._loadFile()


    def add(self, _object):
        self._entities = []
        self._loadFile()
        Repository.add(self, _object)
        self._saveFile()

    def remove(self, element):
        self._entities = []
        self._loadFile()
        Repository.remove(self, element)
        self._saveFile()

    def update(self, element, element_updated):
        self._entities = []
        self._loadFile()
        Repository.update(self, element, element_updated)
        self._saveFile()

    def _saveFile(self):
        '''
        1. Open text file for writing 'w'
        2. for each element in the repository:
            a. transform it into one-line string
            b. write it to the file
        3. close file
        '''
        filepath = self._fileName
        file = open(filepath, 'wb')

        for element in Repository.get_all(self):
            pickle.dump(element, file)

        file.close()

    def _loadFile(self):

        filepath = self._fileName
        file = open(filepath, "rb")

        if os.path.getsize(filepath) > 0:
            with open(filepath, "rb") as file:
                while True:
                    try:
                        _object = pickle.load(file)
                        Repository.add(self, _object)

                    except EOFError:
                        break

        file.close()