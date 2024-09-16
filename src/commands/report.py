import discord

class ReportReasonModal(discord.ui.Modal):
    def __init__(self, report_message):
        super().__init__(title="Report Reason")
        self.report_message = report_message
        self.reason = discord.ui.TextInput(label="Reason for report", style=discord.TextStyle.paragraph)
        self.add_item(self.reason)

    async def on_submit(self, interaction: discord.Interaction):
        await self.report_message.edit(
            content=f"{self.report_message.content}\n\n**Reason:**\n\n{self.reason.value}"
        )

        await interaction.response.send_message("Your report has been submitted for review", ephemeral=True)
