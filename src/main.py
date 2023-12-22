import sys
import sqlite3


def main() -> int:
    """Echo the input arguments to standard output"""
    phrase = ','.join(sys.argv)
    print(phrase)
    return 0


if __name__ == '__main__':
    sys.exit(main())
