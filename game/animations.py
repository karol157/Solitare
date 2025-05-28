import asyncio
import math
from textual.widget import Widget
from textual.geometry import Offset


class Animation:
    """
    Animates a card widget moving smoothly from a source container to a target container.
    """

    def __init__(self, source: tuple[int, str], target: tuple[int, str], board):
        """
        source: (row_index, index_within_container_or_tag)
        target: (row_index, index_within_container_or_tag)
        board: reference to the Textual board instance
        """
        self.board = board
        self.source_row, self.source_idx = source
        self.target_row, self.target_idx = target

        # Determine container types by index/tag
        self.source_type = (
            "deck"
            if self.source_idx == "D"
            else "stock"
            if self.source_idx == "S"
            else "foundation"
        )
        self.target_type = "foundation" if isinstance(self.target_idx, int) else "deck"

        # Query the container widgets
        self.source_container: Widget = board.query_one(
            f"#{self.source_type}{self.source_row}"
        )
        self.target_container: Widget = board.query_one(
            f"#{self.target_type}{self.target_row}"
        )

        self.source_container.styles.overflow = "visible"
        self.source_container.children[-1].styles.z_index = 10

        # Get the moving card widget:
        idx = (
            int(self.source_idx)
            if isinstance(self.source_idx, str) and self.source_idx.isdigit()
            else self.source_idx
        )
        self.card: Widget = self.source_container.children[idx]

        # Record start and end positions
        self.source_position = self.card.region.offset
        self.target_position = self.target_container.children[-1].region.offset

        # initialize the card's offset style so we can animate it
        self.card.styles.offset = (self.source_position.x, self.source_position.y)

        with open("file.txt", "a") as f:
            f.write(f"{self.target_position.y}  {self.target_position.x} \n")

    def ease_in_out(self, t: float) -> float:
        """
        Cubic ease-in-out curve for t in [0, 1].
        """
        return t * t * (3 - 2 * t)

    async def animate(self):
        # Compute vector and distance
        dx = self.target_position.x - self.source_position.x
        dy = self.target_position.y - self.source_position.y
        distance = math.hypot(dx, dy)
        duration = max(0.2, distance / 40) / 2  # at least 0.2s; ~40px/sec
        # Animate the combined offset property with easing
        """await self.card.animate(
            "offset",
            (self.target_position.x, self.target_position.y),
            duration=duration,
            easing=self.ease_in_out
        )"""
        await self.card.animate(
            "offset", value=Offset(1, 1), duration=duration, easing=self.ease_in_out
        )

    async def animate_p1(self):
        await self.card.animate(
            "offset",
            value=Offset(self.target_position.x / 2, self.target_position.y / 2 - 6),
            duration=0.1,
            easing=self.ease_in_out,
        )

    async def animate_p2(self):
        # Compute vector and distance
        dx = self.target_position.x - self.source_position.x
        dy = self.target_position.y - self.source_position.y
        distance = math.hypot(dx, dy)
        duration = max(0.2, distance / 40) / 2  # at least 0.2s; ~40px/sec
        # Animate the combined offset property with easing
        """await self.card.animate(
            "offset",
            (self.target_position.x, self.target_position.y),
            duration=duration,
            easing=self.ease_in_out
        )"""
        await self.card.animate(
            "offset",
            value=Offset(
                self.target_position.x / 2 - 4, self.target_position.y / 2 - 6
            ),
            duration=2,
            easing=self.ease_in_out,
        )

    async def animate_p3(self):
        dx = self.target_position.x - self.source_position.x
        dy = self.target_position.y - self.source_position.y
        distance = math.hypot(dx, dy)
        duration = max(0.2, distance / 40) / 2  # at least 0.2s; ~40px/sec
        # Animate the combined offset property with easing
        await self.card.animate(
            "offset",
            value=Offset(self.target_position.x / 2, self.target_position.y / 2 - 6),
            duration=duration,
            easing=self.ease_in_out,
        )

    def start(self):
        """
        Launch the animation coroutine in the event loop.
        """
        asyncio.create_task(self.animate())
