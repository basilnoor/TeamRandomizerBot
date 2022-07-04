# -----------------------------------------------------------------------------------------------
# Name: Basil Noor
#       This file contains code for the TeamRandomizer Bot on discord.
#       Using hikari api for the discord bot implementation w/ lightbulb framework for commands.
# -----------------------------------------------------------------------------------------------

import os
import string
from dotenv import load_dotenv
from trlogic import *

import hikari       # discord api wrapper
import lightbulb    # command framework for hikari
import aiosqlite

# Initializing dotenv and bot w/discord token
load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = lightbulb.BotApp(
    token = TOKEN,
)

# Connecting bot to SQLite and creating a database
@bot.listen(hikari.StartedEvent)
async def on_start(event):
    print("TeamRandomizerBot by Basyl has started!")
    # connect to sqlite db on bot start up
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            # creating table to store data in db
            await cursor.execute("CREATE TABLE IF NOT EXISTS users (name STRING, rank STRING)")
            await cursor.execute("CREATE TABLE IF NOT EXISTS maps (name STRING)")
        await db.commit()

# /tr
# TeamRandomizer group command to help organize subcommands for tr bot
@bot.command
@lightbulb.command("tr", "TeamRandomizer")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def tr(ctx):
    pass

# /tr help
# Help subcommand lists all /tr bot commands with information on how to use them
@tr.child
@lightbulb.command("help", "View a list of commands for TRBot")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def help(ctx):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            help_embed = hikari.Embed(
                title = "List of Commands", 
                description = """**Player commands:**
```/tr players - Lists all the players in the database```
```/tr add_player - Allows you to add a player w/ a given rank```
> ***Player names must be unique***
> *If you don't play ranked just use an educated guess on where you'd be placed. Be honest!*
> 
> All ranks except 'pro' have 3 levels. Use **lowercase**. Eg. d1, d2, d3 (d1 < d2 < d3)
> Add rank 'pro' for anyone with a rank **higher** than d3.
> Add rank 'b1' for anyone with a rank **lower** than bronze eg. iron.
> Therefore, to add a rank of silver 3, input **s3**.
> 
> **Acceptable ranks:**
> *bronze(b), silver(s), gold(g), platinum(p), diamond(d) or pro*

```/tr remove_player - Removes a player from the database based on their name```
```/tr edit_player - Allows you to edit a players rank```
```/tr start - Use this command to generate two randomized teams based on a weighted elo system```
> *Add a space after every player, but all players are added as a single string under **'names'**.*
> *Make sure to add every players name **exactly** as it is in the database.*
> *If the power level difference between the teams is **> 4**, consider generating teams again.*
> 
> *Example input: 'john jeff jeoff jim gym'*

**Map commands:**
```/tr maps - Lists all the maps in the database```
```/tr add_map - Allows you to add a map into the database```
```/tr remove_map - Allows you to remove a map from the database```
```/tr pick_map - Picks a random map from the database```
                """,
                color = hikari.Color.from_hex_code("#088F8F")
            )
            help_embed.set_footer("TeamRandomizerBot by Basyl")
            await ctx.respond(help_embed)
        await db.commit()

# /tr add_player
# Add_player subcommand adds a player with a given rank to the 'users' SQLite database
@tr.child
@lightbulb.option("rank", "Enter players rank", type = string)
@lightbulb.option("name", "Enter player name", type = string)
@lightbulb.command("add_player", "Add a player to the database")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def add_player(ctx):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT name FROM users WHERE name = ?", (ctx.options.name,))
            data = await cursor.fetchone()
            rank = ctx.options.rank
            name = ctx.options.name
            if data or rank not in accepted_ranks or len(name) > 25:
                add_embed_fail = hikari.Embed(
                    title = "Failed to Add Player", 
                    description = f"""!ERROR! Player: **{ctx.options.name}** already exists or rank: **{ctx.options.rank}** is not valid
> refer to '/tr help' for player name and rank rules.
                    """,
                    color = hikari.Color.from_hex_code("#C70039")
                )
                await ctx.respond(add_embed_fail)
            else:
                await cursor.execute("INSERT INTO users (name, rank) VALUES (?, ?)", (ctx.options.name, ctx.options.rank,))
                add_embed_success = hikari.Embed(
                    title = "Player Successfully Added", 
                    description = f"Player: **{ctx.options.name}** has been added (rank: **{ctx.options.rank}**)",
                    color = hikari.Color.from_hex_code("#32CD32")
                )
                await ctx.respond(add_embed_success)
        await db.commit()

# /tr remove_player
# Remove_player subcommand removes a given player from the 'users' database
@tr.child
@lightbulb.option("name", "Enter player name", type = string)
@lightbulb.command("remove_player", "Remove a player from the database")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def remove_player(ctx):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT name FROM users WHERE name = ?", (ctx.options.name,))
            data = await cursor.fetchone()
            if data:
                await cursor.execute("DELETE FROM users WHERE name = ?", (ctx.options.name,))
                remove_embed_success = hikari.Embed(
                    title = "Player Successfully Removed", 
                    description = f"Player: **{ctx.options.name}** has been deleted",
                    color = hikari.Color.from_hex_code("#32CD32")
                )
                await ctx.respond(remove_embed_success)
            else:
                remove_embed_fail = hikari.Embed(
                    title = "Failed to Remove Player", 
                    description = f"""!ERROR! Player: **{ctx.options.name}** does not exist
> refer to '/tr help' for player name and rank rules.
                    """,
                    color = hikari.Color.from_hex_code("#C70039")
                )
                await ctx.respond(remove_embed_fail)
        await db.commit()

# /tr edit_player
# Edit_player subcommand updates a given players rank in the database
@tr.child
@lightbulb.option("rank", "Enter players rank", type = string)
@lightbulb.option("name", "Enter player name", type = string)
@lightbulb.command("edit_player", "Ppdate a players rank")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def edit_player(ctx):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT name FROM users WHERE name = ?", (ctx.options.name,))
            data = await cursor.fetchone()
            rank = ctx.options.rank
            if data and rank in accepted_ranks:
                await cursor.execute("UPDATE users SET rank = ? WHERE name = ?", (ctx.options.rank, ctx.options.name,))
                edit_embed_success = hikari.Embed(
                    title = "Player Successfully Edited", 
                    description = f"Player: **{ctx.options.name}** has a new rank: **{ctx.options.rank}**",
                    color = hikari.Color.from_hex_code("#32CD32")
                )
                await ctx.respond(edit_embed_success)                
            else:
                edit_embed_fail = hikari.Embed(
                    title = "Failed to Edit Player", 
                    description = f"""!ERROR! Player: **{ctx.options.name}** does not exist or rank: **{ctx.options.rank}** is not valid
> refer to '/tr help' for player name and rank rules.
                    """,
                    color = hikari.Color.from_hex_code("#C70039")
                )
                await ctx.respond(edit_embed_fail)
        await db.commit()

# /tr players
# Players subcommand lists all the players in the database w/ their ranks
@tr.child
@lightbulb.command("players", "View all the players in the database")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def players(ctx):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT * FROM users")
            data = await cursor.fetchall()
            # formatting output in trlogic.py
            players_string = list_players(data)
            players_embed = hikari.Embed(
                title = "List of Players", 
                description = players_string,
                color = hikari.Color.from_hex_code("#E37383")
            )
            await ctx.respond(players_embed)    
        await db.commit()

# /tr start
# Start subcommand generates two random teams w/ weighted system
@tr.child
@lightbulb.option("names", "Enter player names", type = string)
@lightbulb.command("start", "Team Randomzier")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def pick_map(ctx):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT * FROM users")
            data = await cursor.fetchall()
            # error_embed
            error_embed = hikari.Embed(
                    title = "Failed to Generate Teams", 
                    description = f"""!ERROR! Make sure player names were inputted correctly and you enter atleast 2 names
> refer to '/tr help' for TRBot rules.
                    """,
                    color = hikari.Color.from_hex_code("#C70039")
            )
            # Check if all names are in database
            players_playing = []
            players_string = list_players(data)
            player_names = ctx.options.names
            list_of_players = player_names.split()
            # returns error_embed if not enough players
            if len(list_of_players) < 2:
                await ctx.respond(error_embed)
                return
            # returns error_embed if any name is not in database
            for player in list_of_players:
                if player not in players_string:
                    await ctx.respond(error_embed)
                    return
                # if name exists add the player_profile to the list of players_playing
                else:
                    await cursor.execute("SELECT rank FROM users WHERE name = ?", (player,))
                    player_rank = await cursor.fetchone()
                    rank_value = find_rank(player_rank[0])
                    player_profile = (player, rank_value)
                    players_playing.append(player_profile)
            # randomize teams
            # Returns (team 1, team 2, team 1 power, team 2 power)
            balanced_teams = randomize(players_playing)
            
            # Formatting output for teams using the tuple returned from randomize()
            team_1 = balanced_teams[0]
            team_2 = balanced_teams[1]
            team_1_pwr = balanced_teams[2]
            team_2_pwr = balanced_teams[3]

            display_string = ">>> "
            display_string += f"**Team 1** *(power level: {team_1_pwr})*\n"
            display_string += "```\n"
            for index in range(0, len(team_1)):
                if index == (len(team_1)-1):
                    display_string += f"{team_1[index]}"  
                    break
                display_string += f"{team_1[index]} \n"
            display_string += " ```"
            display_string += "-------------------------------\n"
            display_string += f"**Team 2** *(power level: {team_2_pwr})*\n"
            display_string += "```\n"
            for index in range(0, len(team_2)):
                if index == (len(team_2)-1):
                    display_string += f"{team_2[index]}"  
                    break
                display_string += f"{team_2[index]} \n"
            display_string += " ```"

            final_title = find_title()
            final_embed = hikari.Embed(
                title = final_title, 
                description = display_string,
                color = hikari.Color.from_hex_code("#088F8F"),
            )
            await ctx.respond(final_embed)    
        await db.commit()

# children commands for maps
# /tr add_map
# Add_map subcommand adds a map to the 'maps' SQLite database
@tr.child
@lightbulb.option("name", "Enter map name", type = string)
@lightbulb.command("add_map", "Add a map to the database")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def add_map(ctx):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT name FROM maps WHERE name = ?", (ctx.options.name,))
            data = await cursor.fetchone()
            name = ctx.options.name
            if data or len(name) > 25:
                add_embed_fail = hikari.Embed(
                    title = "Failed to Add Map", 
                    description = f"""!ERROR! Map: **{ctx.options.name}** already exists
> refer to '/tr help' for TRBot rules.
                    """,
                    color = hikari.Color.from_hex_code("#C70039")
                )
                await ctx.respond(add_embed_fail)
            else:
                await cursor.execute("INSERT INTO maps (name) VALUES (?)", (ctx.options.name,))
                add_embed_success = hikari.Embed(
                    title = "Map Successfully Added", 
                    description = f"Map: **{ctx.options.name}** has been added",
                    color = hikari.Color.from_hex_code("#32CD32")
                )
                await ctx.respond(add_embed_success)
        await db.commit()

# /tr remove_map
# Remove_map subcommand removes a given map from the 'maps' database
@tr.child
@lightbulb.option("name", "Enter map name", type = string)
@lightbulb.command("remove_map", "Remove a map from the database")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def remove_map(ctx):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT name FROM maps WHERE name = ?", (ctx.options.name,))
            data = await cursor.fetchone()
            if data:
                await cursor.execute("DELETE FROM maps WHERE name = ?", (ctx.options.name,))
                remove_embed_success = hikari.Embed(
                    title = "Map Successfully Removed", 
                    description = f"Map: **{ctx.options.name}** has been deleted",
                    color = hikari.Color.from_hex_code("#32CD32")
                )
                await ctx.respond(remove_embed_success)
            else:
                remove_embed_fail = hikari.Embed(
                    title = "Failed to Remove Map", 
                    description = f"""!ERROR! Map: **{ctx.options.name}** does not exist
> refer to '/tr help' for TRBot rules.
                    """,
                    color = hikari.Color.from_hex_code("#C70039")
                )
                await ctx.respond(remove_embed_fail)
        await db.commit()

# /tr maps
# Maps subcommand lists all the maps in the database
@tr.child
@lightbulb.command("maps", "View all the maps in the database")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def maps(ctx):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT * FROM maps")
            data = await cursor.fetchall()
            maps_string = ">>> "
            for map in data:
                maps_string += f"```{map[0]}``` "
            maps_embed = hikari.Embed(
                title = "List of Maps", 
                description = maps_string,
                color = hikari.Color.from_hex_code("#E37383")
            )
            await ctx.respond(maps_embed)    
        await db.commit()

# /tr pick_map
# Pick_map subcommand returns a random map from the database
@tr.child
@lightbulb.command("pick_map", "Return a random map from the database")
@lightbulb.implements(lightbulb.SlashSubCommand)
async def pick_map(ctx):
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT * FROM maps")
            data = await cursor.fetchall()
            chosen_map = pick_random_map(data)
            maps_embed = hikari.Embed(
                title = "Map Selected:", 
                description = f"**{chosen_map.upper()}**",
                color = hikari.Color.from_hex_code("#088F8F")
            )
            await ctx.respond(maps_embed)    
        await db.commit()

if __name__ == "__main__":
    bot.run()