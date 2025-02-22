#!/usr/bin/env python3
import logging
import getopt
import sys
import os

from businesslogic.collector import Collector


LOG_LEVEL = {
    'CRITICAL': logging.CRITICAL,
    'ERROR': logging.ERROR,
    'WARNING': logging.WARNING,
    'INFO': logging.INFO,
    'DEBUG': logging.DEBUG
}


def is_globalplaceholder_valid(placeholderpath):
    return os.path.exists(placeholderpath)


if __name__ == '__main__':
    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, 'i:l:e:g:', ['instructions=', 'loglevel=', 'examiner=', 'globalplaceholders='])
    except getopt.GetoptError:
        print("mosk.py -i <instructionsfile> -l [CRITICAL]")
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-i', '--instructions'):
            instructionsfile = arg
        elif opt in ('-l', '--loglevel'):
            if arg.upper() in LOG_LEVEL.keys():
                logging.basicConfig(level=LOG_LEVEL[arg.upper()], format='%(asctime)s  %(name)s  %(levelname)s: %(message)s')
            else:
                raise KeyError("'{}' not a valid log level.".format(arg))
        elif opt in ('-e', '--examiner'):
            examiner = arg
        elif opt in ('-g', '--globalplaceholders'):
            if is_globalplaceholder_valid(arg):
                globalplaceholders = arg
            else:
                print(f"Globale placeholder file '{arg}' does not exist.")
                sys.exit(2)

    try:
        logger = logging.getLogger(__name__)
        collector = Collector.get_collector(instructionsfile=instructionsfile, examiner=examiner,
                                            placeholderfile=globalplaceholders)
        collector.collect()
        logger.info("Collection complete.")
    except NameError:
        print("The arguments 'instructionsfile', and 'examiner' are mandatory.")
        sys.exit(2)
    except FileNotFoundError:
        print(f"Could not initialize parser. Instructions file '{instructionsfile}' does not exist.")
        sys.exit(2)
