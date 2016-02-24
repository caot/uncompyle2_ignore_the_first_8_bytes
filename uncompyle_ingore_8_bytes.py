from uncompyle2 import uncompyle, dis

import sys
import os
import getopt
import StringIO


def _load_module(filename, ignore_the_first_8_bytes=False, is_zlib_decompress=False):
    '''
    load a module without importing it
    _load_module(filename: string): code_object
    filename:    name of file containing Python byte-code object
            (normally a .pyc)
    code_object: code_object from this file
    '''

    if is_zlib_decompress:
        fp = filename
    else:
        fp = open(filename, 'rb')

    if not ignore_the_first_8_bytes:
        magic = fp.read(4)
        try:
            version = float(magics.versions[magic])
        except KeyError:
            raise ImportError, "Unknown magic number %s in %s" % (ord(magic[0]) + 256 * ord(magic[1]), filename)
        if (version > 2.7) or (version < 2.5):
            raise ImportError, "This is a Python %s file! Only Python 2.5 to 2.7 files are supported." % version
        # print version
        fp.read(4)  # timestamp
    else:
        version = '%s.%s' % sys.version_info[:2]
        version = float(version)

    co = dis.marshalLoad(fp)
    fp.close()
    print 'version: ', version
    return version, co


def _get_outstream(outfile):
    print 'outfile: ', outfile
    dir = os.path.dirname(outfile)
    failed_file = outfile + '_failed'
    if os.path.exists(failed_file):
        os.remove(failed_file)
    try:
        os.makedirs(dir)
    except OSError:
        pass
    return open(outfile, 'w')


def uncompyle_file(filename, outstream=None, showasm=0, showast=0, ignore_the_first_8_bytes=False, is_zlib_decompress=False):
    '''
    ref: uncompyle2.uncompyle_file

    decompile Python byte-code file (.pyc)
    '''
    version, co = _load_module(filename, ignore_the_first_8_bytes=True, is_zlib_decompress=is_zlib_decompress)
    if type(co) == list:
        for con in co:
            uncompyle(version, con, outstream, showasm, showast)
    else:
        uncompyle(version, co, outstream, showasm, showast)
    co = None


def main(in_base, out_base, files, codes, outfile=None, showasm=0, showast=0, do_verify=0, is_zlib_decompress=False):
    of = None

    if of:  # outfile was given as parameter
        outstream = _get_outstream(outfile)
    elif out_base is None:
        outstream = sys.stdout
    else:
        outfile = os.path.join(out_base, file) + '_dis'
        outstream = _get_outstream(outfile)

    uncompyle_file(files, outstream, ignore_the_first_8_bytes=True, is_zlib_decompress=is_zlib_decompress)


def decompile(files, is_zlib_decompress):
    if sys.version[:3] != '2.7':
        print >>sys.stderr, 'Error:  uncompyle2 requires Python 2.7.'
        sys.exit(-1)

    showasm = showast = do_verify = numproc = recurse_dirs = 0
    outfile = '-'
    out_base = None
    codes = []
    timestamp = True
    timestampfmt = "# %Y.%m.%d %H:%M:%S %Z"

    in_base = None
    out_base = None
    src_base = None

    main(src_base, out_base, files, codes, outfile, showasm, showast, do_verify, is_zlib_decompress)


def decompile_zlib_decompress(zlib_decompress):
    '''
    StringIO — Read and write strings as files

    This module implements a file-like class, StringIO, that reads and writes a 
    string buffer (also known as memory files). See the description of file 
    objects for operations (section File Objects). (For standard strings, see 
    str and unicode.)
    '''
    fio = cStringIO.StringIO(zlib_decompress)
    is_zlib_decompress = True

    decompile(fio, is_zlib_decompress)
    fio.close()
