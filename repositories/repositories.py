from sqlalchemy.orm import Session
import pandas as pd
from models.models import Award

class AwardRepository:
    @staticmethod
    def find_all(db: Session) -> list[Award]:
        return db.query(Award).all()

    @staticmethod
    def save(db: Session, award: Award) -> Award:
        if award.id:
            db.merge(award)
        else:
            db.add(award)
        db.commit()
        return award
    
    @staticmethod
    def save_from_csv(db: Session, csv_file: str) -> None:
        df_awards = pd.read_csv(csv_file, delimiter=';')
        # Fill NaN values with 'no' using a dictionary
        df_awards = df_awards.fillna({'winner': 'no'})
        df_awards['winner'] = df_awards['winner'].str.lower()

        # Replace Yes and No with True and False
        df_awards['winner'] = df_awards['winner'].apply(lambda x: True if x == 'yes' else False)

        for _, row in df_awards.iterrows():
            award = Award(**row)
            if not AwardRepository.exists_by_id(db, award.id):
                db.add(award)

        db.commit()

    @staticmethod
    def find_by_id(db: Session, id: int) -> Award:
        return db.query(Award).filter(Award.id == id).first()

    @staticmethod
    def exists_by_id(db: Session, id: int) -> bool:
        return db.query(Award).filter(Award.id == id).first() is not None

    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        award = db.query(Award).filter(Award.id == id).first()
        if award is not None:
            db.delete(award)
            db.commit()

    @staticmethod
    def get_winner(db: Session) -> dict:
        awards_data = db.query(Award).all()

        df = pd.DataFrame([award.__dict__ for award in awards_data])

        producer_wins = {}
        for _, row in df.iterrows():
            producer = row['producers']
            year = row['year']
            if row['winner'] == True:
                if producer not in producer_wins:
                    producer_wins[producer] = []
                producer_wins[producer].append(year)
        
        # Calculate the intervals between the years the producers won
        producer_intervals = []
        for producer, years in producer_wins.items():
            years.sort()
            for i in range(1, len(years)):
                interval = years[i] - years[i-1]
                producer_intervals.append({
                    "producer": producer,
                    "interval": interval,
                    "previousWin": years[i-1],
                    "followingWin": years[i]
                })
        
        if not producer_intervals:
            return {}
        
        # Get the producer with the smallest and largest interval
        min_interval = min(producer_intervals, key=lambda x: x['interval'])
        max_interval = max(producer_intervals, key=lambda x: x['interval'])
        
        # Get the producers with the smallest and largest interval
        min_intervals = [interval for interval in producer_intervals if interval['interval'] == min_interval['interval']]
        max_intervals = [interval for interval in producer_intervals if interval['interval'] == max_interval['interval']]
        
        # Create the result dictionary
        result = {
            "min": min_intervals,
            "max": max_intervals
        }
        return result