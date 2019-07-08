
import logging

class LOG:
    """The log module.
    """
    @staticmethod
    def console_info(msg):
        """
        The log level is Info.
        """
        logging.basicConfig(
            level = logging.INFO, 
            format = '[%(levelname)s] - %(asctime)s - %(message)s'
        )

        logging.info(msg)


LOG.console_info('Start info')