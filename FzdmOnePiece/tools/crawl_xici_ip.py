import requests
from scrapy.selector import Selector
import MySQLdb


conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="leelr1952", db="fzdmop", charset="utf8")
cursor = conn.cursor()

def crawl_ip():
    """
    获取西刺代理ip
    :return:
    """
    ip_list = []
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit "
                            "537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"}
    # for i in range(10):
    # for循环次数太多，本机ip被封，此处使用代理访问，西刺代理过段时间解封
    # proxies = {"http":"182.139.161.2:9797","https":"182.139.161.2:9797"}
    for i in range(2):
        re = requests.get("http://www.xicidaili.com/nn/{0}".format(i+1), headers=headers)

        selector = Selector(text=re.text)
        all_trs = selector.css("#ip_list tr")
        for tr in all_trs[1:]:
            speed_str = tr.css(".bar::attr(title)").extract()[0]
            if speed_str:
                speed = speed_str.split("秒")[0]
            all_text = tr.css("td::text").extract()

            ip = all_text[0]
            port = all_text[1]
            proxy_type = all_text[5]

            ip_list.append((ip,port,proxy_type,speed))

    for ip_info in ip_list:
        cursor.execute(
            "INSERT IGNORE INTO proxy_ip(ip,port,speed,proxy_type) VALUES('{0}','{1}',{2},'{3}')".format(
                ip_info[0], ip_info[1], ip_info[3], ip_info[2]
            )
        )
        conn.commit()
# crawl_ip()


class GetIp(object):

    def delete_ip(self,ip):
        # 删除数据库中的不可用ip
        delete_sql = """
                    DELETE FROM proxy_ip WHERE ip = '{0}'
                    """.format(ip)
        cursor.execute(delete_sql)
        conn.commit()
        return True

    def judge_ip(self, ip, port, proxy_type):
        # 判断ip是否可用
        http_url = "https://lol.qq.com/"
        proxy_url_type = 'http' if proxy_type == 'http' else 'https'
        proxy_url = proxy_url_type+ "://{0}:{1}".format(ip,port)

        try:
            proxy_dict = {
                "http":proxy_url
            }
            response = requests.get(http_url, proxies=proxy_dict)
        except Exception as e:
            print("invalid ip and port" + proxy_url)
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if code >= 200 and code <300:
                print("effective ip:" + proxy_url)
                return True
            else:
                print("invalid ip and port")
                self.delete_ip(ip)
                return False

    def get_random_ip(self):
        # 从数据库随机获取一个ip
        random_get_sql = """
                        SELECT ip,port,proxy_type FROM proxy_ip
                        ORDER BY RAND()
                        LIMIT 1
                        """
        result = cursor.execute(random_get_sql)
        for ip_info in cursor.fetchall():
            ip = ip_info[0]
            port = ip_info[1]
            proxy_type = ip_info[2].lower()

            judge_resulet = self.judge_ip(ip,port,proxy_type)
            if judge_resulet:
                print("这里返回有效代理ip{2}://{0}:{1}".format(ip,port,proxy_type))
                return "{2}://{0}:{1}".format(ip,port,proxy_type)
            else:
                return self.get_random_ip()

if __name__ == "__main__":
    get_ip = GetIp()
    get_ip.get_random_ip()
    # crawl_ip()

