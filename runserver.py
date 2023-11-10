
#----------------------------------------------------------------------
# runserver.py
# Authors: Maria Aguirre, Johana Lara
#----------------------------------------------------------------------

import sys
import argparse
import reg

def main():

    parser = argparse.ArgumentParser(
        description='Server for the registrar applications',
        allow_abbrev=False
    )

    parser.add_argument('port',
        help='the port at which the server should listen')
    args = parser.parse_args()

    try:
        port = int(args.port)
    except Exception:
        print(
            'Invalid Port Number: Port must be an integer.',
              file=sys.stderr )
        sys.exit(2)


    try:
        reg.app.run(host = '0.0.0.0', port = port, debug = True)
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
