from lib.inout import Bin, Xmx
from lib.tools import VDJtools, Mixcr, Migec, MigecHistogram


class Pipe:
    def __init__(self):
        self._bin = Bin()
        self._xmx = Xmx()
        self._tools = {}

    def execute(self, log):
        raise Exception("Can't execute the pipeline.")

    def check(self):
        if len(self._tools) > 0:
            for tool in self._tools.values():
                tool.check()
        else:
            raise Exception("The empty pipeline.")

# end of class Pipe


class MiSeqPipe(Pipe):
    def __init__(self, in_dir, out_dir):
        super(MiSeqPipe, self).__init__()
        self._tools['migec'] = Migec(in_dir, out_dir)
        self._tools['mixcr'] = Mixcr(in_dir, out_dir)
        self._tools['vdjtools'] = VDJtools(out_dir)
        self._tools['migec_hist'] = MigecHistogram()
        self._overseq = None
        self._collisions = None


    def set_overseq(self, overseq):
        self._overseq = overseq

    def set_collisions(self, collisions):
        self._collisions = collisions

    def execute(self, log):
        try:
            log.add('====================MIGEC====================\n')
            migec = self._tools['migec']
            log.add('>>>CheckoutBatch<<<\n' + migec.checkout_batch())
            log.add('>>>Histogram<<<\n' + migec.histogram())
            log.add('>>>HistogramDrawing<<<\n' + migec.draw())
            log.add('>>>AssembleBatch<<<\n' + migec.assemble_batch(self._overseq, self._collisions))
        except Exception as error:
            log.add('\nMIGEC error:\n{}'.format(error))
            log.write()
            exit('...error')

        try:
            log.add('\n====================MIXCR====================\n')
            mixcr = self._tools['mixcr']
            log.add('>>>Analyze<<<\n' + mixcr.analyze(migec.get_assemble_dir()))
        except Exception as error:
            log.add('\nMIXCR error:\n{}'.format(error))
            log.write()
            exit('...error')

        try:
            log.add('\n====================VDJtools==================\n')
            vdjtools = self._tools['vdjtools']
            log.add('>>>Convert<<<\n' + vdjtools.convert(mixcr.get_analyze_dir()))
            log.add('>>>Filter<<<\n' + vdjtools.filter())
        except Exception as error:
            log.add('\nVDJtools error:\n{}'.format(error))
            log.write()
            exit('...error')

        log.add('\n...done')
        log.write()

# end of class MiSeqPipe


class NextSeqPipe(Pipe):
    def __init__(self, in_dir, out_dir):
        super(NextSeqPipe, self).__init__()
        self._tools['migec'] = Migec(in_dir, out_dir)
        self._tools['mixcr'] = Mixcr(in_dir, out_dir)
        self._tools['vdjtools'] = VDJtools(out_dir)
        self._tools['migec_hist'] = MigecHistogram()
        self._overseq = None
        self._collisions = None

    def set_overseq(self, overseq):
        self._overseq = overseq

    def set_collisions(self, collisions):
        self._collisions = collisions

    def execute(self, log):
        try:
            log.add('====================MIGEC====================\n')
            migec = self._tools['migec']
            log.add('>>>CheckoutBatch<<<\n' + migec.checkout_batch())
            log.add('>>>Histogram<<<\n' + migec.histogram())
            log.add('>>>HistogramDrawing<<<\n' + migec.draw())
            log.add('>>>AssembleBatch<<<\n' + migec.assemble_batch(self._overseq, self._collisions))
        except Exception as error:
            log.add('\nMIGEC error:\n{}'.format(error))
            log.write()
            exit('...error')

        try:
            log.add('\n====================MIXCR====================\n')
            mixcr = self._tools['mixcr']
            log.add('>>>Align<<<\n' + mixcr.align(migec.get_assemble_dir()))
            log.add('>>>Assemble<<<\n' + mixcr.assemble(mixcr.get_alignment_dir()))
            log.add('>>>ExportClones<<<\n' + mixcr.export(mixcr.get_clones_dir()))
        except Exception as error:
            log.add('\nMIXCR error:\n{}'.format(error))
            log.write()
            exit('...error')

        try:
            log.add('\n====================VDJtools==================\n')
            vdjtools = self._tools['vdjtools']
            log.add('>>>Convert<<<\n' + vdjtools.convert(mixcr.get_clones_dir()))
            log.add('>>>Filter<<<\n' + vdjtools.filter())
        except Exception as error:
            log.add('\nVDJtools error:\n{}'.format(error))
            log.write()
            exit('...error')

        log.add('\n...done')
        log.write()

# end of class NextSeqPipe

