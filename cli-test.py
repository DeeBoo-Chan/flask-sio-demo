# -*- coding: utf-8 -*-


try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen


def main(times=1024):
    url = 'http://127.0.0.1:5000/task?msg=hello'
    for i in range(0, times):
        print('{0:5} / {1}'.format(i + 1, times))
        urlopen(url)

if __name__ == '__main__':
    main(256)