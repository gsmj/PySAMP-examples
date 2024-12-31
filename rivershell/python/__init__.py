from pysamp import (
    on_gamemode_init,
    add_player_class,
    set_game_mode_text,
    show_player_markers,
    show_name_tags,
    set_world_time,
    game_mode_exit,
    game_text_for_all,
    set_timer,
    set_vehicle_to_respawn,
    send_death_message
)
from samp import (  # type: ignore
    PLAYER_STATE_DRIVER,
    PLAYER_STATE_ONFOOT,
    INVALID_PLAYER_ID,
)
from pysamp.vehicle import Vehicle
from .player import Player
from . import vehicles
from .consts import (
    TEAM_GREEN,
    TEAM_BLUE,
    OBJECTIVE_VEHICLE_GREEN,
    OBJECTIVE_VEHICLE_BLUE,
    CAPS_TO_WIN,
    OBJECTIVE_COLOR,
)

is_objective_reached: bool = False
blue_times_capped: int = 0
green_times_capped: int = 0


@on_gamemode_init
def on_init() -> None:
    print("\n----------------------------------")
    print("  Rivershell by Kye 2006\nRe-written for PySAMP")
    print("----------------------------------\n")
    set_game_mode_text("Rivershell")
    show_player_markers(1)
    show_name_tags(True)
    set_world_time(7)

    add_player_class(162,1980.0054,-266.6487,2.9653,348.9788,0,0,31,400,29,400)
    add_player_class(157,1980.0054,-266.6487,2.9653,348.9788,0,0,31,400,29,400)
    add_player_class(154,2359.2703,540.5911,1.7969,180.6476,0,0,31,400,29,400)
    add_player_class(138,2294.0413,541.8565,1.7944,188.6283,0,0,31,400,29,400)
    vehicles.add_static_vehicles()


@Player.on_connect
@Player.using_registry
def on_player_connect(player: Player) -> None:
    player.set_color(0x888888FF)
    player.game_text("~r~SA-MP:~w~Rivershell", 2000, 5)


@Player.on_disconnect
@Player.using_registry
def on_player_disconnect(player: Player, reason: int) -> None:
    Player.delete_registry(player)


@Player.on_request_class
@Player.using_registry
def on_player_request_class(player: Player, class_id: int) -> None:
    player.setup_for_class_selection()
    player.set_team_from_class(class_id)


@Player.on_spawn
@Player.using_registry
def on_player_spawn(player: Player) -> None:
    player.set_team_color()
    if player.team_id == TEAM_GREEN:
        player.game_text(
            "Defend the ~g~GREEN ~w~team's ~y~Reefer~n~~w~"
            "Capture the ~b~BLUE ~w~team's ~y~Reefer",
            6000,
            5
        )

    if player.team_id == TEAM_BLUE:
        player.game_text(
            "Defend the ~b~BLUE ~w~team's ~y~Reefer~n~~w~"
            "Capture the ~g~GREEN ~w~team's ~y~Reefer",
            6000,
            5
        )

    player.set_world_bounds(2444.4185, 1687.5696, 631.2963, -454.9898)


@Player.on_enter_checkpoint
@Player.using_registry
def on_player_enter_checkpoint(player: Player) -> None:
    if is_objective_reached:
        return

    vehicle_id = player.get_vehicle_id()
    if (vehicle_id == OBJECTIVE_VEHICLE_GREEN and
        player.team_id == TEAM_GREEN):
        global green_times_capped
        green_times_capped += 1
        if green_times_capped == CAPS_TO_WIN:
            game_text_for_all("~g~GREEN ~w~team wins!", 3000, 5)
            set_timer(game_mode_exit, 1000, False)

        else:
            game_text_for_all(
                "~g~GREEN ~w~team captured the ~y~boat!", 3000, 5
            )
            set_vehicle_to_respawn(OBJECTIVE_VEHICLE_GREEN)

    if (vehicle_id == OBJECTIVE_VEHICLE_BLUE and
        player.team_id == TEAM_BLUE):
        global blue_times_capped
        blue_times_capped += 1
        if blue_times_capped == CAPS_TO_WIN:
            game_text_for_all("~b~BLUE ~w~team wins!", 3000, 5)
            set_timer(game_mode_exit, 1000, False)

        else:
            game_text_for_all(
                "~b~BLUE ~w~team captured the ~y~boat!", 3000, 5
            )
            set_vehicle_to_respawn(OBJECTIVE_VEHICLE_BLUE)

    global is_objective_reached
    is_objective_reached = True

@Player.on_death
@Player.using_registry
def on_player_death(player: Player, killer: Player, reason: int) -> bool:
    send_death_message(
        killer.id if killer != INVALID_PLAYER_ID else INVALID_PLAYER_ID,
        player.id,
        reason
    )
    if killer == INVALID_PLAYER_ID:
        return

    if player.team_id != killer.team_id:
        send_death_message(killer.id, player.id, reason)
        killer.set_score(killer.get_score() + 1)


@Vehicle.on_stream_in
def on_vehicle_stream_in(vehicle: Vehicle, for_player: Player) -> bool:
    for_player = for_player.from_registry_native(for_player)
    if (for_player.team_id == TEAM_GREEN and
        vehicle.id == OBJECTIVE_VEHICLE_BLUE):
        return vehicle.set_params_for_player(for_player, 1, 1)

    if (for_player.team_id == TEAM_BLUE and
        vehicle.id == OBJECTIVE_VEHICLE_GREEN):
        return vehicle.set_params_for_player(for_player, 1, 1)

    return vehicle.set_params_for_player(for_player, 1, 0)


@Player.on_key_state_change
@Player.using_registry
def on_player_key_state_change(
    player: Player,
    new_state: int,
    old_state: int,
) -> None:
    if new_state == PLAYER_STATE_DRIVER:
        vehicle_id = player.get_vehicle_id()
        if (player.team_id == TEAM_GREEN and
            vehicle_id == OBJECTIVE_VEHICLE_GREEN or
            vehicle_id == OBJECTIVE_VEHICLE_BLUE):
            player.set_color(OBJECTIVE_COLOR)
            player.set_checkpoint(1982.6150, -220.6680, -0.2432, 7.0)
            player.is_objective = True

        player.game_text(
            "~w~Take the ~y~boat ~w~back to the ~r~spawn!", 3000, 5
        )

    if new_state == PLAYER_STATE_ONFOOT and player.is_objective:
        player.set_team_color()
        player.disable_checkpoint()



# 	else if(newstate == PLAYER_STATE_ONFOOT)
# 	{
# 		if(playerid == gObjectiveGreenPlayer) {
# 		    gObjectiveGreenPlayer = (-1);
# 		    SetPlayerToTeamColor(playerid);
# 	  		DisablePlayerCheckpoint(playerid);
# 		}

# 		if(playerid == gObjectiveBluePlayer) {
# 		    gObjectiveBluePlayer = (-1);
# 		    SetPlayerToTeamColor(playerid);
# 		    DisablePlayerCheckpoint(playerid);
# 		}
# 	}

#     return 1;
