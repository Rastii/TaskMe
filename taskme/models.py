import datetime as dt
from sqlalchemy import Table, Column, ForeignKey, Integer, String,\
Boolean, Text, DateTime
from sqlalchemy.orm import relationship, backref, deferred
#from sqlalchemy.dialects.sqlite import DATETIME
from taskme.database import Base, db_session
from sqlalchemy.orm.collections import attribute_mapped_collection
import datetime

def now():
    return datetime.datetime.now()

group_members = Table('group_members', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('group_id', Integer, ForeignKey('groups.id')))

class User(Base):
    __tablename__ = 'users'
    id          = Column(Integer, primary_key=True)
    login       = Column(String(64), unique=True)
    name        = Column(String(128))
    email       = Column(String(64), unique=True)
    role        = Column(String(64))
    password    = deferred(Column(String(60)))
    enabled     = deferred(Column(Boolean))
    groups      = relationship("Group", secondary=group_members,
                    backref='users')
    assigned_tasks  = relationship("Task", 
                        primaryjoin="User.id==Task.assigned_by")
    created_tasks   = relationship("Task",
                        primaryjoin="User.id==Task.assigned_to")

    def __init__(self, fname, lname, login, email, password, role=None):
        self.name       = fname + ' ' + lname
        self.login      = login
        self.password   = password
        self.email      = email.lower()
        self.enabled    = True
        self.role       = 'User'
        if role:
            self.role = role

    def __repr__(self):
        return '< User id: %d, name: %s, login: %s, email: %s >' %\
            (self.id, self.name, self.login, self.email)


    def enable(self):
        self.enabled = True

    def update(self, fname=None, lname=None,
                login=None, password=None, email=None, role=None):
        if fname and lname:
            self.name = fname + ' ' + lname
        elif fname:
            self.name = fname + ' ' + self.name.split(' ')[1]
        elif lname:
            self.name = self.name.split(' ')[0] + ' ' + lname
        if login and not \
        db_session.query(User).filter(User.login==login).count():
            self.login = login
        if password:
            self.password = password
        if email and not \
        db_session.query(User).filter(User.login==login).count():
            self.email = email
        if role:
            self.role = role

    # These four are required helpers for flask user login
    def get_id(self):
        return unicode(self.id)

    def is_active(self):
        return self.enabled

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True


class Group(Base):
    __tablename__ = 'groups'
    id          = Column(Integer, primary_key=True)
    name        = Column(String(128), unique=True)
    password    = deferred(Column(String(60)))
    tasks       = relationship("Task", backref="groups")

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def __repr__(self):
        return '< Group id: %s, Group name: %s >' %\
            (self.id, self.name)

class Task(Base):
    __tablename__ = 'tasks'
    id              = Column(Integer, primary_key=True)
    name            = Column(String(128))
    description     = Column(Text())
    category        = Column(Integer, ForeignKey('categories.id'))
    assigned_by     = Column(Integer, ForeignKey('users.id'))
    assigned_to     = Column(Integer, ForeignKey('users.id'))
    assigned_date   = Column(DateTime, default=now())
    group           = Column(Integer, ForeignKey('groups.id'))
    updates         = relationship("Update", backref="tasks")
    completed       = Column(Boolean)

    def __init__(self, name, description, category, assigned_by, 
                    assigned_to, group):
        self.name = name
        self.description = description
        self.category = category
        self.assigned_by = assigned_by
        self.assigned_to = assigned_to
        self.completed = False
        self.group = group

    def __repr__(self):
        return '< Task id: %s, Task name: %s, Task category: %s, \
                assigned_to: %s, assigned_by: %s, date: %s, group: %s, \
                completed: %s >' %\
                (self.id, self.name, self.category, self.assigned_to, 
                    self.assigned_by, self.assigned_date, self.group,
                    self.complted)

class Category(Base):
    __tablename__ = 'categories'
    id              = Column(Integer, primary_key=True)
    name            = Column(String(128), unique=True)
    tasks           = relationship("Task", backref="categories")

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        print '< Category id: %s, Category name: %s >' % (self.id, self.name)

class Update(Base):
    __tablename__ = 'task_updates'
    id              = Column(Integer, primary_key=True)
    description     = Column(Text())
    task            = Column(Integer, ForeignKey("tasks.id"))
    update_time     = Column(DateTime, default=now())

    def __init__(self, description, task=None):
        self.description = description
        if task:
            self.task = task
