import os
import re
import glob
import inspect
import random
import string

import requests
import zipfile
import io


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
            return glb[0]

        return None

    def path(self):
        return self._bin

# end of class Bin (Singleton)


class ToolChecker:
    def __init__(self):
        self._bin = Bin()

    def check_tools(self, objects):
        checked = 0
        for obj in objects:
            if not obj.name:
                raise Exception("Can't find the tool name")

            if not self._bin.find(obj.name):
                tool_dir = '/' + re.sub(r'\.[^.]*$', '', re.sub(r'[^A-Za-z0-9._-]', '', obj.name))
                if not obj.url:
                    raise Exception("Can't find the tool URL to install: {}".format(obj.name))
                print('Installing: {}'.format(obj.url), end=" ")

                r = requests.get(obj.url)
                z = zipfile.ZipFile(io.BytesIO(r.content))
                z.extractall(self._bin.path() + tool_dir)

                if self._bin.find(obj.name):
                    print('...OK')
                else:
                    raise Exception("Can't install the tool from: {}".format(obj.url))
            checked += 1

        return checked

# end of class ToolChecker


class SampleInfo:
    class Info:
        def __init__(self):
            self.sample_name = None
            self.chain = None
            self.barcode = None
            self.R1 = None
            self.R2 = None
            self.baseline = None
            self.subject_id = None
            self.antigen = None
            self.reads_exp = None

        def set(self, line):
            line = line.strip()
            fields = re.split(r'\t', line)
            if len(fields) == 9:
                (self.sample_name,
                 self.chain,
                 self.barcode,
                 self.R1, self.R2,
                 self.baseline,
                 self.subject_id,
                 self.antigen,
                 self.reads_exp
                 ) = [field.strip() for field in fields]
                return True
            return False

    # end of class Info()

    def __init__(self, file_name=None):
        self._file = file_name
        self._records = list()

    def find(self, dir_name):
        sample_info = None
        for file_name in glob.glob(re.sub(r'/$', '', dir_name) + '/*[Ss]ample*[Ii]nfo*'):
            if sample_info:
                raise Exception(
                    'It seems there are several SampleInfo files (it needs only one):\n1) {}\n2) {}\n'.format(
                        sample_info, file_name))
            else:
                sample_info = file_name
        self._file = sample_info

        return self._file

    def get_file(self):
        return self._file

    def get_records(self):
        return self._records

    def parse(self):
        if not self._file:
            raise Exception('No SampleInfo file in the directory: {}'.format(self._file))

        n_samples = 0
        with open(self._file, 'r') as file:
            for line in file:
                if re.search(r'\sR1\s+R2\s', line):
                    continue  # skip the file header

                inf = self.Info()
                if not inf.set(line):
                    raise Exception("Wrong record in SampleInfo file: {}\nline:{}".format(self._file, line))
                self._records.append(inf)
                n_samples += 1

        if n_samples == 0:
            raise Exception("Wrong format of SampleInfo file (no any samples): {}".format(self._file))

        return self._records

# end of class SampleInfo


class Tool:
    name = None
    url = None

# end of class Tool


class JavaTool(Tool):
    def __init__(self, path):
        self._jar = (path.find(self.name) or [None])[0]
        self._xmx = Xmx().get()

# end of class JavaTool


class VDJtools(JavaTool):
    name = 'vdjtools*.jar'
    url = 'https://github.com/mikessh/vdjtools/releases/download/1.2.1/vdjtools-1.2.1.zip'

    def __init__(self, outdir='.'):
        super(VDJtools, self).__init__()
        self._outdir = re.sub(r'/$', '', outdir)
        self._vdj_dir = self._outdir + '/vdj'

    def convert(self, dir_name):
        output = ''
        for file_name in glob.glob(re.sub(r'/$', '', dir_name) + '/*clonotypes*.txt'):
            cmd = 'java ' + self._xmx + ' -jar ' + self._jar
            cmd += ' Convert -S mixcr {} {}/{}'.format(file_name, self._vdj_dir, 'vdj')
            stream = os.popen(cmd)
            output += '>{}<\n'.format(file_name) + stream.read()
        return output

    def filter(self, dir_name=None):
        dir_name = dir_name if dir_name else self._vdj_dir

        output = ''
        for file_name in glob.glob(re.sub(r'/$', '', dir_name) + '/vdj.*clonotypes*.txt'):
            cmd = 'java ' + self._xmx + ' -jar ' + self._jar
            cmd += ' FilterNonFunctional {} {}/{}'.format(file_name, self._vdj_dir, 'nc')
            stream = os.popen(cmd)
            output += '>{}<\n'.format(file_name) + stream.read()

        return output

    def get_vdj_dir(self):
        return self._vdj_dir

# end of class VDJtools


class Mixcr(JavaTool):
    name = 'mixcr*.jar'
    url = 'https://github.com/milaboratory/mixcr/releases/download/v3.0.13/mixcr-3.0.13.zip'

    def __init__(self, indir='.', outdir='.'):
        super(Mixcr, self).__init__()
        self._indir = re.sub(r'/$', '', indir)
        self._outdir = re.sub(r'/$', '', outdir)
        self._analyze_dir = self._outdir + '/analyze'

    def analyze(self, assemble_dir):
        assemble_dir = re.sub(r'/$', '', assemble_dir)
        info = SampleInfo()
        if not info.find(self._indir):
            raise Exception('No SampleInfo file in the directory: {}'.format(self._indir))

        os.makedirs(self._analyze_dir, exist_ok=True)

        output = ''
        for record in info.parse():
            cmd = 'java ' + self._xmx + ' -jar ' + self._jar
            cmd += ' analyze amplicon -s hsa --starting-material rna '
            cmd += '--5-end no-v-primers --3-end c-primers --adapters no-adapters --receptor-type {}'.format(
                record.chain
            )
            cmd += ' {}/{}_R1.*.fastq.gz'.format(assemble_dir, record.sample_name)
            cmd += ' {}/{}_R2.*.fastq.gz'.format(assemble_dir, record.sample_name)
            cmd += ' {}/{}'.format(self._analyze_dir, record.sample_name)
            stream = os.popen(cmd)
            output += '>>>{}<<<\n'.format(record.sample_name) + stream.read()

        return output

    def get_analize_dir(self):
        return self._analyze_dir

# end of class Mixcr


class Migec(JavaTool):
    name = 'migec*.jar'
    url = 'https://github.com/mikessh/migec/releases/download/1.2.9/migec-1.2.9.zip'

    def __init__(self, indir='.', outdir='.'):
        super(Migec, self).__init__()
        self._util = None
        self._indir = re.sub(r'/$', '', indir)
        self._outdir = re.sub(r'/$', '', outdir)
        self._checkout_dir = self._outdir + '/checkout'
        self._histogram_dir = self._outdir + '/histogram'
        self._assemble_dir = self._outdir + '/assemble'
        self._barcodes_file = self._inspector()

    def _inspector(self):
        info = SampleInfo()
        if not info.find(self._indir):
            raise Exception('No SampleInfo file in the directory: {}'.format(self._indir))

        barcodes = ''
        for record in info.parse():
            r1 = re.sub(r'.*/', '', record.R1)
            r1 = self._indir + '/' + r1
            r2 = re.sub(r'.*/', '', record.R2)
            r2 = self._indir + '/' + r2

            if record.barcode == '':
                raise Exception("No barcode in SampleInfo file: {}".format(info.get_file()))
            if not os.path.isfile(r1):
                raise Exception("Wrong R1 file name in SampleInfo file: {}".format(info.get_file()))
            if not os.path.isfile(r2):
                raise Exception("Wrong R2 file name in SampleInfo file: {}".format(info.get_file()))

            barcodes += '\t'.join((record.sample_name, record.barcode, '', r1, r2)) + '\n'

        barcodes_file = self._outdir + '/barcodes.csv'
        os.makedirs(self._outdir, exist_ok=True)

        try:
            with open(barcodes_file, 'w') as file:
                file.write(barcodes)
        except IOError:
            print("Can't create barcode file: {}".format(barcodes_file))

        return barcodes_file

    def checkout_batch(self):
        cmd = 'java ' + self._xmx + ' -jar ' + self._jar
        cmd += ' CheckoutBatch -cute {} {}'.format(self._barcodes_file, self._checkout_dir)
        stream = os.popen(cmd)
        output = stream.read()

        return output

    def histogram(self):
        cmd = 'java ' + self._xmx + ' -jar ' + self._jar
        cmd += ' Histogram {} {}'.format(self._checkout_dir, self._histogram_dir)
        stream = os.popen(cmd)
        output = stream.read()

        return output

    def assemble_batch(self, overseq=0, collisions=False):
        cmd = 'java ' + self._xmx + ' -jar ' + self._jar
        cmd += ' AssembleBatch'
        if overseq:
            cmd += ' --force-overseq {}'.format(overseq)
            if collisions:
                cmd += ' --force-collision-filter'
        cmd += ' -c {} {} {}'.format(self._checkout_dir, self._histogram_dir, self._assemble_dir)
        stream = os.popen(cmd)
        output = stream.read()

        return output

    def get_assemble_dir(self):
        return self._assemble_dir

    def draw(self):
        hist = Bin().get('histogram.R')[0]
        cmd = 'cd {}; Rscript {}'.format(self._histogram_dir, hist)
        stream = os.popen(cmd)
        output = stream.read()

        return output

# end of class Migec



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

