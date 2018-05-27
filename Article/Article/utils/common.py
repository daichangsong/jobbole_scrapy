import hashlib
import MySQLdb


def get_md5(url):
    if isinstance(url, str):
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

if __name__ == '__main__':
    # conn = MySQLdb.connect(host="127.0.0.1", user="root", password="Alves123",
    #                        db="scrapyspider")
    # cursor = conn.cursor()
    # print(get_md5("http://jobbole.com".encode('utf-8')))
    pass
