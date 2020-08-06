import neovim
import sys


@neovim.plugin
class Main(object):
    def __init__(self, vim):
        self.vim = vim

    @neovim.function('QimMain')
    def qimMain(self, args):
        ver = sys.version
        self.vim.command(f'echo "{ver}"')
