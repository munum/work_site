from sqlalchemy import Column, ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from work_site.extensions import db
from work_site.utils import get_current_time, STRING_LEN


class Dated(object):
    available_at = Column(db.DateTime, nullable=False, default=get_current_time)
    available_until = Column(db.DateTime)
    updated_at = Column(db.DateTime, nullable=False, default=get_current_time)
    created_at = Column(db.DateTime, nullable=False, default=get_current_time)


class Owned(object):

    @declared_attr
    def created_by(self):
        return Column(db.BigInteger, db.ForeignKey('T_USERS.id'))

    @declared_attr
    def last_updated_by(self):
        return Column(db.BigInteger, db.ForeignKey('T_USERS.id'))


class Publishable(Dated, Owned):
    published = Column(db.Boolean, nullable=False, default=False)


class Classifiable(object):
    classification = Column(db.Integer)


class Rankable(object):
    rank = Column(db.Integer, nullable=False, default=1)


class Tag(db.Model, Rankable):
    __tablename__ = 'T_TAGS'

    id = Column(db.BigInteger, primary_key=True)
    name = Column(db.String(STRING_LEN), nullable=True)
    type = Column(db.String(STRING_LEN))

    __mapper_args__ = {
        'polymorphic_identity': 'tag',
        'polymorphic_on': 'type'
    }


class ContentTag(Tag):
    __tablename__ = 'T_CONTENT_TAGS'

    tag_id = Column(db.BigInteger, ForeignKey(Tag.id))
    content_id = Column(db.BigInteger, ForeignKey('T_CONTENTS.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'contenttag'
    }


class UserTag(Tag):
    __tablename__ = 'T_USER_TAGS'

    tag_id = Column(db.BigInteger, ForeignKey(Tag.id))
    user_id = Column(db.BigInteger, ForeignKey('T_USERS.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'usertag'
    }

class ContentTaggable(object):

    @declared_attr
    def tags(self):
        return relationship(ContentTag)


class SubContent(Publishable, Rankable, db.Model):
    __tablename__ = 'T_SUBCONTENTS'

    id = Column(db.BigInteger, primary_key=True)
    associate_with = Column(db.BigInteger, ForeignKey('T_CONTENTS.id'))
    payload = Column(db.BigInteger, ForeignKey('T_FILES.id'))


class ContainsAttachments(object):

    @declared_attr
    def attachments(self):
        return relationship(SubContent)


class Content(db.Model):
    __tablename__ = 'T_CONTENTS'

    id = Column(db.BigInteger, primary_key=True)

    type = Column(db.String(STRING_LEN))

    __mapper_args__ = {
        'polymorphic_identity': 'content',
        'polymorphic_on': 'type'
    }

class Media(db.Model):
    __tablename__ = 'T_FILES'

    id = Column(db.BigInteger, primary_key=True)
    path = Column(db.String(STRING_LEN), nullable=False)
    type = Column(db.String(STRING_LEN))

    __mapper_args__ = {
        'polymorphic_identity': 'media',
        'polymorphic_on': 'type'
    }


class File(Media):
    media_id = Column(db.BigInteger, ForeignKey(Media.id))

    __mapper_args__ = {
        'polymorphic_identity': 'file'
    }


class Image(Media):
    image_id = Column(db.BigInteger, ForeignKey(Media.id))
    thumb = Column(db.String(STRING_LEN))

    __mapper_args__ = {
        'polymorphic_identity': 'image'
    }