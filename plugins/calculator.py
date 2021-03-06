# Copyright 2018 Twixes

# This file is part of Somsiad - the Polish Discord bot.

# Somsiad is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# Somsiad is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with Somsiad.
# If not, see <https://www.gnu.org/licenses/>.

from py_expression_eval import Parser
import discord
from somsiad import somsiad


parser = Parser()


@somsiad.bot.command(aliases=['oblicz', 'policz'])
@discord.ext.commands.cooldown(
    1, somsiad.conf['command_cooldown_per_user_in_seconds'], discord.ext.commands.BucketType.user
)
async def calculate(ctx, *, data):
    """Calculates the provided expressions and sends the results.
    If calculation is not possible with available data, simplifies the expression.
    """
    input_data = data.replace('\\', '').strip(';').split(';')
    expression = input_data[0].strip()
    variables_list = input_data[1:]
    variables_dict = {}
    for variable in variables_list:
        key_value_pair = variable.split('=')
        try:
            variables_dict[key_value_pair[0].strip()] = float(key_value_pair[1].strip())
        except (IndexError, ValueError):
            embed = discord.Embed(
                title=':warning: Podano nieprawidłowe zmienne!',
                color=somsiad.color
            )
            return await ctx.send(ctx.author.mention, embed=embed)

    try:
        parsed_expression = parser.parse(expression)
    except Exception:
        embed = discord.Embed(
            title=':warning: Podano nieprawidłowe wyrażenie!',
            color=somsiad.color
        )
    else:
        input_info = (
            [expression] +
            [f'{variable[0]} = {variable[1]}' for variable in variables_dict.items()]
        )
        input_info_string = '\n'.join(input_info)
        try:
            result = parsed_expression.evaluate(variables_dict)
        except Exception:
            try:
                result = parsed_expression.simplify(variables_dict).toString()
            except Exception:
                embed = discord.Embed(
                    title=':warning: Podano nieprawidłowe wyrażenie lub zmienne!',
                    color=somsiad.color
                )
            else:
                embed = discord.Embed(
                    title=':1234: Uproszczono wyrażenie',
                    color=somsiad.color
                )
                embed.add_field(name='Wejście', value=input_info_string.replace('*', '\*'), inline=False)
                embed.add_field(name='Wyjście', value=result.replace('*', '\*'), inline=False)
        else:
            embed = discord.Embed(
                title=':1234: Obliczono wartość wyrażenia',
                color=somsiad.color
            )
            embed.add_field(name='Wejście', value=input_info_string.replace('*', '\*'), inline=False)
            embed.add_field(name='Wyjście', value=result, inline=False)

    return await ctx.send(ctx.author.mention, embed=embed)

@calculate.error
async def calculate_error(ctx, error):
    if isinstance(error, discord.ext.commands.MissingRequiredArgument):
        embed = discord.Embed(
            title=':warning: Nie podano wyrażenia do obliczenia!',
            color=somsiad.color
        )
        await ctx.send(ctx.author.mention, embed=embed)
