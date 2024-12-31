from pysamp import (
    on_gamemode_init,
    set_game_mode_text,
    add_player_class,
    get_tick_count,
    send_client_message_to_all
)
from pysamp.timer import set_timer


@on_gamemode_init
def on_ready():
    print("\n----------------------------------")
    print("  This is a blank GameModeScript")
    print("----------------------------------\n")
    set_timer(one_second_timer, 1000, True)
    set_game_mode_text("Timer Test")
    add_player_class(
        0,
        1958.3783,
        1343.1572,
        15.3746,
        269.1425,
        0,
        0,
        0,
        0,
        0,
        0,
    )


def one_second_timer():
    send_client_message_to_all(0xFF0000, f"Ticks: {get_tick_count()}")
