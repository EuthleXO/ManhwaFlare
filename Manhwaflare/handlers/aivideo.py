# © ManhwaFlare — @flexyy | dragonByte | @dragonByte_Network
# Do not remove credits
"""AI videos list + download."""
from __future__ import annotations
import asyncio
import logging
import os
import tempfile

import aiohttp
from telegram import InputFile
from telegram.ext import ContextTypes

from Manhwaflare.nav import nav_enter
from Manhwaflare.scrapers import aivideos as aivideos_mod
from Manhwaflare.text import sc
from Manhwaflare.ui.keyboards import btn, back_kb
from Manhwaflare.ui.wait import panel_edit

log = logging.getLogger("mf.aivideo")

async def _show_ai_videos(q, context, page: int = 1) -> None:
    """List AI videos with pagination inline buttons."""
    import aiohttp
    nav_enter(context, "aivideos")
    page = max(1, int(page or 1))
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
            data = await aivideos_mod.list_videos(session, page)
    except Exception as e:
        await panel_edit(q, f"<b>{sc('error')}</b>\n<code>{e}</code>", back_kb())
        return
    items = data.get("items") or []
    last = int(data.get("last_page") or 1)
    total = int(data.get("total") or len(items))
    context.user_data["ai_videos"] = items
    context.user_data["ai_page"] = page
    lines = [
        f"<blockquote><b>{sc('AI videos')}</b></blockquote>",
        f"<b>{sc('page')}:</b> {page}/{last} · <b>{sc('total')}:</b> {total}",
        "",
        sc("tap a video to download"),
    ]
    rows = []
    for i, v in enumerate(items[:24]):
        title = (v.get("title") or v.get("slug") or "?")[:40]
        rows.append([btn(sc(f"{title}")[:58], f"p:aiv:{i}", "primary")])
    nav = []
    if page > 1:
        nav.append(btn(sc("« prev"), f"p:aivp:{page-1}", "primary"))
    if page < last:
        nav.append(btn(sc("next »"), f"p:aivp:{page+1}", "primary"))
    if nav:
        rows.append(nav)
    await panel_edit(q, "\n".join(lines), back_kb(*rows))


async def _download_ai_video(q, context, slug: str, item: dict) -> None:
    """Fetch HLS and send video to user (ffmpeg → mp4 when possible)."""
    import os
    import tempfile
    import aiohttp
    from telegram import InputFile

    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=40)) as session:
            detail = await aivideos_mod.get_video(session, slug)
    except Exception as e:
        await panel_edit(q, f"<b>{sc('error')}</b>\n<code>{e}</code>", back_kb(
            [btn(sc("AI videos"), "p:aivideos", "primary")]
        ))
        return
    if not detail:
        await panel_edit(q, sc("video not found"), back_kb([btn(sc("AI videos"), "p:aivideos", "primary")]))
        return
    hls = detail.get("hls_url") or ""
    title = detail.get("title") or item.get("title") or slug
    manga = detail.get("manga_title") or ""
    eps = detail.get("episodes") or []

    if eps and len(eps) > 1 and not context.user_data.get("_aiv_force"):
        lines = [
            f"<blockquote><b>{manga or title}</b></blockquote>",
            f"<b>{sc('episodes')}:</b> {len(eps)}",
            sc("select episode to download"),
        ]
        rows = []
        for ep in eps[:20]:
            if not isinstance(ep, dict):
                continue
            es = str(ep.get("slug") or "")
            et = str(ep.get("title") or es)[:40]
            rows.append([btn(sc(et), f"p:aivep:{es}", "primary")])
        if hls:
            rows.insert(0, [btn(sc(f"download · {title[:30]}"), f"p:aivep:{slug}", "success")])
        await panel_edit(q, "\n".join(lines), back_kb(*rows, [btn(sc("AI videos"), "p:aivideos", "primary")]))
        return

    if not hls:
        await panel_edit(
            q,
            f"<b>{title}</b>\n{sc('no stream url')}\n<a href='{detail.get('page_url','')}'>open on site</a>",
            back_kb([btn(sc("AI videos"), "p:aivideos", "primary")]),
        )
        return

    await panel_edit(
        q,
        f"<b>› › {sc('downloading')}...</b>\n<code>{title[:60]}</code>",
        back_kb(),
    )
    tmpdir = tempfile.mkdtemp(prefix="aiv_")
    out_path = os.path.join(tmpdir, f"{slug[:40]}.mp4")
    ok = False
    try:
        # Prefer stream copy; fall back to re-encode if needed
        for args in (
            ["ffmpeg", "-y", "-protocol_whitelist", "file,http,https,tcp,tls,crypto",
             "-i", hls, "-c", "copy", "-bsf:a", "aac_adtstoasc", "-t", "900", out_path],
            ["ffmpeg", "-y", "-i", hls, "-c:v", "libx264", "-c:a", "aac",
             "-preset", "veryfast", "-t", "600", out_path],
        ):
            try:
                if os.path.isfile(out_path):
                    os.remove(out_path)
            except Exception:
                pass
            try:
                proc = await asyncio.create_subprocess_exec(
                    *args,
                    stdout=asyncio.subprocess.DEVNULL,
                    stderr=asyncio.subprocess.DEVNULL,
                )
                try:
                    await asyncio.wait_for(proc.wait(), timeout=240)
                except asyncio.TimeoutError:
                    proc.kill()
                    await proc.wait()
                if proc.returncode == 0 and os.path.isfile(out_path) and os.path.getsize(out_path) > 50_000:
                    ok = True
                    break
            except FileNotFoundError:
                log.warning("ffmpeg not installed")
                ok = False
                break
            except Exception as e:
                log.warning("ffmpeg aiv: %s", e)
                ok = False
    except Exception as e:
        log.warning("ffmpeg outer: %s", e)
        ok = False

    cap = (
        f"<blockquote><b>{manga}</b></blockquote>\n"
        f"<b>{title}</b>\n"
        f"<a href='{detail.get('page_url','')}'>source</a>"
    )[:1024]

    try:
        if ok:
            size = os.path.getsize(out_path)
            if size < 48 * 1024 * 1024:
                with open(out_path, "rb") as f:
                    await context.bot.send_video(
                        chat_id=q.message.chat_id,
                        video=InputFile(f, filename=f"{slug[:30]}.mp4"),
                        caption=cap,
                        parse_mode="HTML",
                        supports_streaming=True,
                    )
                await panel_edit(
                    q,
                    f"<blockquote><b>{sc('sent')}</b></blockquote>\n<b>{title}</b>",
                    back_kb([btn(sc("AI videos"), "p:aivideos", "primary")]),
                )
            else:
                await context.bot.send_message(
                    q.message.chat_id,
                    f"<b>{title}</b>\n{sc('file too large for telegram')}\n"
                    f"<a href='{hls}'>stream link (m3u8)</a>",
                    parse_mode="HTML",
                    disable_web_page_preview=True,
                )
                await panel_edit(q, f"<b>{title}</b>\n{sc('link sent')}", back_kb([btn(sc("AI videos"), "p:aivideos", "primary")]))
        else:
            await context.bot.send_message(
                q.message.chat_id,
                f"<blockquote><b>{manga or 'AI Video'}</b></blockquote>\n"
                f"<b>{title}</b>\n\n"
                f"<a href='{hls}'>▶ HLS stream</a>\n"
                f"<a href='{detail.get('page_url','')}'>open on manhwa18</a>",
                parse_mode="HTML",
                disable_web_page_preview=True,
            )
            await panel_edit(
                q,
                f"<blockquote><b>{sc('stream link sent')}</b></blockquote>\n"
                f"<i>{sc('install ffmpeg on server for direct mp4')}</i>",
                back_kb([btn(sc("AI videos"), "p:aivideos", "primary")]),
            )
    except Exception as e:
        log.exception("send aiv")
        await panel_edit(q, f"<b>{sc('error')}</b>\n<code>{e}</code>", back_kb([btn(sc("AI videos"), "p:aivideos", "primary")]))
    finally:
        try:
            if os.path.isfile(out_path):
                os.remove(out_path)
            os.rmdir(tmpdir)
        except Exception:
            pass


