

def load_input(filemane):
    with open(filemane, 'r') as f:
        data = f.read().strip()
    return data


def find_first_marker(txt, n):
    nm1 = n-1
    for i in range(nm1, len(txt)):
        subtxt = txt[i-nm1:i+1]
        if len(set(subtxt)) == n:
            return i+1, subtxt
    return None, ''


if __name__ == '__main__':

    for data in [
            'mjqjpqmgbljsphdztnvjfqwrcgsmlb',
            'bvwbjplbgvbhsrlpgdmjqwftvncz',
            'nppdvjthqldpwncqszvftbrmjlhg',
            'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg',
            'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw']:
        print(data, find_first_marker(data, 4), find_first_marker(data, 14))

    data = load_input('input')
    print('part1', find_first_marker(data, 4))
    print('part2', find_first_marker(data, 14))