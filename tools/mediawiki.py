from __future__ import annotations

import html
import json
import re
import time
import urllib.parse
import urllib.request
import urllib.error
from dataclasses import dataclass


API_URL = "https://isaac.huijiwiki.com/api.php"
WIKI_BASE_URL = "https://isaac.huijiwiki.com/wiki/"
# 伪装成纯净的最新版 Chrome 浏览器，不要带任何自定义后缀
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"


@dataclass
class SearchResult:
    title: str
    snippet: str
    pageid: int | None = None

    @property
    def url(self) -> str:
        return WIKI_BASE_URL + urllib.parse.quote(self.title.replace(" ", "_"))


@dataclass
class WikiPage:
    title: str
    extract: str
    url: str
    pageid: int | None = None


class WikiApiError(RuntimeError):
    """Raised when the wiki API cannot return useful content."""


def search_wiki(query: str, limit: int = 5) -> list[SearchResult]:
    """Search Isaac HuijiWiki through the MediaWiki API."""
    payload = _request_json(
        {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "srlimit": str(limit),
            "format": "json",
            "formatversion": "2",
        }
    )

    rows = payload.get("query", {}).get("search", [])
    return [
        SearchResult(
            title=row.get("title", ""),
            snippet=_clean_html(row.get("snippet", "")),
            pageid=row.get("pageid"),
        )
        for row in rows
        if row.get("title")
    ]


def get_wiki_page(title: str) -> WikiPage:
    """Fetch a plain-text extract for a page title."""
    payload = _request_json(
        {
            "action": "query",
            "prop": "extracts",
            "explaintext": "1",
            "exsectionformat": "plain",
            "redirects": "1",
            "titles": title,
            "format": "json",
            "formatversion": "2",
        }
    )

    pages = payload.get("query", {}).get("pages", [])
    if not pages:
        raise WikiApiError(f"No page returned for title: {title}")

    page = pages[0]
    if page.get("missing"):
        raise WikiApiError(f"Page does not exist: {title}")

    resolved_title = page.get("title", title)
    extract = _normalize_text(page.get("extract", ""))
    if not extract:
        raise WikiApiError(f"Page has no readable extract: {resolved_title}")

    return WikiPage(
        title=resolved_title,
        extract=extract,
        url=WIKI_BASE_URL + urllib.parse.quote(resolved_title.replace(" ", "_")),
        pageid=page.get("pageid"),
    )


def _request_json(params: dict[str, str]) -> dict:
    query = urllib.parse.urlencode(params)
    req = urllib.request.Request(
        f"{API_URL}?{query}",
        headers={
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": "https://isaac.huijiwiki.com/",
            "Origin": "https://isaac.huijiwiki.com",
            "User-Agent": USER_AGENT,
            # 下面这些 Sec- 开头的请求头是绕过现代防火墙的关键
            "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
        },
    )

    last_error: Exception | None = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                charset = resp.headers.get_content_charset() or "utf-8"
                return json.loads(resp.read().decode(charset, errors="replace"))
        except urllib.error.HTTPError as exc:
            if exc.code == 403:
                raise WikiApiError(
                    "Wiki API returned HTTP 403 Forbidden. The site may block scripted "
                    "requests or require browser verification."
                ) from exc
            last_error = exc
            if exc.code < 500:
                break
        except Exception as exc:  # noqa: BLE001 - keep CLI error friendly.
            last_error = exc
        if attempt < 2:
            time.sleep(0.8 * (attempt + 1))

    if isinstance(last_error, urllib.error.HTTPError):
        raise WikiApiError(
            f"Wiki API request failed: HTTP {last_error.code} {last_error.reason}"
        ) from last_error
    if last_error is not None:
        raise WikiApiError(f"Wiki API request failed: {last_error}") from last_error

    try:
        raise WikiApiError("Wiki API request failed for an unknown reason.")
    except Exception as exc:
        raise WikiApiError(f"Wiki API request failed: {exc}") from exc


def _clean_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    return html.unescape(_normalize_text(text))


def _normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
