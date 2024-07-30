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
        df_awards = pd.read_csv(csv_file, delimiter=";")
        # Fill NaN values with 'no' using a dictionary
        df_awards = df_awards.fillna({"winner": "no"})
        df_awards["winner"] = df_awards["winner"].str.lower()

        # Replace Yes and No with True and False
        df_awards["winner"] = df_awards["winner"].apply(
            lambda x: True if x == "yes" else False
        )

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
        # Get all the data from the database (filtering by winner = True)
        awards_data = db.query(Award).filter(Award.winner == True).all()
        
        # Create a DataFrame from the data
        df = pd.DataFrame([award.__dict__ for award in awards_data])
        
        # Get the producers and the year of the awards
        df = df[['year','producers']]
        
        # Split producers and expand with producer
        df = df.assign(producers=df['producers'].str.split(', | and ')).explode('producers')
        
        # Some cases remain with and
        df['producers'] = df['producers'].apply(lambda x: x.replace("and",''))
        
        # Strip white spaces
        df['producers'] = df['producers'].str.strip()
        
        # Sort by producer and year
        df = df.sort_values(by=['producers', 'year'])

        # Lowercase the producers
        df['producers'] = df['producers'].str.lower()

        # Calculate the difference in years between consecutive awards for the same producer
        df['year_diff'] = df.groupby('producers')['year'].diff()

        # Get the previous and following win years
        df['previousWin'] = df.groupby('producers')['year'].shift(1)

        # Get the following win year
        df['followingWin'] = df['year']

        # Drop rows with NaN values
        df = df.dropna()

        #Find the minimum and maximum intervals
        min_interval_value = df['year_diff'].min()
        max_interval_value = df['year_diff'].max()

        # Get the producers with the minimum and maximum intervals
        min_interval = df[df['year_diff'] == min_interval_value]
        max_interval = df[df['year_diff'] == max_interval_value]

        # Prepare the output in the desired format
        result = {
            "min": [
                {
                    "producer": row['producers'].title(),
                    "interval": int(row['year_diff']),
                    "previousWin": int(row['previousWin']),
                    "followingWin": int(row['followingWin'])
                }
                for _, row in min_interval.iterrows()
            ],
            "max": [
                {
                    "producer": row['producers'].title(),
                    "interval": int(row['year_diff']),
                    "previousWin": int(row['previousWin']),
                    "followingWin": int(row['followingWin'])
                }
                for _, row in max_interval.iterrows()
            ]
        }


        return result
