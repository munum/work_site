# -*- coding: utf-8 -*-
import datetime

from flask.ext.script import Manager

from work_site import create_app
from work_site.extensions import db
from work_site.user import User, UserDetail, ADMIN, ACTIVE
from work_site.utils import SEX_TYPE


app = create_app()
manager = Manager(app)


@manager.command
def run():
    """Run in local machine."""

    app.run()


@manager.command
def initdb():
    """Init/reset database."""

    db.drop_all()
    db.create_all()

    admin = User(
            name=u'admin',
            email=u'admin@example.com',
            paypal=u'admin@example.com',
            password=u'123456',
            role_code=ADMIN,
            status_code=ACTIVE,
            user_detail=UserDetail(
                first_name=u'Happy',
                middle_name=u'',
                last_name=u'Admin',
                sex_code=SEX_TYPE.MALE,
                date_of_birth=datetime.datetime.now() - datetime.timedelta(weeks=520),
                url=u'http://admin.example.com',
                location=u"Admin's hut",
                bio=u'A happy admin guy'))
    db.session.add(admin)
    db.session.commit()


manager.add_option('-c', '--config',
                   dest="config",
                   required=False,
                   help="config file")

if __name__ == "__main__":
    manager.run()
