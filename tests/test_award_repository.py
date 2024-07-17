import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
from models.models import Award  
from repositories.repositories import AwardRepository 
from database.database import Base  



@pytest.fixture(scope="module")
def db_session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)


def test_find_all(db_session):
    award1 = Award(id=1, title="Award 1", producers="Producer 1", studios="Studio 1", year=2000, winner=True)
    award2 = Award(id=2, title="Award 2", producers="Producer 2", studios="Studio 2", year=2001, winner=False)
    db_session.add_all([award1, award2])
    db_session.commit()

    awards = AwardRepository.find_all(db_session)
    assert len(awards) == 2

def test_save(db_session):
    award = Award(id=3, title="Award 3", producers="Producer 3", year=2002, winner=True)
    saved_award = AwardRepository.save(db_session, award)
    assert saved_award.id == 3

def test_save_from_csv(db_session, tmpdir):
    csv_content = """id;title;producers;year;winner
4;Award 4;Producer 4;2003;yes
5;Award 5;Producer 5;2004;no
"""
    csv_file = tmpdir.join("awards.csv")
    csv_file.write(csv_content)

    AwardRepository.save_from_csv(db_session, str(csv_file))
    award4 = AwardRepository.find_by_id(db_session, 4)
    award5 = AwardRepository.find_by_id(db_session, 5)
    assert award4 is not None
    assert award4.winner is True
    assert award5 is not None
    assert award5.winner is False

def test_find_by_id(db_session):
    award = Award(id=6, title="Award 6", producers="Producer 6", year=2005, winner=False)
    db_session.add(award)
    db_session.commit()

    found_award = AwardRepository.find_by_id(db_session, 6)
    assert found_award is not None
    assert found_award.title == "Award 6"

def test_exists_by_id(db_session):
    award = Award(id=7, title="Award 7", producers="Producer 7", year=2006, winner=True)
    db_session.add(award)
    db_session.commit()

    assert AwardRepository.exists_by_id(db_session, 7) is True
    assert AwardRepository.exists_by_id(db_session, 999) is False

def test_delete_by_id(db_session):
    award = Award(id=8, title="Award 8", producers="Producer 8", year=2007, winner=False)
    db_session.add(award)
    db_session.commit()

    AwardRepository.delete_by_id(db_session, 8)
    deleted_award = AwardRepository.find_by_id(db_session, 8)
    assert deleted_award is None

def test_get_winner(db_session):
    award1 = Award(id=9, title="Award 9", producers="Producer 9", year=2008, winner=True)
    award2 = Award(id=10, title="Award 10", producers="Producer 9", year=2010, winner=True)
    award3 = Award(id=11, title="Award 11", producers="Producer 11", year=2012, winner=True)
    award4 = Award(id=12, title="Award 12", producers="Producer 9", year=2014, winner=True)
    award5 = Award(id=13, title="Award 13", producers="Producer 9", year=2016, winner=True)
    db_session.add_all([award1, award2, award3, award4, award5])
    db_session.commit()

    result = AwardRepository.get_winner(db_session)
    assert result["min"][0]["interval"] == 2
    assert result["min"][0]["producer"] == "Producer 9"
    assert result["min"][0]["previousWin"] == 2008
    assert result["min"][0]["followingWin"] == 2010

    assert result["max"][0]["interval"] == 4
    assert result["max"][0]["producer"] == "Producer 9"
    assert result["max"][0]["previousWin"] == 2010
    assert result["max"][0]["followingWin"] == 2014