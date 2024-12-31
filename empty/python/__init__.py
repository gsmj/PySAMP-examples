from pysamp import on_gamemode_init
from .player import Player


@on_gamemode_init
def on_gamemode_init():
    ...


@Player.on_connect
@Player.using_registry
def on_player_connect(player: Player) -> None:
    ...


@Player.on_disconnect
@Player.using_registry
def on_player_disconnect(player: Player) -> None:
    Player.delete_registry(player)
    ...
