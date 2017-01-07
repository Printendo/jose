#!/usr/bin/env python3

import discord
import asyncio
import sys

from chatterbot import ChatBot
chatbot = ChatBot(
    "José",
    storage_adapter='chatterbot.storage.JsonFileStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.BestMatch'
    ],
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)

chatbot.train("chatterbot.corpus.portuguese.conversations")

sys.path.append("..")
import jauxiliar as jaux
import josecommon as jcommon
import joseerror as je

from random import SystemRandom
random = SystemRandom()

ARTIF_CHATINESS = .1

class JoseArtif(jaux.Auxiliar):
    def __init__(self, cl):
        jaux.Auxiliar.__init__(self, cl)
        self.jose_mention = "<@%s>" % jcommon.JOSE_ID

    async def ext_load(self):
        return True, ''

    async def ext_unload(self):
        return True, ''

    async def e_on_message(self, message):
        # give up on anything related, use chatterbot
        self.current = message
        msg = message.content.replace(self.jose_mention, "")
        answer = chatbot.get_response(msg)

        if random.random() < ARTIF_CHATINESS:
            await self.say(answer)
        elif self.jose_mention in message.content:
            await self.say(answer)

    async def c_command(self, message, args):
        pass
