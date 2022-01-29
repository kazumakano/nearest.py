import numpy as np
import particle_filter.script.parameter as pf_param
from particle_filter.script.map import Map as PfMap


class Map(PfMap):
    def draw_pos(self, pos: np.ndarray) -> None:
        if pf_param.ENABLE_CLEAR:
            self.clear()
        self._draw_pos((0, 0, 255), False, pos)
