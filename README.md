# wub hub

Simple rcon dashboard with minecraft helpers for kids playing on creative mode.

## Requirements

- Python 3.8+
- Minecraft Java server with RCON enabled

You will also need to use pipx to install Poetry, the dependency manager used in this project.

## Limitations

This app is limited to helping one player at a time, and you need to configure the name of the player using environment variables.

Also, since this app is a mere hobby application for kids use in a private home server, it is not setup behind any authentication process or such. Please read the security notice at the bottom for more information.

## Configuration

Set the environment variables below before launching the app:

- `ENVIRONMENT`: set to `production` to hide debug logs, or anything else such as `development` to show them.
- `MINECRAFT_SERVER`: the hostname or ip of your Minecraft RCON server.
- `MINECRAFT_RCON_PORT`: the port of your Minecraft RCON server.
- `MINECRAFT_RCON_PASSWORD`: the password of your Minecraft RCON server.
- `TARGET_PLAYER`: the name of the player you want to target in the helper actions.
- `HOME_COORDINATES`: optional, can be set to the overworld coordinates of the player home in the format `-50 120 85`. if configured, the app will display an additional button to teleport into these coordinates.

## Usage

You don't need to setup a virtual environment, but you need to have pipx installed to be able to install Poetry as a global package. Poetry will then manage the virtual environment for you.

- First install Poetry if you still don't have it: `pipx install poetry`
- Install project dependencies: `poetry install`
- Start the app: `poetry run streamlit run wub_hub/main.py` *
 
*PS: Sorry about this mouthful of a command, I'm still trying to get poetry scripts and streamlit to work well together. 😅

## Security notice

You should know that exposing the port of your RCON server is a huge security risk for your Minecraft server. Anyone that is able to log in to your RCON server will be able to issue administrative commands to your Minecraft server, and will have the ability to list online players, kick or ban anyone, and summon TNTs in the whole world to break your precious buildings.

Proceed at your own risk. It is highly recommended to keep your RCON port locked behind a firewall or a private network, such as only exposing the RCON port behind Docker containers instead of exporting the port to the host machine.

Furthermore, it is also recommended to keep your instance of this application hidden behind a firewall or private network that is only accessible by your target player.

## License

This project is licensed under the terms of the GNU AGPLv3.

Read the [LICENSE](LICENSE) file for more information.
