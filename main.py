import sys
import os
from runtime_app import RuntimeApp

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def main() -> None:
    RuntimeApp().run_cli()


if __name__ == "__main__":
    main()
