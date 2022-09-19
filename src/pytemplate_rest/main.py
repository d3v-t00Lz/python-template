from .app import APP
from .args import parse_args

def main():
    args = parse_args()
    APP.run(**args.__dict__)

