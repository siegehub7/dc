
import discord
from discord.ext import commands
import random
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

DISCORD_BOT_TOKEN = 'MTM3NDI1MjUxMDQxNTY4NzcyMw.GDlMam.BWHO9MNh0ehCiNaof2oSFw0Sgg1P5azamncdPE'

PAYPAL_EMAIL = "siegehub7@gmail.com"

# Replace with real Role IDs from your server
ROLE_IDS = {
    1: 123456789012345678,  # Small Tournament
    2: 223456789012345678,  # Medium Tournament
    3: 323456789012345678,  # Large Tournament
    4: 423456789012345678,  # Small Giveaway
    5: 523456789012345678,  # Medium Giveaway
    6: 623456789012345678,  # Large Giveaway
    7: 723456789012345678,  # Wheel Spin
    8: 823456789012345678   # VIP
}

ITEMS = {
    1: {'name': 'Small Tournament ($10)', 'price': 10},
    2: {'name': 'Medium Tournament ($30)', 'price': 30},
    3: {'name': 'Large Tournament ($60)', 'price': 60},
    4: {'name': 'Small Giveaway ($10)', 'price': 10},
    5: {'name': 'Medium Giveaway ($30)', 'price': 30},
    6: {'name': 'Large Giveaway ($60)', 'price': 60},
    7: {'name': 'Wheel Spin ($50)', 'price': 50},
    8: {'name': 'VIP Access ($200)', 'price': 200},
}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def shop(ctx):
    """List available items."""
    msg = "**Available Items:**\n"
    for key, item in ITEMS.items():
        msg += f"{key}. {item['name']} - ${item['price']}\n"
    await ctx.send(msg)

@bot.command()
async def buy(ctx, item_number: int):
    """Send the PayPal payment link."""
    if item_number not in ITEMS:
        await ctx.send("Invalid item number.")
        return
    item = ITEMS[item_number]
    await ctx.send(
        f"To purchase **{item['name']}**, send **${item['price']}** to PayPal: `{PAYPAL_EMAIL}`\n"
        f"After payment, reply with `!confirmpay YOUR_TRANSACTION_ID` to confirm."
    )

@bot.command()
async def confirmpay(ctx, transaction_id: str):
    """Simulate payment confirmation and assign role."""
    await ctx.send("Payment received! Please enter the item number you paid for using `!itemnumber [number]`.")
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    try:
        msg = await bot.wait_for('message', check=check, timeout=60)
        item_number = int(msg.content.replace("!itemnumber ", "").strip())
        if item_number not in ITEMS:
            await ctx.send("Invalid item number.")
            return

        if item_number == 7:
            result = random.choice(list(ROLE_IDS.keys())[:-1] + ["Retry", "Nothing"])
            if result == "Retry":
                await ctx.send("You landed on **Retry**. Use `!buy 7` to spin again.")
                return
            elif result == "Nothing":
                await ctx.send("Unlucky! You landed on **Nothing**.")
                return
            else:
                role = ctx.guild.get_role(ROLE_IDS[result])
                await ctx.author.add_roles(role)
                await ctx.send(f"{ctx.author.mention} won **{ITEMS[result]['name']}** in the wheel spin!")
        elif item_number == 8:
            for i in range(1, 7):
                role = ctx.guild.get_role(ROLE_IDS[i])
                if role:
                    await ctx.author.add_roles(role)
            await ctx.send(f"{ctx.author.mention} has been granted **VIP Access**!")
        else:
            role = ctx.guild.get_role(ROLE_IDS[item_number])
            if role:
                await ctx.author.add_roles(role)
            await ctx.send(f"{ctx.author.mention} has been granted **{ITEMS[item_number]['name']}**!")
    except Exception as e:
        await ctx.send("Something went wrong or you took too long.")

keep_alive()
bot.run('MTM3NDI1MjUxMDQxNTY4NzcyMw.GDlMam.BWHO9MNh0ehCiNaof2oSFw0Sgg1P5azamncdPE')
