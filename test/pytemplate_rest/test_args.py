from pytemplate_rest.args import parse_args

def test_parse_args():
    args = parse_args(['--dev',])
    assert args.dev == True

