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


# -- Classes
class Dependency:
    """A helper class for toybox dependencies."""

    def __init__(self, url, at):
        """Create a dependency given a URL and a tag or branch."""

        self.at = at
        self.url = url

        if not self.url.endswith('.git'):
            self.url = self.url + '.git'

        if not self.url.startswith('http://'):
            if not self.url.startswith('https'):
                # -- Let's make sure there is a .com,.net,etc.. before the first slash in the path.
                # -- Github usernames cannot have dots in them so testing like this should be ok.
                first_dot_index = self.url.find('.')
                first_slash_index = self.url.find('/')

                if first_dot_index < 0 or first_dot_index > first_slash_index:
                    # -- We assume a url with no server is one from Github.
                    if not self.url.startswith('/'):
                        self.url = '/' + self.url

                    self.url = 'https://github.com' + self.url
                else:
                    self.url = 'https://' + self.url

        # -- We find the first slash after the http part of the URL.
        first_slash_index = self.url.find('/', 8)

        if first_slash_index < 1:
            raise SyntaxError('Malformed dependency URL \'' + url + '\' in Boxfile.')

        self.username = self.url[first_slash_index + 1:]

        first_slash_index = self.username.find('/')

        if first_slash_index < 1:
            raise SyntaxError('Malformed dependency URL \'' + url + '\' in Boxfile.')

        self.repo_name = self.username[first_slash_index + 1:-4]
        self.username = self.username[:first_slash_index]
        self.folder = self.username + '/' + self.repo_name

    def printInfo(self):
        print('       - ' + self.url + ' @ ' + self.at)