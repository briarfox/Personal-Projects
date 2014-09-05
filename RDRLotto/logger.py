import logging
logging.basicConfig(filename='logfile.log',
                    level=logging.DEBUG,
                    format='%(levelname)s %(asctime)s %(name)s:%(message)s') # include timestamp)
LEVEL = {"debug": logging.DEBUG,
          "info": logging.INFO,
          "warning": logging.WARNING,
          "critical": logging.CRITICAL,
          }

def get_log(name='misc',level = "debug"):
    
    log1 = logging.getLogger(name)
    log1.setLevel(LEVEL[level])
    return log1



