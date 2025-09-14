import discord
from discord.ext import commands, tasks
from datetime import datetime
from threading import Thread
from flask import Flask

from config import TOKEN, COMMAND_PREFIX, CANAL_SERVICIO, ROL_SERVICIO, CANAL_TOP_DOMINGO
from data_manager import cargar_servicios, guardar_servicios, agregar_historial

# ---------------- BOT SETUP ----------------
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
bot = commands.Bot(
    command_prefix=COMMAND_PREFIX,
    intents=intents,
    case_insensitive=True
)

# ---------------- DATOS ----------------
servicios = cargar_servicios()

# ---------------- MINI WEBSERVER PARA 24/7 ----------------
app = Flask("")

@app.route("/")
def home():
    return "Bot SAPD activo!"

def run_webserver():
    app.run(host="0.0.0.0", port=8080)

Thread(target=run_webserver).start()

# ---------------- EVENTOS ----------------
@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")
    top_semanal.start()

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

    if usuario_id not in servicios or isinstance(servicios[usuario_id], list):
        servicios[usuario_id] = datetime.now().isoformat()
        guardar_servicios(servicios)
        await miembro.add_roles(rol)
        embed = discord.Embed(
            title="🚨 Inicio de Servicio",
            description=f"👮 **{usuario_nombre}** se ha colocado en **Servicio SAPD**.",
            color=0x2ecc71,
            timestamp=datetime.now()
        )
        embed.set_footer(text="Sistema de Control SAPD")
        await ctx.send(embed=embed)
    else:
        inicio = datetime.fromisoformat(servicios.pop(usuario_id))
        fin = datetime.now()
        duracion = fin - inicio
        segundos_totales = int(duracion.total_seconds())
        agregar_historial(servicios, usuario_id, segundos_totales)
        await miembro.remove_roles(rol)
        horas, resto = divmod(segundos_totales, 3600)
        minutos, segundos = divmod(resto, 60)
        tiempo_str = f"{horas}h {minutos}m {segundos}s"
        embed = discord.Embed(
            title="✅ Fin de Servicio",
            description=f"👮 **{usuario_nombre}** finalizó su **Servicio SAPD**.\n⏳ Tiempo en servicio: **{tiempo_str}**",
            color=0xe74c3c,
            timestamp=datetime.now()
        )
        embed.set_footer(text="Sistema de Control SAPD")
        await ctx.send(embed=embed)

# ---------------- LOOP TOP SEMANAL ----------------
@tasks.loop(minutes=1)
async def top_semanal():
    now = datetime.now()
    # Domingo a las 10:30 (ajusta hora/minuto a tu preferencia)
    if now.weekday() == 6 and now.hour == 10 and now.minute == 30:
        for guild in bot.guilds:
            canal = bot.get_channel(CANAL_TOP_DOMINGO)
            if not canal:
                print(f"❌ Canal del top semanal no encontrado. ID usado: {CANAL_TOP_DOMINGO}")
                continue
            print(f"✅ Publicando Top Semanal en el canal: {canal}")

            servicios_actuales = cargar_servicios()
            totales = {}
            roles_ignorar = ["Bot's", "Koya", "Pancake", "Control-SAPD", "ProBot ✨"]

            for miembro in guild.members:
                if any(discord.utils.get(miembro.roles, name=r) for r in roles_ignorar):
                    continue
                usuario_nombre = miembro.display_name
                user_id = str(miembro.id)
                if user_id in servicios_actuales:
                    datos = servicios_actuales[user_id]
                    if isinstance(datos, list):
                        total_segundos = sum(datos)
                    else:
                        inicio = datetime.fromisoformat(datos)
                        total_segundos = int((datetime.now() - inicio).total_seconds())
                else:
                    total_segundos = 0
                totales[usuario_nombre] = total_segundos

            top_usuarios = sorted(totales.items(), key=lambda x: x[1], reverse=True)
            embed = discord.Embed(
                title="🏆 Top Semanal de Servicio SAPD",
                description="Ranking de usuarios por tiempo total en servicio",
                color=0x3498db,
                timestamp=datetime.now()
            )
            for i, (usuario_nombre, segundos) in enumerate(top_usuarios, start=1):
                horas, resto = divmod(segundos, 3600)
                minutos, s = divmod(resto, 60)
                tiempo_str = f"{int(horas)}h {int(minutos)}m {int(s)}s"
                embed.add_field(name=f"{i}. {usuario_nombre}", value=tiempo_str, inline=False)

            await canal.send(embed=embed)
            print("✅ Top semanal publicado con éxito.")

# ---------------- RUN BOT ----------------
if __name__ == "__main__":
    bot.run(TOKEN)
