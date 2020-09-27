from discord.ext import commands


class Counting(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 753626223967469691
        self.counting = {}
        self.bot.loop.create_task(self.load())

    async def load(self):
        query = 'SELECT next, author_id FROM counting'
        res = await self.bot.db.fetchrow(query)
        if res:
            self.counting = {
                'next': res['next'],
                'author_id': res['author_id']
            }

    async def update_counting(self, next, author_id):
        self.counting = {
            'next': next,
            'author_id': author_id
        }
        query = 'UPDATE counting SET next = $1, author_id = $2'
        await self.bot.db.execute(query, next, author_id)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == self.channel_id:
            try:
                number = int(message.content)
                if number != self.counting['next']:
                    await message.delete()
                else:
                    if self.counting['author_id'] == message.author.id:
                        await message.delete()
                    else:
                        await update_counting()
            except ValueError:
                await message.delete()


def setup(bot):
    bot.add_cog(Counting(bot))
