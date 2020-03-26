from gym_minigrid.roomgrid import RoomGrid
from gym_minigrid.register import register


class MultipleRewardRoom(RoomGrid):
    """
    Multiple rooms contain different rewards.
    """

    def __init__(
        self, num_rows=3, obj_type="ball", room_size=6, seed=None, fixed_seed=None
    ):
        self.obj_type = obj_type
        self.fixed_seed = fixed_seed

        super().__init__(
            room_size=room_size, num_rows=num_rows, max_steps=10 * room_size, seed=seed
        )

    def _gen_grid(self, width, height):
        super()._gen_grid(width, height)

        # Connect the middle column rooms into a hallway
        for j in range(1, self.num_rows):
            self.remove_wall(1, j, 3)

        # Place the agent in the middle
        self.place_agent(1, self.num_rows // 2)

        # Make sure all rooms are accessible
        # self.connect_all(within_timesteps=self.max_steps, self_locking=True)

        high_reward_room = (self._rand_elem((0, 2)), self._rand_int(0, self.num_rows))
        obj, _ = self.add_object(
            high_reward_room[0],
            high_reward_room[1],
            kind="reward",
            value=1,
            color="yellow",
        )

        rewads_per_room = 3

        reward_values = [self._rand_float(0, 1) for _ in range(2 * self.num_rows)]
        while rewads_per_room * max(reward_values) <= 1:
            reward_values = [self._rand_float(0, 1) for _ in range(2 * self.num_rows)]

        for col in (0, 2):
            for row in range(self.num_rows):
                # using col as door_idx places the door at the right side of the room
                door, _ = self.add_door(
                    col, row, door_idx=col, color="green", self_locking=True
                )
                if (col, row) != high_reward_room:
                    for _ in range(rewads_per_room):
                        value = reward_values[int(col == 2) * self.num_rows + row]
                        obj, _ = self.add_object(
                            col, row, kind="reward", value=value, color="blue"
                        )

        self.mission = "find the highest reward"

    def reset(self):
        if self.fixed_seed is not None:
            self.seed(1)
        return super().reset()


register(
    id="MiniGrid-MultipleRewardRoomS4R1-v0",
    entry_point="gym_minigrid.envs:MultipleRewardRoom",
    kwargs={"room_size": 4, "num_rows": 1, "fixed_seed": 1},
)

register(
    id="MiniGrid-MultipleRewardRoomS4R2-v0",
    entry_point="gym_minigrid.envs:MultipleRewardRoom",
    kwargs={"room_size": 4, "num_rows": 2, "fixed_seed": 1},
)

register(
    id="MiniGrid-MultipleRewardRoomS4R3-v0",
    entry_point="gym_minigrid.envs:MultipleRewardRoom",
    kwargs={"room_size": 4, "num_rows": 3, "fixed_seed": 1},
)

register(
    id="MiniGrid-MultipleRewardRoomS5R3-v0",
    entry_point="gym_minigrid.envs:MultipleRewardRoom",
    kwargs={"room_size": 5, "num_rows": 3, "fixed_seed": 1},
)

register(
    id="MiniGrid-MultipleRewardRoomS6R3-v0",
    entry_point="gym_minigrid.envs:MultipleRewardRoom",
    kwargs={"room_size": 6, "num_rows": 3, "fixed_seed": 1},
)
