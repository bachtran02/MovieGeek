import discord
from discord.ext import commands


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        # description = {invite link}, {GitHub link}, ...
        description = "Get all the information of your favorite movie / TV show in a matter of seconds!"
        e = discord.Embed(color=discord.Color.from_rgb(255, 255, 255), title="Help Menu", description=description)
        e.add_field(name="*movie", value='Type "*movie {your movie name} [{search index}]" (search index is optional)',
                    inline=False)
        e.add_field(name="*help", value='Type "*help" to open the help menu', inline=False)
        e.set_image(url="https://media.giphy.com/media/X3Yj4XXXieKYM/giphy.gif")
        await ctx.send(embed=e)

        # search result for actors
        # search result for companies
        # give list of trending movies / TV shows
        # suggest a random movie / TV show


def setup(bot):
    bot.add_cog(Misc(bot))
