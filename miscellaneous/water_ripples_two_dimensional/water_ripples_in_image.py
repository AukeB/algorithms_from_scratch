"""Module that simulates 2D water ripples using PyGame."""

import pygame as pg
import numpy as np
import matplotlib.cm as cm

class WaterRipples:
    """Simulation of 2D water ripples using a discrete wave equation."""

    def __init__(
        self,
        window_width: int = 2000,
        window_height: int = 2000,
        number_of_columns: int = 100,
        number_of_rows: int = 100,
        damping: float = 0.99,
        wave_brightness: int = 255,
        maximum_brightness: int = 255,
        cursor_splash_size: int = 2,
        framerate: int = 30
    ) -> None:
        """
        Initialize the ripple simulation class.

        The simulation maintains two grids (previous_state and current_state). At
        each step, values propagate from the previous grid to the current grid,
        and then the grids are swapped.

        Args:
            window_width: Width of the PyGame window in pixels.
            window_height: Height of the PyGame window in pixels.
            number_of_columns: Number of columns in the simulation grid.
            number_of_rows: Number of rows in the simulation grid.
            damping: Factor between 0 and 1 that reduces wave amplitude each frame.
            wave_brightness: Intensity value for the waves. Defaults to 255. While 
                the simulation itself allows values outside the range [0, 255], the
                visualization clips to this range, so higher values effectively produce
                higher visual contrast in the ripples.
            framerate: Target framerate for rendering. Units: frames / second.
        """
        self.window_width = window_width
        self.window_height = window_height
        self.number_of_columns = number_of_columns
        self.number_of_rows = number_of_rows
        self.damping = damping
        self.wave_brightness = wave_brightness
        self.maximum_brightness = maximum_brightness
        self.cursor_splash_size = cursor_splash_size
        self.framerate = framerate

        self.current_state = np.zeros((number_of_rows, number_of_columns), dtype=np.float32)
        self.previous_state = np.zeros((number_of_rows, number_of_columns), dtype=np.float32)

        self.previous_state[number_of_rows // 2, number_of_columns // 2] = self.wave_brightness

        self.grid_cell_width = int(self.window_width / number_of_columns)
        self.grid_cell_height = int(self.window_height / number_of_rows)

        pg.init()
        self.screen = pg.display.set_mode((self.window_width, self.window_height))
        self.clock = pg.time.Clock()
    
    def _swap_states(self) -> None:
        """
        Swap the current and previous simulation states.

        This avoids copying arrays: after each propagation step,
        the roles of the two grids are exchanged.
        """
        self.current_state, self.previous_state = self.previous_state, self.current_state
    
    def _propagate(self) -> None:
        """
        Perform one simulation step of wave propagation.

        For each grid cell, the new value is computed as the average of
        its four orthogonal neighbors in the previous state, minus the
        current value. The damping factor reduces amplitude to simulate
        energy loss.
        """
        neighbor_sum = (
            self.previous_state[:-2, 1:-1] +
            self.previous_state[2:, 1:-1] +
            self.previous_state[1:-1, :-2] +
            self.previous_state[1:-1, 2:]
        )

        self.current_state[1:-1, 1:-1] = ( 
            neighbor_sum / 2 - self.current_state[1:-1, 1:-1] # Apply ripple formula
        )

        self.current_state[1:-1, 1:-1] *= self.damping

    def _draw_current_state(
        self,
        normalized_trapezoid: dict[str, float] = {
            "y_top": 0.1,
            "y_bottom": 0.9,
            "x_top_left": 0.3,
            "x_top_right": 0.7,
            "x_bottom_left": 0,
            "x_bottom_right": 1,
        }
        ) -> None:
        """
        Render the current simulation state to the PyGame window.

        The floating-point grid is clipped to [0, 255], converted to
        an 8-bit grayscale image, stacked into an RGB surface, and
        scaled to the window size.
        """
        # All values smaller than 0 become 0, and larger than 255 become 255.
        current_state: np.ndarray = np.clip(self.current_state, 0, 255).astype(np.float32)

        # Scale from 0–255 to 0.3–1.0 (raise the floor so the darkest is lighter)
        normalized_state = current_state / self.maximum_brightness
        scaled_state = 0.1 + 0.8 * normalized_state  # remap 0→0.3, 255→1.0

        colormap = cm.get_cmap("bone")
        rgb_array = (colormap(scaled_state)[..., :3] * 255).astype(np.uint8)

        trapezoid = {key: (value * self.window_height if key.startswith("y") else value*self.window_width) for key, value in normalized_trapezoid.items()}

        for y in range(len(scaled_state)):
            for x in range(len(scaled_state[y])):
                color = rgb_array[y][x]

                x_left = trapezoid["x_top_left"] + (normalized_trapezoid["x_bottom_left"] - normalized_trapezoid["x_top_left"]) * y * (self.window_width / self.number_of_columns)
                x_right = trapezoid["x_top_right"] + (normalized_trapezoid["x_bottom_right"] - normalized_trapezoid["x_top_right"]) * y * (self.window_height / self.number_of_rows)
                scaled_grid_cell_width = (x_right - x_left) / self.number_of_columns
                left = x_left + x * scaled_grid_cell_width

                scaled_grid_cell_height = self.grid_cell_height * (normalized_trapezoid["y_bottom"] - normalized_trapezoid["y_top"])
                top = trapezoid["y_top"] + y * scaled_grid_cell_height

                pg.draw.polygon(
                    self.screen,
                    color,
                    [
                        (left, top),
                        (left + scaled_grid_cell_width, top),
                        (left + scaled_grid_cell_width, top + scaled_grid_cell_height),
                        (left, top + scaled_grid_cell_height)
                    ]
                )
    
    def _handle_mouse(self, event: pg.event.Event) -> None:
        """
        Handle mouse clicks by creating a disturbance in the ripple grid.

        Args:
            event (pg.event.Event): The PyGame mouse event.

        Notes:
            The disturbance is added to the `previous_state` array at the 
            grid cell corresponding to the mouse position. A small square 
            region is disturbed instead of a single cell to make the 
            ripple visible.
        """
        if event.type == pg.MOUSEBUTTONDOWN:
            mx, my = event.pos

            grid_x = mx // self.grid_cell_width
            grid_y = my // self.grid_cell_height

            self.previous_state[
                max(grid_y - self.cursor_splash_size, 1):min(grid_y + self.cursor_splash_size, self.number_of_rows-1),
                max(grid_x - self.cursor_splash_size, 1):min(grid_x + self.cursor_splash_size, self.number_of_columns-1)
            ] = self.wave_brightness

    def execute(self) -> None:
        """
        Run the simulation loop until the user exits.

        Handles events (QUIT, ESC), updates the simulation each frame,
        draws the current state, and enforces the desired framerate.
        """
        # Main loop
        running = True

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    self._handle_mouse(event)

            self.screen.fill((0, 0, 0))
            self._propagate()
            self._draw_current_state()
            self._swap_states()
            
            pg.display.flip()
            self.clock.tick(self.framerate)

        pg.quit()


water_ripples = WaterRipples()
water_ripples.execute()
