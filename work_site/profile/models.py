from sqlalchemy import Column, ForeignKey
from work_site.core.models import Publishable, Content, Rankable, ContentTaggable, ContainsAttachments, Classifiable
from work_site.extensions import db
from work_site.profile.constants import SKILL_PROFILE_STATUS


class SkillProfile(Publishable, Content, Rankable, ContentTaggable, ContainsAttachments, Classifiable, db.Model):
    __tablename__ = 'T_SKILL_PROFILES'

    id = Column(db.BigInteger, primary_key=True)
    content_id = Column(db.BigInteger, ForeignKey(Content.id))
    user_id = Column(db.BigInteger, ForeignKey('T_USERS.id'))
    body = Column(db.Text, nullable=False)

    status_code = Column(db.SmallInteger, default=SKILL_PROFILE_STATUS.INACTIVE)