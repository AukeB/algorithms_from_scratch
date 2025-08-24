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
        number_of_columns: int = 500,
        number_of_rows: int = 500,
        damping: float = 0.99,
        intensity_value: int = 300,
        cursor_splash_size: int = 3,
        framerate: int = 60
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
            intensity_value: Intensity value for the waves. Defaults to 255. While 
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
        self.intensity_value = intensity_value
        self.cursor_splash_size = cursor_splash_size
        self.framerate = framerate

        self.current_state = np.zeros((number_of_rows, number_of_columns), dtype=np.float32)
        self.previous_state = np.zeros((number_of_rows, number_of_columns), dtype=np.float32)

        self.previous_state[number_of_rows // 2, number_of_columns // 2] = self.intensity_value

        self.grid_cell_width = int(self.window_width / number_of_columns)
        self.grid_cell_height = int(self.window_height / number_of_rows)

        pg.init()
        self.screen = pg.display.set_mode((self.window_width, self.window_height))
        self.clock = pg.time.Clock()
    
    def _propagate(self) -> None:
        """
        Perform one simulation step of wave propagation.

        For each grid cell, the new value is computed as the average of
        its four orthogonal neighbors in the previous state, minus the
        current value. The damping factor reduces amplitude to simulate
        energy loss.

        Ater applying this algorithm, the current_state and previous_state
        are swapped.
        """
        # Compute neighbor sum matrix
        neighbor_sum = (
            self.previous_state[:-2, 1:-1] +
            self.previous_state[2:, 1:-1] +
            self.previous_state[1:-1, :-2] +
            self.previous_state[1:-1, 2:]
        )

         # Apply ripple formula
        self.current_state[1:-1, 1:-1] = ( 
            neighbor_sum / 2 - self.current_state[1:-1, 1:-1]
        )

        # Apply damping
        self.current_state[1:-1, 1:-1] *= self.damping

        # Python swapping
        self.current_state, self.previous_state = self.previous_state, self.current_state

    def _draw_current_state(self) -> None:
        """
        Render the current simulation state to the PyGame window.

        The floating-point grid is clipped to [0, 255], converted to
        an 8-bit grayscale image, stacked into an RGB surface, and
        scaled to the window size.
        """
        
        arr = np.clip(self.current_state, 0, 255).astype(np.float32)

        # Scale from 0–255 to 0.3–1.0 (raise the floor so the darkest is lighter)
        t = arr / 255.0
        t = 0.2 + 0.8 * t  # remap 0→0.3, 255→1.0

        colormap = cm.get_cmap("hot")
        rgb_array = (colormap(t)[..., :3] * 255).astype(np.uint8)

        surface = pg.surfarray.make_surface(rgb_array.swapaxes(0, 1))
        surface = pg.transform.scale(surface, (self.window_width, self.window_height))

        self.screen.blit(surface, (0, 0))
    
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
            ] = self.intensity_value

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
            
            pg.display.flip()
            self.clock.tick(self.framerate)

        pg.quit()


water_ripples = WaterRipples()
water_ripples.execute()
