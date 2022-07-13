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


import json
import os

from dependency import Dependency


# -- Classes
class Boxfile:
    """Read and parse a toybox config file."""

    def __init__(self, boxfile_folder):
        """Read the Boxfile for the current folder."""

        self.boxfile_path = os.path.join(boxfile_folder, 'Boxfile')
        self.dependencies = []

        if not os.path.exists(self.boxfile_path):
            # -- If we can't find it we may still create it later.
            return

        json_content = None

        try:
            with open(self.boxfile_path, 'r') as file:
                json_content = json.load(file)
        except Exception as e:
            raise SyntaxError('Malformed JSON in Boxfile \'' + self.boxfile_path + '\'.\n' + str(e) + '.')
        except KeyboardInterrupt:
            pass

        if json_content is None:
            return

        for key in json_content.keys():
            self.addDependency(key, json_content[key])

    def addDependency(self, url, at):
        new_dependency = Dependency(url, at)

        for dep in self.dependencies:
            if dep.url == new_dependency.url:
                raise SyntaxError('Dependency for URL \'' + dep.url + '\' already exists.')

        self.dependencies.append(new_dependency)

    def removeDependency(self, url):
        for dep in self.dependencies:
            if dep.url == url:
                dep.deleteFolder()

                self.dependencies.remove(dep)

                return

        raise SyntaxError('Couldn\'t find any dependency for URL \'' + dep.url + '\'.')

    def save(self):
        json_content = {}

        for dep in self.dependencies:
            if dep.url in json_content:
                raise SyntaxError('Found two entries for URL \'' + dep.url + '\' when saving Boxfile.')

            json_content[dep.url] = dep.at

        out_file = open(self.boxfile_path, 'w')
        json.dump(json_content, out_file, indent=4)

        out_file.close()
