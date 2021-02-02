#!/usr/bin/env python3
import getopt
import sys

from businesslogic.log import LOG_LEVEL, setup_logging, mosk_logger
from instructionparsers.xmlparser import XmlParser
from businesslogic.collector import Collector
from protocol.logfileprotocol import LogFileProtocol


def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'i:l:e:', ['instructions=', 'loglevel=', 'examiner='])
    except getopt.GetoptError:
        print("mosk.py -i <instructionsfile> -l [CRITICAL")
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-i', '--instructions'):
            instructionsfile = arg
        elif opt in ('-l', '--loglevel'):
            if arg in LOG_LEVEL.keys():
                setup_logging(arg)
            else:
                raise KeyError("'{}' not a valid log level.".format(arg))
        elif opt in ('-e', '--examiner'):
            examiner = arg

    try:
        # TODO There needs to be a central, controlling instance where to start. Currently there is no
        # such instance. So, for example, is a problem when it comes to define the phase we are in.
        protocol = LogFileProtocol(examiner)
        xmlparser = XmlParser(instructionsfile, protocol)
        collector = Collector(parser=xmlparser, protocol=protocol)
        collector.collect()
        mosk_logger.info("Collcetion complete.")
    except FileNotFoundError:
        print('Could not initialize parser.')
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
