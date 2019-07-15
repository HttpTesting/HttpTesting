

import hashlib 
import re
import time
from HttpTesting.library.scripts import parse_args_func

class FUNC:
    """
    Framework function library.

    Usage:
        %{FUNC.md5(txt)}%
    """

    @staticmethod
    def md5(txt=''):
        """
        The md5 string is generated.

        Args:
            txt: The string to generate md5.
        Usage:
            ret = md5(txt)
        Return:
            ret: The md5 string is generated.
        """
        mo = hashlib.md5()
        src = txt.encode(encoding='utf-8')
        mo.update(src)   
        
        return mo.hexdigest()

    @staticmethod
    def timestamp():
        """
        The timestamp
        """
        return int(time.time())



if __name__ == "__main__":

    data = {"name":"%{md5('aaaa')}%", "ag":"%{md5('cccc')}%"}
    ret = parse_args_func(FUNC, data)
    print(ret)

    