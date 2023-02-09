from setuptools import setup
from setuptools.command.install_lib import install_lib as _install_lib
from setuptools.command.sdist import sdist as _sdist
from distutils.command.build import build as _build
from distutils.cmd import Command


class compile_translations(Command):
    description = 'compile message catalogs to MO files via django compilemessages'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import os
        import sys
        from django.core.management.commands.compilemessages import Command
        c = Command()
        curdir = os.getcwd()
        os.chdir(os.path.realpath('autocomplete'))
        c.handle(locale=[], exclude=[], ignore_patterns=[], fuzzy=False, verbosity=0)
        os.chdir(curdir)


class build(_build):
    sub_commands = [('compile_translations', None)] + _build.sub_commands


class install_lib(_install_lib):
    def run(self):
        self.run_command('compile_translations')
        _install_lib.run(self)

class sdist(_sdist):
    def run(self):
        self.run_command('compile_translations')
        _sdist.run(self)


setup(
    cmdclass={
        'build': build,
        'install_lib': install_lib,
        'sdist': sdist,
        'compile_translations': compile_translations
    }
)