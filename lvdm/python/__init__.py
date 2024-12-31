import random
from pysamp.player import Player
from pysamp import on_gamemode_init, send_death_message
from . import classes, vehicles
from .spawns import RANDOM_SPAWNS
from .vars import (
    COLOR_GREY,
    COLOR_GREEN,
    COLOR_RED,
    COLOR_YELLOW,
    COLOR_WHITE,
    COLOR_DISCORD,
)
from samp import INVALID_PLAYER_ID  # type: ignore


@on_gamemode_init
def on_ready() -> None:
    print("----------------------------------")
    print("Running LVDM ~MoneyGrub")
    print("Originally coded by Jax")
    print("Re-written for PySAMP")
    print("----------------------------------")
    classes.add_player_classes()
    vehicles.add_static_vehicles()


@Player.on_connect
def on_player_connect(player: Player) -> None:
    player.game_text("~w~SA-MP: ~r~Las Venturas ~g~MoneyGrub", 5000, 5)
    player.send_client_message(
        COLOR_YELLOW,
        "Welcome to Las Venturas MoneyGrub, For help type /help."
    )


@Player.on_request_class
def on_player_request_class(player: Player, class_id: int) -> None:
    player.set_interior(14)
    player.set_pos(258.4893, -41.4008, 1002.0234)
    player.set_facing_angle(270.0)
    player.set_camera_position(256.0815, -43.0475, 1004.0234)
    player.set_camera_look_at(258.4893,-41.4008, 1002.0234)


@Player.on_spawn
def on_player_spawn(player: Player) -> None:
    index = random.randint(0, len(RANDOM_SPAWNS))
    player.set_pos(*RANDOM_SPAWNS[index])
    player.set_interior(0)
    player.toggle_clock(True)
    player.give_weapon(24, 300)


@Player.on_death
def on_player_death(player: Player, killer: Player, reason: int) -> None:
    if killer == INVALID_PLAYER_ID:
        return

    send_death_message(killer.id, player.id, reason)
    killer.set_score(killer.get_score() + 1)


@Player.command
def help(player: Player) -> None:
    player.send_client_message(COLOR_RED, "This is /help commands in PySAMP")
    player.send_client_message(
        COLOR_GREEN, "Try to type a few more commands and see the result!"
    )
    player.send_client_message(
        COLOR_WHITE, "Commands: /foo, /calculate, /discord"
    )


@Player.command(aliases=("bar", ))
def foo(player: Player):
    player.send_client_message(COLOR_YELLOW, f"Hi, {player.get_name()}!")
    player.send_client_message(
        COLOR_GREY, "This command has aliases, try /bar"
    )


@Player.command
def calculate(player: Player, a: int, b: int) -> None:
    try:
        a = int(a)
    except:  # noqa: E722
        return player.send_client_message(
            COLOR_RED, "Whoops, you entered the wrong number for parameter a!"
        )

    try:
        b = int(b)
    except:  # noqa: E722
        return player.send_client_message(
            COLOR_RED, "Hey, you entered the wrong number for parameter b!"
        )

    player.send_client_message(
        COLOR_GREY,
        f"The result is {a + b}!"
    )


@Player.command
def discord(player: Player) -> None:
    player.send_client_message(
        COLOR_DISCORD,
        "Join our Discord: https://discord.gg/9Bf6A4MPfX"
    )
