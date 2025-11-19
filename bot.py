#Create by Jxdn
import discord, random
from discord.ext import commands
from discord import ui
from discord.ui import button
from handle.mysql import *

try:
  with open('config.json', 'r') as file:
    config = json.load(file)
except FileNotFoundError:
  config = {}
  
#------------------------------#
TOKEN = config['TOKEN']
PREFIX = config['PREFIX']
NAME = config['TAG']
ROLE_ID = config['ROLE_ID']
THUMBNAIL = config['THUMBNAIL']
IMAGE = config['IMAGE']
ICON = config['ICON']
KARCIS = config['KARCIS_IMAGE']
WARNA = 0x00F3FF
#------------------------------#

intents = discord.Intents().all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents)
    
@bot.event
async def on_ready():
    bot.add_view(Buttons())
    await bot.tree.sync()
    await bot.change_presence(activity=discord.Game("Testing"))
    print(f'Bot Online Logged in as {bot.user.name}')
    is_connected = check_mysql_connection()
    if is_connected:
      print("MySQL has successfully connected")
    else:
      print("Mysql Tidak Connect")

def randomOTP():
    otp = random.randint(100000, 999999)
    return otp

class YesOrNo(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
    
  @button(label="Yes", custom_id="lupa_sandi_yes", style=discord.ButtonStyle.green)
  async def yes_button(self, interaction: discord.Interaction, button: discord.ui.Button):
    try:
      user_id = interaction.user.id
      new_password = ""
      old_pin, new_pin = reset_password(user_id, new_password)
      user_ucp = check_id(user_id)
      if user_ucp:
        embed_response = discord.Embed(title="Password Reset | Mostline Roleplay", color=WARNA)
        embed_response.add_field(name="✅ Berhasil", value="Silakan cek DM Anda untuk melihat detailnya.")
        embed_response.set_thumbnail(url=ICON)
        embed_response.set_footer(text="@Mostline Roleplay", icon_url=ICON)
        await interaction.response.send_message(embed=embed_response, ephemeral=True)
        
        user = await bot.fetch_user(user_id)
        embed = discord.Embed(title="Password Reset | Mostline Roleplay", color=WARNA, description="Password UCP Anda berhasil direset. Silakan register ulang di Game.")
        embed.add_field(name="Akun UCP", value=f"```{user_ucp['ucp']}```")
        embed.add_field(name="Code Pemulihan", value=f"```{new_pin}```", inline=False)
        embed.add_field(name="", value="""
Masuklah ke server dan masukan kode baru untuk membuat ulang password!

#MostlineRoleplay
        """)
        embed.set_thumbnail(url=ICON)
        embed.set_footer(text="@Mostline Roleplay", icon_url=ICON)
        await user.send(embed=embed)
      else:
        await interaction.response.send_message("❌ Terjadi kesalahan saat mengambil informasi UCP.", ephemeral=True)
    except discord.Forbidden:
      await interaction.response.send_message("❌ Saya tidak bisa mengirimi Anda DM. Silakan aktifkan DM dari anggota server.", ephemeral=True)
    except Exception as e:
      await interaction.response.send_message(f"❌ Terjadi kesalahan: {e}", ephemeral=True)
        
  @button(label="No", custom_id="lupa_sandi_no", style=discord.ButtonStyle.red)
  async def no_button(self, interaction: discord.Interaction, button: discord.ui.Button):
    await interaction.response.edit_message(content="Anda memilih No. Pembatalan lupa sandi.")
    self.stop()
    
class Buttons(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
    
  @discord.ui.button(label="Take Karcis", custom_id="register_id", style=discord.ButtonStyle.green, emoji="🎟️")
  async def register(self, interaction: discord.Interaction, button: discord.Button):
    user_ucp = check_id(interaction.user.id)
    if user_ucp is not None:
      await interaction.response.send_message(f"Anda sudah mendaftar sebelumnya dengan nama UCP **{user_ucp['ucp']}**.", ephemeral=True)
    else:
      await interaction.response.send_modal(ModalApplicationForm(interaction.user.id))
    
  @discord.ui.button(label="Lupa Sandi", custom_id="lupa_sandi", style=discord.ButtonStyle.red, emoji="🔐")
  async def lupapw(self, interaction: discord.Interaction, button: discord.ui.Button):
    user_ucp = check_id(interaction.user.id)
    if user_ucp is not None:
        await interaction.response.send_message("Anda yakin ingin melanjutkan lupa sandi?", view=YesOrNo(), ephemeral=True)
    else:
        await interaction.response.send_message("Anda tidak memiliki akun UCP.", ephemeral=True)
 
  @discord.ui.button(label="Check Karcis", custom_id="check", style=discord.ButtonStyle.primary, emoji="🧾")
  async def checkuco(self, interaction: discord.Interaction, button: discord.ui.Button):
    user_info = get_user_info(interaction.user.id)
    if user_info:
      user = await bot.fetch_user(interaction.user.id)
      user_name = user_info['ucp']
      user_pin = user_info['verifycode']
      embed = discord.Embed(title="Check Akun | Mostline Roleplay", color=WARNA, description="""
Berhasil check ucp, dibawah ini untuk detail akun anda.
      """)
      embed.add_field(name="UCP", value=f"```{user_info['ucp']}```")
      embed.add_field(name="Verify Code", value=f"```{user_info['verifycode']}```")
      embed.add_field(name="Status", value=f"````Verified```")
      embed.set_thumbnail(url=ICON)
      embed.set_footer(text="@Mostline Roleplay", icon_url=ICON)
      await user.send(embed=embed)
      embed = discord.Embed(title="Check Akun | Mostline Roleplay", color=WARNA)
      embed.add_field(name="✅ Berhasil ", value="> Silakan check DM anda untuk melihat informasi akun")
      embed.set_thumbnail(url=ICON)
      embed.set_footer(text="@Mostline Roleplay", icon_url=ICON)
      await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
      await interaction.response.send_message(f"❌Tidak ada data untuk nama ucp anda.", ephemeral=True)
      
  @discord.ui.button(label="Reffund Karcis", custom_id="reffund", style=discord.ButtonStyle.grey, emoji="♻️")
  async def reff(self, interaction: discord.Interaction, button: discord.ui.Button):
    global ROLE_ID, NAME
    role = interaction.guild.get_role(ROLE_ID)
    role_id = ROLE_ID
    member_roles = [role.id for role in interaction.user.roles]
    if role_id in member_roles:
      await interaction.response.send_message("❌Anda sudah terdaftar, tidak dapat menggambil reffund.", ephemeral=True)
      return
    
    user_ucp = check_id(interaction.user.id)
    if user_ucp is not None:
      await interaction.response.send_message(f"✅ Reffund telah berhasil nama UCP anda adalah **{user_ucp['ucp']}**", ephemeral=True)
      await interaction.user.edit(nick=f"{NAME} | {user_ucp['ucp']}")
      role = interaction.guild.get_role(ROLE_ID)
      if role:
        await interaction.user.add_roles(role)
 
      
class ModalApplicationForm(discord.ui.Modal, title='Register UCP'):
  def __init__(self, user_id, **kwargs):
    super().__init__(**kwargs)
    self.user_id = user_id
    
  NamaUcp = ui.TextInput(label='Nama UCP', style=discord.TextStyle.short, placeholder="Example: Jaden")
  async def on_submit(self, interaction: discord.Interaction):
    nama = self.NamaUcp.value
    discord_id = self.user_id
    
    global NAME, ROLE_ID
    
    checkUCP = ucp_check(nama)
    if checkUCP:
      await interaction.response.send_message(f"Nama UCP **{checkUCP['ucp']}** sudah digunakan. Silakan pilih nama UCP lain.", ephemeral=True)
    else:
      await interaction.user.edit(nick=f'{NAME} | {nama}')
      role = interaction.guild.get_role(ROLE_ID)
      if role:
        await interaction.user.add_roles(role)
        
      nama = self.NamaUcp.value
      discord_id = self.user_id
      password = ""
      salt = ""
      extrac = "0"
      code = randomOTP()
      await interaction.response.send_message("✅Register telah berhasil mohon check DM anda untuk mendapatkan  Verifikasi Code", ephemeral=True)
      register_user(nama, code, discord_id, password, salt, extrac)
      print(f"\033[0;32mNAMA UCP \033[0m: {nama} | \033[0;32mPIN \033[0m: {code} | \033[0;32mBerhasil Register\033[0m")
      try:
        user = await bot.fetch_user(discord_id)
        embed = discord.Embed(title="MOSTLINE ROLEPLAY", color=WARNA, description="""
Yang terhormat, notknown997#0.
Mohon perhatian anda, pengambilan Tiket berhasil dilakukan. Gunakan UCP untuk login ke dalam server! Segera masuk ke dalam server melalui Pintu gate #1 (login in-game) dan masukkan kode verifikasi di bawah!
        """)
        embed.add_field(name="Nama UCP", value=f"```{nama}```")
        embed.add_field(name="Verify Code", value=f"```{code}```")
        embed.set_image(url=KARCIS)
        embed.set_thumbnail(url=THUMBNAIL)
        embed.set_footer(text="@Mostline Roleplay", icon_url=ICON)
        await user.send(embed=embed)
      except discord.Forbidden:
        await interaction.response.send_message("Saya tidak bisa mengirimi Anda DM. Silakan aktifkan DM dari anggota server.", ephemeral=True)
        return
              
@bot.tree.command()
@commands.has_permissions(administrator=True)
async def setregister(interaction: discord.Interaction):
  if not interaction.user.guild_permissions.administrator:
    return await interaction.response.send_message("Anda tidak bisa menggunakan command ini karena anda bukan administrator.", ephemeral=True)
    
  embed = discord.Embed(title='',color=WARNA, description="""### **__LOKET KARCIS MOSTLINE__**
Channel ini merupakan tempat dimana anda dapat mengatur ucp sendiri. Terdapat beberapa yang harus kamu ketahui, Diantaranya :
  """)
  embed.add_field(name="〘🎟️Take Karcis〙", value="""
> Sebagaimana dengan judulnya, ini merupakan tombol dimana kamu dapat mengambil karcis kamu (membuat akun UCP). Sebelum kamu bermain Most Line maka karcis adalah kewajiban utama yang harus kamu miliki,disinilah tempatnya!
  """)
  embed.add_field(name="〘🧾Cek Karcis〙", value="""
> Kamu dapat melihat status karcismu apakah sudah terverifikasi ataukah belum, kamu juga dapat melihat informasi kode verifikasi melalui ini jikalau kamu belum menerima DM dari BOT sebelumnya.
  """)
  embed.add_field(name="〘🔐Lupa Paswword〙", value="""
> Sesuai dengan namanya, button ini merupakan tempat apabila anda melupai atau anda ingin mengganti password dan apabila anda ingin mengganti password anda itu bakal terbatas dan Maximal mengganti password anda adalah sebanyak 3×.
  """)
  embed.add_field(name="〘♻️Reffund Karcis〙", value="""
> Apabila anda sudah pernah mendaftarkan ucp anda atau sudah mengambil karcis lalu anda out dari dc Most Line, lalu join kembali ke dc Most Line anda dapat mengambil kembali Karcis anda Dangan button ini.
  """)
  embed.set_thumbnail(url=THUMBNAIL)
  embed.set_image(url=IMAGE)
  embed.set_footer(text="@Mostline Roleplay", icon_url=ICON)
  await interaction.response.send_message(embed=embed, view=Buttons())
  
bot.run(TOKEN)