import os.path as path
from datetime import datetime, timedelta
from typing import Any
import numpy as np
import particle_filter.script.parameter as pf_param
import particle_filter.script.utility as pf_util
from particle_filter.script.log import Log
from particle_filter.script.truth import Truth
from script.map import Map
from script.window import Window


def _set_main_params(conf: dict[str, Any]) -> None:
    global BEGIN, END, LOG_FILE, INIT_POS, LOST_TJ_POLICY, RESULT_DIR_NAME

    BEGIN = datetime.strptime(conf["begin"], "%Y-%m-%d %H:%M:%S")
    END = datetime.strptime(conf["end"], "%Y-%m-%d %H:%M:%S")
    LOG_FILE = str(conf["log_file"])
    INIT_POS = np.array(conf["init_pos"], dtype=np.float16)
    LOST_TJ_POLICY = np.int8(conf["lost_tj_policy"])
    RESULT_DIR_NAME = None if conf["result_dir_name"] is None else str(conf["result_dir_name"])

def nearest(conf: dict[str, Any], enable_show: bool = True) -> None:
    log = Log(BEGIN, END, path.join(pf_param.ROOT_DIR, "log/observed/", LOG_FILE))
    result_dir = pf_util.make_result_dir(RESULT_DIR_NAME)
    map = Map(log.mac_list, result_dir)
    if pf_param.TRUTH_LOG_FILE is not None:
        truth = Truth(BEGIN, END, result_dir)

    if pf_param.ENABLE_DRAW_BEACONS:
        map.draw_beacons(True)
    if pf_param.ENABLE_SAVE_VIDEO:
        map.init_recorder()

    estim_pos = np.array(INIT_POS, dtype=np.float16)
    lost_ts_buf = np.empty(0, dtype=datetime)
    t = BEGIN
    while t <= END:
        print(f"main.py: {t.time()}")
        win = Window(t, log)

        win.check_is_lost()

        if LOST_TJ_POLICY == 1:
            if not pf_param.IS_LOST:
                estim_pos = map.beacon_pos_list[win.get_strong_beacon_index()]
                map.draw_pos(estim_pos)
            if pf_param.TRUTH_LOG_FILE is not None:
                map.draw_truth(truth.update_err(t, estim_pos, map.resolution, pf_param.IS_LOST), True)

        elif LOST_TJ_POLICY == 2:
            if pf_param.TRUTH_LOG_FILE is not None and pf_param.IS_LOST:
                last_estim_pos = estim_pos
                lost_ts_buf = np.hstack((lost_ts_buf, t))
            elif not pf_param.IS_LOST:
                estim_pos = map.beacon_pos_list[win.get_strong_beacon_index()]
                map.draw_pos(estim_pos)

                if pf_param.TRUTH_LOG_FILE is not None:
                    buf_len = len(lost_ts_buf)
                    for i, lt in enumerate(lost_ts_buf):
                        map.draw_truth(truth.update_err(lt, pf_util.get_lerped_pos(estim_pos, last_estim_pos, i, buf_len), map.resolution, True), True)
                    lost_ts_buf = np.empty(0, dtype=datetime)
                    map.draw_truth(truth.update_err(t, estim_pos, map.resolution, False), True)

        if pf_param.ENABLE_SAVE_VIDEO:
            map.record()
        if enable_show:
            map.show()

        t += timedelta(seconds=pf_param.WIN_STRIDE)

    print("main.py: reached end of log")
    if pf_param.ENABLE_SAVE_IMG:
        map.save_img()
    if pf_param.ENABLE_SAVE_VIDEO:
        map.save_video()
    if pf_param.ENABLE_WRITE_CONF:
        pf_util.write_conf(conf, result_dir)
    if pf_param.TRUTH_LOG_FILE is not None:
        truth.export_err()
    if enable_show:
        map.show(0)

if __name__ == "__main__":
    import argparse
    from particle_filter.script.parameter import set_params

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--conf_file", help="specify config file", metavar="PATH_TO_CONF_FILE")
    parser.add_argument("--no_display", action="store_true", help="run without display")
    args = parser.parse_args()

    conf = set_params(args.conf_file)
    _set_main_params(conf)

    nearest(conf, not args.no_display)
