# Copyright 2018 ondondil & Twixes

# This file is part of Somsiad - the Polish Discord bot.

# Somsiad is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# Somsiad is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with Somsiad.
# If not, see <https://www.gnu.org/licenses/>.

import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
from somsiad_helper import *

@client.command(aliases=['pomocy', 'pomoc'])
@commands.cooldown(1, conf['cooldown'], commands.BucketType.user)
async def help(ctx):
    em = discord.Embed(title='Lecę na ratunek!' , colour=0x269d9c)
    em.add_field(name='Dobry!', value='Somsiad jestem. Pomagam w różnych kwestiach, wystarczy mnie zawołać.'
        ' Odpowiadam na wszystkie zawołania z poniższej listy. Pamiętaj tylko zawsze, by zacząć od "' + conf['prefix'] +
        '". W nawiasach podane są alternatywne nazwy zawołań - tak dla różnorodności.')
    em.add_field(name=conf['prefix'] + '8ball (8-ball, eightball, 8) <pytanie>',
        value='Zadaje <pytanie> magicznej kuli.', inline=False)
    em.add_field(name=conf['prefix'] + 'flip', value='Wywraca stół.', inline=False)
    em.add_field(name=conf['prefix'] + 'fix (unflip)', value='Odwraca wywrócony stół.', inline=False)
    em.add_field(name=conf['prefix'] + 'gugiel (g) <zapytanie>',
        value='Wysyła <zapytanie> do wyszukiwarki Google i zwraca najlepiej pasujący wynik.', inline=False)
    em.add_field(name=conf['prefix'] + 'img (i) <zapytanie>',
        value='Wysyła <zapytanie> do wyszukiwarki Qwant i zwraca najlepiej pasujący do niego obrazek.', inline=False)
    em.add_field(name=conf['prefix'] + 'isitup (isup) <url>',
        value='Za pomocą serwisu isitup.org wykrywa status danej strony.', inline=False)
    em.add_field(name=conf['prefix'] + 'pomocy (pomoc, help)', value='Wysyła użytkownikowi tę wiadomość.', inline=False)
    em.add_field(name=conf['prefix'] + 'lenny (lennyface)', value='Wstawia lenny face\'a - ( ͡° ͜ʖ ͡°).', inline=False)
    em.add_field(name=conf['prefix'] + 'ping', value='pong', inline=False)
    em.add_field(name=conf['prefix'] + 'r <nazwa>', value='Zwraca pełny URL subreddita <nazwa>.', inline=False)
    em.add_field(name=conf['prefix'] + 'shrug', value='¯\_(ツ)_/¯', inline=False)
    em.add_field(name=conf['prefix'] + 'wikipedia (w) <termin>',
        value='Sprawdza znaczenie <terminu> w polskiej wersji Wikipedii.', inline=False)
    em.add_field(name=conf['prefix'] + 'wikipediaen (wen) <termin>',
        value='Sprawdza znaczenie <terminu> w anglojęzycznej wersji Wikipedii.', inline=False)
    em.add_field(name=conf['prefix'] + 'urban (u) <słowo>', value='Sprawdza znaczenie <słowa> w Urban Dictionary.',
        inline=False)
    em.add_field(name=conf['prefix'] + 'youtube (yt, tuba) <zapytanie>',
        value='Wysyła <zapytanie> do YouTube i zwraca najlepiej pasujący wynik.', inline=False)
    await ctx.author.send(embed=em)
