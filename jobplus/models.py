from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# 创建数据库ORM对象
db = SQLAlchemy()

# 创建基类,普通数据表类继承该基类
class Base(db.Model):

    # 不将该表当作Model类
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,default=datetime.utcnow, onupdate=datetime.utcnow)

# 创建数据库表结构

# 多对多关系
user_job = db.Table(
        'user_job',
        db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE')),
        db.Column('job_id', db.Integer, db.ForeignKey('job.id', ondelete='CASCADE'))
        )

# 求职者表
class User(Base):
    __tablename__ = 'user'

    ROLE_USER = 10
    ROLE_COMPANY = 20
    ROLE_ADMIN = 30

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False, index=True)
    email = db.Column(db.String(64), unique=True, nullable=False, index=True)
    _password = db.Column('password', db.String(256), nullable=False)
    user_job = db.relationship('Job', secondary=user_job)
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    #user_company = db.relationship('Company')
    resume = db.relationship('Resume', uselist=False)

    def __repr__(self):
        return '<User:{}>'.format(self.username)

    @property
    def password(self):
        return self._password

    # 密码加盐
    @password.setter
    def password(self, orig_password):
        self._password = generate_password_hash(orig_password)

    def check_password(self, password):
        return check_password_hash(self._password, password)

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    @property
    def is_company(self):
        return self.role == self.ROLE_COMPANY

# 简历表
class Resume(Base):
    __tablename__ = 'resume'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', uselist=False)

    job_experience = db.relationship('JobExperience')
    edu_experience = db.relationship('EduExperience')
    project_experience = db.relationship('ProjectExperience')

# 经历表
class Experience(Base):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    begin_at = db.Column(db.DateTime)
    end_at = db.Column(db.DateTime)
    description = db.Column(db.String(1024))

# 职位经验表
class JobExperience(Experience):
    __tablename__ = 'job_experience'

    company = db.Column(db.String(32), nullable=False)
    city = db.Column(db.String(32), nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
    resume = db.relationship('Resume', uselist=False)

# 教育经验表
class EduExperience(Experience):
    __tablename__ = 'edu_experience'

    school = db.Column(db.String(32), nullable=False)

    specialty = db.Column(db.String(32), nullable=False)
    degree = db.Column(db.String(16))
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
    resume = db.relationship('Resume', uselist=False)

# 项目经验表
class ProjectExperience(Experience):
    __tablename__ = 'project_experience'

    name = db.Column(db.String(32), nullable=False)

    # 项目中的角色
    role = db.Column(db.String(32))

    # 项目中用到的技术
    technologys = db.Column(db.String(64))
    resume_id = db.Column(db.Integer, db.ForeignKey('resume.id'))
    resume = db.relationship('Resume', uselist=False)

# 职位表
class Job(Base):

    __tablename__ = 'job'

    id = db.Column(db.Integer, primary_key=True)
    applicants_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    applicants = db.relationship('User', uselist=False)
    name = db.Column(db.String(64))
    #salary_range = db.Column(db.Integer, nullable=False)
    salary_low = db.Column(db.Integer, nullable=False)
    salary_high = db.Column(db.Integer, nullable=False)
    experience_requirement = db.Column(db.String(256))
    location = db.Column(db.String(64))
    tags = db.Column(db.String(128))
    degree_requirement = db.Column(db.String(32))
    is_fulltime = db.Column(db.Boolean, default=True)

    # 是否在招聘
    is_open = db.Column(db.Boolean, default=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id', ondelete='CASCADE'))
    company = db.relationship('Company', uselist=False)

    # job company relationship
    company_information = db.relationship('company')
    publish_time = db.Column(db.String(32), nullable=False)
    job_description = db.Column(db.String(256), nullable=False)
    job_requirement = db.Column(db.String(256), nullable=False)
    views_count = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Job:{}>'.format(self.jobname)

# 企业表
class Company(Base):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False, index=True)
    slug = db.Column(db.String(24), unique=True, nullable=False, index=True)
    logo = db.Column(db.String(256), nullable=False)
    contact = db.Column(db.String(24), nullable=False)
    email = db.Column(db.String(24), nullable=False)
    website = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(256))
    location = db.Column(db.String(32), nullable=False)
    # 公司详情
    about = db.Column(db.String(1024))
    # 公司标签
    tags = db.Column(db.String(128))
    # 公司技术栈
    stack = db.Column(db.String(128))
    # 团队介绍
    team_introduction = db.Column(db.String(256))
    # 公司福利
    welfares = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'))
    user = db.relationship('User', uselist=False,backref=db.backref('company', uselist=False))


    def __repr__(self):
        return '<Company {}>'.format(self.name)

class Dilivery(Base):
    __tablename__ = 'delivery'

    # 企业审核
    STATUS_WAITING = 1
    # 被拒绝
    STATUS_REJECT = 2
    # 被接收,等面试
    STATUS_ACCEPT = 3

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id', ondelete='SET NULL'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'))
    status = db.Column(db.SmallInteger, default=STATUS_WAITING)

    # 企业回应
    response = db.Column(db.String(256))

