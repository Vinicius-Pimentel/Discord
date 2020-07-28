import discord
from discord import Client
from discord.ext import commands
import asyncio
from discord.utils import get
client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print('Bot iniciado com sucesso.')
    print(client.user.name)
    print(client.user.id)
    activity = discord.Game(name="Vinicius ASMR", type=3)
    await client.change_presence(status=discord.Status.idle, activity=activity)

@client.command()
@commands.has_permissions(administrator=True)
@commands.has_role('🌐 ▸ Fundador')
async def embed(message):
    embed=discord.Embed(title="✔ Gostaria de fazer uma doação? Veja como e os benefícios:",
                        description="Doações ajudam o canal se manter e comprar novos equipamentos para melhorar a qualidade. Confira abaixo como fazer sua doação e os benefícios de se tornar um doador.",
                        color=0xf10909)
    embed.set_author(name="Vinicius ASMR",
                     url="https://www.youtube.com/c/ViniciusASMR1",
                     icon_url = "https://cdn.discordapp.com/attachments/737407456006897716/737460313221234758/unnamed.jpg")
    embed.add_field(name="⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀✽ Como doar? ✽",
                    value="➔ Você pode doar pelo Mercado Pago ou pelo PayPal!\n" 
                          '➔ E-mail do Mercado Pago: gamvacp@gmail.com\n' 
                          '➔ E-mail do PayPal: dosgamersumgamer@gmail.com\n' 
                          '➔ Qualquer quantia é muito bem vinda!\n',
                    inline=False)
    embed.add_field(name="⠀⠀⠀⠀⠀⠀⠀⠀⠀✽ Quais são os benefícios de um Doador? ✽",
                    value='➔ Os doadores recebem uma tag exclusiva! (Apoiador)\n' 
                          '➔ Quantias generosas geram desconto em alguns tipos de divulgação!\n',
                    inline=True)
    embed.set_footer(text="Atenciosamente, Vinicius ASMR.")
    await message.channel.send(content=None, embed=embed)

@client.command()
async def youtuber(message):
    embed = discord.Embed(title="✔ Servidores que tenho tag YouTuber:",
                          description="Lista completa de todos os servidores que eu tenho tag YouTuber.",
                          color=0xf10909)
    embed.add_field(name="✽ Rede Stone ✽",
                    value="➔ Servidor de Factions.\n"
                          '➔ Servidor de RankUP.\n'
                          '➔ IP: redestone.com\n',
                    inline = False)
    embed.add_field(name="✽ Rede Dark ✽",
                    value="➔ Servidor de MiniGames.\n"
                          '➔ Servidor de RankUP.\n'
                          '➔ IP: rededark.com\n',
                    inline = False)
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/737305748144390184/737355745581989938/youtube.png')
    await message.channel.send(content=None, embed=embed)

@client.command()
async def ajuda(ctx):
    await ctx.send('.youtuber: Veja os servidores que tenho tag YouTuber\n'
                   'Poucos comandos para players foram disponibilizados\n'
                   'Bot se encontra em fase BETA.')

@client.command()
@commands.has_permissions(administrator=True)
@commands.has_role('🌐 ▸ Fundador')
async def limpar(ctx, amount=100):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f'{amount} mensagens foram removidas!')

@client.command()
@commands.has_permissions(administrator=True)
@commands.has_role('🌐 ▸ Fundador')
async def expulsar(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} foi expulso(a).\n')
    await ctx.send('https://cdn.discordapp.com/emojis/736007157903917188.gif?v=1')

@client.command()
@commands.has_permissions(administrator=True)
@commands.has_role('🌐 ▸ Fundador')
async def banir(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} foi banido(a).')
    await ctx.send('https://cdn.discordapp.com/emojis/737652098295922759.gif?v=1')

@client.command()
@commands.has_permissions(administrator=True)
async def mutar(ctx, member : discord.Member):
    guild = ctx.guild
    for role in guild.roles:
        if role.name == "Silenciado":
            await member.add_roles(role)
            await ctx.send(f'{member.mention} foi silenciado.')
            return

            overwrite = discord.PermissionsOverwrite(send_messages=False)
            newRole = await guild.create_role(name="Silenciado")

            for channel in guild.text_channels:
                await channel.set_permissions(newRole, overwrite=overwrite)

            await member.add_roles(newRole)
            await ctx.send(f'{member.mention} foi silenciado.')

@client.command()
@commands.has_permissions(administrator=True)
async def desmutar(ctx, member : discord.Member):
    guild = ctx.guild
    for role in guild.roles:
        if role.name == "Silenciado":
            await member.remove_roles(role)
            await ctx.send(f'{member.mention} foi desmutado.')
            return

@client.command()
@commands.has_permissions(administrator=True)
async def tempban(ctx, member : discord.Member):
    guild = ctx.guild
    for role in guild.roles:
        if role.name == "🔅 ▸ Membro":
            await member.remove_roles(role)
        elif role.name == "teste":
            await member.remove_roles(role)
        elif role.name == "⚽️ ▸ Amigos":
            await member.remove_roles(role)
        elif role.name == "Expulso":
            await member.add_roles(role)
    await ctx.send(f'{member.mention} foi banido temporariamente.')

@client.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, member: discord.Member):
    guild = ctx.guild
    for role in guild.roles:
        if role.name == 'Expulso':
            await member.remove_roles(role)
        elif role.name == '🔅 ▸ Membro':
            await member.add_roles(role)
    await ctx.send(f'{member.mention} foi desbanido.')

@client.command()
@commands.has_permissions(administrator=True)
@commands.has_role('🌐 ▸ Fundador')
async def say(ctx, *, msg):
    await ctx.message.delete()
    await ctx.send(msg)

            
client.run('TOKEN')
