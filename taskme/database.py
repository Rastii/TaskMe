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

    """Categories
    """
    bugs = Category('Bugs')
    db_session.add(bugs)

    ui_dev = Category('UI Development')
    db_session.add(ui_dev)

    backend_dev = Category('Backend Development')
    db_session.add(backend_dev)
    db_session.commit()


    """Tasks
    """
    task1 = Task('UI Work', 'Start working on the UI you lazy SOB',
            ui_dev.id, luke.id, dennis.id, hackers.id)

    task2 = Task('Backend Work', 'Finish up the backend you lazy SOB',
            backend_dev.id, dennis.id, luke.id, hackers.id)
    db_session.add(task1)
    db_session.add(task2)
    db_session.commit()
#query to take note of 
#db_session.query(User).filter(User.login == 'rastii').filter(User.groups.any(Group.name == 'hackers')).count()