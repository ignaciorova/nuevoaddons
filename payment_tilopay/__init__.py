# -*- coding: utf-8 -*-
#################################################################################
# Author      : ABL Solutions.
# Copyright(c): 2017-Present ABL Solutions.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#################################################################################
from . import models
from . import controllers

from odoo.addons.payment import setup_provider, reset_payment_provider


def post_init_hook(env):
    setup_provider(env, 'tilopay')


def uninstall_hook(env):
    reset_payment_provider(env, 'tilopay')