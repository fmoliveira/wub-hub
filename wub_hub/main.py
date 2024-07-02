import os
import streamlit as st
from rcon.source import Client
from PIL import Image

rcon_server = os.environ.get('MINECRAFT_SERVER') or '127.0.0.1'
rcon_port = os.environ.get('MINECRAFT_RCON_PORT') or 25575
rcon_password = os.environ.get('MINECRAFT_RCON_PASSWORD')
target_player = os.environ.get('TARGET_PLAYER')

img_setblock = Image.open('images/setblock.webp')
img_light = Image.open('images/light.webp')
img_barrier = Image.open('images/barrier.webp')

if 'init' not in st.session_state:
  st.session_state.init = True
  st.session_state.command = ''
  st.session_state.output = ''

st.write('# wub hub')
st.write('---')

# if st.session_state.command != '':
#   st.code(st.session_state.command.replace('\n', '\n'), language='html')
  
# if st.session_state.output != '':
#   st.code(st.session_state.output.replace('\n', '\n'), language='html')

def send_command(command):
  try:
    with Client(rcon_server, rcon_port, passwd=rcon_password) as client:
      st.session_state.command = command
      st.session_state.output = client.run(command)
  except ConnectionError:
    st.session_state.output = "Failed!" # may show some indicator later, but now it's just best to avoid disrupting the ui

def execute_positioned(command):
  send_command(f'execute positioned as {target_player} run {command}')

def execute_as(command):
  send_command(f'execute as {target_player} run {command}')

# def cmd_help():
#   send_command('help')

# def cmd_list():
#   send_command('list')

def cmd_setblock():
  execute_positioned('setblock ~ ~ ~ minecraft:shroomlight')

def cmd_light():
  execute_as('give @s minecraft:light')

def cmd_barrier():
  execute_as('give @s minecraft:barrier')

# st.button('help', on_click=cmd_help)
# st.button('list', on_click=cmd_list)

col1, col2, col3 = st.columns(3)

with col1:
  st.image(img_setblock)
  st.button('SET BLOCK', on_click=cmd_setblock)
  
with col2:
  st.image(img_light)
  st.button('LIGHT', on_click=cmd_light)

with col3:
  st.image(img_barrier)
  st.button('BARRIER', on_click=cmd_barrier)

style = '''
<style>
/* center images and buttons in each container */
div.element-container { text-align: center; }
div[data-testid="stFullScreenFrame"] div { justify-content: center; }

/* hide development controls + full screen button */
.stDeployButton, #MainMenu, button[data-testid="StyledFullScreenButton"] { display: none; }

/* reduce visual clutter from heading spacing */
hr { opacity: 0; }
</style>
'''

st.markdown(style, unsafe_allow_html=True)
