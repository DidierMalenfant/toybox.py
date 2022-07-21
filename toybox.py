#!/usr/bin/env python3
#
# Copyright 2022 by Didier Malenfant.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import getopt
import sys
import os
import shutil

from boxfile import Boxfile
from dependency import toyboxesFolder


# -- Constants
VERSION_NUMBER = '0.0.1'


# -- Functions
def printVersion():
    print('🧸 toybox.py v' + VERSION_NUMBER)


def printUsage():
    printVersion()
    print('Usage:')
    print('    toybox help                      - Show a help message.')
    print('    toybox version                   - Get the Toybox version.')
    print('    toybox info                      - Describe your dependency set.')
    print('    toybox add <dependency>          - Add a new dependency.')
    print('    toybox remove <dependency>       - Remove a dependency.')
    print('    toybox update                    - Update all the dependencies.')
    print('    toybox update <dependency>       - Update a single dependency.')


def boxfileFolder():
    return os.getcwd()


def toyboxesBackupFolder():
    return toyboxesFolder() + '.backup'


def backupToyboxes():
    toyboxes_folder = toyboxesFolder()
    toyboxes_backup_folder = toyboxesBackupFolder()
    if os.path.exists(toyboxes_folder):
        shutil.move(toyboxes_folder, toyboxes_backup_folder)


def restoreToyboxesBackup():
    toyboxes_folder = toyboxesFolder()
    if os.path.exists(toyboxes_folder):
        shutil.rmtree(toyboxes_folder)

    toyboxes_backup_folder = toyboxesBackupFolder()
    if os.path.exists(toyboxes_backup_folder):
        shutil.move(toyboxes_backup_folder, toyboxes_folder)


def deleteToyboxesBackup():
    toyboxes_backup_folder = toyboxesBackupFolder()
    if os.path.exists(toyboxes_backup_folder):
        shutil.rmtree(toyboxes_backup_folder)


# -- Classes
class ArgumentError(Exception):
    """Error caused when command line arguments have something wrong in them."""
    pass


class Toybox:
    """A dependency management system for Lua on the Playdate."""
    """Based on toybox by Jeremy McAnally (https://github.com/jm/toybox)."""

    def __init__(self, args):
        """Initialise toybox based on user configuration."""

        try:
            # -- Gather the arguments
            opts, other_arguments = getopt.getopt(args, '')

            if len(other_arguments) == 0:
                raise SyntaxError('Expected a command!  Maybe start with `toybox help`?')

            number_of_arguments = len(other_arguments)

            self.argument = None

            i = 0
            self.command = other_arguments[i]
            i += 1

            if i != number_of_arguments:
                self.argument = other_arguments[i]
                i += 1

            if i != number_of_arguments:
                raise SyntaxError('Too many commands on command line.')

        except getopt.GetoptError:
            raise ArgumentError('Error reading arguments.')
        except KeyboardInterrupt:
            pass

    def main(self):
        switch = {
            'help': printUsage,
            'version': printVersion,
            'info': self.printInfo,
            'add': self.addDependency,
            'remove': self.removeDependency,
            'update': self.update
        }

        if self.command is None:
            print('No command found.\n')
            self.printUsage()
            return

        if self.command not in switch:
            raise ArgumentError('Unknow command \'' + self.command + '\'.')

        switch.get(self.command)()

    def printInfo(self):
        box_file = Boxfile(boxfileFolder())
        if len(box_file.dependencies) == 0:
            print('Boxfile is empty.')
        else:
            for dep in box_file.dependencies:
                print('       - ' + dep.description())

    def addDependency(self):
        if self.argument is None:
            raise SyntaxError('Expected an argument to \'add\' command.')

        at = 'HEAD'

        box_file = Boxfile(boxfileFolder())
        box_file.addDependency(self.argument, at)
        box_file.save()

        print('Added a dependency for \'' + self.argument + '\' at \'' + at + '\'.')

    def removeDependency(self):
        if self.argument is None:
            raise SyntaxError('Expected an argument to \'remove\' command.')

        box_file = Boxfile(boxfileFolder())
        box_file.removeDependency(self.argument)
        box_file.save()

        print('Removed a dependency for \'' + self.argument + '\'.')

    def installDependency(self, dep):
        print('Installing \'' + dep.description() + '\'.')
        dep.install()

        box_file = Boxfile(dep.folder())
        for child_dep in box_file.dependencies:
            self.installDependency(child_dep)

        self.dependencies.append(dep)

    def update(self):
        if self.argument is not None:
            raise SyntaxError('Currently not implemented.')

        self.dependencies = []

        backupToyboxes()

        try:
            box_file = Boxfile(boxfileFolder())
            for dep in box_file.dependencies:
                self.installDependency(dep)
        except Exception:
            restoreToyboxesBackup()
            raise

        deleteToyboxesBackup()

        print('Finished.')


def main():
    try:
        # -- Remove the first argument (which is the script filename)
        Toybox(sys.argv[1:]).main()
    except ArgumentError as e:
        print(str(e) + '\n')
        printUsage()
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        print('Execution interupted by user.')
        pass


if __name__ == '__main__':
    main()
