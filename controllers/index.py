#!/usr/bin/env python
# -*- coding: utf-8 -*-
from shrine.web import get
from shrine.conf import settings


class ProjectOwner(object):
    def __init__(self, name):
        self.name = name


def project_route(path=''):
    return '/(?P<owner>[\w_-]+)/(?P<project>[\w_-]+){0}'.format("/" + path.lstrip('/'))


class Project(object):
    Owner = ProjectOwner

    def __init__(self, name, owner):
        self.name = name
        self.owner = owner

    def url(self, *args):
        return '/'.join(['/', settings.DOMAIN, self.owner.name, self.name] + list(args))


@get('^/$')
def index(controller):
    controller.redirect('/Yipit/yipit-merchants/feed')


@get(project_route())
def project(controller, owner, project):
    controller.redirect('/'.join([owner, project, 'feed']))


@get(project_route('feed'))
def feed(controller, owner, project):
    controller.render('feed.html',
                      project=Project(project, owner=ProjectOwner(owner)))


@get(project_route('code'))
def code(controller, owner, project):
    controller.render('code.html',
                      project=Project(project, owner=ProjectOwner(owner)))


@get(project_route('scoreboard'))
def scoreboard(controller, owner, project):
    controller.render('scoreboard.html',
                      project=Project(project, owner=ProjectOwner(owner)))


@get(project_route('ci'))
def continuous_integration(controller, owner, project):
    controller.render('continuous-integration.html',
                      project=Project(project, owner=ProjectOwner(owner)))


@get('/robots.txt')
def robots(controller, *args, **kw):
    controller.set_header('Cache-Control', 'public, max-age=86400')  # 24hrs
    controller.finish("User-agent: *\nDisallow: /")
