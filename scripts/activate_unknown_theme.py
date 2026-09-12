from CTFd import create_app
from CTFd.utils import get_config, set_config


def main():
    app = create_app()
    with app.app_context():
        before = get_config("ctf_theme")
        set_config("ctf_theme", "unknown")
        after = get_config("ctf_theme")
        print(f"ctf_theme: {before!r} -> {after!r}")


if __name__ == "__main__":
    main()
