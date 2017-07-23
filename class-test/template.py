import os
import jinja2
from config import Global
import logging
from logger import Logger

logger = Logger()


class Template(object):
    def delete_template(self, filename):
        """ docstring """
        if os.path.isfile(filename) and os.access(filename, os.R_OK):
            logging.critical("Found Existing file: %s" % (filename))
            logging.critical("Deleting: %s" % (filename))
            os.remove(filename)
        return 0

    def write_template(self, template_values, template_source, template_dest, template_path, template_type):
        """ docstring """
        self.delete_template(template_dest)
        result = ""
        logging.error("[ EXEC  ] - Writing Template %s: %s:" % (template_type, template_source))
        logging.error("\tLooking for template (%s%s) to write %s" % (template_path, template_source, template_dest))
        logging.error("\ttemplate_values: %s" % (template_values))
        logging.error("\ttemplate_source: %s" % (template_source))
        logging.error("\ttemplate_dest: %s" % (template_dest))
        logging.error("\ttemplate_path: %s" % (template_path))
        jinja2_env = jinja2.Environment(loader=jinja2.FileSystemLoader([template_path]))
        template = jinja2_env.get_template(template_source)
        result = template.render(template_values)
        os.open(template_dest, os.O_CREAT)
        fd = os.open(template_dest, os.O_RDWR)
        os.write(fd, result)
        file_stat = os.stat(template_dest)
        file_size = file_stat.st_size
        logging.error("\tCreated Packer Template: %s ( %s )" % (template_dest, file_size))
        os.close(fd)
        return 0

    def write_services_template(self, template_values, template_source, template_dest, template_path, template_type):
        """ docstring """
        logging.critical("Deleting file: %s" % (template_dest))
        self.delete_template(template_dest)
        result = ""
        logging.error("[ EXEC  ] - Writing Template %s: %s:" % (template_type, template_source))
        logging.error("\tLooking for template (%s%s) to write %s" % (template_path, template_source, template_dest))
        logging.error("\ttemplate_values: %s" % (template_values))
        logging.error("\ttemplate_source: %s" % (template_source))
        logging.error("\ttemplate_dest: %s" % (template_dest))
        logging.error("\ttemplate_path: %s" % (template_path))
        jinja2_env = jinja2.Environment(loader=jinja2.FileSystemLoader([template_path]))
        template = jinja2_env.get_template(template_source)
        result = template.render(template_values)
        with open(template_dest, 'w') as output:
            output.write(result)
            logging.error("\t Adding default_services to %s" % (template_dest))
            for service in Global.default_services:
                filename = Global.services_template_path + service + ".service"
                logging.error("\t  Read filename: %s" % (filename))
                with open(filename, 'r') as f:
                    for line in f:
                        output.write(line)
                    f.closed
        output.closed
        file_stat = os.stat(template_dest)
        file_size = file_stat.st_size
        logging.error("\tCreated Services Script: %s ( %s )" % (template_dest, file_size))
        # os.close(fd)
        return 0
