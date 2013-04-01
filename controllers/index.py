#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from shrine.web import get
from shrine.conf import settings
from django.db import models


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


make_choices = lambda: list(set(filter(lambda x: len(x) > 3 and len(x) < 10 and x.isalnum() and x[0].upper() == x[0], dir(models))))


class Hotspot(object):
    def __init__(self, data, CHOICES=[]):
        self.grade, self.css_class = data.items()[0]
        name = random.choice(CHOICES)
        CHOICES.remove(name)
        self.name = 'django.db.models.{0}'.format(name)

    @property
    def url(self):
        return '#'


@get('^/$')
def index(controller):
    controller.redirect('/Yipit/yipit-merchants/feed')


@get(project_route())
def project(controller, owner, project):
    controller.redirect('/'.join([owner, project, 'feed']))


@get(project_route('feed'))
def feed(controller, owner, project):
    grades = [
        {'A': 'violet'},
        {'B': 'purple'},
        {'C': 'blue'},
        {'D': 'green'},
        {'E': 'orange'},
        {'F': 'red'},
    ]

    CHOICES = make_choices()

    context = {
        'project': Project(project, owner=ProjectOwner(owner)),
        'hotspots': [Hotspot(random.choice(grades), CHOICES) for x in range(8)],

    }
    controller.render('feed.html', **context)


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
