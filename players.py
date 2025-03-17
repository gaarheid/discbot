import discord
import requests
import asyncio
from discord import app_commands

TOKEN = "MTM1MTIwMjQxMDA2ODA1NDA4OQ.GTgvx-.EDJY04HSipRncMRHZpq-XliVncB5rkOlFw_Fqw"
SERVER_ID = "32139049"
GUILD_ID = 1349740526282477598  # Voeg je Guild ID toe
API_URL = f"https://api.battlemetrics.com/servers/{SERVER_ID}"

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

async def update_status():
    await client.wait_until_ready()
    while not client.is_closed():
        try:
            response = requests.get(API_URL)
            data = response.json()
            player_count = data['data']['attributes']['players']
            max_players = data['data']['attributes']['maxPlayers']
            status = f"{player_count}/{max_players} spelers online"
            await client.change_presence(activity=discord.Game(name=status))
        except Exception as e:
            print(f"Error updating status: {e}")
        await asyncio.sleep(60)  # Elke minuut bijwerken

@client.event
async def on_ready():
    print(f'Bot is ingelogd als {client.user}')
    guild = discord.Object(id=GUILD_ID)
    await tree.sync(guild=guild)  # Alleen synchroniseren met specifieke guild
    client.loop.create_task(update_status())

@tree.command(name="serverstatus", description="Bekijk de huidige serverstatus", guild=discord.Object(id=GUILD_ID))
async def serverstatus(interaction: discord.Interaction):
    try:
        response = requests.get(API_URL)
        data = response.json()
        player_count = data['data']['attributes']['players']
        max_players = data['data']['attributes']['maxPlayers']
        server_name = data['data']['attributes']['name']
        
        embed = discord.Embed(title="Server Status", color=discord.Color.green())
        embed.add_field(name="Server Naam", value=server_name, inline=False)
        embed.add_field(name="Spelers Online", value=f"{player_count}/{max_players}", inline=False)
        embed.set_footer(text="BattleMetrics API - Real-time server status")
        
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        await interaction.response.send_message("Er is een fout opgetreden bij het ophalen van de serverstatus.", ephemeral=True)
        print(f"Error fetching server status: {e}")

client.run('MTM1MTIwMjQxMDA2ODA1NDA4OQ.GTgvx-.EDJY04HSipRncMRHZpq-XliVncB5rkOlFw_Fqw')
