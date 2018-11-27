from Gmail.gmail import get_email
from Calendar.cal import add
from parseschedule import parse

def main():
    email = get_email()
    times = parse(email)
    add(times)

if __name__ == '__main__':
    main()