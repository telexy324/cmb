#!/usr/bin/env python
import os
from app import create_app, db
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand
from flask_uploads import UploadSet, DOCUMENTS
from flask_uploads import configure_uploads, patch_request_class
from app.main.forms import files


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
configure_uploads(app, (files,))
patch_request_class(app, size=100*1024*1024)


def make_shell_context():
    return dict(app=app, db=db)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host='0.0.0.0', port=5000))


if __name__ == '__main__':
    manager.run()