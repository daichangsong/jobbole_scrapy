from scrapy.cmdline import execute
import sys
import os


# 获取当前main文件的绝对路径的上级目录路径，并将其添加到path中
print(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(['scrapy', 'crawl', 'jobbole'])