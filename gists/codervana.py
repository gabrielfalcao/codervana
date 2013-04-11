# -*- coding: utf-8 -*-

# ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ

# vakratunda mahaakaaya suryakoti samaprabhaa

# nirvighnam kurumedeva sarvakaaryeshu sarvadaa

# ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ


# Salutations to the supreme Lord Ganesh, whose curved trunk and
# massive body shines like a million suns and showers his blessings on
# everyone.

# Oh my lord of lords Ganesh, kindly remove all obstacles, always and
# forever from all my activities and endeavors.

#                            _.!._
#                           /O*@*O\
#                          <\@(_)@/>
#                 ,;,   .--;`     `;--.   ,
#                 O@O_ /   |d     b|   \ _hnn
#                 | `/ \   |       |   / \` |
#                 &&&&  :ॐॐ;\     /;ॐॐ;  &&&&
#                 |  \ / `ॐॐ/|   |ॐॐ'  \ /  |
#                 \   %%%%`</|   |ॐ'`%%%%   /
#                  '._|_ \   |   |'  / _|_.'
#                    _/  /   \   \   \  \
#                   / (\(     '.  '-._&&&&
#                  (  ()ॐॐ,    o'--.._`\-)
#                   '-():`ॐॐॐॐॐॐॐॐॐॐ'()()()
#                    /:::::/()`Y`()\:::::\
#                    \::::( () | () )::::/
#                     `"""`\().'.()/'"""`

# ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ ॐ

from __future__ import unicode_literals

import os
import sys
import logging
import requests
import requests_cache

from functools import partial
from urlparse import urlsplit
from os.path import join, abspath, dirname, relpath


LOCAL_FILE = lambda *path: join(abspath(dirname(__file__)), *path)
REPOSITORIES_ROOT = LOCAL_FILE('repos')
REPO_FILE = lambda *path: join(REPOSITORIES_ROOT, *path)


log = logging.getLogger('codervana')
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler(sys.stdout))


def makedirs(path):
    try:
        os.makedirs(path)
        return True
    except OSError:
        return False


class GithubEndpoint(object):
    base_url = u'https://api.github.com'

    def __init__(self, token):
        self.token = token
        self.headers = {
            'authorization': 'token {0}'.format(token),
            'X-GitHub-Media-Type: github.beta': 'github.beta'
        }

    def full_url(self, path):
        url = u"/".join([self.base_url, path.lstrip('/')])
        log.debug("[GithubEndpoint.full_url] %s", url)
        return url

    def retrieve(self, path, data=None):
        log.debug("[GithubEndpoint.retrieve] GET %s with %s", path, str(path))
        return self.json(requests.get(
            self.full_url(path),
            data=data or {},
            headers=self.headers,
        ))

    def save(self, path, data=None):
        log.debug("[GithubEndpoint.save] PUT %s with %s", path, str(path))
        return self.json(requests.put(
            self.full_url(path),
            headers=self.headers,
        ))

    def json(self, response):
        log.debug("[GithubEndpoint.json] got response %s (%s)", str(response.status_code), str(response.headers))
        return response.json()


class LocalStem(object):
    # mode = "100644"
    # path = "README.md"
    # sha = "9b21a51f0ed2604c3000b82c8c76c505fe852565"
    # size = 3820 if type == "blob"
    # type = "blob" or "tree"
    # url = "https://api.github.com/.../git/blobs/9b21a51.."
    size = 0

    def __init__(self, stem, api):
        self.__dict__.update(stem)
        self.api = api
        self.data = {}

        self.is_tree = (self.type == 'tree')
        self.is_blob = (self.type == 'blob')
        self.children = []

    def fetch(self):
        if self.data:
            # caching, baby
            return self.data

        path = urlsplit(self.url).path
        reply = self.api.retrieve(path)
        if self.is_tree:
            contents = reply['tree']
        elif self.is_blob:
            contents = reply['content'].decode(reply['encoding'])

        return reply, contents

    def create_directory(self, path):
        makedirs(path)

    def create_blob(self, path, data):
        with open(path, 'wb') as f:
            f.write(data)

    def exists(self, destination):
        in_disk = os.path.exists(destination)
        is_file = in_disk and not os.path.isdir(destination)
        in_disk_size = is_file and os.stat(destination).st_size or 0
        return in_disk and in_disk_size == self.size

    def __repr__(self):
        return '<LocalStem path="{path}", type="{type}", sha="{sha}">'.format(**self.__dict__)

    def persist(self, root):
        destination = join(root, self.path)
        if self.is_blob and self.exists(destination):
            log.info("[LocalStem.persist] \033[1;32mIgnoring existing \033[1;37m%s\033[0m %s", self.type.upper(), relpath(destination))
            return

        meta, contents = self.fetch()

        make_stem = partial(LocalStem, api=self.api)

        if self.is_tree:
            log.info("[LocalStem.persist] \033[1;33mCreating Tree\033[0m %s as %s", self.sha, relpath(destination))
            self.create_directory(destination)

            for kernel in map(make_stem, contents):
                log.info("[LocalStem.persist] \033[1;31mFetching subtrees\033[0m of %s at %s", self.sha, relpath(destination))
                kernel.persist(destination)
                self.children.append(kernel)

        elif self.is_blob:
            log.info("[LocalStem.persist] \033[1;34mPersisting blob\033[0m %s as %s", self.sha, relpath(destination))
            self.create_blob(destination, contents)


class RepositoryFetcher(object):
    def __init__(self, api):
        self.api = api

        self.owner = None
        self.repository = None

    @property
    def destination(self):
        return join(*filter(bool, [REPOSITORIES_ROOT, self.owner, self.repository]))

    def fetch(self, owner, repository, tree='HEAD'):
        self.owner = owner
        self.repository = repository
        self.grab_tree(tree)

    def api_path(self, prefix, *path):
        return "/{0}".format(join(prefix, self.owner, self.repository, *path).lstrip(os.sep))

    def grab_tree(self, tree):
        path = self.api_path('repos', 'git', 'trees', tree)
        reply = self.api.retrieve(path)
        sha = reply.get('sha', None)
        if sha != tree:
            raise RuntimeError("reply got SHA {0} but expected {1}".format(sha, tree))

        make_stem = partial(LocalStem, api=self.api)

        makedirs(self.destination)
        for stem in map(make_stem, reply['tree']):
            stem.persist(self.destination)


makedirs(REPOSITORIES_ROOT)
api = GithubEndpoint("55f225146ced2eeb28352c5697495f05429429be")

requests_cache.install_cache()
fetcher = RepositoryFetcher(api)
fetcher.fetch("gabrielfalcao", "lettuce")
