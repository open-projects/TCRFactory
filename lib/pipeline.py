from lib.inout import Bin, Xmx
from lib.tools import VDJtools, Mixcr, Migec


class Pipe:
    def __init__(self):
        self._bin = Bin()
        self._xmx = Xmx()

    def execute(self, log):
        raise Exception("Can't execute the pipeline")

# end of class Pipe


class MiSeqPipe(Pipe):
    def __init__(self):
        ...

    def execute(self, log):
        ...

# end of class MiSeqPipe


class NextSeqPipe(Pipe):
    def __init__(self):
        ...

    def execute(self, log):
        ...

# end of class NextSeqPipe

