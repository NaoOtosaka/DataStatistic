from api.lib.project import setup as project_setup
from api.lib.tester import setup as tester_setup
from api.lib.developer import setup as developer_setup


def main():
    project_setup()
    tester_setup()
    developer_setup()


if __name__ == '__main__':
    main()