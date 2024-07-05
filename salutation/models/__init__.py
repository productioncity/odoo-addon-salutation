# -*- coding: utf-8 -*-
from . import models

def post_load_hook():
    models.post_load_hook()

def pre_init_check(cr):
    models.pre_init_check(cr)

def post_init_hook(env):
    models.post_init_hook(env)
