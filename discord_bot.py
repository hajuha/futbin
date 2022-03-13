from email import message
import discord
from main import SoccerGuru
from discord.ext import commands
from config import getToken
from datetime import datetime
import re
import math

PRICE_PATTERN = r'([``])(?:(?=(\\?))\2.)*?\1'

bot = commands.Bot(command_prefix='$', help_command=None)


@bot.command()
async def help(ctx):
    message = "**Search FUT Card database:**\n---```\n$rn [nation] [rating] [amount]\n```\nGet [*amount*] of [*nation*] cards which rating below or equal to [*rating*]\nNation: eng, ger, fra, spa, bra, ita,...\n---```\n$rl [league] [rating] [amount]\n```\nGet [*amount*] of [*league*] cards which rating below or equal to [*rating*]\nLeague: eng1, fra1, Ger1, ITA1,...\n---```\n$rr [rating] [amount]\n```\nGet [*amount*] cards which rating below or equal to [*rating*]\n"
    await ctx.send(message)
# @bot.command()
# async def ovr(ctx, rating=100, league="", number=10):
#     # await ctx.send("Updating...")
#     a = SoccerGuru()
#     league = league.upper()
#     player_dict = a.unload_pickle()
#     player_dict = a.filter(player_dict, rating, league, "")
#     overall_list = list(player_dict.keys())
#     overall_list.sort()
#     overall_list = reversed(overall_list)
#     memberlist = []
#     for i in range(number):
#         try:
#             overall = next(overall_list)
#             for j in range(0, len(player_dict[overall])):
#                 player = player_dict[overall][j]
#                 memberlist.append(
#                     f"{str(overall)} {player[2]} {player[0]} {player[1]} {player[4]}")
#         except Exception as e:
#             print(e)
#             break
#     if len(memberlist) == 0:

#         await ctx.send("No player found ! DM <@!333070457278562306> for more info")
#     else:
#         memberlist = [f"```Top {league} {rating} cards:"] + memberlist
#         await ctx.send("\n".join(memberlist)+"```")


@bot.command()
async def rl(ctx, league="", rating=99, number=10):
    # await ctx.send("Updating...")
    a = SoccerGuru()
    league = league.upper()
    player_dict = a.unload_pickle()
    player_dict = a.filter(player_dict, rating, league, "")
    overall_list = list(player_dict.keys())
    overall_list.sort()
    overall_list = reversed(overall_list)
    memberlist = []
    count = 0
    while count < min(number, 25):
        try:
            overall = next(overall_list)
            for j in range(0, len(player_dict[overall])):
                player = player_dict[overall][j]
                memberlist.append(
                    f"{str(overall)} {player[0]} {player[1]} {player[4]}")
                count += 1
        except Exception as e:
            print(e)
            break
    if len(memberlist) == 0:
        await ctx.send("No player found ! DM <@!333070457278562306> for more info")
    else:
        memberlist = [
            f"```\nTop {number} {league} {rating} cards: \n"] + memberlist
        await ctx.send("\n".join(memberlist)+"```")


@bot.command()
async def rr(ctx, rating=99, number=10):
    # await ctx.send("Updating...")
    a = SoccerGuru()
    player_dict = a.unload_pickle()
    player_dict = a.filter(player_dict, rating, "", "")
    overall_list = list(player_dict.keys())
    overall_list.sort()
    overall_list = reversed(overall_list)
    memberlist = []
    count = 0
    while count < min(number, 25):
        try:
            overall = next(overall_list)
            for j in range(0, len(player_dict[overall])):
                player = player_dict[overall][j]

                memberlist.append(
                    f"{str(overall)} {player[2]} {player[0]} {player[1]} {player[4]}")
                count += 1
        except Exception as e:
            print(e)
            break
    if len(memberlist) == 0:

        await ctx.send("No player found ! DM <@!333070457278562306> for more info")
    else:
        memberlist = [f"```Top {number} {rating} cards: "] + memberlist
        await ctx.send("\n".join(memberlist)+"```")


@bot.command()
async def rn(ctx, nation="ENG", rating=99, number=10):
    # await ctx.send("Updating...")
    nation = nation.upper()
    nations = {'ENG': "14",
               'FRA': "18",
               "GER": "21",
               "SPA": "45",
               'NED': '34',
               'POR': '38',
               'ITA': '27',
               'ARG': '52',
               'BRA': '54',
               'BEL': '7',
               'DEN': '13',
               'MEX': '83',
               'URU': '60',
               'CRO': '10',
               'RUS': '40',
               }
    nation_code = nations.get(nation, None)
    if nation_code is None:
        legit_nation = list(nations.keys())
        embed = discord.Embed()
        inner = '\n'.join(legit_nation)
        embed.add_field(
            name="You should enter the following nations:", value=inner, inline=False)

        await ctx.send(embed=embed)
    else:
        a = SoccerGuru()
        player_dict = a.unload_pickle()
        player_dict = a.filter(player_dict, rating, "", nation_code)
        overall_list = list(player_dict.keys())
        overall_list.sort()
        overall_list = reversed(overall_list)
        memberlist = []
        count = 0
        while count < min(number, 25):
            try:
                overall = next(overall_list)
                for j in range(0, len(player_dict[overall])):
                    player = player_dict[overall][j]
                    memberlist.append(
                        f"{str(overall)} {player[2]} {player[0]} {player[1]} {player[4]}")
                    count += 1
            except Exception as e:
                print(e)
                break
        if len(memberlist) == 0:

            await ctx.send("No player found ! DM <@!333070457278562306> for more info")
        else:
            memberlist = [
                f"```Top {number} {nation} {rating} cards: "] + memberlist
            await ctx.send("\n".join(memberlist)+"```")


@bot.command()
async def rnpage(ctx, nation="ENG", rating=99, number=10):
    # await ctx.send("Updating...")
    nation = nation.upper()
    nations = {'ENG': "14",
               'FRA': "18",
               "GER": "21",
               "SPA": "45",
               'NED': '34',
               'POR': '38',
               'ITA': '27',
               'ARG': '52',
               'BRA': '54',
               'BEL': '7',
               'DEL': '13',
               'MEX': '83',
               'URU': '60',
               'CRO': '10',
               'RUS': '40',
               }
    nation_code = nations.get(nation, None)
    if nation_code is None:
        legit_nation = list(nations.keys())
        embed = discord.Embed()
        inner = '\n'.join(legit_nation)
        embed.add_field(
            name="You should enter the following nations:", value=inner, inline=False)

        await ctx.send(embed=embed)
    else:
        a = SoccerGuru()
        player_dict = a.unload_pickle()
        player_dict = a.filter(player_dict, rating, "", nation_code)
        overall_list = list(player_dict.keys())
        overall_list.sort()
        overall_list = reversed(overall_list)
        memberlist = []
        count = 0
        while count < min(number, 25):
            try:
                overall = next(overall_list)
                for j in range(0, len(player_dict[overall])):
                    player = player_dict[overall][j]
                    memberlist.append(
                        f"{str(overall)} {player[2]} {player[0]} {player[1]} {player[4]}")
                    count += 1
            except Exception as e:
                print(e)
                break
        if len(memberlist) == 0:

            await ctx.send("No player found ! DM <@!333070457278562306> for more info")
        else:
            memberlist = [
                f"```Top {number} {nation} {rating} cards: "] + memberlist
            await ctx.send("\n".join(memberlist)+"```")


@bot.command()
async def pages(ctx):
    contents = ["This is page 1!", "This is page 2!",
                "This is page 3!", "This is page 4!"]
    pages = 4
    cur_page = 1
    message = await ctx.send(f"Page {cur_page}/{pages}:\n{contents[cur_page-1]}")
    # getting the message object for editing and reacting

    await message.add_reaction("◀️")
    await message.add_reaction("▶️")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
        # This makes sure nobody except the command sender can interact with the "menu"

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=60, check=check)
            # waiting for a reaction to be added - times out after x seconds, 60 in this
            # example

            if str(reaction.emoji) == "▶️" and cur_page != pages:
                cur_page += 1
                await message.edit(content=f"Page {cur_page}/{pages}:\n{contents[cur_page-1]}")
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == "◀️" and cur_page > 1:
                cur_page -= 1
                await message.edit(content=f"Page {cur_page}/{pages}:\n{contents[cur_page-1]}")
                await message.remove_reaction(reaction, user)

            else:
                await message.remove_reaction(reaction, user)
                # removes reactions if the user tries to go forward on the last page or
                # backwards on the first page
        except asyncio.TimeoutError:
            await message.delete()
            break
            # ending the loop if user doesn't react after x seconds
tom_id = "736909539668131881"
guru_bot_id = "668075833780469772"
price_alert = 300000

@bot.event
async def on_message(message):
    try:
        if str(message.guild.id) == tom_id:

            if ".claim" in message.content.lower():
                channel = message.channel

                def check(m):            
                    
                    if str(m.author.id) == guru_bot_id and m.channel == channel:
                        return True

                msg = await bot.wait_for('message', check=check)
                embed_msg = msg.embeds[0]
                m1 = re.search(PRICE_PATTERN, embed_msg.description)
                player = embed_msg.title.split()[0]
                
                if m1 and player != "Hãy":
                    price = int(m1.group().replace(",","").replace("`",""))
                    if price > price_alert:
                        await message.channel.send(f"`BIG CLAIM ALERT` <@&926665190974562354> <@!{message.author.id}> đã claim được `{player}` giá `{price}` lúc <t:{math.floor(datetime.timestamp(message.created_at))}:f>")
                    else:
                        await message.channel.send(f"<@!{message.author.id}> đã claim được `{player}` giá `{price}` lúc <t:{math.floor(datetime.timestamp(message.created_at))}:f>")
                else:
                    msg_2 = await bot.wait_for('message', check=check)
                    embed_msg_2 = msg_2.embeds[0]

                    m2 = re.search(PRICE_PATTERN, embed_msg_2.description)
                    player = embed_msg_2.title.split()[0]
                    
                    if m2 and player != "Hãy":
                        price = int(m2.group().replace(",","").replace("`",""))
                        if price > 300000:
                            await message.channel.send(f"`BIG CLAIM ALERT` <@&926665190974562354> <@!{message.author.id}> đã claim được `{player}` giá `{price}` lúc <t:{math.floor(datetime.timestamp(message.created_at))}:f>")
                        else:
                            await message.channel.send(f"<@!{message.author.id}> đã claim được `{player}` giá `{price}` lúc <t:{math.floor(datetime.timestamp(message.created_at))}:f>")
                
    except Exception as e:
        print(e)

    await bot.process_commands(message)
    
# @bot.command()
# async def roles(ctx):
#     print(", ".join([str(r.id)+str(r.name) for r in ctx.guild.roles]))

# @bot.event
# async def on_message(message):
#     if message.content.startswith('sclaim'):
#         channel = bot.get_channel(925681747755143220)
#         message = await channel.fetch_message(951172294737264661)
#         embed_msg = message.embeds[0]
#         pattern = r'([``])(?:(?=(\\?))\2.)*?\1'
#         m1 = re.search(pattern, embed_msg.description)
#         try:
#             if m1:
#                 price = int(m1.group().replace(",","").replace("`",""))
#                 player = embed_msg.title.split()[0]
#                 print(player, price)
#                 # await message.channel.send(f"CLAIM-ALERT <@!{message.author.id}> đã claim được `{player}` giá `{price}` lúc <t:{math.floor(datetime.timestamp(message.created_at))}:f>py")
#             else:
#                 await message.channel.send(embed =embed_msg)
#         except Exception as e:
#             print(e)
    # if message.content.startswith('"claim'):
        # channel = message.channel

        # def check(m):            
            
        #     if str(m.author.id) == "668075833780469772" and m.channel == channel:
        #         return True

        # msg = await bot.wait_for('message', check=check)
        # embed = msg.embeds[0];
        # await channel.send(embed=embed
        # )

token = getToken()
bot.run(token)