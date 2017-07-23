import logging
from logger import Logger
import os


class Exec(object):

    def Packer(self, binary, packer_template, shell_template, salt_template, userdata_template):
        ''' docstring '''
        logging.warning("\tLaunching: %s" % (binary))
        logging.warning("\tUsing Template: %s" % (packer_template))
        logging.critical("exec: %s build %s" % (binary, packer_template))
        try:
            os.system(binary + ' build ' + packer_template)
        except:
            logging.exception("Packer exception occurred")
        logging.error("Removing Packer template: %s" % (packer_template))
        os.remove(packer_template)
        logging.error("Removing Shell template: %s" % (shell_template))
        os.remove(shell_template)
        logging.error("Removing Salt Grains template: %s" % (salt_template))
        os.remove(salt_template)
        logging.error("Removing Userdata template: %s" % (userdata_template))
        os.remove(userdata_template)
        return 0
