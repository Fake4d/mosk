import logging
from collections import namedtuple
from os import path

from baseclasses.artefact import ArtefactBase
from businesslogic.support import get_userfolders


TermianlHistory = namedtuple('TerminalHistory', ['Path', 'Content'])


class ShellHistoryOfAllUsers(ArtefactBase):
    _logger = logging.getLogger(__name__)

    def __init__(self, *args, **kwargs):
        ArtefactBase.__init__(self, *args, **kwargs)
        self.__title = 'ShellHistoryOfAllUsers'
        self.__collectionmethod = 'os.file'
        self.__description = \
            'Retrieves all user folers and tries to find bash shell and zhs shell history files and\r\n' \
            'then tries to store their content.\r\n' \
            'IMPORTANT: None-Unicode-Characters wont be stored.'

    def __str__(self):
        result = 'Collection Timestamp: {}\r\n\r\n'.format(self.data.currentdatetime)
        for data in self.data.collecteddata:
            result = result + "{}START{}\nPATH: {}\n\nCONTENT:\n{}\n{} END {}".format('*' * 20, '*' * 20,
                                                                                      data.Path, data.Content,
                                                                                      '+' * 20, '+' * 20)
        return result

    def collect(self):
        userfolders = list(get_userfolders())
        self.data = list(ShellHistoryOfAllUsers._collect_bash_history(userfolders))

    def title(self):
        return self.__title

    def collectionmethod(self):
        return self.__collectionmethod

    def description(self):
        return self.__description

    @staticmethod
    def _collect_bash_history(userfolders):
        historyfilepaths = [path.join(folder, history) for folder in userfolders
                            for history in ['.bash_history', '.zsh_history']]
        for historyfile in historyfilepaths:
            if path.exists(historyfile):
                ShellHistoryOfAllUsers._logger.debug("Found terminal history file '{}'.".format(historyfile))
                with open(historyfile, encoding='unicode_escape') as hf:
                    yield TermianlHistory(Path=historyfile, Content=hf.read())
