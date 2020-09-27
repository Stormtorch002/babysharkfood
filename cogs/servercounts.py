from discord.ext import commands, tasks
import discord
import re


class ServerCounts(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.guild = self.bot.get_guild(725805218507391036)
        self.online = self.guild.get_channel(759600846265909249)
        self.offline = self.guild.get_channel(759600847251963945)
        self.extractor = re.compile('[A-Za-z][:] (\d+)')
        self.online_name = 'Online: {}'
        self.offline_name = 'Offline: {}'
        self.update_counters.start()

    @tasks.loop(minutes=10)
    async def update_counters(self):
        online = 0
        for member in self.guild.members:
            if member.status is not discord.Status.offline:
                online += 1
        offline = self.guild.member_count - online
        if self.extractor.findall(self.online.name)[0] != str(online):
            await self.online.edit(name=self.online_name.format(online))
        if self.extractor.findall(self.offline.name)[0] != str(offline):
            await self.offline.edit(name=self.offline_name.format(offline))

    @update_counters.error
    async def counters_error(self, error):
        print(type(error))
        raise error


def setup(bot):
    bot.add_cog(ServerCounts(bot))
