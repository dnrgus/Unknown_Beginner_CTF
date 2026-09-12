from CTFd import create_app

from seed_unknown_all_challenges import seed


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed()
