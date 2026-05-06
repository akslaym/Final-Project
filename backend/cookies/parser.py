"""Parse cookies from JSON and Netscape export formats."""

from .models import RawCookie


def parse_json_export(data: list[dict]) -> list[RawCookie]:
    cookies = []
    for entry in data:
        cookies.append(RawCookie(
            name=entry.get("name", ""),
            value=entry.get("value", ""),
            domain=entry.get("domain", entry.get("host", "")),
            path=entry.get("path", "/"),
            expires=str(entry.get("expirationDate", entry.get("expires", ""))) or None,
            secure=entry.get("secure", False),
            http_only=entry.get("httpOnly", entry.get("http_only", False)),
            same_site=entry.get("sameSite", entry.get("same_site", None)),
        ))
    return cookies


def parse_netscape_format(text: str) -> list[RawCookie]:
    cookies = []
    for line in text.strip().splitlines():
        if line.startswith("#") or not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) >= 7:
            cookies.append(RawCookie(
                domain=parts[0],
                path=parts[2],
                secure=parts[3].upper() == "TRUE",
                expires=parts[4] if parts[4] != "0" else None,
                name=parts[5],
                value=parts[6],
            ))
    return cookies
