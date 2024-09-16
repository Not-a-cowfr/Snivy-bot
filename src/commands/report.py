import discord

class ReportReasonModal(discord.ui.Modal):
    def __init__(self, report_message):
        super().__init__(title="Report Reason")
        self.report_message = report_message
        self.reason = discord.ui.TextInput(label="Reason for report", style=discord.TextStyle.paragraph)
        self.add_item(self.reason)

    async def on_submit(self, interaction: discord.Interaction):
        embed = self.report_message.embeds[0]
        embed.add_field(name="Reason", value=self.reason.value, inline=False)
        await self.report_message.edit(embed=embed)

        await interaction.response.send_message("Your report has been submitted for review", ephemeral=True)