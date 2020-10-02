import discord
from discord.ext import commands, tasks
from discord.ext.commands import cooldown, BucketType, CommandOnCooldown, BadArgument, CommandNotFound, \
    MaxConcurrencyReached
import asyncio
import random
from random import randint
import json
import time
import datetime

client = commands.Bot(command_prefix='.')
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)


@client.event
async def on_command_error(ctx, exc):
    if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
        pass
    elif isinstance(exc, CommandOnCooldown):
        await ctx.send(f"Este comando está com cooldown. Tente novamente em {exc.retry_after:,.2f} segundos.")
    elif isinstance(exc, MaxConcurrencyReached):
        await ctx.send(
            f"Este comando está sendo utilizado por outro membro no momento, aguarde um pouco {ctx.author.mention}.")


@client.event
async def on_ready():
    print('Bot iniciado com sucesso.')
    print(client.user.name)
    print(client.user.id)
    await client.change_presence(activity=discord.Game('Vinicius ASMR'))


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
    embed.timestamp = datetime.datetime.utcnow()
    embed.set_footer(text="Atenciosamente, Vinicius ASMR.")
    await message.channel.send(content=None, embed=embed)


@client.command()
async def ajuda(ctx):
    guild = ctx.guild
    emoji = discord.utils.get(guild.emojis, name='seta')
    embed = discord.Embed(title="Confira a lista de comandos e suas funções.",
                          description="Estes são todos os comandos que membros do servidor podem usar.", color=0x0b77ea)
    embed.set_author(
        name="Suporte - Vinicius ASMR",
        icon_url="https://cdn.discordapp.com/attachments/738188017847762985/741269006773649528/7978f09acb58b076348efe2a0850fe78.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/738188017847762985/741271581791223918/COMANDOS.png")
    embed.add_field(name=f"{emoji} .conta / .banco", value="Verificar seu saldo (carteira e banco).\n"
                                                           "Uso correto: .conta / .banco", inline=False)
    embed.add_field(name=f"{emoji} .mendigar",
                    value="Ganhar uma quantia entre 1 e 100 reais (cooldown de 5 segundos).\n"
                          "Uso correto: .mendigar",
                    inline=False)
    embed.add_field(name=f"{emoji} .sacar", value="Tirar uma quantia da sua conta bancária.\n"
                                                  "Uso correto: .sacar 10", inline=False)
    embed.add_field(name=f"{emoji} .depositar", value="Colocar uma quantia na sua conta bancária.\n"
                                                      "Uso correto: .depositar 10", inline=False)
    embed.add_field(name=f"{emoji} .enviar", value="Enviar uma quantia para outro membro do servidor.\n"
                                                   "Uso correto: .enviar @NomeDaPessoa 10", inline=False)
    embed.add_field(name=f"{emoji} .roubar", value="Roube outro membro do servidor (cooldown de 60 segundos).\n"
                                                   "Uso correto: .roubar @NomeDaPessoa", inline=False)
    embed.add_field(name=f"{emoji} .apostar",
                    value="Aposte em Pedra, Papel ou Tesoura e tenha a chance de duplicar a quantia apostada (cooldown de 5 segundos).\n"
                          "Uso correto: .apostar Pedra/Papel/Tesoura 10",
                    inline=False)
    embed.add_field(name=f"{emoji} .dado",
                    value="Acerte o número que o dado vai cair e ganhe 10x mais o valor apostado (cooldown de 5 segundos).\n"
                          "Uso correto: .dado 2/3/4/5/6/7/8/9/10/11/12 10",
                    inline=False)
    embed.add_field(name=f"{emoji} .cavalo",
                    value="Aposte no cavalo mais rápido e ganhe 8x a quantia apostada. Você pode apostar no cavalo Verde, Azul, Amarelo, Vermelho e Roxo (cooldown de 60 segundos).\n"
                          "Uso correto: .cavalo Verde/Azul/Amarelo/Vermelho/Roxo 10",
                    inline=False)
    embed.add_field(name=f"{emoji} .trabalhar",
                    value="Trabalhe e ganhe uma quantia entre 500 e 1000 reais (cooldown de 10 minutos).\n"
                          "Uso correto: .trabalhar", inline=False)
    embed.add_field(name=f"{emoji} .recompensa",
                    value="Colete a recompensa e ganhe uma quantia entre 1000 e 5000 reais (cooldown de 24 horas).\n"
                          "Uso correto: .recompensa",
                    inline=False)
    embed.set_footer(text="Dúvidas? Contate a equipe de Moderação.")
    await ctx.send(embed=embed)


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
async def tempban(ctx, member: discord.Member, mute_time: int):
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
        await ctx.send(
            f'{emoji} Você não pode executar esse comando aqui, {ctx.author.mention}. Vá até o canal de comandos.')


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
        sendpiada = piadas[randint(0, 9)]
        await ctx.send(f'{ctx.author.mention}, {sendpiada}')
        await ctx.message.add_reaction(emoji)
    else:
        await ctx.send(f'Você não pode executar esse comando aqui, {ctx.author.mention}. Vá até o canal de comandos.')


@client.command(aliases=['banco'])
async def conta(ctx):
    if ctx.channel.id == 737996406165471273:
        user = ctx.author
        await open_account(ctx.author)
        users = await get_bank_data()

        walletAmount = users[str(user.id)]["carteira"]
        bankAmount = users[str(user.id)]["banco"]

        em = discord.Embed(title=f"Conta bancária de {ctx.author.name} ", color=discord.Color.green())
        em.add_field(name="Carteira", value=walletAmount)
        em.add_field(name="Banco", value=bankAmount)
        await ctx.send(embed=em)
    else:
        await ctx.send(f'Você não pode usar comandos aqui, {ctx.author.mention}!')


@client.command()
@cooldown(1, 10, BucketType.user)
async def mendigar(ctx):
    if ctx.channel.id == 737996406165471273:
        user = ctx.author
        await open_account(ctx.author)
        users = await get_bank_data()
        earnings = random.randrange(101)
        await ctx.send(f"Alguém te deu {earnings} reais, {ctx.author.mention}!")
        users[str(user.id)]["carteira"] += earnings
        with open("mainbank.json", "w") as f:
            json.dump(users, f)
    else:
        await ctx.send(f'Você não pode usar comandos aqui, {ctx.author.mention}!')


@client.command()
async def sacar(ctx, amount=None):
    if ctx.channel.id == 737996406165471273:
        await open_account(ctx.author)

        if amount == None:
            await ctx.send(f"Digite a quantia a ser sacada, {ctx.author.mention}.\n"
                           f"Exemplo: .sacar 10")
            return

        bal = await update_bank(ctx.author)
        amount = int(amount)
        if amount > bal[1]:
            await ctx.send("Você não tem dinheiro suficiente.")
            return
        if amount < 0:
            await ctx.send("A quantia deve ser maior que 0.")
            return

        await update_bank(ctx.author, amount)
        await update_bank(ctx.author, -1 * amount, "banco")

        await ctx.send(f"Você sacou {amount} reais, {ctx.author.mention}!")
    else:
        await ctx.send(f'Você não pode usar comandos aqui, {ctx.author.mention}!')


@client.command()
async def depositar(ctx, amount=None):
    if ctx.channel.id == 737996406165471273:
        await open_account(ctx.author)

        if amount == None:
            await ctx.send(f"Digite a quantia a ser depositada, {ctx.author.mention}.\n"
                           f"Exemplo: .depositar 10")
            return

        bal = await update_bank(ctx.author)
        amount = int(amount)
        if amount > bal[0]:
            await ctx.send("Você não tem dinheiro suficiente.")
            return
        if amount < 0:
            await ctx.send("A quantia deve ser maior que 0.")
            return

        await update_bank(ctx.author, -1 * amount)
        await update_bank(ctx.author, amount, "banco")

        await ctx.send(f"Você depositou {amount} reais, {ctx.author.mention}!")
    else:
        await ctx.send(f'Você não pode usar comandos aqui, {ctx.author.mention}!')


@client.command()
async def enviar(ctx, member: discord.Member, amount=None):
    if ctx.channel.id == 737996406165471273:
        await open_account(ctx.author)
        await open_account(member)

        if amount == None:
            await ctx.send("Digite a quantia a ser tranferida.")
            return

        bal = await update_bank(ctx.author)
        amount = int(amount)
        if amount > bal[1]:
            await ctx.send("Você não tem dinheiro suficiente.")
            return
        if amount < 0:
            await ctx.send("A quantia deve ser maior que 0.")
            return

        await update_bank(ctx.author, -1 * amount, "banco")
        await update_bank(member, amount, "banco")

        await ctx.send(f"{ctx.author.mention} enviou {amount} reais para {member.mention}!")
    else:
        await ctx.send(f'Você não pode usar comandos aqui, {ctx.author.mention}!')


@client.command()
@cooldown(1, 60, BucketType.user)
async def roubar(ctx, member: discord.Member, amount=None):
    if ctx.channel.id == 737996406165471273:
        await open_account(ctx.author)
        await open_account(member)

        bal = await update_bank(member)
        if bal[0] < 30:
            await ctx.send(f"A vítima tem menos que 30 reais, cria vergonha na cara {ctx.author.mention}!")
            return
        earnings = random.randrange(0, bal[0])

        await update_bank(ctx.author, earnings)
        await update_bank(member, -1 * earnings)

        await ctx.send(f"Você roubou {member} e conseguiu {earnings} reais!")
    else:
        await ctx.send(f'Você não pode usar comandos aqui, {ctx.author.mention}!')


@client.command()
@cooldown(1, 5, BucketType.user)
async def apostar(ctx, args, amount=None):
    if ctx.channel.id == 737996406165471273:
        await open_account(ctx.author)
        amount = int(amount)
        bal = await update_bank(ctx.author)
        if amount == None:
            await ctx.send("Digite a quantia a ser apostada.")
            return
        elif amount > bal[0]:
            await ctx.send(f"Você não tem dinheiro suficiente, {ctx.author.mention}.")
            return
        elif amount < 0:
            await ctx.send(f"A quantia deve ser maior que 0, {ctx.author.mention}. ")
        else:
            computador = random.choice(['Pedra', 'Papel', 'Tesoura'])
            pc = ['Pedra', 'Papel', 'Tesoura']
            if args not in pc:
                await ctx.send(f'Você não pode apostar em "{args}", tente novamente.\n'
                               f'Apostas aceitas: Pedra, Papel e Tesoura.')
            else:
                guild = ctx.guild
                emoji2 = discord.utils.get(guild.emojis, name='sim')
                emoji3 = discord.utils.get(guild.emojis, name='no')
                emoji4 = discord.utils.get(guild.emojis, name='sininho')
                aposta = discord.Embed(title=f"Aposta de {ctx.author.name} ", color=discord.Color.green())
                aposta.add_field(name="Sua escolha:", value=args)
                aposta.add_field(name="Escolha do BOT:", value=computador)
                a = await ctx.send(embed=aposta)
                await update_bank(ctx.author, -1 * amount, "carteira")
                if computador == 'Pedra':  # pc jogou pedra
                    if args == 'Pedra':
                        await ctx.send(f'{ctx.author.mention}, empatou e você recebeu seu dinheiro de volta.')
                        await update_bank(ctx.author, 1 * amount)
                        await a.add_reaction(emoji4)
                    elif args == 'Papel':
                        await ctx.send(f'{ctx.author.mention}, você ganhou e recebeu {2 * amount} reais!')
                        await update_bank(ctx.author, 2 * amount)
                        await a.add_reaction(emoji2)
                    elif args == 'Tesoura':
                        await ctx.send(f'{ctx.author.mention}, você perdeu.')
                        await a.add_reaction(emoji3)
                elif computador == 'Papel':  # pc jogou papel
                    if args == 'Pedra':
                        await ctx.send(f'{ctx.author.mention}, você perdeu.')
                        await a.add_reaction(emoji3)
                    elif args == 'Papel':
                        await ctx.send(f'{ctx.author.mention}, empatou e você recebeu seu dinheiro de volta.')
                        await update_bank(ctx.author, 1 * amount)
                        await a.add_reaction(emoji4)
                    elif args == 'Tesoura':
                        await ctx.send(f'{ctx.author.mention}, você ganhou e recebeu {2 * amount} reais!')
                        await update_bank(ctx.author, 2 * amount)
                        await a.add_reaction(emoji2)
                elif computador == 'Tesoura':  # pc jogou tesoura
                    if args == 'Pedra':
                        await ctx.send(f'{ctx.author.mention}, você ganhou e recebeu {2 * amount} reais!')
                        await update_bank(ctx.author, 2 * amount)
                        await a.add_reaction(emoji2)
                    elif args == 'Papel':
                        await ctx.send(f'{ctx.author.mention}, você perdeu.')
                        await a.add_reaction(emoji3)
                    elif args == 'Tesoura':
                        await ctx.send(f'{ctx.author.mention}, empatou e você recebeu seu dinheiro de volta.')
                        await update_bank(ctx.author, 1 * amount)
                        await a.add_reaction(emoji4)
    else:
        await ctx.send(f'Você não pode usar comandos aqui, {ctx.author.mention}!')


@client.command()
@cooldown(1, 5, BucketType.user)
async def dado(ctx, args, amount=None):
    if ctx.channel.id == 737996406165471273:
        args = int(args)
        await open_account(ctx.author)
        amount = int(amount)
        bal = await update_bank(ctx.author)
        if amount == None:
            await ctx.send("Digite a quantia a ser apostada.")
            return
        elif amount > bal[0]:
            await ctx.send(f"Você não tem dinheiro suficiente, {ctx.author.mention}.")
            return
        elif amount < 0:
            await ctx.send(f"A quantia deve ser maior que 0, {ctx.author.mention}. ")
        else:
            dado1 = randint(1, 6)
            dado2 = randint(1, 6)
            dado3 = dado1 + dado2
            await update_bank(ctx.author, -1 * amount, "carteira")
            valores = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
            if args not in valores:
                await ctx.send(f'Você não pode apostar em "{args}"!\n'
                               f'Números permitidos: 2 à 12.')
            else:
                guild = ctx.guild
                emojiyes = discord.utils.get(guild.emojis, name='sim')
                emojino = discord.utils.get(guild.emojis, name='no')
                emojidado = discord.utils.get(guild.emojis, name='dado')
                dados = discord.Embed(title=f"Lançamento de dados de {ctx.author.name} ", color=discord.Color.blue())
                dados.add_field(name="Seu número:", value=args)
                dados.add_field(name=f"{emojidado}Dado 1:", value=dado1, inline=True)
                dados.add_field(name=f"{emojidado}Dado 2:", value=dado2, inline=True)
                dados.add_field(name="Soma dos dados:", value=dado3, inline=False)
                message = await ctx.send(embed=dados)
                if args == dado3:
                    await ctx.send(f'Você acertou e ganhou {10 * amount} reais, {ctx.author.mention}!')
                    await update_bank(ctx.author, 10 * amount)
                    await message.add_reaction(emojiyes)
                else:
                    await ctx.send(f'Você errou e perdeu {amount} reais, {ctx.author.mention}!')
                    await message.add_reaction(emojino)
    else:
        await ctx.send(f'Você não pode usar comandos aqui, {ctx.author.mention}!')


@client.command()
@cooldown(1, 600, BucketType.user)
async def trabalhar(ctx):
    if ctx.channel.id == 737996406165471273:
        user = ctx.author
        await open_account(ctx.author)
        users = await get_bank_data()
        earnings = random.randrange(500, 1000)
        await ctx.send(f"Você trabalhou e conseguiu {earnings} reais, {ctx.author.mention}!")
        users[str(user.id)]["banco"] += earnings
        with open("mainbank.json", "w") as f:
            json.dump(users, f)
    else:
        await ctx.send(f'Você não pode usar comandos aqui, {ctx.author.mention}!')


@client.command()
@cooldown(1, 86400, BucketType.user)
async def recompensa(ctx):
    if ctx.channel.id == 737996406165471273:
        user = ctx.author
        await open_account(ctx.author)
        users = await get_bank_data()
        earnings = random.randrange(1000, 5000)
        await ctx.send(f"Você coletou a recompensa diária e conseguiu {earnings} reais, {ctx.author.mention}!\n"
                       f"Você poderá coletá-la de novo amanhã no mesmo horário.")
        users[str(user.id)]["banco"] += earnings
        with open("mainbank.json", "w") as f:
            json.dump(users, f)
    else:
        await ctx.send(f'Você não pode usar comandos aqui, {ctx.author.mention}!')


@client.command()
@commands.has_permissions(administrator=True)
@commands.has_role('🌐 ▸ Fundador')
async def setar(ctx, amount=None):
    amount = int(amount)
    await open_account(ctx.author)
    await update_bank(ctx.author, amount, "banco")
    await ctx.send(f"O poder divino te abençoou com {amount} reais, {ctx.author.mention}!")


@client.command()
@commands.max_concurrency(1, per=BucketType.user, wait=False)
async def cavalo(ctx, args, amount=None):
    if ctx.channel.id == 737996406165471273:
        await open_account(ctx.author)
        amount = int(amount)
        bal = await update_bank(ctx.author)
        if amount == None:
            await ctx.send("Digite a quantia a ser apostada.")
            return
        elif amount > bal[0]:
            await ctx.send(f"Você não tem dinheiro suficiente, {ctx.author.mention}.")
            return
        elif amount < 0:
            await ctx.send(f"A quantia deve ser maior que 0, {ctx.author.mention}. ")
        else:
            cavalos = random.choice(['Verde', 'Azul', 'Amarelo', 'Vermelho', 'Roxo'])
            aceitas = ['Verde', 'Azul', 'Amarelo', 'Vermelho', 'Roxo']
            if args not in aceitas:
                await ctx.send(f'Você não pode apostar no cavalo "{args}", {ctx.author.mention}!\n'
                               f'Cavalos inscritos na corrida: Verde, Azul, Amarelo, Vermelho e Roxo.')
            else:
                await ctx.send(f'A corrida já vai começar, {ctx.author.mention}...\n'
                               f'Valor apostado: {amount}')
                await update_bank(ctx.author, -1 * amount, "carteira")
                guild = ctx.guild
                emojirun = discord.utils.get(guild.emojis, name='carregando')
                emojiverde = discord.utils.get(guild.emojis, name='verde')
                emojiazul = discord.utils.get(guild.emojis, name='azul')
                emojiamarelo = discord.utils.get(guild.emojis, name='amarelo')
                emojivermelho = discord.utils.get(guild.emojis, name='vermelho')
                emojiroxo = discord.utils.get(guild.emojis, name='roxo')
                greenhorsepathstart = ('Cavalo verde começa em um ritmo lento',
                                       'Cavalo verde começa em um ritmo moderado',
                                       'Cavalo verde começa em um ritmo acelerado')
                bluehorsepathstart = ('Cavalo azul começa em um ritmo lento',
                                      'Cavalo azul começa em um ritmo moderado',
                                      'Cavalo azul começa em um ritmo acelerado')
                yellowpathstart = ('Cavalo amarelo começa em um ritmo lento',
                                   'Cavalo amarelo começa em um ritmo moderado',
                                   'Cavalo amarelo começa em um ritmo acelerado')
                redpathstart = ('Cavalo vermelho começa em um ritmo lento',
                                'Cavalo vermelho começa em um ritmo moderado',
                                'Cavalo vermelho começa em um ritmo acelerado')
                purplepathstart = ('Cavalo roxo começa em um ritmo lento',
                                   'Cavalo roxo começa em um ritmo moderado',
                                   'Cavalo roxo começa em um ritmo acelerado')

                greenpathmiddle = ('Cavalo verde está dando tudo de si',
                                   'Cavalo verde tropeça mas se levanta',
                                   'Cavalo verde segue firme para o final')
                bluepathmiddle = ('Cavalo azul está dando tudo de si',
                                  'Cavalo azul tropeça mas se levanta',
                                  'Cavalo azul segue firme para o final')
                yellowpathmiddle = ('Cavalo amarelo está dando tudo de si',
                                    'Cavalo amarelo tropeça mas se levanta',
                                    'Cavalo amarelo segue firme para o final')
                redpathmiddle = ('Cavalo vermelho está dando tudo de si',
                                 'Cavalo vermelho tropeça mas se levanta',
                                 'Cavalo vermelho segue firme para o final')
                purplepathmiddle = ('Cavalo roxo está dando tudo de si',
                                    'Cavalo roxo tropeça mas se levanta',
                                    'Cavalo roxo segue firme para o final')

                greenpathend = ('Cavalo verde corre na direção da linha de chegada',
                                'Cavalo verde está ficando para trás',
                                'Cavalo verde está exausto')
                bluepathend = ('Cavalo azul corre na direção da linha de chegada',
                               'Cavalo azul está ficando para trás',
                               'Cavalo azul está exausto')
                yellowpathend = ('Cavalo amarelo corre na direção da linha de chegada',
                                 'Cavalo amarelo está ficando para trás',
                                 'Cavalo amarelo está exausto')
                redpathend = ('Cavalo vermelho corre na direção da linha de chegada',
                              'Cavalo vermelho está ficando para trás',
                              'Cavalo vermelho está exausto')
                purplepathend = ('Cavalo roxo corre na direção da linha de chegada',
                                 'Cavalo roxo está ficando para trás',
                                 'Cavalo roxo está exausto')

                greenchoice = random.choice(greenhorsepathstart)
                bluechoice = random.choice(bluehorsepathstart)
                yellowchoice = random.choice(yellowpathstart)
                redchoice = random.choice(redpathstart)
                purplechoice = random.choice(purplepathstart)

                greenchoice1 = random.choice(greenpathmiddle)
                bluechoice1 = random.choice(bluepathmiddle)
                yellowchoice1 = random.choice(yellowpathmiddle)
                redchoice1 = random.choice(redpathmiddle)
                purplechoice1 = random.choice(purplepathmiddle)

                greenchoice2 = random.choice(greenpathend)
                bluechoice2 = random.choice(bluepathend)
                yellowchoice2 = random.choice(yellowpathend)
                redchoice2 = random.choice(redpathend)
                purplechoice2 = random.choice(purplepathend)
                time.sleep(5)
                corrida = discord.Embed(title=f"Corrida de cavalos de {ctx.author.name} ", color=discord.Color.blue())
                corrida.add_field(name=f"{emojiverde} Cavalo verde:", value=greenchoice, inline=False)
                corrida.add_field(name=f"{emojiazul} Cavalo azul:", value=bluechoice, inline=False)
                corrida.add_field(name=f"{emojiamarelo} Cavalo amarelo:", value=yellowchoice, inline=False)
                corrida.add_field(name=f"{emojivermelho} Cavalo vermelho:", value=redchoice, inline=False)
                corrida.add_field(name=f"{emojiroxo} Cavalo roxo:", value=purplechoice, inline=False)
                corrida.add_field(name='⠀', value='⠀', inline=False)
                corrida.add_field(name=f'{emojirun} Corrida em progresso', value='Aguarde o desfecho da corrida⠀')
                await ctx.send(embed=corrida)
                time.sleep(5)
                corrida1 = discord.Embed(title=f"Corrida de cavalos de {ctx.author.name} ", color=discord.Color.blue())
                corrida1.add_field(name=f"{emojiverde} Cavalo verde:", value=greenchoice1, inline=False)
                corrida1.add_field(name=f"{emojiazul} Cavalo azul:", value=bluechoice1, inline=False)
                corrida1.add_field(name=f"{emojiamarelo} Cavalo amarelo:", value=yellowchoice1, inline=False)
                corrida1.add_field(name=f"{emojivermelho} Cavalo vermelho:", value=redchoice1, inline=False)
                corrida1.add_field(name=f"{emojiroxo} Cavalo roxo:", value=purplechoice1, inline=False)
                corrida1.add_field(name='⠀', value='⠀', inline=False)
                corrida1.add_field(name=f'{emojirun} Corrida em progresso', value='Aguarde o desfecho da corrida⠀')
                await ctx.send(embed=corrida1)
                time.sleep(5)
                corrida2 = discord.Embed(title=f"Corrida de cavalos de {ctx.author.name} ", color=discord.Color.blue())
                corrida2.add_field(name=f"{emojiverde} Cavalo verde:", value=greenchoice2, inline=False)
                corrida2.add_field(name=f"{emojiazul} Cavalo azul:", value=bluechoice2, inline=False)
                corrida2.add_field(name=f"{emojiamarelo} Cavalo amarelo:", value=yellowchoice2, inline=False)
                corrida2.add_field(name=f"{emojivermelho} Cavalo vermelho:", value=redchoice2, inline=False)
                corrida2.add_field(name=f"{emojiroxo} Cavalo roxo:", value=purplechoice2, inline=False)
                corrida2.add_field(name='⠀', value='⠀', inline=False)
                corrida2.add_field(name=f'{emojirun} Momentos finais da corrida',
                                   value='Vencedor irá ser anunciado em poucos segundos⠀')
                await ctx.send(embed=corrida2)
                time.sleep(5)
                corrida3 = discord.Embed(title=f"Corrida de cavalos de {ctx.author.name} ", color=discord.Color.blue())
                if cavalos == 'Verde':
                    corrida3.add_field(name=f"{emojiverde} Cavalo vencedor:", value=cavalos, inline=False)
                    await ctx.send(embed=corrida3)
                elif cavalos == 'Azul':
                    corrida3.add_field(name=f"{emojiazul} Cavalo vencedor:", value=cavalos, inline=False)
                    await ctx.send(embed=corrida3)
                elif cavalos == 'Amarelo':
                    corrida3.add_field(name=f"{emojiamarelo} Cavalo vencedor:", value=cavalos, inline=False)
                    await ctx.send(embed=corrida3)
                elif cavalos == 'Vermelho':
                    corrida3.add_field(name=f"{emojivermelho} Cavalo vencedor:", value=cavalos, inline=False)
                    await ctx.send(embed=corrida3)
                elif cavalos == 'Roxo':
                    corrida3.add_field(name=f"{emojiroxo} Cavalo vencedor:", value=cavalos, inline=False)
                    await ctx.send(embed=corrida3)
                if args == cavalos:
                    await ctx.send(f'Seu cavalo foi o vencedor e você ganhou {8 * amount} reais, {ctx.author.mention}!')
                    await update_bank(ctx.author, 8 * amount)
                else:
                    await ctx.send(f'Seu cavalo perdeu a corrida e você perdeu seu dinheiro, {ctx.author.mention}!')
    else:
        await ctx.send(f'Você não pode usar comandos aqui, {ctx.author.mention}!')


@client.command()
@cooldown(1, 5, BucketType.user)
async def cassino(ctx, amount=None):
    if ctx.channel.id == 737996406165471273:
        await open_account(ctx.author)
        amount = int(amount)
        bal = await update_bank(ctx.author)
        if amount == None:
            await ctx.send("Digite a quantia a ser apostada.")
            return
        elif amount > bal[0]:
            await ctx.send(f"Você não tem dinheiro suficiente, {ctx.author.mention}.")
            return
        elif amount < 0:
            await ctx.send(f"A quantia deve ser maior que 0, {ctx.author.mention}. ")
        else:
            await update_bank(ctx.author, -1 * amount, "carteira")
            guild = ctx.guild
            emoji = discord.utils.get(guild.emojis, name='lemon')
            emoji2 = discord.utils.get(guild.emojis, name='strawberry')
            emoji3 = discord.utils.get(guild.emojis, name='apple')
            lemon = (':lemon:')
            morango = (':strawberry:')
            apple = (':apple:')
            opções = (lemon, morango, apple)
            opt0 = random.choice(opções)
            opt1 = random.choice(opções)
            opt2 = random.choice(opções)
            ganhar = (':lemon:', ':lemon:', ':lemon:')
            ganhar2 = (':strawberry:', ':strawberry:', ':strawberry:')
            ganhar3 = (':apple:', ':apple:', ':apple:')
            jackpot = opt0 + opt1 + opt2
            aposta = discord.Embed(title=f"Caça-Níqueis de {ctx.author.name} ", color=discord.Color.green())
            aposta.add_field(name="Dinheiro apostado:", value=(f'{amount} reais.'))
            aposta.add_field(name="Jackpot:", value=(f'{50 * amount} reais.'), inline=True)
            aposta.add_field(name="⠀", value='⠀')
            aposta.add_field(name='Caça-Níquel caiu em:', value=jackpot)
            await ctx.send(embed=aposta)
            if jackpot == ':lemon::lemon::lemon:':
                await update_bank(ctx.author, 50 * amount)
                await ctx.send(f'Você ganhou, {ctx.author.mention}!\n'
                               f'Dinheiro ganho: {50 * amount}')
            elif jackpot == ':strawberry::strawberry::strawberry:':
                await update_bank(ctx.author, 50 * amount)
                await ctx.send(f'Você ganhou, {ctx.author.mention}!\n'
                               f'Dinheiro ganho: {50 * amount}')
            elif jackpot == ':apple::apple::apple:':
                await update_bank(ctx.author, 50 * amount)
                await ctx.send(f'Você ganhou, {ctx.author.mention}!\n'
                               f'Dinheiro ganho: {50 * amount}')
            else:
                await ctx.send(f'Você perdeu, {ctx.author.mention}!')
    else:
        await ctx.send(f'Você não pode usar comandos aqui, {ctx.author.mention}!')


async def open_account(user):
    users = await get_bank_data()
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["carteira"] = 0
        users[str(user.id)]["banco"] = 0
    with open("mainbank.json", "w") as f:
        json.dump(users, f)
    return True


async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f)
    return users


async def update_bank(user, change=0, mode="carteira"):
    users = await get_bank_data()
    users[str(user.id)][mode] += change
    with open("mainbank.json", "w") as f:
        json.dump(users, f)
    bal = [users[str(user.id)]["carteira"], users[str(user.id)]["banco"]]
    return bal


@client.event
async def on_member_join(member=discord.Member):
    role = discord.utils.get(member.guild.roles, name="🔅 ▸ Membro")
    await member.add_roles(role)
    channel = client.get_channel(id=742424758993551393)
    embed = discord.Embed(title=f"{member.name} entrou no servidor!",
                          description="Seja bem-vindo e fique atento nas regras para evitar constrangimentos futuros.",
                          color=discord.Color.blue())
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_author(name="Suporte - Vinicius ASMR",
                     url="https://www.youtube.com/c/ViniciusASMR1",
                     icon_url="https://cdn.discordapp.com/attachments/737407456006897716/737460313221234758/unnamed.jpg")
    embed.timestamp = datetime.datetime.utcnow()
    msgs = ['Obrigado por entrar!', 'Você é especial <3', 'Boa estadia :)', 'Se comporte...', 'Leia as regras ;)']
    escolha = random.choice(msgs)
    embed.set_footer(text=f"{escolha}")
    await channel.send(content=None, embed=embed)

client.run('SEU TOKEN')
