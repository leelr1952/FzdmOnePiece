import requests
import os
from FzdmOnePiece.utils.common import get_md5


if __name__ == "__main__":
    agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/" \
            "537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"

    header = {
        "User-Agent": agent,
    }

    # http://222.160.218.70:9999
    # http://112.81.143.4:8118

    proxies = {"https": "http://112.81.143.4:8118"}
    res = requests.get("http://manhua.fzdm.com/2/", headers=header, proxies=proxies)
    print(res.status_code)