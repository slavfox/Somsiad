# Copyright 2018 Twixes

# This file is part of Somsiad - the Polish Discord bot.

# Somsiad is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# Somsiad is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with Somsiad.
# If not, see <https://www.gnu.org/licenses/>.

from typing import List, Dict, Union, Optional
import discord
from somsiad import somsiad
from server_data import server_data_manager
from utilities import TextFormatter


class Oof:
    TABLE_NAME = 'oof'
    TABLE_COLUMNS = (
        'user_id INTEGER NOT NULL PRIMARY KEY',
        'oofs INTEGER NOT NULL DEFAULT 0'
    )

    @classmethod
    def get_oofs(cls, server: discord.Guild, user: Union[discord.User, discord.Member] = None) -> Optional[int]:
        """Returns the number of times the provided user oofed on the provided server.
        If not provided a user, returns the total number of oofs on the server.
        """
        server_data_manager.ensure_table_existence_for_server(server.id, cls.TABLE_NAME, cls.TABLE_COLUMNS)
        if user is None:
            server_data_manager.servers[server.id]['db_cursor'].execute(
                'SELECT oofs FROM oof',
            )
            result = server_data_manager.servers[server.id]['db_cursor'].fetchall()
            if result:
                oofs = 0
                for oofer in result:
                    oofs += oofer['oofs']
            else:
                oofs = None
        else:
            server_data_manager.servers[server.id]['db_cursor'].execute(
                'SELECT oofs FROM oof WHERE user_id = ?',
                (user.id,)
            )
            result = server_data_manager.servers[server.id]['db_cursor'].fetchone()
            oofs = None if result is None else result['oofs']
        return oofs

    @classmethod
    def get_oofers(cls, server: discord.Guild) -> List[Dict[str, int]]:
        """Returns a tuple of users who have oofed on the provided server, sorted by the number of oofs, descending."""
        server_data_manager.ensure_table_existence_for_server(server.id, cls.TABLE_NAME, cls.TABLE_COLUMNS)
        server_data_manager.servers[server.id]['db_cursor'].execute(
            'SELECT user_id, oofs FROM oof'
        )
        rows = (
            server_data_manager.dict_from_row(row)
            for row in server_data_manager.servers[server.id]['db_cursor'].fetchall()
        )
        sorted_rows = sorted(rows, key=lambda row: row['oofs'], reverse=True)
        return sorted_rows

    @classmethod
    def ensure_user_registration(cls, server: discord.Guild, user: Union[discord.User, discord.Member]):
        """Ensure that the provided user is a registered oofer on the provided server."""
        if cls.get_oofs(server, user) is None:
            server_data_manager.servers[server.id]['db_cursor'].execute(
                'INSERT INTO oof(user_id) VALUES(?)',
                (user.id,)
            )
            server_data_manager.servers[server.id]['db'].commit()

    @classmethod
    def increment(cls, server: discord.Guild, user: Union[discord.User, discord.Member]):
        """Increments the number of oofs by 1 for the provided user on the provided server."""
        cls.ensure_user_registration(server, user)
        server_data_manager.servers[server.id]['db_cursor'].execute(
            'UPDATE oof SET oofs = oofs + 1 WHERE user_id = ?',
            (user.id,)
        )
        server_data_manager.servers[server.id]['db'].commit()


@somsiad.bot.group(invoke_without_command=True, case_insensitive=True)
@discord.ext.commands.cooldown(
    1, somsiad.conf['command_cooldown_per_user_in_seconds'], discord.ext.commands.BucketType.user
)
@discord.ext.commands.guild_only()
async def oof(ctx):
    Oof.increment(ctx.guild, ctx.author)
    await ctx.send('Oof!')


@oof.group(aliases=['ile'], invoke_without_command=True, case_insensitive=True)
@discord.ext.commands.cooldown(
    1, somsiad.conf['command_cooldown_per_user_in_seconds'], discord.ext.commands.BucketType.user
)
@discord.ext.commands.guild_only()
async def oof_how_many(ctx, member: discord.Member = None):
    await ctx.invoke(oof_how_many_member, member)


@oof_how_many.command(aliases=['member', 'user', 'członek', 'użytkownik'])
@discord.ext.commands.cooldown(
    1, somsiad.conf['command_cooldown_per_user_in_seconds'], discord.ext.commands.BucketType.user
)
@discord.ext.commands.guild_only()
async def oof_how_many_member(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    oofs = Oof.get_oofs(ctx.guild, member)
    oofs = 0 if oofs is None else oofs

    if member == ctx.author:
        embed = discord.Embed(
            title='Masz na koncie '
            f'{TextFormatter.word_number_variant(oofs, "oofnięcie", "oofnięcia", "oofnięć")}',
            color=somsiad.color
        )
    else:
        embed = discord.Embed(
            title=f'{member.display_name} ma na koncie '
            f'{TextFormatter.word_number_variant(oofs, "oofnięcie", "oofnięcia", "oofnięć")}',
            color=somsiad.color
        )

    await ctx.send(ctx.author.mention, embed=embed)


@oof_how_many_member.error
async def oof_how_many_member_error(ctx, error):
    if isinstance(error, discord.ext.commands.BadArgument):
        embed = discord.Embed(
            title=':warning: Nie znaleziono na serwerze pasującego użytkownika!',
            color=somsiad.color
        )
        await ctx.send(ctx.author.mention, embed=embed)


@oof_how_many.command(aliases=['server', 'serwer'])
@discord.ext.commands.cooldown(
    1, somsiad.conf['command_cooldown_per_user_in_seconds'], discord.ext.commands.BucketType.user
)
@discord.ext.commands.guild_only()
async def oof_how_many_server(ctx):
    await ctx.invoke(oof_server)


@oof.command(aliases=['server', 'serwer'])
@discord.ext.commands.cooldown(
    1, somsiad.conf['command_cooldown_per_user_in_seconds'], discord.ext.commands.BucketType.user
)
@discord.ext.commands.guild_only()
async def oof_server(ctx):
    oofers = Oof.get_oofers(ctx.guild)
    total_oofs = Oof.get_oofs(ctx.guild)
    total_oofs = 0 if total_oofs is None else total_oofs

    top_oofers = []
    for oofer in enumerate(oofers[:5]):
        top_oofers.append(
            f'{oofer[0]+1}. <@{oofer[1]["user_id"]}> – '
            f'{TextFormatter.word_number_variant(oofer[1]["oofs"], "oofnięcie", "oofnięcia", "oofnięć")}'
        )
    top_oofers_string = '\n'.join(top_oofers)

    embed = discord.Embed(
        title=f'Do tej pory oofnięto na serwerze {TextFormatter.word_number_variant(total_oofs, "raz", "razy")}',
        color=somsiad.color
    )
    if top_oofers:
        embed.add_field(name='Najaktywniejsi ooferzy', value=top_oofers_string, inline=False)

    await ctx.send(ctx.author.mention, embed=embed)
