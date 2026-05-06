"""Read cookie metadata from browser SQLite databases (Chrome, macOS/Linux/Windows)."""

import platform
import shutil
import sqlite3
import tempfile
from pathlib import Path

from .models import RawCookie

_CHROME_EPOCH_OFFSET = 11644473600  # seconds between 1601-01-01 and 1970-01-01
_SAMESITE_MAP = {-1: None, 0: "none", 1: "lax", 2: "strict"}


def _chrome_profiles_dir() -> Path | None:
    system = platform.system()
    home = Path.home()
    if system == "Darwin":
        return home / "Library" / "Application Support" / "Google" / "Chrome"
    elif system == "Linux":
        return home / ".config" / "google-chrome"
    elif system == "Windows":
        local = Path.home() / "AppData" / "Local"
        return local / "Google" / "Chrome" / "User Data"
    return None


def _find_chrome_cookie_dbs() -> list[tuple[str, Path]]:
    chrome_dir = _chrome_profiles_dir()
    if not chrome_dir or not chrome_dir.exists():
        return []

    results: list[tuple[str, Path]] = []
    default = chrome_dir / "Default" / "Cookies"
    if default.exists():
        results.append(("Default", default))

    for profile_dir in sorted(chrome_dir.iterdir()):
        if profile_dir.name.startswith("Profile ") and profile_dir.is_dir():
            db = profile_dir / "Cookies"
            if db.exists():
                results.append((profile_dir.name, db))

    return results


def _read_cookie_db(db_path: Path) -> list[RawCookie]:
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp_path = Path(tmp.name)
    tmp.close()

    try:
        shutil.copy2(db_path, tmp_path)
        wal = db_path.parent / (db_path.name + "-wal")
        shm = db_path.parent / (db_path.name + "-shm")
        if wal.exists():
            shutil.copy2(wal, tmp_path.parent / (tmp_path.name + "-wal"))
        if shm.exists():
            shutil.copy2(shm, tmp_path.parent / (tmp_path.name + "-shm"))

        conn = sqlite3.connect(f"file:{tmp_path}?mode=ro", uri=True)
        cur = conn.cursor()

        cur.execute("""
            SELECT host_key, name, path, expires_utc,
                   is_secure, is_httponly, samesite,
                   creation_utc, last_access_utc, top_frame_site_key,
                   is_persistent
            FROM cookies
        """)

        cookies: list[RawCookie] = []
        for row in cur.fetchall():
            (host, name, path, expires_chrome, secure, httponly, samesite,
             creation_utc, last_access_utc, top_frame_site_key,
             is_persistent) = row

            if expires_chrome and expires_chrome > 0:
                expires_unix = str(int(expires_chrome / 1_000_000 - _CHROME_EPOCH_OFFSET))
            else:
                expires_unix = None

            created_at = None
            if creation_utc and creation_utc > 0:
                created_at = str(int(creation_utc / 1_000_000 - _CHROME_EPOCH_OFFSET))

            last_accessed = None
            if last_access_utc and last_access_utc > 0:
                last_accessed = str(int(last_access_utc / 1_000_000 - _CHROME_EPOCH_OFFSET))

            cookies.append(RawCookie(
                name=name,
                value="",
                domain=host,
                path=path,
                expires=expires_unix,
                secure=bool(secure),
                http_only=bool(httponly),
                same_site=_SAMESITE_MAP.get(samesite),
                created_at=created_at,
                last_accessed=last_accessed,
                top_frame_site=top_frame_site_key or None,
                is_persistent=bool(is_persistent),
            ))

        conn.close()
        return cookies

    finally:
        tmp_path.unlink(missing_ok=True)
        (tmp_path.parent / (tmp_path.name + "-wal")).unlink(missing_ok=True)
        (tmp_path.parent / (tmp_path.name + "-shm")).unlink(missing_ok=True)


class BrowserProfile:
    def __init__(self, browser: str, profile_name: str, db_path: Path, cookie_count: int):
        self.browser = browser
        self.profile_name = profile_name
        self.db_path = db_path
        self.cookie_count = cookie_count


def discover_profiles() -> list[BrowserProfile]:
    profiles: list[BrowserProfile] = []

    for profile_name, db_path in _find_chrome_cookie_dbs():
        try:
            count = _count_cookies(db_path)
            profiles.append(BrowserProfile("chrome", profile_name, db_path, count))
        except Exception:
            pass  # Skip unreadable profiles

    return profiles


def _count_cookies(db_path: Path) -> int:
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp_path = Path(tmp.name)
    tmp.close()
    try:
        shutil.copy2(db_path, tmp_path)
        wal = db_path.parent / (db_path.name + "-wal")
        if wal.exists():
            shutil.copy2(wal, tmp_path.parent / (tmp_path.name + "-wal"))
        conn = sqlite3.connect(f"file:{tmp_path}?mode=ro", uri=True)
        count = conn.execute("SELECT COUNT(*) FROM cookies").fetchone()[0]
        conn.close()
        return count
    finally:
        tmp_path.unlink(missing_ok=True)
        (tmp_path.parent / (tmp_path.name + "-wal")).unlink(missing_ok=True)


def scan_browser(browser: str = "chrome", profile: str = "all") -> list[RawCookie]:
    if browser != "chrome":
        raise ValueError(f"Unsupported browser: {browser}. Currently supported: chrome")

    dbs = _find_chrome_cookie_dbs()
    if not dbs:
        raise FileNotFoundError("No Chrome cookie databases found on this machine")

    all_cookies: list[RawCookie] = []
    for prof_name, db_path in dbs:
        if profile != "all" and prof_name != profile:
            continue
        all_cookies.extend(_read_cookie_db(db_path))

    return all_cookies
