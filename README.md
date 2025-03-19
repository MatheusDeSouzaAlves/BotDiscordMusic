# BotDiscordMusic
### Meu BOT autoral de Discord que reproduz músicas
Video de Demonstração: https://youtu.be/K9_8XxPgE20

## Contexto
 É comum que existam vários bots no Discord que reproduzem músicas, resolvi criar o meu próprio por hobby utlizando Python.

## Como funciona?
 O usuário digita o comando "1play {nome da música}", o Bot pesquisa o texto no youtube e acessa o conteúdo do vídeo mais provável, baixa temporariamente o áudio e reproduz no canal que o usuário está ativo. Após a reprodução, o áudio não fica salvo e não ocupa espaço no armazenamento do usuário

## Outros comandos
`1stop - Para a música`

`1pause - Pausa a música`

`1resume - Retoma a música`

`1playq - Adiciona a música na fila`

`1next - Passa para a próxima música na fila`
## GUIA PARA CRIAR O SEU BOT NO DISCORD (Também presente no código)

Configuração do Ambiente de Desenvolvimento

1. Instalar o Python

Certifique-se de que o Python 3.8 ou superior está instalado.

Baixe o Python em: https://www.python.org/downloads/


2. Instalar o Discord.py

No terminal, instale a biblioteca discord.py usando o pip:

`pip install discord.py`

3. Instalar o YouTube-DL ou YT-DLP

Para baixar músicas do YouTube, instale o yt-dlp (versão mais moderna do youtube-dl):

`pip install yt-dlp`

Certifique-se de que o yt-dlp está acessível no PATH do sistema.

4. Instalar o FFmpeg

O FFmpeg é necessário para processar áudio.

Baixe em: https://github.com/BtbN/FFmpeg-Builds/releases

Extraia a pasta e adicione o diretório bin do FFmpeg ao PATH do sistema.

Alternativamente, coloque a pasta na pasta Documentos (método recomendado para este código).

5. Configurar o Token do Bot

Acesse o portal de desenvolvedores do Discord: https://discord.com/developers/applications

Crie uma nova aplicação e gere o TOKEN do bot.

Armazene o TOKEN de forma segura.

No código, utilize:

bot.run('SEU_TOKEN_AQUI')

6. Configurar Variáveis de Ambiente (Opcional, mas Recomendado)

Para manter o TOKEN e outras informações sensíveis fora do código, use um arquivo .env.

Criar o arquivo .env

Crie um arquivo .env no diretório do projeto e adicione:

TOKEN=seu_token_aqui

Instalar e carregar as variáveis no Python

Instale a biblioteca python-dotenv:

`pip install python-dotenv`

No código Python, carregue as variáveis do .env:

`from dotenv import load_dotenv`
`import os`

`load_dotenv()`
`token = os.getenv('TOKEN')`

7. Configuração da IDE

Utilize uma IDE que suporte Python, como VSCode, PyCharm ou Sublime Text.
Certifique-se de que o Python está configurado corretamente na IDE.

8. Iniciar o Bot

Após configurar tudo, execute o bot no terminal:
