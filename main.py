import discord
from discord import Client
from discord.ext import commands
import asyncio
from discord.utils import get
from random import randint

client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    print('Bot iniciado com sucesso.')
    print(client.user.name)
    print(client.user.id)
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('Vinicius ASMR'))

client.reaction_roles = []
@client.event
async def on_raw_reaction_add(payload):
    for role, msg, emoji in client.reaction_roles:
        if msg.id == payload.message_id and emoji == payload.emoji.name:
            await payload.member.add_roles(role)

@client.event
async def on_raw_reaction_remove(payload):
    for role, msg, emoji in client.reaction_roles:
        if msg.id == payload.message_id and emoji == payload.emoji.name:
            await client.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)

@client.command()
@commands.has_permissions(administrator=True)
@commands.has_role('🌐 ▸ Fundador')
async def reação(ctx, role: discord.Role = None, msg: discord.Message = None, emoji=None):
    if role != None and msg != None and emoji != None:
        await msg.add_reaction(emoji)
        client.reaction_roles.append((role, msg, emoji))
    else:
        await ctx.send("Argumentos inválidos.")

@client.command()
@commands.has_permissions(administrator=True)
@commands.has_role('🌐 ▸ Fundador')
async def mensagem(message, *, args):
    embedtest = discord.Embed(description=args, color=0x4bd60a)
    embedtest.set_footer(text="Atenciosamente, Vinicius ASMR.")
    embedtest.set_author(name="Vinicius ASMR",
                     url="https://www.youtube.com/c/ViniciusASMR1",
                     icon_url="https://cdn.discordapp.com/attachments/737407456006897716/737460313221234758/unnamed.jpg")
    await message.channel.send(content=None, embed=embedtest)




@client.command()
@commands.has_permissions(administrator=True)
@commands.has_role('🌐 ▸ Fundador')
async def embed(message):
    embed = discord.Embed(title="✔ Gostaria de fazer uma doação? Veja como e os benefícios:",
                          description="Doações ajudam o canal se manter e comprar novos equipamentos para melhorar a qualidade. Confira abaixo como fazer sua doação e os benefícios de se tornar um doador.",
                          color=0xf10909)
    embed.set_author(name="Vinicius ASMR",
                     url="https://www.youtube.com/c/ViniciusASMR1",
                     icon_url="https://cdn.discordapp.com/attachments/737407456006897716/737460313221234758/unnamed.jpg")
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
                    inline=False)
    embed.add_field(name="✽ Rede Dark ✽",
                    value="➔ Servidor de MiniGames.\n"
                          '➔ Servidor de RankUP.\n'
                          '➔ IP: rededark.com\n',
                    inline=False)
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
async def mute(ctx, member: discord.Member, mute_time: int):
    role = discord.utils.get(ctx.guild.roles, name="Silenciado")
    await member.add_roles(role)
    roles = discord.utils.get(ctx.guild.roles, name="🔅 ▸ Membro")
    roles1 = discord.utils.get(ctx.guild.roles, name="⚽️ ▸ Amigos")
    await member.remove_roles(roles, roles1)
    await ctx.send(f'{member.mention} foi silenciado com sucesso.')

    await asyncio.sleep(mute_time)
    await member.remove_roles(role)
    await member.add_roles(roles)
    await ctx.send(f'{member.mention} foi liberado do silêncio com sucesso.')

@client.command()
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member):
    guild = ctx.guild
    for role in guild.roles:
        if role.name == "Silenciado":
            await member.remove_roles(role)
            await ctx.send(f'{member.mention} foi desmutado.')
            return
        elif role.name == "🔅 ▸ Membro":
            await member.add_roles(role)


@client.command()
@commands.has_permissions(administrator=True)
async def tempban(ctx, member: discord.Member, mute_time : int):
    role = discord.utils.get(ctx.guild.roles, name="Expulso")
    await member.add_roles(role)
    roles = discord.utils.get(ctx.guild.roles, name="🔅 ▸ Membro")
    roles1 = discord.utils.get(ctx.guild.roles, name="⚽️ ▸ Amigos")
    await member.remove_roles(roles, roles1)
    await ctx.send(f'{member.mention} foi temporariamente banido com sucesso.')

    await asyncio.sleep(mute_time)
    await member.remove_roles(role)
    await member.add_roles(roles)
    await ctx.send(f'{member.mention} foi liberado do banimento temporário com sucesso.')


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


@client.command()
async def print(ctx):
    if ctx.channel.id == 737996406165471273:
        letras = (
            'a', 'b', 'c', 'd', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
            'w', 'x',
            'y', 'z',
            '0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
        caractere1 = letras[randint(0, 34)]
        caractere2 = letras[randint(0, 34)]
        caractere3 = letras[randint(0, 34)]
        caractere4 = letras[randint(0, 34)]
        caractere5 = letras[randint(0, 34)]
        caractere6 = letras[randint(0, 34)]
        mstring = "https://prnt.sc/" + caractere1 + caractere2 + caractere3 + caractere4 + caractere5 + caractere6
        await ctx.send(f'{ctx.author.mention}, a sua print gerada aleatoriamente é: {mstring}')
    else:
        guild = ctx.guild
        emoji = discord.utils.get(guild.emojis, name='nop')
        await ctx.send(f'{emoji} Você não pode executar esse comando aqui, {ctx.author.mention}. Vá até o canal de comandos.')

@client.command()
async def piada(ctx):
    guild = ctx.guild
    emoji = discord.utils.get(guild.emojis, name='puto')
    if ctx.channel.id == 737996406165471273:
        piadas = ('O que o advogado do frango foi fazer na delegacia? Foi soltar a franga!',
                  'Por que na Argentina as vacas vivem olhando pro céu? Por que tem bois nos ares!',
                  'Para que serve óculos verde? Para verdeperto',
                  'Para que serve óculos vermelho? Para vermelhor',
                  'Por que a mu lher do Hulk divorciou-se dele? Por que ela queria um homem mais maduro',
                  'Por que o jacaré tirou o jacarezinho da escola? Por que ele réptil de ano',
                  'Você sabe qual e o contrário de volátil? Vem cá sobrinho',
                  'O que um cromossomo falou pro outro? Cromossomos bonitos!',
                  'Batman pegou seu bat-sapato social e seu bat-blazer. Aonde ele foi? A um bat-zado',
                  'Se o cachorro tivesse religião, qual seria? Cão-domblé')
        sendpiada = piadas[randint(0,9)]
        await ctx.send(f'{ctx.author.mention}, {sendpiada}')
        await ctx.message.add_reaction(emoji)
    else:
        await ctx.send(f'Você não pode executar esse comando aqui, {ctx.author.mention}. Vá até o canal de comandos.')

@client.event
async def on_member_join(ctx):
    role = discord.utils.get(ctx.guild.roles, name = "🔅 ▸ Membro")
    await ctx.add_roles(role)


client.run('TOKEN DO SEU BOT')
