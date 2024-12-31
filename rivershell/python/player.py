import functools
from pysamp.player import Player as BasePlayer
from typing import Callable, Any, Optional


TEAM_COLORS: dict[int, int] = {
    0: 0x77CC77FF,
    1: 0x7777DDFF
}


class Player(BasePlayer):
    _registry = {}
    """
    Retrieve an instance from the registry, creating it if needed.
    """
    def __init__(self, playerid):
        super().__init__(playerid)
        self.team_id: Optional[int] = None
        self.is_objective: bool = False


    @classmethod
    def from_registry_native(cls, player: BasePlayer) -> "Player":
        if isinstance(player, int):
            player_id = player

        if isinstance(player, BasePlayer):
            player_id = player.id

        player = cls._registry.get(player_id)
        if not player:
            cls._registry[player_id] = player = cls(player_id)

        return player

    @classmethod
    def using_registry(cls, func: Callable) -> Callable:
        """
        This should be used to make sure that our callback takes an instance \
        of the class from the dictionary
        """
        @functools.wraps(func)
        def from_registry(*args, **kwargs) -> Any:
            args = list(args)
            args[0] = cls.from_registry_native(args[0])
            return func(*args, **kwargs)

        return from_registry

    @classmethod
    def delete_registry(cls, player: BasePlayer) -> None:
        """
        Removes an instance from the registry
        """
        playerid = player.id
        del cls._registry[playerid]

    def set_team_color(self) -> bool:
        return self.set_color(TEAM_COLORS[self.team_id])

    def setup_for_class_selection(self) -> None:
        self.set_pos(1984.4445, 157.9501, 55.9384)
        self.set_camera_position(1984.4445, 160.9501, 55.9384)
        self.set_camera_look_at(1984.4445 ,157.9501, 55.9384)
        self.set_facing_angle(0.0)

    def set_team_from_class(self, class_id: int) -> None:
        self.game_text(
            f"{'~g~GREEN ~w~TEAM' if class_id == 0 else '~b~BLUE ~w~TEAM'}",
            1000,
            5
        )
        if class_id in (0, 1):
            self.team_id = 0

        else:
            self.team_id = 1
