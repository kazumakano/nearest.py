from datetime import datetime
import numpy as np
import particle_filter.script.parameter as pf_param
from particle_filter.script.log import Log


class Window:
    def __init__(self, current: datetime, log: Log) -> None:
        ts, mac, rssi = log.slice_win(current)

        self.rssi_list = np.full(len(log.mac_list), -np.inf, dtype=np.float16)
        if pf_param.WIN_POLICY == 1:
            for i in range(len(ts)):
                for j, m in enumerate(log.mac_list):
                    if m == mac[i] and self.rssi_list[j] < rssi[i]:
                        self.rssi_list[j] = rssi[i]
                        break    
        elif pf_param.WIN_POLICY == 2:
            for i in reversed(range(len(ts))):
                for j, m in enumerate(log.mac_list):
                    if m == mac[i] and np.isneginf(self.rssi_list[j]):
                        self.rssi_list[j] = rssi[i]
                        break

    def check_is_lost(self) -> None:
        pf_param.IS_LOST = len(np.where(np.isneginf(self.rssi_list))[0]) == len(self.rssi_list)

    def get_strong_beacon_index(self) -> int:
        max_rssi = -np.inf
        strong_beacon_index = -1
        for i, r in enumerate(self.rssi_list):
            if r > max_rssi:
                max_rssi = r
                strong_beacon_index = i

        return strong_beacon_index
