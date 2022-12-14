import argparse

def arg_parser():
    # host='0.0.0.0', port=1337, access_log=False
    parser = argparse.ArgumentParser('pytemplate REST server')
    parser.add_argument(
        '--host',
        dest='host',
        default='0.0.0.0',
        help='IP address or hostname to listen on (default: 0.0.0.0)',
    )
    parser.add_argument(
        '--port',
        dest='port',
        type=int,
        default=8080,
        help='The port to listen on (default: 8080)',
    )
    parser.add_argument(
        '--dev',
        dest='dev',
        action='store_true',
        default=False,
        help='Run server in dev mode (slower)',
    )
    parser.add_argument(
        '--debug',
        dest='debug',
        action='store_true',
        default=False,
        help='Run server with debug logging output (slower)',
    )
    parser.add_argument(
        '--access-log',
        dest='access_log',
        action='store_true',
        default=False,
        help='Log accesses to the server',
    )
    return parser

def parse_args(args=None):
    parser = arg_parser()
    return parser.parse_args(args)

