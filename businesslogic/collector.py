import logging
from instructionparsers.xmlparser import XmlParser
from contextlib import suppress
from instructionparsers.wrapper import InstructionWrapper
from baseclasses.artefact import ArtefactBase
from baseclasses.protocol import ProtocolBase
from businesslogic.placeholders import Placeholder
from protocol.logfileprotocol import LogFileProtocol


# TODO There should be a way to provide comments for the protocol by defining them in the instructions file
class Collector:
    _logger = logging.getLogger(__name__)

    def __init__(self, parser: XmlParser, protocol: ProtocolBase):
        self._parser = parser
        self._protocol = protocol

    @classmethod
    def get_collector(cls, instructionsfile: str, examiner: str = '',
                      placeholderfile: str = Placeholder.get_globalplaceholderfile()):
        Placeholder.set_globalplaceholderfile(placeholderfile)
        protocol = LogFileProtocol(examiner)
        xmlparser = XmlParser(instructionsfile, protocol)
        collector = cls(parser=xmlparser, protocol=protocol)
        return collector

    def collect(self):
        self._document_metadata()
        self._collect_from_instrcutions(self._parser.instructions)

    def _document_metadata(self):
        for metafield in self._parser.metadatafields:
            self._protocol.writer_protocol_entry(entryheader='',
                                                 entrydata="{}: {}"
                                                 .format(metafield, self._parser.get_metadata(metafield)))

    def _collect_from_instrcutions(self, current_instruction: InstructionWrapper, callpath: str = ''):
        if callpath == '':
            callpath = str(current_instruction)
        else:
            callpath = "{}->{}".format(callpath, str(current_instruction))

        # travel down to the leaf elements of the instruction tree
        # which are artefacts
        for child in current_instruction.instructionchildren:
            self._collect_from_instrcutions(child, callpath)

        # HACK: This is a rather whaky way of determining if the object is right
        # Another way would be to use 'isinstance' which I try not to use to
        # avoid implementing my own ABC.
        if 'collect' in dir(current_instruction.instruction):
            self._collect_and_document(current_instruction.instruction, callpath=callpath)

            if current_instruction.placeholdername != '':
                Placeholder.update_placeholder(current_instruction.placeholdername,
                                               current_instruction.instruction.data)
                Collector._logger.info("Stored artefact data '{}' as placeholder '{}'.".
                                       format(current_instruction.instruction.data,
                                              current_instruction.placeholdername))
        else:
            Collector._logger.debug(callpath)

    def _collect_and_document(self, artefact: ArtefactBase, callpath: str):
        # The following implicitly calls ArtefactBase.collect() because
        # ArtefactBase implements __call__.
        with suppress(BaseException):
            artefact()
            Collector._logger.debug("{} - collected data".format(callpath))

        self._protocol.writer_protocol_entry(entrydata=artefact.getdocumentation(),
                                             entryheader=callpath)
        self._protocol.writer_protocol_entry(entryheader='', entrydata=' ')

        if artefact.data is None:
            self._protocol.writer_protocol_entry(entrydata="Could not collect data for artefact '{}'\n"
                                                           "due to unhandled exception."
                                                 .format(str(type(artefact))),
                                                 entryheader='')
        else:
            with suppress(TypeError):
                self._protocol.writer_protocol_entry(entrydata=str(artefact), entryheader='')

        self._protocol.writer_protocol_entry(entryheader='', entrydata=' ')

    # TODO document start date
    # TODO document start time
    # TODO document end date
    # TODO document end time
