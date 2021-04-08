import re
import os
import inspect
import glob


class Bin:
    def __new__(cls, bin_dir=None):
        if not hasattr(cls, 'instance'):
            if bin_dir:
                cls._bin = re.sub(r'/$', '', bin_dir)
            else:
                previous_frame = inspect.currentframe().f_back  # find the caller
                (filename, line_number, function_name, lines, index) = inspect.getframeinfo(previous_frame)
                real_path = os.path.dirname(filename)
                cls._bin = re.sub(r'/$', '', real_path) + '/bin'
            os.makedirs(cls._bin, exist_ok=True)
            cls.instance = super(Bin, cls).__new__(cls)

        return cls.instance

    def find(self, file_name):
        path = self._bin + '/**/' + re.sub(r'^/', '', file_name)
        glb = glob.glob(path, recursive=True)
        if len(glb) > 0:
            return os.path.abspath(glb[0])

        return None

    def path(self):
        return self._bin

# end of class Bin (Singleton)


class Xmx:
    def __new__(cls, mem='8G'):
        if not re.search(r'^\d+[GM]$', mem):
            raise Exception("Wrong value of memory usage limit: {} (default value is '8G')".format(mem))
        if not hasattr(cls, 'instance'):
            cls._mem = mem
            cls.instance = super(Xmx, cls).__new__(cls)

        return cls.instance

    def get(self):
        xmx = '-Xmx' + self._mem

        return xmx

# end of class Xmx (Singleton)


class Log:
    def __init__(self, log_file=None):
        self._file_name = log_file
        self._log = ''

    def add(self, string):
        self._log += string if re.search(r'\n$', string) else string + "\n"

    def write(self):
        if self._file_name:
            with open(self._file_name, "w") as lg:
                lg.write(self._log)

# end of class Log

