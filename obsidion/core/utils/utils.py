import discord
from typing import List, Iterable

from .chat_formatting import box
from .predicates import MessagePredicate
import asyncio
import contextlib


async def send_interactive(
    ctx, messages: Iterable[str], box_lang: str = None, timeout: int = 15
) -> List[discord.Message]:
    """Send multiple messages interactively.

    The user will be prompted for whether or not they would like to view
    the next message, one at a time. They will also be notified of how
    many messages are remaining on each prompt.

    Parameters
    ----------
    messages : `iterable` of `str`
        The messages to send.
    box_lang : str
        If specified, each message will be contained within a codeblock of
        this language.
    timeout : int
        How long the user has to respond to the prompt before it times out.
        After timing out, the bot deletes its prompt message.

    """
    messages = tuple(messages)
    ret = []

    for idx, page in enumerate(messages, 1):
        if box_lang is None:
            msg = await ctx.send(page)
        else:
            msg = await ctx.send(box(page, lang=box_lang))
        ret.append(msg)
        n_remaining = len(messages) - idx
        if n_remaining > 0:
            if n_remaining == 1:
                plural = ""
                is_are = "is"
            else:
                plural = "s"
                is_are = "are"
            query = await self.send(
                "There {} still {} message{} remaining. "
                "Type `more` to continue."
                "".format(is_are, n_remaining, plural)
            )
            try:
                resp = await ctx.bot.wait_for(
                    "message",
                    check=MessagePredicate.lower_equal_to("more", ctx),
                    timeout=timeout,
                )
            except asyncio.TimeoutError:
                with contextlib.suppress(discord.HTTPException):
                    await query.delete()
                break
            else:
                try:
                    await ctx.channel.delete_messages((query, resp))
                except (discord.HTTPException, AttributeError):
                    # In case the bot can't delete other users' messages,
                    # or is not a bot account
                    # or channel is a DM
                    with contextlib.suppress(discord.HTTPException):
                        await query.delete()
    return ret
