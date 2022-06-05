# -*- coding: UTF-8 -*-


"""Unittests for emoji.core"""

from __future__ import unicode_literals

import random
import re
import emoji
import pytest



def ascii(s):
    # return escaped Code points \U000AB123
    return s.encode("unicode-escape").decode()

def test_non_rgi_zwj():
    #print(emoji.demojize(u'\U0001F468\U0000200D\U0001F469\U0001F3FF\U0000200D\U0001F467\U0001F3FB\U0000200D\U0001F466\U0001F3FE'))
    print(ascii(emoji.demojize(u'\U0001F468\U0000200D\U0001F469\U0001F3FF\U0000200D\U0001F467\U0001F3FB\U0000200D\U0001F466\U0001F3FE')))
    #assert 1 == 2