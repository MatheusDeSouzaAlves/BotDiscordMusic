# ==============================================================
# PASSOS PARA CONFIGURAR O AMBIENTE DE DESENVOLVIMENTO:
# ==============================================================
# 1. INSTALAR O PYTHON:
#    - Certifique-se de que o Python 3.8 ou superior está instalado.
#    - Baixe o Python em: https://www.python.org/downloads/
#    - Ao instalar, marque a opção "Add Python to PATH" para facilitar a execução no terminal.

# 2. INSTALAR O DISCORD.PY:
#    - No terminal, instale a biblioteca discord.py usando o pip:
#      pip install discord.py

# 3. INSTALAR O YOUTUBE-DL OU YT-DLP:
#    - Para baixar músicas do YouTube, é necessário o yt-dlp (uma versão mais moderna e ativa do youtube-dl).
#    - Instale o yt-dlp via pip:
#      pip install yt-dlp
#    - Certifique-se de que o yt-dlp está acessível no PATH do sistema.

# 4. INSTALAR O FFmpeg:
#    - O FFmpeg é necessário para processar o áudio das músicas.
#    - Baixe o FFmpeg em: https://github.com/BtbN/FFmpeg-Builds/releases
#    - Após o download, extraia a pasta e adicione o diretório "bin" do FFmpeg ao PATH do sistema.
#    - Ou coloque na pasta Documentos (USADO NESSE CÒDIGO, UTILIZE DESSA FORMA)
#      Para isso, no Windows, você pode adicionar o caminho "C:/ffmpeg/bin" (exemplo) no "Variáveis de Ambiente".

# 5. CONFIGURAR O TOKEN DO BOT:
#    - Acesse o portal de desenvolvedores do Discord em: https://discord.com/developers/applications
#    - Crie uma nova aplicação e gere o TOKEN do BOT.
#    - Armazene esse TOKEN de maneira segura. Ele será usado no código para autenticar o bot.
#    - Use o seguinte formato no seu código:
#      bot.run('SEU_TOKEN_AQUI')

# 6. VARIÁVEIS DE AMBIENTE (opcional, mas recomendado):
#    - Caso queira manter o TOKEN do bot e outras informações sensíveis fora do código, você pode usar um arquivo `.env`.
#    - Exemplo de um arquivo `.env`:
#      TOKEN=seu_token_aqui
#    - Use a biblioteca `python-dotenv` para carregar o arquivo `.env` no seu código:
#      pip install python-dotenv
#    - No código, carregue as variáveis de ambiente:
#      from dotenv import load_dotenv
#      load_dotenv()
#      token = os.getenv('TOKEN')

# 7. CONFIGURAÇÃO DO AMBIENTE DE DESENVOLVIMENTO (IDE):
#    - Certifique-se de estar usando uma IDE ou editor de texto que suporte Python, como VSCode, PyCharm ou Sublime Text.
#    - Verifique se o Python está configurado corretamente no seu editor de código.

# 8. INICIAR O BOT:
#    - Após configurar tudo, no terminal, navegue até o diretório do código e execute:
#      python nome_do_arquivo.py
# ==============================================================


import discord
from discord.ui import Button, View
from discord.ext import commands

# Usando yt-dlp em vez de youtube_dl para o download de vídeos
import yt_dlp as youtube_dl
import os


musicQueue = []

# Caminho do FFmpeg para executar o comando de áudio no Discord
FFMPEG_PATH = '{caminho do arquivo ffmpeg}'

# Criação dos "intents" necessários para o bot interagir com o Discord
intents = discord.Intents.all()

# Criação do objeto 'bot' com o prefixo "!" para comandos e 'intents' configurados
bot = commands.Bot(command_prefix="1", intents=intents)

# Evento que ocorre quando o bot está pronto e logado no Discord


@bot.event
async def on_ready():
    # Imprime no console quando o bot estiver online
    print(f"Logado como {bot.user}!")

# Comando que faz o bot entrar no canal de voz onde o usuário está


@bot.command(aliases=['entrar', 'Join', 'j'])
async def join(ctx):
    # Verifica se o autor do comando está em um canal de voz
    if ctx.author.voice:
        # Se estiver, o bot entra no canal de voz do usuário
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        # Se o autor não estiver em um canal de voz, o bot envia uma mensagem dizendo que precisa estar em um canal de voz
        await ctx.send(f"### {ctx.author.mention} como vou entrar se tu não tá em nenhum canal, fera?")

# Comando que faz o bot sair do canal de voz


@bot.command(aliases=['Leave', 'quit', 'sair', 'q', 'l'])
async def leave(ctx):
    # Verifica se o bot está em um canal de voz
    if ctx.voice_client:
        # Se estiver, ele desconecta do canal de voz
        await ctx.voice_client.disconnect()
    else:
        # Se o bot não estiver em um canal de voz, envia uma mensagem avisando
        await ctx.send(f"### {ctx.author.mention} vou sair de onde? Não tô em nenhum canal brother")

# Comando que faz o bot tocar música de um link do YouTube


@bot.command(aliases=['Play', 'p', 'tocar'])
async def play(ctx, *, song_name=None):

    if not song_name or song_name == '':
        await ctx.send(f"### {ctx.author.mention} é pra tocar o que irmão? Tu nem digitou nada")
        return

    # Verifica se o bot já está em um canal de voz
    if not ctx.voice_client:
        if ctx.author.voice:
            # Se o bot não está em um canal de voz, entra no canal de voz do usuário
            channel = ctx.author.voice.channel
            await channel.connect()
        else:
            # Se o autor não estiver em um canal de voz, envia mensagem
            await ctx.send(f"### {ctx.author.mention} como vou entrar se tu não tá em nenhum canal, fera?")
            return  # Finaliza o comando aqui caso o usuário não esteja em um canal de voz

    # O bot está no canal de voz, então pode continuar a reprodução da música
    ctx.voice_client.stop()  # Para qualquer áudio em execução

    # Especifica opções para o FFmpeg, como reconectar em caso de falha de stream
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn'  # Não inclui o vídeo no stream
    }

    # Opções para o yt-dlp, especificando que queremos a melhor qualidade de áudio disponível
    YDL_OPTIONS = {'format': 'bestaudio'}

    # Tentando buscar pelo nome da música no YouTube se não for uma URL direta
    search_url = f"ytsearch:{song_name}"  # Cria uma URL de busca no YouTube

    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        # Extrai as informações do primeiro vídeo encontrado
        info = ydl.extract_info(search_url, download=False)
        if 'entries' in info:
            video = info['entries'][0]  # Pega o primeiro resultado da busca
            url2 = video['url']  # Pega a URL do áudio

            global title
            global uploader

            # Pega o título do vídeo ou fallback para a URL se não encontrar um título válido
            title = video.get('title', 'Título não disponível')
            uploader = video.get('uploader', 'Canal desconhecido')
            thumb = video.get('thumbnail')
            duration = video.get('duration')
            # Pegando a letra da música

            minutosDivision = duration / 60
            minutosInteiros = int(minutosDivision)  # Parte inteira (minutos)
            # Parte decimal convertida para segundos
            segundosInteiros = round((minutosDivision - minutosInteiros) * 60)

            # Formata para garantir que os segundos tenham 2 casas decimais, se necessário
            minutosResult = "{:02d}:{:02d}".format(
                minutosInteiros, segundosInteiros)

            # Se o título for uma URL, faça algo para verificar
            if title.startswith("http"):
                title = "Música desconhecida"

            # Criando o embed com as informações do vídeo
            embed = discord.Embed(
                title=title,
                description=f"{uploader}\n\n ⏳ {minutosResult}\n\n Tá na mão chefe(▀̿Ĺ̯▀̿ ̿)",
                color=discord.Color.blue()  # Cor opcional
            )


            ############# CRIANDO BOTAO PARA ALGUMA FUNÇÃO ####################
            # # Criando um botão
            # botao = Button(
            #     label='Clique aqui', style=discord.ButtonStyle.primary, custom_id='mostrar_letra')

            # # Criando uma View para o botão (necessário para o Discord interativo)
            # view = discord.ui.View()
            # view.add_item(botao)  # Adiciona o botão à View
            

            # Rodapé do Embed com o nome e a foto do autor
            embed.set_footer(
                text=f"by {ctx.author.display_name}", icon_url=ctx.author.avatar.url)

            # Imagem do Embed
            embed.set_image(url=thumb)

            # Envia o embed com a imagem, informações e o botão ( se existir botao, descomente)
            await ctx.send(embed=embed
                        #    , view=view
                           )

            # O bot começa a tocar o áudio no canal de voz
            ctx.voice_client.play(discord.FFmpegPCMAudio(
                url2, executable=FFMPEG_PATH, **FFMPEG_OPTIONS))

        else:
            await ctx.send("### achei nada com esse nome brother")


# @bot.event
# async def on_interaction(interaction):
#     # Verifica se o botão pressionado foi o de mostrar a letra
#     if interaction.type == discord.InteractionType.component:
#         if interaction.data['custom_id'] == 'mostrar_letra':
#             # Gerar o link direto para a página da letra da música
#             link_lyrics = f"https://www.letras.mus.br/{uploader.replace(' ', '-').lower()}/{
#                 title.replace(' ', '-').lower()}/"
#             embed = discord.Embed(
#                 title="Letra da música",
#                 description=f"Você pode ver a letra completa [aqui]({
#                     link_lyrics})",
#                 color=discord.Color.green()
#             # ephemeral=True define a mensagem visível somente para quem solicitou
#             await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.command(aliases=['Playq', 'pq', 'fila', 'playq'])
async def playqueue(ctx, *, song_name=None):

    # Verificação se o usuário digitou o nome da música
    # descomente pra ver um bglh doido
    if not song_name or song_name == '':
        await ctx.send(f"### {ctx.author.mention} é pra tocar o quê? Tu nem digitou nada...")
        return

    # Verifica se o bot já está em um canal de voz
    if not ctx.voice_client:
        if ctx.author.voice:
            # Se o bot não está em um canal de voz, entra no canal de voz do usuário
            channel = ctx.author.voice.channel
            await channel.connect()
        else:
            # Se o autor não estiver em um canal de voz, envia mensagem
            await ctx.send(f"### {ctx.author.mention} como vou entrar se tu não tá em nenhum canal, fera?")
            return  # Finaliza o comando aqui caso o usuário não esteja em um canal de voz

    # Especifica opções para o FFmpeg, como reconectar em caso de falha de stream
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn'  # Não inclui o vídeo no stream
    }

    # Opções para o yt-dlp, especificando que queremos a melhor qualidade de áudio disponível
    YDL_OPTIONS = {'format': 'bestaudio'}

    # Tentando buscar pelo nome da música no YouTube se não for uma URL direta
    search_url = f"ytsearch:{song_name}"  # Cria uma URL de busca no YouTube

    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        # Extrai as informações do primeiro vídeo encontrado
        info = ydl.extract_info(search_url, download=False)
        if 'entries' in info:
            video = info['entries'][0]  # Pega o primeiro resultado da busca
            url2 = video['url']  # Pega a URL do áudio

            # Pega o título do vídeo ou fallback para a URL se não encontrar um título válido
            title = video.get('title', 'Título não disponível')
            uploader = video.get('uploader', 'Canal desconhecido')

            # Se o título for uma URL, faça algo para verificar
            if title.startswith("http"):
                title = "Música desconhecida"


############ CONFIGURAÇÕES DE FILA #################

            # Adiciona a música à fila
            musicQueue.append(url2)

            # Se não estiver tocando nada, começa a tocar a música da fila
            if not ctx.voice_client.is_playing():
                await playNext(ctx)
            else:
                # Se estiver tocando, adiciona à fila
                await ctx.send(f"### {ctx.author.mention} adicionado na fila, mestre🤠 \n## {title}\n### {uploader}")

        else:
            await ctx.send(f"###  {ctx.author.mention} achei nada com esse nome chefia")


@bot.command(aliases=['next', 'playnext', 'proxima'])
async def playNextMusic(ctx, *, song_name=None):
    playNext(ctx)


# Função para tocar a próxima música na fila
async def playNext(ctx):
    if not ctx.voice_client:
        await ctx.send("### Não estou em um canal de voz!")
        return

    if musicQueue:
        url = musicQueue.pop(0)
        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
        ctx.voice_client.play(discord.FFmpegPCMAudio(
            url, executable=FFMPEG_PATH, **FFMPEG_OPTIONS), after=lambda e: afterSong(ctx, e))
        await ctx.send(f"### Agora tocando: {url}")
    else:
        await ctx.send("### Não há músicas na fila! Adicione algumas e eu toco!")


# Função chamada quando a música termina de tocar
async def afterSong(ctx, error):
    if error:
        print(f"Erro ao tocar a música: {error}")
    # Depois que a música termina, tenta tocar a próxima
    if musicQueue:
        bot.loop.create_task(playNext(ctx))
    else:
        await ctx.send(f"### Fim da lista de reprodução 👌")


@bot.command(aliases=['Stop', 's', 'parar'])
async def stop(ctx):
 # Verifica se o bot já está em um canal de voz
    if ctx.voice_client:
        # Se o bot já estiver tocando música, para a música atual
        ctx.voice_client.stop()
        await ctx.send(f"### {ctx.author.mention} cê que manda, parei a música🤝")


@bot.command(aliases=['Pause', 'pausar'])
async def pause(ctx):
 # Verifica se o bot já está em um canal de voz
    if ctx.voice_client:
        # Se o bot já estiver tocando música, pausa a música atual
        ctx.voice_client.pause()
        await ctx.send(f"### {ctx.author.mention} música pausada ¬_¬")


@bot.command(aliases=['Resume', 'retomar'])
async def resume(ctx):
 # Verifica se o bot já está em um canal de voz
    if ctx.voice_client:
        # Se o bot já estiver tocando música, pausa a música atual
        ctx.voice_client.resume()
        await ctx.send(f"### {ctx.author.mention} música retomada💃🕺")


# O bot é iniciado com o token de autenticação 
# Substitua 'SEU_TOKEN_AQUI' pelo token real do seu bot
bot.run("SEU_TOKEN_AQUI")
