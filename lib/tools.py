import os
import re
import glob

import requests
import zipfile
import io
import subprocess

from lib.inout import Bin, Xmx


class SampleInfo:
    class Record:
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

    # end of class Record

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
                line = line.strip()
                if len(line) > 0:
                    if re.search(r'\sR1\s+R2\s', line):
                        continue  # skip the file header

                    inf = self.Record()
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

    def check(self):
        if not self.name:
            raise Exception("Can't check the tool: the tool name is not determined.")
        raise Exception("Can't check the tool {}: the tool checker is not determined.".format(self.name))

# end of class Tool


class RTool(Tool):
    def check(self):
        rchk = ['Rscript']
        chk = ['Rscript', '-e', 'library({})'.format(self.name)]
        inst = ['Rscript', '-e', 'install.packages("{}", repos="{}")'.format(self.name, self.url)]

        process = subprocess.Popen(rchk, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if not (re.search(r'Usage:', stdout.decode('utf-8')) or re.search(r'Usage:', stderr.decode('utf-8'))):
            raise Exception("Rscript doesn't install")

        process = subprocess.Popen(chk, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if re.search(r'[Ee]rror', stdout.decode('utf-8')) or re.search(r'[Ee]rror', stderr.decode('utf-8')):
            print('Installing: {} from {}'.format(self.name, self.url), end=" ")
            subprocess.Popen(inst, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            process = subprocess.Popen(chk, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if re.search(r'[Ee]rror', stdout.decode('utf-8')) or re.search(r'[Ee]rror', stderr.decode('utf-8')):
                raise Exception("Can't install the tool from: {}".format(self.url))
            print('...OK')

# end of class RTool


class JavaTool(Tool):
    def __init__(self):
        self._xmx = Xmx().get()
        self._bin = Bin()
        self._assign_tool()

    def _assign_tool(self):
        self._jar = self._bin.find(self.name) or None

    def check(self):
        if not self.name:
            raise Exception("Can't check the tool: the tool name is not determined.")

        if not self._bin.find(self.name):
            tool_dir = '/' + re.sub(r'\.[^.]*$', '', re.sub(r'[^A-Za-z0-9._-]', '', self.name))
            if not self.url:
                raise Exception("Can't find the tool URL to install: {}".format(self.name))
            print('Installing: {}'.format(self.url), end=" ")

            r = requests.get(self.url)
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall(self._bin.path() + tool_dir)
            self._assign_tool()

            if self._jar:
                print('...OK')
            else:
                raise Exception("Can't install the tool from: {}".format(self.url))

# end of class JavaTool


class UtilFile(Tool):
    def __init__(self):
        self._bin = Bin()

    def check(self):
        if not self.name:
            raise Exception("Can't check the tool: the tool name is not determined.")

        if not self._bin.find(self.name):
            if not self.url:
                raise Exception("Can't find the tool URL to install: {}".format(self.name))
            print('Installing: {}'.format(self.url), end=" ")

            file_path = self._bin.path() + '/' + self.name
            r = requests.get(self.url, allow_redirects=True)
            with open(file_path, 'wb') as f:
                f.write(r.content)

            if self._bin.find(self.name):
                print('...OK')
            else:
                raise Exception("Can't install the tool from: {}".format(self.url))

# end of class GitHubFolder


class GGplot2(RTool):
    name = 'ggplot2'
    url = 'https://cran.rstudio.com'

# end of class GGplot2


class Reshape(RTool):
    name = 'reshape'
    url = 'https://cran.rstudio.com'

# end of class Reshape


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
        self._alignment_dir = self._outdir + '/alignment'
        self._clones_dir = self._outdir + '/clones'

    def analyze(self, in_dir):
        in_dir = re.sub(r'/$', '', in_dir)
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
            cmd += ' {}/{}_R1.*.fastq.gz'.format(in_dir, record.sample_name)
            cmd += ' {}/{}_R2.*.fastq.gz'.format(in_dir, record.sample_name)
            cmd += ' {}/{}'.format(self._analyze_dir, record.sample_name)
            stream = os.popen(cmd)
            output += '>>>{}<<<\n'.format(record.sample_name) + stream.read()

        return output

    def align(self, in_dir):
        in_dir = re.sub(r'/$', '', in_dir)
        info = SampleInfo()
        if not info.find(self._indir):
            raise Exception('No SampleInfo file in the directory: {}'.format(self._indir))

        os.makedirs(self._alignment_dir, exist_ok=True)

        output = ''
        for record in info.parse():
            cmd = 'java ' + self._xmx + ' -jar ' + self._jar
            cmd += ' align -OreadsLayout=Collinear -s hsa'  # Collinear - relative orientation of paired reads
            cmd += ' -r {}/alignmentReport.txt '.format(self._alignment_dir)
            cmd += ' {}/{}_R1.*.fastq.gz'.format(in_dir, record.sample_name)
            cmd += ' {}/{}_R2.*.fastq.gz'.format(in_dir, record.sample_name)
            cmd += ' {}/{}_alignments.vdjca'.format(self._alignment_dir, record.sample_name)
            stream = os.popen(cmd)
            output += '>>>{}<<<\n'.format(record.sample_name) + stream.read()

        return output

    def assemble(self, in_dir):
        in_dir = re.sub(r'/$', '', in_dir)
        info = SampleInfo()
        if not info.find(self._indir):
            raise Exception('No SampleInfo file in the directory: {}'.format(self._indir))

        os.makedirs(self._clones_dir, exist_ok=True)

        output = ''
        for record in info.parse():
            cmd = 'java ' + self._xmx + ' -jar ' + self._jar
            cmd += ' assemble -r {}/assembleReport.txt '.format(self._clones_dir)
            cmd += ' {}/{}_alignments.vdjca'.format(in_dir, record.sample_name)
            cmd += ' {}/{}_clonotypes.clns'.format(self._clones_dir, record.sample_name)
            stream = os.popen(cmd)
            output += '>>>{}<<<\n'.format(record.sample_name) + stream.read()

        return output

    def export(self, in_dir):
        in_dir = re.sub(r'/$', '', in_dir)
        info = SampleInfo()
        if not info.find(self._indir):
            raise Exception('No SampleInfo file in the directory: {}'.format(self._indir))

        output = ''
        for record in info.parse():
            cmd = 'java ' + self._xmx + ' -jar ' + self._jar
            cmd += ' exportClones -t -o -c {}'.format(record.chain)
            cmd += ' {}/{}_clonotypes.clns'.format(self._clones_dir, record.sample_name)
            cmd += ' {}/{}_clonotypes.txt'.format(self._clones_dir, record.sample_name)
            stream = os.popen(cmd)
            output += '>>>{}<<<\n'.format(record.sample_name) + stream.read()

        return output

    def get_analyze_dir(self):
        return self._analyze_dir

    def get_alignment_dir(self):
        return self._alignment_dir

    def get_clones_dir(self):
        return self._clones_dir

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
        if not self._barcodes_file:
            raise Exception('Migec CheckoutBatch: no barcodes file.')

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
        hist = Bin().find(MigecHistogram.name)
        cmd = 'cd {}; Rscript {}'.format(self._histogram_dir, hist)
        stream = os.popen(cmd)
        output = stream.read()

        return output

# end of class Migec


class MigecHistogram(UtilFile):
    name = 'histogram.R'
    url = 'https://github.com/mikessh/migec/blob/master/util/histogram.R?raw=true'

