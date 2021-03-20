from os import path

from baseclasses.artefact import ArtefactBase
from source.localhost import expandfilepath


class FileExistence(ArtefactBase):
    FILE_PATH_PARAMETER = "filepath"

    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)
        self.__title = 'Filesystem'
        self.__collectionmethod = 'os.path.exists'
        self.__description = 'Find a file by file name including the path or parts of the path.'

    def collect(self):
        filepath = self._parameters[self.FILE_PATH_PARAMETER]
        filepath = expandfilepath(filepath)
        if path.exists(filepath):
            self.data = "File '{}' exists.".format(filepath)
            self.data.sourcepath = filepath
        else:
            self.data = "File '{}' does not exist.".format(filepath)

    def title(self):
        return self.__title

    def collectionmethod(self):
        return self.__collectionmethod

    def description(self):
        return self.__description


class FileContent(ArtefactBase):
    FILE_PATH_PARAMETER = "filepath"

    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)

    def collect(self):
        filepath = self._parameters[self.FILE_PATH_PARAMETER]
        filepath = expandfilepath(filepath)
        if path.exists(filepath):
            with open(filepath) as filetoload:
                self.data = filetoload.read()
        else:
            self.data = "File '{}' does not exist.".format(
                self.get_parameter(self.FILE_PATH_PARAMETER))
