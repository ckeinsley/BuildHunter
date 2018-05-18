from cli_ import cli
from redis.exceptions import ConnectionError

def main():
    try: 
        cli.cli()
    except ConnectionError:
        print('Service Unavailable')

if __name__ == '__main__':
    main()