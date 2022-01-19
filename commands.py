import discord
from discord.ext import commands
from fetchData.omdb_api import omdb_search
from fetchData.tmdb_api import tmdb_search


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def movie(self, ctx, *, in_str=""):  # input format: *movie {movie name} / {year}
        if in_str == "":
            return await self.handle_empty(ctx)

        title, index = self.process_input(in_str)
        if index.isdigit() is False:
            ctx.send(":warning: Invalid input")
            return

        try:
            released, title, runtime, genres, t_bo, overview, poster_url, \
                comp_url, trailer_url, color, year = tmdb_search(title, int(index) - 1)
            release, rated, director_str, actor_str, d_bo, awards, ratings = omdb_search(title, year)
        except TypeError:
            await ctx.send(":x: No movie found!")
            return
        except IndexError:
            await ctx.send(":x: Invalid index!")
            return
        except:
            await ctx.send(":x: Unidentified Error. Please relay error to I'm Peter #1327")
            return

        e = discord.Embed(color=discord.Color.from_rgb(color[0], color[1], color[2]), title=title)

        e.add_field(name="Released", value=release, inline=True)
        e.add_field(name="Duration", value=runtime if released else 'N/A', inline=True)
        e.add_field(name="Rated", value=rated if released else 'N/A', inline=True)
        e.add_field(name="Genres", value=genres, inline=True)
        e.add_field(name="Director", value=director_str, inline=True)
        e.add_field(name="Actors", value=actor_str, inline=True)
        e.add_field(name="Box Office", value=t_bo + '\n' + d_bo if released else 'N/A', inline=True)
        e.add_field(name="Awards", value=awards if released else 'N/A', inline=True)
        e.add_field(name="Rating", value=ratings if released else 'N/A', inline=True)
        e.add_field(name="Overview:", value=overview, inline=False)
        e.set_image(url=poster_url)
        e.set_thumbnail(url=comp_url)

        await ctx.send(embed=e)
        await ctx.send(f":movie_camera: Watch Movie Trailer here:\n{trailer_url}")

    @commands.command()
    async def actor(self, ctx, *, in_str):
        ctx.send("Searching...")

    @staticmethod
    def process_input(in_str):
        if '[' not in in_str:
            return in_str, '1'

        li = [x.strip() for x in in_str.split('[')]

        if len(li) != 2:
            return False, False

        return li[0], li[1][:-1]

    @staticmethod
    async def handle_empty(ctx):
        await ctx.send(":warning: No input was given! ")


def setup(bot):
    bot.add_cog(Commands(bot))
