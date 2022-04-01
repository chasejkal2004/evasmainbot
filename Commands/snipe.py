import discord
from discord.ext import commands


class snipe(commands.Cog):
    """A couple of simple commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.last_msg = None


    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        self.last_msg = message

    @commands.command()
    @commands.has_role('Staff')
    async def snipe(self, ctx: commands.Context):
        """A command to snipe delete messages."""
        if not self.last_msg:  # on_message_delete hasn't been triggered since the bot started
            await ctx.send("There is no message to snipe!")
            return

        author = self.last_msg.author
        content = self.last_msg.content
        embed = discord.Embed(title=f"Message from {author}", description=content)
        embed.set_footer(text = ctx.author.name + "#" + ctx.author.discriminator + " ", icon_url = ctx.author.avatar_url)
        await ctx.send(embed=embed)



def setup(bot: commands.Bot):
    bot.add_cog(snipe(bot))