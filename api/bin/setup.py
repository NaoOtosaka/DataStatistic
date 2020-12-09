from api.lib.project import setup as project_setup
from api.lib.tester import setup as tester_setup


def main():
    project_setup()
    tester_setup()


if __name__ == '__main__':
    main()