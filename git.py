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


import subprocess


# -- Classes
class Git:
    """Utility methods for git repos."""

    def __init__(self, url):
        """Setup access to the git repo at url."""

        self.url = url

    def gitIn(self, arguments, folder):
        commands = ['git'] + arguments.split()
        commands.append(self.url)

        if folder is not None:
            commands.append(folder)

        try:
            process = subprocess.Popen(commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                if str(stdout).startswith('b"usage: git'):
                    # -- git is giving us the usage info back it seems.
                    raise SyntaxError('Invalid git command line')
                else:
                    # -- Or maybe something else went wrong.
                    raise RuntimeError('Error running git: ' + str(stderr)[2:-1].split('\\n')[0])

            # -- Output is bracketed with b'' when converted from bytes.
            return str(stdout)[2:-1]
        except Exception as e:
            raise RuntimeError(str(e))
        except KeyboardInterrupt:
            pass

    def git(self, arguments):
        self.git(arguments, None)

    def listBranches(self):
        branches = []
        refs = self.git('ls-remote --refs').split('\\n')
        for ref in refs:
            last_slash_index = ref.rfind('/')
            if last_slash_index >= 0:
                branches.append(ref[last_slash_index + 1:])

    def listTags(self, name):
        tags = []
        refs = self.git('ls-remote --tags').split('\\n')
        for ref in refs:
            last_slash_index = ref.rfind('/')
            if last_slash_index >= 0:
                tags.append(ref[last_slash_index + 1:])

    def isABranch(self, name):
        for branch in self.listBranches():
            if branch == name:
                return True

        return False

    def isATag(self, name):
        for tag in self.listTags():
            if tag == name:
                return True

        return False

    def cloneIn(self, tag, folder):
        self.gitIn('clone --quiet --depth 1  --branch ' + tag, folder)
