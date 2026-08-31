# © ManhwaFlare — @flexyy | dragonByte | @dragonByte_Network
"""Plugin: referral codes."""
from __future__ import annotations
from telegram import Update
from telegram.ext import ContextTypes
from Manhwaflare import db
from Manhwaflare.text import sc, mono
from Manhwaflare.ui.keyboards import back_kb
from Manhwaflare.ui.wait import panel_edit
from Manhwaflare.plugins import register_command, register_panel


async def cmd_ref(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    code = await db.get_or_create_referral(user.id)
    if context.args:
        res = await db.apply_referral(user.id, context.args[0])
        msg = {
            "ok": sc("referral applied +3 bonus"),
            "invalid": sc("invalid code"),
            "self": sc("cannot use own code"),
            "already": sc("already referred"),
        }.get(res, res)
        await update.message.reply_text(msg)
        return
    await update.message.reply_text(
        f"<b>{sc('your referral code')}</b>\n<code>{code}</code>\n\n"
        f"{sc('share with friends')}\n"
        f"{sc('both get +3 chapters')}\n"
        f"{sc('redeem')}: {mono('/ref CODE')}",
        parse_mode="HTML",
    )


async def panel_ref(q, context, user, is_owner, is_admin) -> None:
    code = await db.get_or_create_referral(user.id)
    await panel_edit(
        q,
        f"<b>{sc('referral')}</b>\n<code>{code}</code>\n\n"
        f"{sc('friends use')}: /ref {code}\n"
        f"{sc('both get +3 chapters')}",
        back_kb(),
    )


register_command("ref", cmd_ref, "Referral code")
register_panel("ref", panel_ref)
