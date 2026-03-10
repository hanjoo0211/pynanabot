from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_PROFILES_DIR = BASE_DIR / 'profiles'


def read_profile(sender: str, profiles_dir=DEFAULT_PROFILES_DIR) -> str:
    path = Path(profiles_dir) / f'{sender}.md'
    if not path.exists():
        return ''
    return path.read_text(encoding='utf-8')


def write_profile(sender: str, content: str, profiles_dir=DEFAULT_PROFILES_DIR) -> None:
    path = Path(profiles_dir) / f'{sender}.md'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')
