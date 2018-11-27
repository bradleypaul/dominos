import re
import collections

def format_date(date_string):
    date = date_string.split('/')
    formatted_date = rotate_date(date)
    return '-'.join(formatted_date)

def rotate_date(date_array):
    d = collections.deque(date_array)
    d.rotate(1)
    return list(d)

def parse_time(time):
    return time.split(':')

def format_time(hour, minute, pm):
    seconds = '00'
    if pm == 'PM':
        hour = str(12 + int(hour))

    return f'{hour}:{minute}:{seconds}'

def parse_times(time_string):
    times = time_string.split(' ')
    start = format_time(*parse_time(times[0]), times[1])
    end = format_time(*parse_time(times[3]), times[4])
    return {
        'start': start,
        'end': end
    }
    
def parse(data):
    lines = data.splitlines()
    lines = filter(lambda x: re.compile('DeliveryExpert').search(x), lines)
    lines = [i.split(', ') for i in lines]
    
    time_dict = []

    for i in lines:
        date = format_date(i[1])
        times = parse_times(i[3])
        time_dict.append({
            'start': f"{date}T{times['start']}",
            'end': f"{date}T{times['end']}"
        })
    return time_dict

def main():
    with open('dominos.txt') as f:
        data = f.read()
    print(parse(data))
    

if __name__ == '__main__':
    main()