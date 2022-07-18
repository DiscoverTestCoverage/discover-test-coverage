"""Create a syslog remote server."""

from fortify_coverage_cli import output

import logging
import logging.handlers
import socketserver

LOG_FILE = ".fortify.log"
HOST, PORT = "127.0.0.1", 2525

logger = logging.getLogger("fortify-syslog")


class SyslogUDPHandler(socketserver.BaseRequestHandler):
    """Syslog UDP handler for receiving debugging messages."""

    def handle(self):
        """Receive a message and then display it in output and log it to a file."""
        global logger
        # receive the message from the syslog logging client
        message = bytes.decode(self.request[0].strip(), encoding="utf-8")
        # remote not-printable characters that can appear in message
        enhanced_message = str(message).replace("<15>", "")
        enhanced_message = enhanced_message.replace("\x00", "")
        # display the message inside of the syslog's console
        output.console.print(enhanced_message)
        # write the logging message to a file using a rotating file handler
        logger.debug(enhanced_message)


def run_syslog_server():
    """Run a syslog server."""
    global logger
    # always log all of the messages to a file
    logger.setLevel(logging.DEBUG)
    # create a RotatingFileHandler such that:
    # -- it is stored in a file
    # -- it can never be bigger than 1 MB
    # -- one backup is created when log file gets too big
    rotating_file_handler = logging.handlers.RotatingFileHandler(
        LOG_FILE, maxBytes=1048576, backupCount=1
    )
    # add the rotating file handler to the logger
    logger.addHandler(rotating_file_handler)
    # startup the server and then let it run forever
    try:
        server = socketserver.UDPServer((HOST, PORT), SyslogUDPHandler)
        server.serve_forever(poll_interval=0.5)
    # let the server crash and raise an error on SystemExit and IOError
    except SystemExit:
        raise
    except IOError:
        raise
    # display a diagnostic message when server is manually stopped
    except KeyboardInterrupt:
        output.console.print(":person_shrugging: Shut down fortify's sylog server")
        output.console.print()
