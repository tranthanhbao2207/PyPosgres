from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

from app import app


@app.route('/custom_views')
def index():
    return 'hello cust'

