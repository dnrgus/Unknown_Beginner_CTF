from CTFd import create_app
from CTFd.models import Challenges, Flags, Solves, Users, db
from CTFd.utils import get_config
from CTFd.utils.crypto import hash_password
from CTFd.utils.security.csrf import generate_nonce


VERIFY_USER = "unknown-theme-check"
VERIFY_EMAIL = "unknown-theme-check@example.com"


def ensure_user():
    user = Users.query.filter_by(name=VERIFY_USER).first()
    if user:
        return user

    user = Users(
        name=VERIFY_USER,
        email=VERIFY_EMAIL,
        password=hash_password("password"),
        type="user",
        verified=True,
        hidden=True,
    )
    db.session.add(user)
    db.session.commit()
    return user


def main():
    app = create_app()

    with app.app_context():
        assert get_config("ctf_theme") == "unknown", "ctf_theme is not unknown"

        challenge = Challenges.query.order_by(Challenges.value.asc(), Challenges.id.asc()).first()
        assert challenge is not None, "no challenges found"

        flag = Flags.query.filter_by(challenge_id=challenge.id).first()
        assert flag is not None, f"no flag found for challenge {challenge.id}"

        user = ensure_user()
        nonce = generate_nonce()

        with app.test_client() as client:
            with client.session_transaction() as session:
                session["id"] = user.id
                session["name"] = user.name
                session["type"] = user.type
                session["nonce"] = nonce

            response = client.post(
                "/api/v1/challenges/attempt",
                json={"challenge_id": challenge.id, "submission": flag.content},
                headers={"CSRF-Token": nonce},
            )
            payload = response.get_json()

        status = payload["data"]["status"]
        assert response.status_code == 200, payload
        assert status in {"correct", "already_solved"}, payload

        solved = Solves.query.filter_by(
            challenge_id=challenge.id,
            user_id=user.id,
        ).first()
        assert solved is not None, "solve row was not created"

        print(
            f"theme=unknown, challenge_api_submit={status}, "
            f"challenge_id={challenge.id}, user={user.name}"
        )


if __name__ == "__main__":
    main()
