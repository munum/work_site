from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from work_site.core.models import Publishable, Classifiable, Dated, Content, Rankable, ContentTaggable, ContainsAttachments, Image
from work_site.extensions import db
from work_site.job.constants import JOB_APPLICATION_STATUS, JOB_POST_STATUS, COMPLETED_WORK_STATUS
from work_site.profile.models import SkillProfile
from work_site.utils import STRING_LEN


class JobPost(Publishable, Content, Rankable, ContentTaggable, ContainsAttachments, Classifiable, db.Model):
    __tablename__ = 'T_JOB_POSTS'

    id = Column(db.BigInteger, primary_key=True)
    content_id = Column(db.BigInteger, ForeignKey(Content.id))
    title = Column(db.Text, nullable=False)
    summary = Column(db.Text, nullable=False)
    body = Column(db.Text, nullable=False)

    #id = Column(db.BigInteger, primary_key=True)
    #title = Column(db.Text, nullable=False)
    #summary = Column(db.Text, nullable=False)

    status_code = Column(db.SmallInteger, default=JOB_POST_STATUS.INACTIVE)

    __mapper_args__ = {
        'polymorphic_identity': 'jobpost'
    }

    @property
    def status(self):
        return JOB_APPLICATION_STATUS[self.status_code]


class RelatedJobApplications(Rankable, db.Model):
    __tablename__ = 'T_RELATED_JOB_APPLICATIONS'

    id = Column(db.BigInteger, primary_key=True)
    source_id = Column(db.BigInteger, ForeignKey('T_JOB_APPLICATIONS.id'))
    target_id = Column(db.BigInteger, ForeignKey('T_JOB_APPLICATIONS.id'))
    relatedness = Column(db.Integer, nullable=False, default=0)


class JobCategory(db.Model):
    __tablename__ = 'T_CATEGORIES'

    id = Column(db.BigInteger, primary_key=True)
    name = Column(db.String(STRING_LEN), nullable=False)


class JobApplication(Publishable, Content, Rankable, Classifiable, db.Model):
    __tablename__ = 'T_JOB_APPLICATIONS'

    id = Column(db.BigInteger, primary_key=True)
    content_id = Column(db.BigInteger, ForeignKey(Content.id))
    title = Column(db.Text)
    summary = Column(db.Text)
    body = Column(db.Text, nullable=False)
    category_id = Column(db.BigInteger, ForeignKey(JobCategory.id), nullable=False)

    skillprofile = relationship(SkillProfile, uselist=False)
    front_picture = Column(db.BigInteger, ForeignKey(Image.id))

    related_applications = relationship(RelatedJobApplications, foreign_keys=[RelatedJobApplications.source_id])

    status_code = Column(db.SmallInteger, default=JOB_APPLICATION_STATUS.INACTIVE)

    __mapper_args__ = {
        'polymorphic_identity': 'jobapplication'
    }

    @property
    def status(self):
        return JOB_APPLICATION_STATUS[self.status_code]


class CompletedWork(Publishable, Content, Classifiable, db.Model):
    __tablename__ = 'T_COMPLETED_WORK'

    id = Column(db.BigInteger, primary_key=True)
    content_id = Column(db.BigInteger, ForeignKey(Content.id))
    title = Column(db.Text)
    summary = Column(db.Text)
    body = Column(db.Text, nullable=False)

    status_code = Column(db.SmallInteger, default=COMPLETED_WORK_STATUS.INACTIVE)

    __mapper_args__ = {
        'polymorphic_identity': 'completedwork'
    }


class TrendingJobs(Dated, Rankable, db.Model):
    __tablename__ = 'T_TRENDING_JOBS'

    id = Column(db.BigInteger, primary_key=True)

    user_id = Column(db.BigInteger, ForeignKey('T_USERS.id'))
    application_id = Column(db.BigInteger, ForeignKey(JobApplication.id))
