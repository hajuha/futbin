from email import message
import discord
from main import SoccerGuru
from discord.ext import commands
from config import getToken

bot = commands.Bot(command_prefix='$')


@bot.command()
async def ovr(ctx, rating=100, league="", number=10):
    # await ctx.send("Updating...")
    a = SoccerGuru()
    league = league.upper()
    player_dict = a.unload_pickle()
    player_dict = a.filter(player_dict, rating, league, "")
    overall_list = list(player_dict.keys())
    overall_list.sort()
    overall_list = reversed(overall_list)
    memberlist = []
    for i in range(number):
        try:
            overall = next(overall_list)
            for j in range(0, len(player_dict[overall])):
                player = player_dict[overall][j]
                memberlist.append(
                    f"{str(overall)} {player[2]} {player[0]} {player[1]} {player[4]}")
        except Exception as e:
            print(e)
            break
    if len(memberlist) == 0:

        await ctx.send("No player found ! DM <@!333070457278562306> for more info")
    else:
        memberlist = [f"```Top {league} {rating} cards:"] + memberlist
        await ctx.send("\n".join(memberlist)+"```")


@bot.command()
async def rl(ctx, league="", number=10):
    # await ctx.send("Updating...")
    a = SoccerGuru()
    league = league.upper()
    player_dict = a.unload_pickle()
    player_dict = a.filter(player_dict, 100, league, "")
    overall_list = list(player_dict.keys())
    overall_list.sort()
    overall_list = reversed(overall_list)
    memberlist = []
    for i in range(number):
        try:
            overall = next(overall_list)
            for j in range(0, len(player_dict[overall])):
                player = player_dict[overall][j]
                memberlist.append(
                    f"{str(overall)} {player[0]} {player[1]} {player[4]}")
        except Exception as e:
            print(e)
            break
    if len(memberlist) == 0:
        await ctx.send("No player found ! DM <@!333070457278562306> for more info")
    else:
        memberlist = [f"```\nTop {league} cards: \n"] + memberlist
        await ctx.send("\n".join(memberlist)+"```")


@bot.command()
async def rr(ctx, rating=100, number=10):
    # await ctx.send("Updating...")
    a = SoccerGuru()
    player_dict = a.unload_pickle()
    player_dict = a.filter(player_dict, rating, "", "")
    overall_list = list(player_dict.keys())
    overall_list.sort()
    overall_list = reversed(overall_list)
    memberlist = []
    for i in range(number):
        try:
            overall = next(overall_list)
            for j in range(0, len(player_dict[overall])):
                player = player_dict[overall][j]
                print(player)
                memberlist.append(
                    f"{str(overall)} {player[2]} {player[0]} {player[1]} {player[4]}")
        except Exception as e:
            print(e)
            break
    if len(memberlist) == 0:

        await ctx.send("No player found ! DM <@!333070457278562306> for more info")
    else:
        memberlist = [f"```Top {rating} cards: "] + memberlist
        await ctx.send("\n".join(memberlist)+"```")


@bot.command()
async def rn(ctx, nation="ENG", number=10):
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
               'BEL': '7'}
    nation_code = nations.get(nation)
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
        player_dict = a.filter(player_dict, 100, "", nation_code)
        overall_list = list(player_dict.keys())
        overall_list.sort()
        overall_list = reversed(overall_list)
        memberlist = []
        for i in range(number):
            try:
                overall = next(overall_list)
                for j in range(0, len(player_dict[overall])):
                    player = player_dict[overall][j]
                    memberlist.append(
                        f"{str(overall)} {player[2]} {player[0]} {player[1]} {player[4]}")
            except Exception as e:
                print(e)
                break
        if len(memberlist) == 0:

            await ctx.send("No player found ! DM <@!333070457278562306> for more info")
        else:
            memberlist = [f"```Top {nation} cards: "] + memberlist
            await ctx.send("\n".join(memberlist)+"```")

token = getToken()
bot.run(token)
