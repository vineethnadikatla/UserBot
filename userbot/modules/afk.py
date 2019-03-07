# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.b (the "License");
# you may not use this file except in compliance with the License.
#
import time

from telethon import events
from telethon.events import StopPropagation

from userbot import (AFKREASON, COUNT_MSG, ISAFK, LOGGER, LOGGER_GROUP, USERS)
from userbot.events import register


@register(incoming=True)
async def mention_afk(e):
    global COUNT_MSG
    global USERS
    global ISAFK
    if e.message.mentioned and not (await e.get_sender()).bot:
        if ISAFK:
            if e.sender_id not in USERS:
                await e.reply(
                    "Sorry! My boss is AFK due to ```"
                    + AFKREASON
                    + "```. Would ping him to look into the message soon😉"
                )
                USERS.update({e.sender_id: 1})
                COUNT_MSG = COUNT_MSG + 1
            elif e.sender_id in USERS:
                if USERS[e.sender_id] % 5 == 0:
                    await e.reply(
                        "Sorry! But my boss is still not here. "
                        "Try to ping him a little later. I am sorry😖."
                        "He told me he was busy with ```"
                        + AFKREASON
                        + "```"
                    )
                    USERS[e.sender_id] = USERS[e.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1
                else:
                    USERS[e.sender_id] = USERS[e.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1


@register(incoming=True)
async def afk_on_pm(e):
    global ISAFK
    global USERS
    global COUNT_MSG
    if e.is_private and not (await e.get_sender()).bot:
        if ISAFK:
            if e.sender_id not in USERS:
                await e.reply(
                    "Sorry! My boss is AFK due to ```"
                    + AFKREASON
                    + "``` I'll ping him to look into the message soon😉"
                )
                USERS.update({e.sender_id: 1})
                COUNT_MSG = COUNT_MSG + 1
            elif e.sender_id in USERS:
                if USERS[e.sender_id] % 5 == 0:
                    await e.reply(
                        "Sorry! But my boss is still not here. "
                        "Try to ping him a little later. I am sorry😖."
                        "He told me he was busy with ```"
                        + AFKREASON
                        + "```"
                    )
                    USERS[e.sender_id] = USERS[e.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1
                else:
                    USERS[e.sender_id] = USERS[e.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1


@register(outgoing=True, pattern="^.notafk$")
async def not_afk(e):
    if not e.text[0].isalpha():
        global ISAFK
        global COUNT_MSG
        global USERS
        global AFKREASON
        ISAFK = False
        await e.edit("I'm no longer AFK.")
        x=await e.respond(
            "`You recieved "
            + str(COUNT_MSG)
            + " messages while you were away. Check log for more details.`"
            + "`This auto-generated message shall be self destructed in 2 seconds.`"
        )
        time.sleep(2)
        await x.delete()
        if LOGGER:
            await e.client.send_message(
                LOGGER_GROUP,
                "You've recieved "
                + str(COUNT_MSG)
                + " messages from "
                + str(len(USERS))
                + " chats while you were away",
            )
            for i in USERS:
                name = await e.client.get_entity(i)
                name0 = str(name.first_name)
                await e.client.send_message(
                    LOGGER_GROUP,
                    "["
                    + name0
                    + "](tg://user?id="
                    + str(i)
                    + ")"
                    + " sent you "
                    + "`"
                    + str(USERS[i])
                    + " messages`",
                )
        COUNT_MSG = 0
        USERS = {}
        AFKREASON = "No Reason"


@register(outgoing=True, pattern="^.afk")
async def set_afk(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        message = e.text
        try:
            string = str(message[5:])
        except:
            string=''
        global ISAFK
        global AFKREASON
        await e.edit("AFK AF!")
        if string != "":
            AFKREASON = string
        if LOGGER:
            await e.client.send_message(LOGGER_GROUP, "You went AFK!")
        ISAFK = True
        raise StopPropagation


@register(outgoing=True)
async def type_afk_is_not_true(e):
    global ISAFK
    global COUNT_MSG
    global USERS
    global AFKREASON
    if ISAFK:
        ISAFK = False
        await e.respond("I'm no longer AFK.")
        x = await e.respond(
            "`You recieved "
            + str(COUNT_MSG)
            + " messages while you were away. Check log for more details.`"
            + "`This auto-generated message shall be self destructed in 2 seconds.`"
        )
        time.sleep(2)
        await x.delete()
        if LOGGER:
            await e.client.send_message(
                LOGGER_GROUP,
                "You've recieved "
                + str(COUNT_MSG)
                + " messages from "
                + str(len(USERS))
                + " chats while you were away",
            )
            for i in USERS:
                name = await e.client.get_entity(i)
                name0 = str(name.first_name)
                await e.client.send_message(
                    LOGGER_GROUP,
                    "["
                    + name0
                    + "](tg://user?id="
                    + str(i)
                    + ")"
                    + " sent you "
                    + "`"
                    + str(USERS[i])
                    + " messages`",
                )
        COUNT_MSG = 0
        USERS = {}
        AFKREASON = "No Reason"
