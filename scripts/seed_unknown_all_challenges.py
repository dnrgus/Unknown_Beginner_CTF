import tempfile
import zipfile
from pathlib import Path

from CTFd import create_app
from CTFd.cache import clear_challenges, clear_standings
from CTFd.models import ChallengeFiles, Challenges, Flags, Hints, Tags, db
from CTFd.utils.uploads import upload_file
from werkzeug.datastructures import FileStorage


CHALLENGES = [
    {
        "name": "동아리 홈페이지",
        "old_names": ["WEB-01 Source Hunter"],
        "category": "Web",
        "value": 100,
        "difficulty": "Easy",
        "connection_info": "http://localhost:8101",
        "flag": "UNKNOWN{view_source_is_a_superpower}",
        "description": "우리 동아리 홈페이지를 만들었다! 아직 개발 중이라 조금 허술하지만... 설마 이상한 건 없겠지?\n\n**접속:** http://localhost:8101",
        "hints": ["화면에 보이는 내용이 전부는 아닐 수 있습니다.", "브라우저의 페이지 소스 보기나 DevTools에서 HTML 주석을 확인해보세요."],
    },
    {
        "name": "나는 관리자다",
        "old_names": ["WEB-02 Cookie Monster"],
        "category": "Web",
        "value": 100,
        "difficulty": "Easy",
        "connection_info": "http://localhost:8102",
        "flag": "UNKNOWN{cookies_are_client_side}",
        "description": "관리자 페이지까지 완성했다. 일반 회원은 절대로 못 들어온다. 분명히...?\n\n**접속:** http://localhost:8102",
        "hints": ["사이트가 브라우저에 저장한 값을 확인해보세요.", "role 쿠키 값을 admin으로 바꿔보세요."],
    },
    {
        "name": "로그인 좀 해줘",
        "old_names": ["WEB-03 Baby SQL"],
        "category": "Web",
        "value": 150,
        "difficulty": "Easy+",
        "connection_info": "http://localhost:8103",
        "flag": "UNKNOWN{baby_sqli_login_bypass}",
        "description": "선배가 로그인 기능을 만들어줬다. 보안도 완벽하다는데 비밀번호를 까먹었다...\n\n**접속:** http://localhost:8103",
        "hints": ["입력한 값이 SQL 조건문에 직접 들어가는지 생각해보세요.", "WHERE 조건이 항상 참이 되도록 기본 SQL Injection payload를 넣어보세요."],
    },
    {
        "name": "비밀번호를 까먹었다",
        "old_names": ["PWN-01 Password Please"],
        "category": "Pwn",
        "value": 100,
        "difficulty": "Easy",
        "connection_info": "nc localhost 8201",
        "flag": "UNKNOWN{strings_find_plaintext}",
        "description": "중요한 프로그램에 비밀번호를 걸어놨는데 내가 비밀번호를 까먹었다. 프로그램 안에 흔적이 남아있을지도?\n\n**접속:** `nc localhost 8201`",
        "hints": ["프로그램 안에 사람이 읽을 수 있는 문자열이 남아 있을 수 있습니다.", "strings 명령으로 바이너리의 printable string을 확인해보세요."],
    },
    {
        "name": "넘치면 안 돼!",
        "old_names": ["PWN-02 Overflow Me"],
        "category": "Pwn",
        "value": 100,
        "difficulty": "Easy",
        "connection_info": "nc localhost 8202",
        "flag": "UNKNOWN{overflow_changes_control_data}",
        "description": "입력칸을 넉넉하게 만들 필요가 있나? 이름 몇 글자 받는 건데 16글자면 충분하지!\n\n**접속:** `nc localhost 8202`",
        "hints": ["입력 길이가 버퍼 크기보다 길 때 옆 값이 바뀔 수 있습니다.", "32바이트 뒤에 little-endian `0x41424344`를 넣어보세요."],
    },
    {
        "name": "절대 실행되지 않는 함수",
        "old_names": ["PWN-03 Return to Win"],
        "category": "Pwn",
        "value": 150,
        "difficulty": "Easy+",
        "connection_info": "nc localhost 8203",
        "flag": "UNKNOWN{return_address_goes_to_win}",
        "description": "이 함수는 아무 데서도 호출하지 않으니까 삭제 안 해도 되겠지? 어차피 실행할 방법도 없잖아.\n\n**접속:** `nc localhost 8203`",
        "hints": ["정상 흐름에서는 호출되지 않는 함수가 바이너리에 남아 있습니다.", "nm/objdump로 win 함수를 찾고 저장된 return address를 덮어보세요."],
    },
    {
        "name": "비밀번호 어디 갔지?",
        "old_names": ["REV-01 Find the Password"],
        "category": "Reversing",
        "value": 100,
        "difficulty": "Easy",
        "connection_info": "",
        "flag": "UNKNOWN{strings_before_running}",
        "description": "비밀번호 검사 프로그램은 있는데 비밀번호를 적어둔 메모를 잃어버렸다. 프로그램은 알고 있지 않을까?",
        "hints": ["복잡한 도구를 열기 전에 문자열부터 관찰해보세요.", "strings에서 비밀번호처럼 보이는 값을 찾아 실행해보세요."],
    },
    {
        "name": "정답 검사기",
        "old_names": ["REV-02 Simple Check"],
        "category": "Reversing",
        "value": 100,
        "difficulty": "Easy",
        "connection_info": "",
        "flag": "UNKNOWN{decompile_the_checks}",
        "description": "친구가 정답을 맞혀야 Flag를 주는 프로그램을 만들었다. 정답을 몰라도 프로그램이 어떻게 검사하는지는 볼 수 있지 않을까?",
        "hints": ["입력값을 검사하는 함수를 찾아보세요.", "각 위치에서 비교하는 문자를 순서대로 적어보세요."],
    },
    {
        "name": "암호화했으니 안전해",
        "old_names": ["REV-03 XOR Password"],
        "category": "Reversing",
        "value": 150,
        "difficulty": "Easy+",
        "connection_info": "",
        "flag": "UNKNOWN{xor_arrays_are_reversible}",
        "description": "비밀번호를 그대로 저장하면 위험하다고 해서 XOR이라는 엄청난 암호화를 했다. 이제 안전하겠지?",
        "hints": ["바이트 배열이 하나의 고정 연산으로 변환되어 있습니다.", "encoded bytes를 `0x5a`와 XOR해보세요."],
    },
    {
        "name": "카이사르의 비밀편지",
        "old_names": ["CRYPTO-01 Caesar Salad"],
        "category": "Crypto",
        "value": 100,
        "difficulty": "Easy",
        "connection_info": "",
        "flag": "UNKNOWN{caesar_is_a_shift}",
        "description": "로마 시대에서 비밀 편지가 도착했다. 카이사르가 직접 암호화했다는데... 생각보다 오래된 방식인 것 같다.",
        "hints": ["알파벳이 일정한 칸만큼 밀려 있습니다.", "문제 파일의 note는 rotated by 13이라고 말합니다."],
    },
    {
        "name": "몇 번을 숨긴 거야?",
        "old_names": ["CRYPTO-02 Base Adventure"],
        "category": "Crypto",
        "value": 100,
        "difficulty": "Easy",
        "connection_info": "",
        "flag": "UNKNOWN{encoding_is_not_encryption}",
        "description": "친구가 Flag를 절대 못 찾게 여러 번 인코딩했다고 자랑한다. 그런데 인코딩이 암호화랑 같은 건가?",
        "hints": ["이건 key가 필요한 암호화가 아니라 표현 방식 변환입니다.", "Base64 -> Hex -> Base64 순서로 풀어보세요."],
    },
    {
        "name": "XOR이면 암호지!",
        "old_names": ["CRYPTO-03 Reused XOR"],
        "category": "Crypto",
        "value": 150,
        "difficulty": "Easy+",
        "connection_info": "",
        "flag": "UNKNOWN{single_byte_xor_is_small}",
        "description": "0부터 255 중 하나를 골라 Flag를 XOR했다. 경우의 수가 무려 256개다. 이 정도면 안전하지 않을까?",
        "hints": ["key 후보가 1바이트라면 전체 경우의 수가 매우 작습니다.", "0부터 255까지 시도하고 `UNKNOWN{`로 시작하는 결과를 찾으세요."],
    },
    {
        "name": "닉네임은 하나면 충분해",
        "old_names": ["OSINT-01 Hidden Username"],
        "category": "OSINT",
        "value": 100,
        "difficulty": "Easy",
        "connection_info": "",
        "flag": "UNKNOWN{username_pivot_found}",
        "description": "친구가 인터넷에서는 절대 자기 흔적을 찾을 수 없다고 한다. 그런데 모든 사이트에서 닉네임이 똑같은 것 같은데...",
        "hints": ["프로필에는 보이는 정보 말고도 식별자가 숨어 있을 수 있습니다.", "HTML 소스에서 username을 찾고 archive에서 같은 이름의 파일을 열어보세요."],
    },
    {
        "name": "여기가 어디게?",
        "old_names": ["OSINT-02 Where Is This?"],
        "category": "OSINT",
        "value": 100,
        "difficulty": "Easy",
        "connection_info": "",
        "flag": "UNKNOWN{blue_harbor_station}",
        "description": "동아리원이 여행 사진 한 장을 보내면서 어디인지 맞혀보라고 한다. 사진 속에 생각보다 많은 정보가 있다.",
        "hints": ["사진 속 간판과 지명처럼 눈에 보이는 단서를 먼저 읽어보세요.", "`UNKNOWN Tower` 단서를 mini map index에서 찾아보세요."],
    },
    {
        "name": "지웠으니까 괜찮겠지?",
        "old_names": ["OSINT-03 Developer Mistake"],
        "category": "OSINT",
        "value": 150,
        "difficulty": "Easy+",
        "connection_info": "",
        "flag": "UNKNOWN{git_history_never_forgets}",
        "description": "동아리 사이트를 만들다가 중요한 정보를 실수로 GitHub에 올렸다. 바로 삭제하고 다시 커밋했으니 이제 아무도 못 보겠지?",
        "hints": ["현재 파일만 보지 말고 과거 기록을 확인해보세요.", "`git log --all --patch`로 삭제된 내용까지 확인해보세요."],
    },
    {
        "name": "분명 파일이 있었는데",
        "old_names": ["MISC-01 Hidden File"],
        "category": "Misc",
        "value": 100,
        "difficulty": "Easy",
        "connection_info": "",
        "flag": "UNKNOWN{dotfiles_can_hide_clues}",
        "description": "선배가 Flag를 폴더 안에 넣었다는데 아무리 찾아도 안 보인다. 진짜 없는 걸까?",
        "hints": ["압축을 푼 뒤 기본 목록에 안 보이는 파일이 있을 수 있습니다.", "`ls -la`로 숨김 파일을 확인하고 `.flag.txt`를 열어보세요."],
    },
    {
        "name": "나는 TXT입니다",
        "old_names": ["MISC-02 Magic Bytes"],
        "category": "Misc",
        "value": 100,
        "difficulty": "Easy",
        "connection_info": "",
        "flag": "UNKNOWN{magic_bytes_reveal_png}",
        "description": "누가 봐도 평범한 텍스트 파일이다. 확장자가 `.txt`인데 설마 다른 파일일 리가...",
        "hints": ["확장자만으로 파일 형식을 믿으면 안 됩니다.", "file 명령이나 파일 첫 바이트를 확인해 PNG signature인지 보세요."],
    },
    {
        "name": "사진에는 사진만 있다",
        "old_names": ["MISC-03 Metadata"],
        "category": "Misc",
        "value": 150,
        "difficulty": "Easy+",
        "connection_info": "",
        "flag": "UNKNOWN{metadata_keeps_secrets}",
        "description": "그냥 평범한 사진 한 장이다. 사진에 Flag도 안 보이고 수상한 것도 없다. 정말 사진만 들어 있을까?",
        "hints": ["이미지에 보이는 픽셀 말고도 파일 안에 정보가 있을 수 있습니다.", "exiftool이나 metadata viewer로 PNG metadata를 확인해보세요."],
    },
]


ROOT = Path(__file__).resolve().parents[1]

CHALLENGE_FILES = {
    "비밀번호를 까먹었다": ("challenges/pwn/password-please/challenge", "pwn-password-please.zip"),
    "넘치면 안 돼!": ("challenges/pwn/overflow-me/challenge", "pwn-overflow-me.zip"),
    "절대 실행되지 않는 함수": ("challenges/pwn/return-to-win/challenge", "pwn-return-to-win.zip"),
    "비밀번호 어디 갔지?": ("challenges/reversing/find-the-password/challenge", "rev-find-the-password.zip"),
    "정답 검사기": ("challenges/reversing/simple-check/challenge", "rev-simple-check.zip"),
    "암호화했으니 안전해": ("challenges/reversing/xor-password/challenge", "rev-xor-password.zip"),
    "카이사르의 비밀편지": ("challenges/crypto/caesar-salad/challenge", "crypto-caesar-salad.zip"),
    "몇 번을 숨긴 거야?": ("challenges/crypto/base-adventure/challenge", "crypto-base-adventure.zip"),
    "XOR이면 암호지!": ("challenges/crypto/reused-xor/challenge", "crypto-reused-xor.zip"),
    "닉네임은 하나면 충분해": ("challenges/osint/hidden-username/challenge", "osint-hidden-username.zip"),
    "여기가 어디게?": ("challenges/osint/where-is-this/challenge", "osint-where-is-this.zip"),
    "지웠으니까 괜찮겠지?": ("challenges/osint/developer-mistake/challenge/developer-mistake-repo.zip", "osint-developer-mistake.zip"),
    "분명 파일이 있었는데": ("challenges/misc/hidden-file/challenge", "misc-hidden-file.zip"),
    "나는 TXT입니다": ("challenges/misc/magic-bytes/challenge", "misc-magic-bytes.zip"),
    "사진에는 사진만 있다": ("challenges/misc/metadata/challenge", "misc-metadata.zip"),
}


def delete_existing(name):
    while True:
        challenge = Challenges.query.filter_by(name=name).first()
        if not challenge:
            return
        Flags.query.filter_by(challenge_id=challenge.id).delete()
        Hints.query.filter_by(challenge_id=challenge.id).delete()
        Tags.query.filter_by(challenge_id=challenge.id).delete()
        db.session.delete(challenge)
        db.session.commit()


def zip_challenge_dir(source_dir, zip_path):
    source = ROOT / source_dir
    if not source.exists():
        raise FileNotFoundError(source)
    if source.is_file():
        zip_path.write_bytes(source.read_bytes())
        return
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(source.rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(source).as_posix())


def attach_challenge_file(challenge, source_dir, filename):
    ChallengeFiles.query.filter_by(challenge_id=challenge.id).delete()
    db.session.commit()

    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = Path(tmpdir) / filename
        zip_challenge_dir(source_dir, zip_path)
        with zip_path.open("rb") as fp:
            storage = FileStorage(stream=fp, filename=filename)
            uploaded = upload_file(
                file=storage,
                type="challenge",
                challenge_id=challenge.id,
                location=f"unknown-{challenge.id}/{filename}",
            )
        print(f"[FILE] {challenge.name} -> {uploaded.location}")


def seed():
    for item in CHALLENGES:
        delete_existing(item["name"])
        for old_name in item.get("old_names", []):
            delete_existing(old_name)
        challenge = Challenges(
            name=item["name"],
            description=item["description"],
            connection_info=item["connection_info"],
            value=item["value"],
            category=item["category"],
            type="standard",
            state="visible",
        )
        db.session.add(challenge)
        db.session.commit()

        db.session.add(Flags(challenge_id=challenge.id, content=item["flag"], type="static"))
        db.session.add(Tags(challenge_id=challenge.id, value=item["difficulty"].lower()))
        db.session.add(Tags(challenge_id=challenge.id, value=item["category"].lower()))
        for idx, hint in enumerate(item["hints"], start=1):
            db.session.add(
                Hints(
                    challenge_id=challenge.id,
                    title=f"Hint {idx}",
                    content=hint,
                    cost=0,
                    type="standard",
                )
            )
        db.session.commit()

        file_info = CHALLENGE_FILES.get(item["name"])
        if file_info:
            attach_challenge_file(challenge, *file_info)
        print(f"[SEEDED] {item['name']}")

    clear_challenges()
    clear_standings()
    print(f"[DONE] {len(CHALLENGES)} challenges seeded")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed()
