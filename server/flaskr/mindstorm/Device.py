import os
import logging
import re

log = logging.getLogger('Device')

# Files that are not useful data attributes
SKIP_FILES = {'device', 'subsystem', 'power', 'hold_pid', 'speed_pid', 'direct', 'bin_data'}

# Pattern for valueN files
VALUE_RE = re.compile(r'^value(\d+)$')


def discover_basedir(basedir):
    """Scan basedir for device classes (subdirectories). Returns dict of {class_name: DeviceClass}."""
    result = {}
    if not os.path.isdir(basedir):
        return result
    for devicename in (name for name in os.listdir(basedir) if name.startswith("lego") or name.startswith("tachomotor")):
        log.info("Adding path " + devicename)
        path = os.path.join(basedir, devicename)
        if os.path.isdir(path):
            result[devicename] = DeviceClass(basedir, devicename)
    return sorted(result)


class DeviceClass:
    """Wraps a device class directory (e.g. tacho-motor, lego-sensor). Lists device subdirectories."""

    def __init__(self, basedir, class_name):
        self.basedir = basedir
        self.class_name = class_name
        self.directory = os.path.join(basedir, class_name)

    def get_devices(self):
        """Returns sorted list of device directory names."""
        if not os.path.isdir(self.directory):
            return []
        return sorted([
            name for name in os.listdir(self.directory)
            if os.path.isdir(os.path.join(self.directory, name))
        ])

    def get_device(self, device_name):
        """Returns a Device instance for the given device name."""
        return Device(self.directory, device_name)


class Attribute:
    """Describes a single sysfs attribute file."""

    def __init__(self, name, attr_type, writable, paired_with=None):
        self.name = name
        self.attr_type = attr_type  # 'int', 'string', 'array', 'dict'
        self.writable = writable
        self.paired_with = paired_with  # e.g. 'commands' for 'command'


class Device:
    """Wraps a single device directory. Auto-discovers attributes from the filesystem."""

    def __init__(self, class_dir, device_name):
        self.device_name = device_name
        self.directory = os.path.join(class_dir, device_name)
        if not os.path.isdir(self.directory):
            raise FileNotFoundError('Device directory not found: {}'.format(self.directory))
        self.attributes = {}
        self._discover_attributes()

    def _file_path(self, name):
        return os.path.join(self.directory, name)

    def _read_raw(self, name):
        """Read raw content of an attribute file."""
        try:
            with open(self._file_path(name), 'r') as f:
                return f.read()
        except (IOError, OSError, UnicodeDecodeError):
            return ''

    def _write_raw(self, name, value):
        """Write a value to an attribute file."""
        with open(self._file_path(name), 'w') as f:
            f.write(str(value))

    def _is_writable(self, filepath):
        """Check if file is writable. On real EV3 this uses actual permissions.
        Falls back to checking group/other write bits via stat."""
        st = os.stat(filepath)
        mode = st.st_mode
        # Check group or other write bits (real EV3 uses these)
        if mode & 0o022:
            return True
        # On the example tree everything is 644 (owner-writable only).
        # Fall back: owner-writable means writable for our purposes.
        return bool(mode & 0o200)

    def _infer_type(self, raw_content):
        """Infer attribute type from file content."""
        content = raw_content.strip()
        if not content:
            return 'string'
        # Dictionary: lines with KEY=VALUE
        if '\n' in content and '=' in content:
            return 'dict'
        # Array: spaces in content (space-separated values)
        if ' ' in content:
            return 'array'
        # Integer
        try:
            int(content)
            return 'int'
        except ValueError:
            pass
        return 'string'

    def _discover_attributes(self):
        """Scan device directory and build attribute metadata."""
        all_files = []
        for name in os.listdir(self.directory):
            filepath = self._file_path(name)
            if os.path.isfile(filepath) and name not in SKIP_FILES:
                all_files.append(name)

        all_files_set = set(all_files)

        # First pass: identify singular/plural pairs
        plural_files = set()
        for name in all_files:
            singular = name[:-1] if name.endswith('s') else None
            if singular and singular in all_files_set:
                plural_files.add(name)

        # Second pass: build attributes
        for name in sorted(all_files):
            filepath = self._file_path(name)
            raw = self._read_raw(name)
            writable = self._is_writable(filepath)

            if name in plural_files:
                # This is the plural (legal values list) - always read-only array
                self.attributes[name] = Attribute(name, 'array', writable=False)
            elif name + 's' in all_files_set:
                # This is the singular (writable, paired with plural)
                self.attributes[name] = Attribute(name, 'string', writable=True, paired_with=name + 's')
            elif VALUE_RE.match(name):
                # valueN file - type is always int, gated by num_values
                self.attributes[name] = Attribute(name, 'int', writable=False)
            else:
                attr_type = self._infer_type(raw)
                self.attributes[name] = Attribute(name, attr_type, writable=writable)

    def _parse_value(self, raw, attr_type):
        """Parse raw file content according to attribute type."""
        content = raw.rstrip('\n')
        if attr_type == 'int':
            if not content:
                return 0
            try:
                return int(content)
            except ValueError:
                return 0
        elif attr_type == 'array':
            return [item for item in content.split(' ') if item]
        elif attr_type == 'dict':
            result = {}
            for line in raw.split('\n'):
                if '=' in line:
                    k, v = line.split('=', 1)
                    result[k] = v.strip()
            return result
        else:
            return content

    def _should_read_value(self, name, current_values):
        """Check if a valueN attribute should be read, based on num_values."""
        m = VALUE_RE.match(name)
        if not m:
            return True
        index = int(m.group(1))
        num_values = current_values.get('num_values')
        if num_values is None:
            return True
        return index < num_values

    def get(self):
        """Read all readable attributes. Respects num_values gating."""
        result = {}
        writable_keys = []

        # Read num_values first if it exists, so we can gate valueN
        if 'num_values' in self.attributes:
            attr = self.attributes['num_values']
            raw = self._read_raw('num_values')
            result['num_values'] = self._parse_value(raw, attr.attr_type)

        # Read remaining attributes
        for name in sorted(self.attributes.keys()):
            if name == 'num_values':
                continue
            attr = self.attributes[name]
            if not self._should_read_value(name, result):
                continue
            raw = self._read_raw(name)
            result[name] = self._parse_value(raw, attr.attr_type)
            if attr.writable:
                writable_keys.append(name)

        result['__writable'] = writable_keys
        return result

    def post(self, **kwargs):
        """Write to writable attributes. Returns list of modified keys."""
        modified = []
        for name, value in kwargs.items():
            if name not in self.attributes:
                continue
            attr = self.attributes[name]
            if not attr.writable:
                continue
            # Flatten lists (take first element)
            if isinstance(value, list):
                value = value[0] if value else ''
            log.debug('Writing "{}" to "{}".'.format(value, name))
            self._write_raw(name, str(value))
            modified.append(name)
        return modified
