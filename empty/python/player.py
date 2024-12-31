import functools
from pysamp.player import Player as BasePlayer
from typing import Callable, Any


class Player(BasePlayer):
    _registry = {}
    """
    Retrieve an instance from the registry, creating it if needed.
    """
    def __init__(self, playerid):
        super().__init__(playerid)
        # Your own attributes here

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
