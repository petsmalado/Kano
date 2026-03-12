import discord
from discord.ext import commands
import openai
import random
import json
import os

# ==============================
# CONFIGURAÇÃO
# ==============================

TOKEN = os.getenv("TOKEN")        # Vai pegar automaticamente a variável do Windows
OPENAI_KEY = os.getenv("OPENAI_KEY")
openai.api_key = OPENAI_KEY

ARQUIVO_DICIONARIO = "dicionario.json"

SUFIXOS = ["enguers", "toleite", "zitos", "vers", "is"]

# ==============================
# SETUP DISCORD
# ==============================

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ==============================
# FUNÇÕES DO DICIONÁRIO
# ==============================

def carregar_girias():
    if not os.path.exists(ARQUIVO_DICIONARIO):
        with open(ARQUIVO_DICIONARIO, "w") as f:
            json.dump({"girias": [
                "malado",
                "pandemonico",
                "gigantoresco",
                "com os pau duro",
                "zé",
                "meu teus"
            ]}, f, indent=4)
    with open(ARQUIVO_DICIONARIO, "r") as f:
        data = json.load(f)
        return data["girias"]

def salvar_girias(girias):
    with open(ARQUIVO_DICIONARIO, "w") as f:
        json.dump({"girias": girias}, f, indent=4)

# ==============================
# MUTADOR DE PALAVRAS
# ==============================

def mutar_palavra(palavra):
    sufixo = random.choice(SUFIXOS)
    if sufixo == "is":
        return f"is{palavra}guers"
    return f"{palavra}{sufixo}"

# ==============================
# EVENTO ON READY
# ==============================

@bot.event
async def on_ready():
    print(f"🔥 Bot conectado como {bot.user}")

# ==============================
# COMANDO DICIONÁRIO
# ==============================

@bot.group(invoke_without_command=True)
async def dicionario(ctx):
    girias = carregar_girias()
    if not girias:
        await ctx.send("📚 O dicionário está vazio, zé.")
        return
    texto = "📚 **Dicionário Oficial Pandemônico:**\n\n"
    for palavra in girias:
        texto += f"- {palavra}\n"
    await ctx.send(texto)

@dicionario.command(name="add")
async def adicionar_giria(ctx, *, nova_giria):
    girias = carregar_girias()
    if nova_giria in girias:
        await ctx.send("⚠️ Essa gíria já existe, meu teus.")
        return
    girias.append(nova_giria)
    salvar_girias(girias)
    await ctx.send(f"🔥 '{nova_giria}' adicionada ao dicionário malado!")

# ==============================
# COMANDO LENDA
# ==============================

@bot.command()
async def lenda(ctx, membro: discord.Member):

    await ctx.send("🎸 Invocando a lenda guitarrística...")

    girias = carregar_girias()
    if not girias:
        await ctx.send("O dicionário está vazio, impossível invocar a lenda.")
        return

    guitarra = mutar_palavra("guitarra")
    solo = mutar_palavra("solo")
    riff = mutar_palavra("riff")
    mangusto = mutar_palavra("mangusto")

    giria1 = random.choice(girias)
    giria2 = random.choice(girias)

    prompt = f"""
Crie uma história para um guitarrista contando das suas origens de forma engraçada e usando muito os sufixos enguers, toleite, zitos, vers, is.

O protagonista é {membro.display_name}.

A história deve:
- Ser muito engraçada
- Parecer uma lenda contada entre amigos
- Envolver guitarristas como seres superiores e situações envolvendo membros de bandas de metal progressivo como se fossem amigos deles, membros de bandas como polyphia, periphery, plini e outras dessa bolha.

Use obrigatoriamente:
{guitarra}
{solo}
{riff}
{mangusto}
{giria1}
{giria2}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um narrador insano de lendas guitarrísticas."},
                {"role": "user", "content": prompt}
            ]
        )

        historia = response["choices"][0]["message"]["content"]

        # Discord limita 2000 caracteres
        if len(historia) > 1900:
            for i in range(0, len(historia), 1900):
                await ctx.send(historia[i:i+1900])
        else:
            await ctx.send(historia)

    except Exception as e:
        await ctx.send("⚠️ Erro ao invocar entidade pandemônica.")
        print("Erro OpenAI:", e)

# ==============================
# RODAR BOT
# ==============================

bot.run(TOKEN)
