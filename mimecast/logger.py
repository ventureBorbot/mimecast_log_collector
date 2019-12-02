import logging
import logging.handlers
import datetime
import configuration
import os


# Set up logging (in this case to terminal)
log = logging.getLogger(__name__)
log.root.setLevel(logging.DEBUG)
log_formatter = logging.Formatter('%(levelname)s %(message)s')
log_handler = logging.StreamHandler()
log_handler.setFormatter(log_formatter)
log.addHandler(log_handler)

# Set up syslog output
syslog_handler = logging.handlers.SysLogHandler(address=(configuration.syslog_details['syslog_server'], configuration.syslog_details['syslog_port']))
syslog_formatter = logging.Formatter('%(message)s')
syslog_handler.setFormatter(syslog_formatter)
syslogger = logging.getLogger(__name__)
syslogger = logging.getLogger('SysLogger')
syslogger.addHandler(syslog_handler)


# Supporting methods
def get_hdr_date():
    date = datetime.datetime.utcnow()
    dt = date.strftime("%a, %d %b %Y %H:%M:%S")
    return dt + " UTC"


def read_file(file_name):
    try:
        with open(file_name, 'r') as f:
            data = f.read()
        return data
    except Exception as e:
        log.error('Error reading file ' + file_name + '. Cannot continue. Exception: ' + str(e))
        quit()


def append_file(file_name, data_to_write): # Do not append duplicate data to file for the sake of IO read & usage
    try:
        found = False
        ttp_logfile = open(file_name, 'r')
        ttp_loglist = ttp_logfile.readlines()
        for line in ttp_loglist:
            if str(data_to_write) in line:
                found = True

        if not found:
            with open(file_name, 'a+', encoding="utf-8") as f:
                f.write(data_to_write + '\n')
    except Exception as e:
        log.error('Error reading file ' + file_name + '. Cannot continue. Exception: ' + str(e))
        quit()


def write_file(file_name, data_to_write):
    try:
        with open(file_name, 'w', encoding="utf-8") as f:
            f.write(data_to_write)
    except Exception as e:
        log.error('Error writing file ' + file_name + '. Cannot continue. Exception: ' + str(e))
        quit()


def delete_file(file_name):
    try:
        os.remove(file_name)
    except Exception as e:
        log.error('Error deleting file ' + file_name + '. Cannot continue. Exception: ' + str(e))
        quit()
