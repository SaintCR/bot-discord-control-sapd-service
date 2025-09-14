import discord
from discord.ext import commands
from datetime import datetime

from config import TOKEN, COMMAND_PREFIX, CANAL_SERVICIO, ROL_SERVICIO
from data_manager import cargar_servicios, guardar_servicios

# ---------------- BOT SETUP ----------------
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

# ---------------- DATOS ----------------
servicios = cargar_servicios()

# ---------------- EVENTOS ----------------
@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

# ---------------- COMANDO ----------------
@bot.command()
async def servicio(ctx):
    if CANAL_SERVICIO and ctx.channel.id != CANAL_SERVICIO:
        return

    usuario_id = str(ctx.author.id)
    usuario_nombre = ctx.author.display_name
    miembro = ctx.author
    rol = discord.utils.get(ctx.guild.roles, name=ROL_SERVICIO)

    if not rol:
        return await ctx.send("⚠️ No encontré el rol **En Servicio**, créalo primero en tu servidor.")

    if usuario_id not in servicios:
        # Guardar inicio
        servicios[usuario_id] = datetime.now().isoformat()
        guardar_servicios(servicios)

        await miembro.add_roles(rol)

        embed = discord.Embed(
            title="🚨 Inicio de Servicio",
            description=f"👮 **{usuario_nombre}** se ha colocado en **Servicio SAPD**.",
            color=0x2ecc71
        )
        embed.set_footer(text="Sistema de Control SAPD")
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)

    else:
        # Calcular duración
        inicio = datetime.fromisoformat(servicios.pop(usuario_id))
        fin = datetime.now()
        guardar_servicios(servicios)

        duracion = fin - inicio
        horas, resto = divmod(duracion.seconds, 3600)
        minutos, segundos = divmod(resto, 60)
        tiempo_str = f"{horas}h {minutos}m {segundos}s"

        await miembro.remove_roles(rol)

        embed = discord.Embed(
            title="✅ Fin de Servicio",
            description=f"👮 **{usuario_nombre}** finalizó su **Servicio SAPD**.\n⏳ Tiempo en servicio: **{tiempo_str}**",
            color=0xe74c3c
        )
        embed.set_footer(text="Sistema de Control SAPD")
        embed.timestamp = datetime.now()
        await ctx.send(embed=embed)

# ---------------- RUN BOT ----------------
if __name__ == "__main__":
    bot.run(TOKEN)
