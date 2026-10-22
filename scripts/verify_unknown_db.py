from CTFd import create_app
from CTFd.models import ChallengeFiles, Challenges, Flags, Hints
from scripts.seed_unknown_all_challenges import CHALLENGES


TARGET_NAMES = {item["name"] for item in CHALLENGES}


def main():
    app = create_app()
    with app.app_context():
        items = [
            challenge
            for challenge in Challenges.query.all()
            if challenge.name in TARGET_NAMES
        ]
        print("count", len(items))
        categories = {}
        for challenge in items:
            categories[challenge.category] = categories.get(challenge.category, 0) + 1
        print("categories", categories)
        for challenge in sorted(items, key=lambda item: item.name):
            flags = Flags.query.filter_by(challenge_id=challenge.id).count()
            hints = Hints.query.filter_by(challenge_id=challenge.id).count()
            files = ChallengeFiles.query.filter_by(challenge_id=challenge.id).count()
            print(
                f"{challenge.name} / {challenge.category} / flags={flags} / hints={hints} / files={files}"
            )


if __name__ == "__main__":
    main()
