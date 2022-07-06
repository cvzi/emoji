# -*- coding: UTF-8 -*-


"""
emoji for Python
~~~~~~~~~~~~~~~~

emoji terminal output for Python.

    >>> import emoji
    >>> print(emoji.emojize('Python is :thumbsup:', use_aliases=True))
    Python is 👍
    >> print(emoji.emojize('Python is :thumbs_up:'))
    Python is 👍
"""


from emoji.core import *
from emoji.unicode_codes import *

__all__ = [
    # emoji.core
    'emojize', 'demojize', 'get_emoji_regexp', 'emoji_count', 'emoji_lis',
    'replace_emoji', 'version',
    # emoji.unicode_codes
    'EMOJI_UNICODE_ENGLISH', 'EMOJI_UNICODE_SPANISH', 'EMOJI_UNICODE_PORTUGUESE',
    'EMOJI_UNICODE_ITALIAN', 'EMOJI_UNICODE_FRENCH', 'EMOJI_UNICODE_GERMAN',
    'UNICODE_EMOJI_ENGLISH', 'UNICODE_EMOJI_SPANISH', 'UNICODE_EMOJI_PORTUGUESE',
    'UNICODE_EMOJI_ITALIAN', 'UNICODE_EMOJI_FRENCH', 'UNICODE_EMOJI_GERMAN',
    'EMOJI_ALIAS_UNICODE_ENGLISH', 'UNICODE_EMOJI_ALIAS_ENGLISH', 'EMOJI_DATA',
]

__version__ = '1.6.1'
__author__ = 'Taehoon Kim, Kevin Wurster and Tahir Jalilov'
__email__ = 'carpedm20@gmail.com'
# and wursterk@gmail.com, tahir.jalilov@gmail.com
__source__ = 'https://github.com/carpedm20/emoji/'
__license__ = '''
New BSD License

Copyright (c) 2014-2021, Taehoon Kim, Kevin Wurster and Tahir Jalilov
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* The names of its contributors may not be used to endorse or promote products
  derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''


# Backup original dictionary before doing anything else
_initial_dict = globals().copy()


import warnings
def _deprecation(message):
    warnings.warn(message, DeprecationWarning, stacklevel=3)



@property
def EMOJI_UNICODE_ENGLISH(module):
    _deprecation("""'emoji.EMOJI_UNICODE_ENGLISH' is deprecated and will be removed in version 2.0.0. Use 'emoji.EMOJI_DATA' instead.
To hide this warning, pin the package to 'emoji~=1.6.1'""")
    return _initial_dict['EMOJI_UNICODE_ENGLISH']


@property
def EMOJI_UNICODE_SPANISH(module):
    _deprecation("""'emoji.EMOJI_UNICODE_SPANISH' is deprecated and will be removed in version 2.0.0. Use 'emoji.EMOJI_DATA' instead.
To hide this warning, pin the package to 'emoji~=1.6.1'""")
    return _initial_dict['EMOJI_UNICODE_SPANISH']


@property
def EMOJI_UNICODE_PORTUGUESE(module):
    _deprecation("""'emoji.EMOJI_UNICODE_PORTUGUESE' is deprecated and will be removed in version 2.0.0. Use 'emoji.EMOJI_DATA' instead.
To hide this warning, pin the package to 'emoji~=1.6.1'""")
    return _initial_dict['EMOJI_UNICODE_PORTUGUESE']


@property
def EMOJI_UNICODE_ITALIAN(module):
    _deprecation("""'emoji.EMOJI_UNICODE_ITALIAN' is deprecated and will be removed in version 2.0.0. Use 'emoji.EMOJI_DATA' instead.
To hide this warning, pin the package to 'emoji~=1.6.1'""")
    return _initial_dict['EMOJI_UNICODE_ITALIAN']


@property
def EMOJI_UNICODE_FRENCH(module):
    _deprecation("""'emoji.EMOJI_UNICODE_FRENCH' is deprecated and will be removed in version 2.0.0. Use 'emoji.EMOJI_DATA' instead.
To hide this warning, pin the package to 'emoji~=1.6.1'""")
    return _initial_dict['EMOJI_UNICODE_FRENCH']


@property
def EMOJI_UNICODE_GERMAN(module):
    _deprecation("""'emoji.EMOJI_UNICODE_GERMAN' is deprecated and will be removed in version 2.0.0. Use 'emoji.EMOJI_DATA' instead.
To hide this warning, pin the package to 'emoji~=1.6.1'""")
    return _initial_dict['EMOJI_UNICODE_GERMAN']


@property
def UNICODE_EMOJI_ENGLISH(module):
    _deprecation("""'emoji.UNICODE_EMOJI_ENGLISH' is deprecated and will be removed in version 2.0.0. Use 'emoji.EMOJI_DATA' instead.
To hide this warning, pin the package to 'emoji~=1.6.1'""")
    return _initial_dict['UNICODE_EMOJI_ENGLISH']


@property
def UNICODE_EMOJI_SPANISH(module):
    _deprecation("""'emoji.UNICODE_EMOJI_SPANISH' is deprecated and will be removed in version 2.0.0. Use 'emoji.EMOJI_DATA' instead.
To hide this warning, pin the package to 'emoji~=1.6.1'""")
    return _initial_dict['UNICODE_EMOJI_SPANISH']


@property
def UNICODE_EMOJI_PORTUGUESE(module):
    _deprecation("""'emoji.UNICODE_EMOJI_PORTUGUESE' is deprecated and will be removed in version 2.0.0. Use 'emoji.EMOJI_DATA' instead.
To hide this warning, pin the package to 'emoji~=1.6.1'""")
    return _initial_dict['UNICODE_EMOJI_PORTUGUESE']


@property
def UNICODE_EMOJI_ITALIAN(module):
    _deprecation("""'emoji.UNICODE_EMOJI_ITALIAN' is deprecated and will be removed in version 2.0.0. Use 'emoji.EMOJI_DATA' instead.
To hide this warning, pin the package to 'emoji~=1.6.1'""")
    return _initial_dict['UNICODE_EMOJI_ITALIAN']


@property
def UNICODE_EMOJI_FRENCH(module):
    _deprecation("""'emoji.UNICODE_EMOJI_FRENCH' is deprecated and will be removed in version 2.0.0. Use 'emoji.EMOJI_DATA' instead.
To hide this warning, pin the package to 'emoji~=1.6.1'""")
    return _initial_dict['UNICODE_EMOJI_FRENCH']


@property
def UNICODE_EMOJI_GERMAN(module):
    _deprecation("""'emoji.UNICODE_EMOJI_GERMAN' is deprecated and will be removed in version 2.0.0. Use 'emoji.EMOJI_DATA' instead.
To hide this warning, pin the package to 'emoji~=1.6.1'""")
    return _initial_dict['UNICODE_EMOJI_GERMAN']


@property
def EMOJI_ALIAS_UNICODE_ENGLISH(module):
    _deprecation("""'emoji.EMOJI_ALIAS_UNICODE_ENGLISH' is deprecated and will be removed in version 2.0.0. Use 'emoji.EMOJI_DATA' instead.
To hide this warning, pin the package to 'emoji~=1.6.1'""")
    return _initial_dict['EMOJI_ALIAS_UNICODE_ENGLISH']


@property
def UNICODE_EMOJI_ALIAS_ENGLISH(module):
    _deprecation("""'emoji.UNICODE_EMOJI_ALIAS_ENGLISH' is deprecated and will be removed in version 2.0.0. Use 'emoji.EMOJI_DATA' instead.
To hide this warning, pin the package to 'emoji~=1.6.1'""")
    return _initial_dict['UNICODE_EMOJI_ALIAS_ENGLISH']







# From: https://erouault.blogspot.com/2014/11/hacking-python-module-constants.html

# Inspired from http://www.dr-josiah.com/2013/12/properties-on-python-modules.html
class _Module(object):
    def __init__(self):
        self.__dict__ = globals()
        self._initial_dict = _initial_dict

        # Transfer properties from the object to the Class
        for k, v in list(self.__dict__.items()):
            if isinstance(v, property):
                setattr(self.__class__, k, v)

        # Replace original module by our object
        import sys
        self._original_module = sys.modules[self.__name__]
        sys.modules[self.__name__] = self

# Custom help() replacement to display the help of the original module
# instead of the one of our instance object
class _MyHelper(object):

    def __init__(self, module):
        self.module = module
        self.original_help = help

        # Replace builtin help by ours
        try:
            import __builtin__ as builtins # Python 2
        except ImportError:
            import builtins # Python 3
        builtins.help = self

    def __repr__(self):
        return self.original_help.__repr__()

    def __call__(self, *args, **kwds):

        if args == (self.module,):
            import sys

            # Restore original module before calling help() otherwise
            # we don't get methods or classes mentioned
            sys.modules[self.module.__name__] = self.module._original_module

            ret = self.original_help(self.module._original_module, **kwds)

            # Reinstall our module
            sys.modules[self.module.__name__] = self.module

            return ret
        elif args == (self,):
            return self.original_help(self.original_help, **kwds)
        else:
            return self.original_help(*args, **kwds)

_MyHelper(_Module())
del _MyHelper
del _Module
