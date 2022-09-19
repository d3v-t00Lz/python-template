"""

"""

def arg_force(
    parser,
    _args=(
        '-f',
        '--force',
    ),
    action='store_true',
    default=False,
    dest='force',
    _help=(
        'Ignore warnings and perform the command.'
    ),
):
    parser.add_argument(
        *_args,
        action=action,
        default=default,
        dest=dest,
        help=_help,
    )

