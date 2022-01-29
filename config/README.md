# config
This is directory for config files.
Put your config files here.
You can customize following parameters:
| Key                  | Description                                           | Notes                                                                | Type          |
| ---                  | ---                                                   | ---                                                                  | ---           |
| begin                | begin datetime of RSSI log                            | must be like 'yyyy-mm-dd hh:mm:ss'                                   | `str`         |
| end                  | end datetime of RSSI log                              | must be like 'yyyy-mm-dd hh:mm:ss'                                   | `str`         |
| log_file             | RSSI log file                                         |                                                                      | `str`         |
| init_pos             | initial position [px]                                 |                                                                      | `list[float]` |
| lost_tj_policy       | policy to interpolate trajectory while lost           | 1. use last position, 2. interpolate linearly                        | `int`         |
| result_dir_name      | name of directory for result files                    | auto generated if unspecified                                        | `str \| None` |
|                      |                                                       |                                                                      |               |
| win_size             | size of sliding window [s]                            |                                                                      | `float`       |
|                      |                                                       |                                                                      |               |
| enable_clear_map     | clear map image at each step or not                   |                                                                      | `bool`        |
| enable_draw_beacons  | draw beacon positions or not                          |                                                                      | `bool`        |
| enable_save_img      | capture image at last or not                          |                                                                      | `bool`        |
| enable_save_video    | record video or not                                   |                                                                      | `bool`        |
| frame_rate           | frame rate of video [fps]                             | synchronized with real speed if 0                                    | `float`       |
| map_conf_file        | map config file                                       |                                                                      | `str`         |
| map_img_file         | map image file                                        |                                                                      | `str`         |
| map_show_range       | range to show map                                     | whole map if unspecified                                             | `list[int]`   |
| win_stride           | stride width of sliding window [s]                    |                                                                      | `float`       |
|                      |                                                       |                                                                      |               |
| truth_log_file       | ground truth position log file                        | disabled if unspecified                                              | `str \| None` |
|                      |                                                       |                                                                      |               |
| enable_write_conf    | write config file or not                              |                                                                      | `bool`        |
|                      |                                                       |                                                                      |               |
| win_policy           | policy to get representative RSSI value in window     | 1: maximum, 2: latest                                                | `int`         |
