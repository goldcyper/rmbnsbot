import requests
from redbot.core import commands, Config

class RmbnsBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890)
        default_guild = {
            "example_setting": "default_value",
        }
        self.config.register_guild(**default_guild)

    @commands.command()
    async def hello(self, ctx):
        """Responds with a greeting."""
        await ctx.send("Hello, world!")

    @commands.command()
    async def nation(self, ctx, nation_name: str):
        """Fetches information about a NationStates nation."""
        nation_data = self.get_nation_data(nation_name)
        if nation_data:
            await ctx.send(f"Nation: {nation_data['name']}\nRegion: {nation_data['region']}")
        else:
            await ctx.send("Nation not found.")

    def get_nation_data(self, nation_name):
        """Fetches nation data from the NationStates API."""
        url = f"https://www.nationstates.net/cgi-bin/api.cgi?nation={nation_name}&q=region"
        headers = {
            "User-Agent": "Redbot v3 (rmbnsbot)",
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return {
                "name": nation_name,
                "region": response.text,
            }
        else:
            return None

    @commands.command()
    async def set_example(self, ctx, value: str):
        """Example command to set a guild-specific setting."""
        await self.config.guild(ctx.guild).example_setting.set(value)
        await ctx.send(f"Example setting set to: {value}")

    @commands.command()
    async def get_example(self, ctx):
        """Example command to get a guild-specific setting."""
        value = await self.config.guild(ctx.guild).example_setting()
        await ctx.send(f"Example setting is: {value}")