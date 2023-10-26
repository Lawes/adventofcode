import numpy as np

def load_input(filemane):
    with open(filemane, 'r') as f:
        transmission = next(f).strip()
    return transmission


def hex2bin(hexa):
    hexa2bin = {
        '0': '0000',
        '1': '0001',
        '2': '0010',
        '3': '0011',
        '4': '0100',
        '5': '0101',
        '6': '0110',
        '7': '0111',
        '8': '1000',
        '9': '1001',
        'A': '1010',
        'B': '1011',
        'C': '1100',
        'D': '1101',
        'E': '1110',
        'F': '1111'
    }

    return ''.join((hexa2bin[t] for t in hexa))


def bin2num(bintxt):
    val = 0
    for d in bintxt:
        val = 2 * val + int(d)
    return val


def product(it):
    res = 1
    for elem in it:
        res *= elem
    return res

class Reader(object):
    def __init__(self, t, isbin=False):
        self.data = hex2bin(t) if not isbin else t
        self.rewind()

    def rewind(self):
        self.pos = 0

    def read(self, n):
        res = self.data[self.pos: self.pos+n]
        self.pos += n

        if self.pos > len(self.data):
            raise ValueError('EOF')
        return res


    def decode(self):
        tokens = []
        while True:
            try:
                lex = self.read_packet()
            except Exception as e:
                break
            tokens.append(lex)
        return tokens


    def read_packet(self):
        version = bin2num(self.read(3))
        typeid = bin2num(self.read(3))

        content = None

        if typeid == 4:
            content = self.read_content_value()
        else:
            content = self.read_content_operator()

        return {'version': version, 'type': typeid, 'content': content}


    def read_content_value(self):
        binval = ''

        while True:
            group = self.read(5)

            prefix = group[0]
            binval += group[1:]
            if prefix == '0':
                break

        return bin2num(binval)


    def read_content_operator(self):
        lenghtid = self.read(1)
        if lenghtid == '0':
            binsize = bin2num(self.read(15))

            subcontent = self.read(binsize)
            content = Reader(subcontent, isbin=True).decode()
        else:
            nsubpacket = bin2num(self.read(11))

            content = []
            for _ in range(nsubpacket):
                content.append(self.read_packet())

        return content


def sum_version(tokens):
    sum = 0
    for t in tokens:
        sum += t['version']
        if isinstance(t['content'], list):
            sum += sum_version(t['content'])

    return sum

def get_val(token):
    val = None
    if token['type'] == 4:
        val = token['content']
    else:
        stack = [get_val(t) for t in token['content']]
        if token['type'] == 0:
            val = np.sum(stack)
        elif token['type'] == 1:
            val = np.prod(stack)
        elif token['type'] == 2:
            val = np.min(stack)
        elif token['type'] == 3:
            val = np.max(stack)
        elif token['type'] == 5:
            val = 1 if stack[0] > stack[1] else 0
        elif token['type'] == 6:
            val = 1 if stack[0] < stack[1] else 0
        elif token['type'] == 7:
            val = 1 if stack[0] == stack[1] else 0

    return val


if __name__ == '__main__':
    device = Reader('EE00D40C823060')

    print(device.decode())

    for test in ['8A004A801A8002F478', '620080001611562C8802118E34', 'C0015000016115A2E0802F182340', 'A0016C880162017C3686B18A3D4780']:
        print('*', test)
        tokens = Reader(test).decode()
        print(tokens)
        print('sum', sum_version(tokens))

    transmission = load_input('input')
    device = Reader(transmission)
    tokens = device.decode()

    print('part1', sum_version(tokens))
    print('part2')

    for test in ['C200B40A82', '04005AC33890', '880086C3E88112', 'CE00C43D881120', 'D8005AC2A8F0', 'F600BC2D8F', '9C005AC2F8F0', '9C0141080250320F1802104A08']:
        t = Reader(test).decode()
        print(test, get_val(t[0]))

    for t in tokens:
       print(get_val(t))