from discord import Embed
from discord.ext import commands
from django.conf import settings
from django.utils.translation import gettext as _

from app_api.modules.status.views import GitHub
from bots.discord_interface.utils import COLOR_SETTINGS, translation_override


@commands.hybrid_command(name="help", help="Creates an overview of the bot and commands", )
@translation_override
async def bot_help(ctx: commands.Context, ) -> None:
    async with ctx.typing():
        embed = Embed(title=_("Help"), color=COLOR_SETTINGS)
        project_version = GitHub.latest_version().get("version", None)
        desc = _(
            "Disclaimer: This bot was not created in cooperation with Prime League or Freaks4u Gaming GmbH. "
            "This bot was designed and programmed due to missed matches. "
            "The bot was realized to the best of our knowledge, "
            "and after a test phase made available for other teams.\n"
            "Nevertheless all information is without guarantee!"
        )
        for command in ctx.bot.commands:
            name = f"📌 /{command.qualified_name}"
            value = command.help
            embed.add_field(name=name, value=value, inline=False)
        general = _(
            "PrimeBot Website for API status and help: {website}\n"
            "Discord Community Server for help and updates: {discord_url}\n"
            "Checkout our Github for contributions: {github_url}\n"
            "_Version: {version}_\n"
        ).format(version=project_version, website=settings.SITE_ID, discord_url=settings.DISCORD_SERVER_LINK,
                 github_url=settings.GITHUB_URL)
        embed.description = f"_{desc}_\n\n{general}"
    await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    bot.add_command(bot_help)
