from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DDL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import event

# Create a base class for declarative class definitions
Base = declarative_base()

# Define the JobStates table
class JobStates(Base):
    __tablename__ = 'job_states'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    # Relationship to Job
    job = relationship("Job", back_populates="job_state")

# Define the Job table
class Job(Base):
    __tablename__ = 'job'

    id = Column(Integer, primary_key=True)
    issue = Column(String, nullable=False)
    job_directory = Column(String, nullable=False)
    job_state_id = Column(Integer, ForeignKey('job_states.id'), nullable=False)

    # Relationship to JobStates
    job_state = relationship("JobStates", back_populates="job")

# Define the JobStateHistory table
class JobStateHistory(Base):
    __tablename__ = 'job_state_history'

    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey('job.id'), nullable=False)
    job_state_id = Column(Integer, ForeignKey('job_states.id'), nullable=False)
    timestamp = Column(String, nullable=False)

def get_session(conn_str):

    # Create an SQLite database and the tables
    engine = create_engine(conn_str)
    Base.metadata.create_all(engine)

    # Create the trigger for tracking job state changes
    trigger = DDL("""
    CREATE TRIGGER track_job_state_change
    AFTER UPDATE OF job_state_id ON job
    FOR EACH ROW
    BEGIN
        INSERT INTO job_state_history (job_id, job_state_id, timestamp)
        VALUES (NEW.id, NEW.job_state_id, datetime('now'));
    END;
    """)

    # Attach the trigger to the database
    event.listen(Base.metadata, 'after_create', trigger)

    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()


def init_db():

    parser = argparse.ArgumentParser(description="Set up a database for a Jira workflow tracker")
    parser.add_argument('database', type=str, help='the connection string to the database')
    args = parser.parse_args()

    session = get_session(conn_str)

    states = session.query(JobStates).count()
    if states > 0:
        print("Database has already been initialized. Doing nothing.")

    else:
        states = [
            JobStates(name='STARTED', description='Job has been started'),
            JobStates(name='FINISHED', description='Job executing has been finished'),
            JobStates(name='PUBLISHED', description='Job resulst have been published')
        ]

        session.add_all(states)
        session.commit()
        session.close()


class DBConnector:

    def __init__(self, conn_str):
        self.logger = get_logger()
        self.session = get_session(conn_str)

    def new_job(self, issue, job_directory):
        self.logger.info(f"Creating new job for {issue}")
        start_state = self.session.query(JobStates).filter_by(name='STARTED').first()
        return Job(issue=issue, job_directory=job_directory, job_state=start_state)

    def transition_job(self, issue, state):
        job = self.session.query(Jobs).filter_by(issue=desired_issue).first()
        if job:
            finish_state = session.query(JobStates).filter_by(name=state).first()
            job.job_state = finish_state
            session.commit()
            return True
        return False

    def finish_job(self, issue):
        result = transition_job(issue, 'FINISHED')
        if result:
            self.logger.info(f"Finishing job for {issue}")
        else:
            self.logger.error(f"Could not find a job for {issue}")

    def publish_job(self, issue):
        result = transition_job(issue, 'PUBLISHED')
        if result:
            self.logger.info(f"Publishing job for {issue}")
        else:
            self.logger.error(f"Could not find a job for {issue}")

