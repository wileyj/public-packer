import logging
import os
from args import Args


class Logger:
    def __init__(self):
        print "Logger"
        args = Args().args
        if args.verbose > 3:
            log_format = '[DEBUG] - %(lineno)-4s %(levelno)-4s %(asctime)-15s  %(message)-4s'
            logging.basicConfig(level=logging.DEBUG, format=log_format)
            os.environ["PACKER_LOG"] = "error"
        elif args.verbose == 3:
            log_format = '[WARN]  - %(lineno)-4s %(levelno)-4s %(message)-4s'
            logging.basicConfig(level=logging.WARNING, format=log_format)
            os.environ["PACKER_LOG"] = "error"
        elif args.verbose == 2:
            log_format = '[ERROR] - %(lineno)-4s %(levelno)-4s %(message)-4s'
            logging.basicConfig(level=logging.ERROR, format=log_format)
            os.environ["PACKER_LOG"] = "error"
        else:
            log_format = '%(message)-4s'
            logging.basicConfig(level=logging.CRITICAL, format=log_format)
            os.environ["PACKER_LOG"] = "info"
