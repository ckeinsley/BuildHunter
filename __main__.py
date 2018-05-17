from cli_ import cli

def main():
    try: 
        cli.cli()
    except ConnectionError:
        print('Service Unavailable')

if __name__ == '__main__':
    main()