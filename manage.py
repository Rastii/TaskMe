import sys
from taskme import app

if len(sys.argv) > 1:
    if sys.argv[1] == 'run':
        app.run(debug=True, host='localhost', port=5000)
        sys.exit()

    elif sys.argv[1] == 'setup':
        from taskme.database import *
        kill_db()
        init_db()
        setup_db()
        sys.exit()

    elif sys.argv[1] == 'shell':
        from flask import *
        from taskme import *
        from taskme.models import *
        from IPython import embed
        embed()
        sys.exit()
print "Usage: %s <run> | <setup> | <shell>" % sys.argv[0]
sys.exit()
