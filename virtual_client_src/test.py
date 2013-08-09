import json
#from copy import deepcopy

import http
import log
import etc

if __name__ == "__main__":
    ht = http.Http()
    ht.connect_times("jsonfe.funshion.com", "/?cli=apad&ver=0.1.0&src=wonder&type=tv", 3)
