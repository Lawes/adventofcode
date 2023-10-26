import hashlib

if __name__ == '__main__':

    n = 609043
    beg = hashlib.md5(b'abcdef609043').hexdigest()[:5]
    print(type(beg), beg)

    key = b'yzbqklnj'

    n = 0
    while True:

        n += 1
        pub = key + str(n).encode('ascii')
        md5 = hashlib.md5(pub).hexdigest()

        if n%10000 == 0:
            print(pub, md5[:5])

        if md5[:6] == '000000':
            break

    print(n)