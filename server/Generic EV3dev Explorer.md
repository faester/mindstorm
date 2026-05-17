# Generic EV3dev Explorer
## Problem
The current app hardcodes device classes (`tacho-motor`, `lego-sensor`) and their attributes in `TachoMotor.py` and `Sensor.py`. Rewiring or connecting new device types requires code changes. The app should instead discover everything from the filesystem at runtime.
## Current State
* `Mindstorm.py` — generic `Directory` (file I/O) and `SensorMotorIO` (typed attribute registry with `get()`/`post()`).
* `TachoMotor.py` / `Sensor.py` — hardcoded attribute lists via `add_int_file`, `add_string_file`, etc.
* `pathbuilder.py` — hardcoded Flask routes for `/motors` and `/sensors`.
* Jinja templates — separate `motors.html`, `motor.html`, `sensors.html`, `sensor.html`.
* Tests in `test_TachoMotor.py` use `../sys/class` (the example tree).
## Key ev3dev Patterns to Support
1. **Singular/plural pairing**: a writable file `X` has legal values listed in `Xs` (e.g. `command`/`commands`, `mode`/`modes`, `stop_action`/`stop_actions`). The plural file is read-only; the singular file is write-only or read-write.
2. **Value gating**: `num_values` controls how many `value0`–`value7` are relevant. Only those should be read and displayed.
3. **Dynamic state**: POSTing to `mode` changes sensor behavior (new `num_values`, `units`, etc.). The UI must re-read after POST.
4. **Type inference from content**: integer (`0`, `360`), space-separated array (`coast brake hold`), key=value dictionary (`uevent`), or plain string.
5. **Write mode from permissions**: on the real EV3, `os.access(path, os.W_OK)` distinguishes read-only from writable. In the example tree all files are `644`, so we'll also support an override/fallback.
## Proposed Changes
### 1. New `flaskr/mindstorm/Device.py` — generic device discovery
Replace the hardcoded `TachoMotor` and `Sensor` classes with a single generic model:
* `DeviceClass(basedir, class_name)` — wraps a device class directory (e.g. `tacho-motor`). Lists device subdirectories.
* `Device(class_dir_path, device_name)` — wraps a single device. Auto-discovers attributes by listing files in the directory.
* Attribute discovery:
    * Skip non-regular files and known non-data entries (`device`, `subsystem`, `power`, `hold_pid`, `speed_pid`, `direct`).
    * Detect singular/plural pairs: if both `X` and `Xs` exist, treat `Xs` as a read-only array and `X` as writable (selected from that list).
    * Detect `valueN` files, gate on `num_values`.
    * Infer type from content: try `int()`, check for `=` lines (dict), check for spaces (array), else string.
    * Infer writability from `os.access(path, os.W_OK)` with group/other write bit, falling back to heuristic (files with `_sp` suffix or known writable names are writable).
* `get()` — reads all readable attributes, respects `num_values` gating.
* `post(**kwargs)` — writes to writable attributes, returns modified keys.
* `discover_basedir(basedir)` — top-level function that scans the basedir, returns a dict of `{class_name: DeviceClass}`.
### 2. Update `pathbuilder.py` — dynamic routes
Replace hardcoded motor/sensor routes with generic routes:
* `/<class_name>/` — list devices in that class.
* `/<class_name>/<device_name>` GET — read all attributes.
* `/<class_name>/<device_name>` POST — write attributes, re-read and return.
* `/` — scan basedir, list all device classes with their devices.
### 3. Update templates — generic rendering
Replace the 4 specific templates with 2 generic ones:
* `device_list.html` — lists devices in a class (replaces `motors.html` / `sensors.html`).
* `device.html` — renders any device: read-only attributes as info panel, writable attributes as form controls, singular/plural pairs as radio buttons, value-gated attributes grouped together.
* Update `main.html` — list all discovered device classes with links.
### 4. Update `__init__.py`
* Remove the swapped route-name bug (`sensor_template`/`motor_template`).
* Keep static file serving.
### 5. Update tests
* Adapt `test_TachoMotor.py` to test the generic `Device` class against the example tree.
* Add sensor tests.
### 6. Keep `Mindstorm.py`
`Directory` remains useful for low-level file I/O. `SensorMotorIO` can be retired since `Device` replaces its role.
### 7. Retire `TachoMotor.py` and `Sensor.py`
No longer needed once `Device.py` handles everything generically.