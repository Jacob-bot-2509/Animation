
import runpy,sys
from manim.utils import tex_file_writing as _tw
_original = _tw.make_tex_compilation_command
def _command(compiler, output_format, tex_file, tex_dir):
    if compiler != 'latex':
        raise ValueError('Only reviewed latex compiler is permitted')
    command = _original(compiler, output_format, tex_file, tex_dir)
    command[1:1] = ['-disable-installer','-disable-write18']
    return command
_tw.make_tex_compilation_command = _command
runpy.run_module('manim', run_name='__main__', alter_sys=True)
