from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///taskme.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False, 
                                        autoflush=False,
                                        bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

from taskme.models import *

def init_db():
    Base.metadata.create_all(engine)

def kill_db():
    Base.metadata.drop_all(engine)

def setup_db():
    from taskme.models import *
    from taskme.views import bcrypt

    """ User Creation
    """
    dennis = User("Dennis", "Skinner", "skinner927", 
            'lol2@lol.com',  
            bcrypt.generate_password_hash('asdfqwer'))
    db_session.add(dennis)
    luke = User("Luke", "Hritsko", "rastii",
            'lol@lol.com',
            bcrypt.generate_password_hash('asdfqwer'))
    db_session.add(luke)
    db_session.commit()

    """Group Creation
    """
    hackers = Group('hackers', 
        bcrypt.generate_password_hash('pwnies'))
    db_session.add(hackers)
    db_session.commit()

    """Group Members
    """
    dennis.groups.append(hackers)
    luke.groups.append(hackers)
    db_session.commit()
#query to take note of 
#db_session.query(User).filter(User.login == 'rastii').filter(User.groups.any(Group.name == 'hackers')).count()