from urllib.error import URLError
from urllib.request import urlopen

SSL_MSG = "unable to get local issuer certificate"


def unsafe_ok(url):
    try:
        urlopen(url)
        return False

    except URLError as e:
        if SSL_MSG in e.reason.verify_message:
            return True
        return False
