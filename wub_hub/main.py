import os
import streamlit as st
from rcon.source import Client
from PIL import Image

# checks the current environment to determine if it will display extra debug helpers in the ui
environment = os.environ.get('ENVIRONMENT') or 'development'
show_debug = environment.lower() != 'production'

# load environment variables for the app configuration
rcon_server = os.environ.get('MINECRAFT_SERVER') or '127.0.0.1'
rcon_port = os.environ.get('MINECRAFT_RCON_PORT') or 25575
rcon_password = os.environ.get('MINECRAFT_RCON_PASSWORD')
target_player = os.environ.get('TARGET_PLAYER')
home_coordinates = os.environ.get('HOME_COORDINATES')

# load ui images
img_setblock = Image.open('images/setblock.webp')
img_light = Image.open('images/light.webp')
img_barrier = Image.open('images/barrier.webp')
img_command_block = Image.open('images/command_block.webp')
img_home = Image.open('images/home.webp')

# initialize empty app state placeholders
if 'init' not in st.session_state:
  st.session_state.init = True
  st.session_state.command = ''
  st.session_state.output = ''

# print the app header with markdown, yay!
st.write('# wub hub')

# display debug commands and outputs in the ui during development mode
if show_debug and st.session_state.command != '':
  st.code(st.session_state.command, language='html')

if show_debug and st.session_state.output != '':
  st.code(st.session_state.output, language='html')

# base setup to send rcon commands to the game server
def send_command(command):
  try:
    st.session_state.command = command # logs the command in the debug ui
    with Client(rcon_server, rcon_port, passwd=rcon_password) as client:
      st.session_state.output = client.run(command) # executes the command and logs the response in the debug ui
  except ConnectionError:
    st.session_state.output = "Failed!" # only show error in the debug ui, this avoids displaying the disruptive error modals from streamlit and getting kids confused or stuck in the ui

# helper command to execute rcon command in the position of the target player
def execute_positioned(command):
  send_command(f'execute positioned as {target_player} run {command}')

# helper command to execute rcon command on behalf of the target player
def execute_as(command):
  send_command(f'execute as {target_player} run {command}')

# command to place a shiny block in the target player's coordinate, helpful to build high up in the air
def cmd_setblock():
  execute_positioned('setblock ~ ~ ~ minecraft:shroomlight keep')

# command to give the target player a light block, only available in creative mode and used as an invisible light source
def cmd_light():
  execute_as('give @s minecraft:light')

# command to give the target player a barrier block, only available in creative mode and used as an invisible indestructible barrier
def cmd_barrier():
  execute_as('give @s minecraft:barrier')

# command to teleport the target player get home, very useful when adventuring too far away from home and is either lost or just want to come back quickly
def cmd_home():
  execute_as(f'execute in minecraft:overworld run tp @s {home_coordinates}')

# extra utilities for messing around
def cmd_command_block():
  execute_as('give @s minecraft:command_block')

def cmd_help():
  send_command('help')

def cmd_list():
  send_command('list')

# extra buttons for debugging
if show_debug:
  with st.container():
    st.button('help', on_click=cmd_help)
    st.button('list', on_click=cmd_list)

# visual fluff
st.write('---')

# prepare layout with variable number of columns
if home_coordinates:
  col1, col2, col3, col4, col5 = st.columns(5)
else:
  col1, col2, col3, col4 = st.columns(4)

# render helper buttons in the screen
with col1:
  st.image(img_setblock)
  st.button('SET BLOCK', on_click=cmd_setblock)
  
with col2:
  st.image(img_light)
  st.button('LIGHT', on_click=cmd_light)

with col3:
  st.image(img_barrier)
  st.button('BARRIER', on_click=cmd_barrier)

with col4:
  st.image(img_command_block)
  st.button('COMMAND BLOCK', on_click=cmd_command_block)

# if home coordinates are configured, then display an additional button to teleport back home
if home_coordinates:
  with col5:
    st.image(img_home)
    st.button('HOME', on_click=cmd_home)

# css hacks to workaround streamlit limitations and touch up the layout a little bit
style = '''
/* center images and buttons in each container */
div.element-container { text-align: center; }
div[data-testid="stFullScreenFrame"] div { justify-content: center; }

/* reduce visual clutter from heading spacing */
hr { opacity: 0; }
'''

# css hacks to hide streamlit development controls when deployed, and avoid kids to get stuck with them
if not show_debug:
  style += '''
  /* hide development controls + full screen button */
  .stDeployButton, #MainMenu, div[data-testid="stHeader"], div[data-testid="stToolbar"], div[data-testid="stStatusWidget"], button[data-testid="StyledFullScreenButton"] {
    display: none;
  }
  '''

# render both css hacks from above
st.markdown(f'<style>{style}</style>', unsafe_allow_html=True)
