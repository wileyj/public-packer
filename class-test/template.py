import os
import logging
from logger import Logger


class template(object):
    logger = Logger()

    def delete(filename):
        """ docstring """
        if os.path.isfile(filename) and os.access(filename, os.R_OK):
            logging.error("Found Existing file: %s" % (filename))
            logging.error("Deleting: %s" % (filename))
            os.remove(filename)
        return 0

    def write_userdata_template(userdata_template_source, userdata_template_dest):
        """ docstring """
        template().delete(userdata_template_dest)
        result = ""
        logging.info("[ EXEC  ] - Writing UserData Template %s" % (userdata_template_dest))
        template = env.get_template(userdata_template_source+".jinja2")
        result = template.render()
        os.open(userdata_template_dest, os.O_CREAT)
        fd = os.open(userdata_template_dest, os.O_RDWR)
        os.write(fd, result)
        file_stat = os.stat(userdata_template_dest)
        file_size = file_stat.st_size
        logging.info("\tCreated userdata file %s ( %s )" % (userdata_template_dest, file_size))
        os.close(fd)
        return 0

    def write_template(template_values, template_source, template_dest, template_path, template_type):
        """ docstring """
        check_and_delete_file(template_dest)
        result = ""
        logging.error("[ EXEC  ] - Writing Template %s: %s:" % (template_type, template_source))
        logging.error("\tLooking for template (%s%s) to write %s" % (template_path, template_source, template_dest))
        print "\ttemplate_values: %s" % (template_values)
        print "\ttemplate_source: %s" % (template_source)
        print "\ttemplate_dest: %s" % (template_dest)
        print "\ttemplate_path: %s" % (template_path)
        packer_env = jinja2.Environment(loader=jinja2.FileSystemLoader([template_path]))
        template = packer_env.get_template(template_source)
        result = template.render(template_values)
        os.open(template_dest, os.O_CREAT)
        fd = os.open(template_dest, os.O_RDWR)
        os.write(fd, result)
        file_stat = os.stat(template_dest)
        file_size = file_stat.st_size
        logging.error("\tCreated Packer Template: %s ( %s )" % (template_dest, file_size))
        os.close(fd)
        return 0

    def write_services_template(template_values, template_source, template_dest, template_path):
        """ docstring """
        check_and_delete_file(template_dest)
        result = ""
        print "[ EXEC  ] - Writing Services Template %s" % (template_source)
        print "looking for %s%s to write %s" % (template_path, template_source, template_dest)
        jinja2_env = jinja2.Environment(loader=jinja2.FileSystemLoader([template_path]))
        template = jinja2_env.get_template(template_source)
        result = template.render(template_values)
        with open(template_dest, 'w') as output:
            output.write(result)
            print "\t Adding default_services to %s" % (template_dest)
            for service in default_services:
                filename = services_template_path+service+".service"
                print "\t  Read filename: %s" % (filename)
                with open(filename, 'r') as f:
                    for line in f:
                        output.write(line)
                    f.closed
        output.closed
        file_stat = os.stat(template_dest)
        file_size = file_stat.st_size
        print "\tCreated Services Script: %s ( %s )" % (template_dest, file_size)
        # os.close(fd)
        return 0
