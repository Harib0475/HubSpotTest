from database import Database
from helper import generate_random_data

from hupspot import HubSpot


def main():
    """
        Main Function for handling all the stuff
    """

    print("-------> Start <-------")

    db = Database()
    table_name = 'HaribContact'  # setting table name
    db.connect_db()  # connecting database
    db.create_table(table_name=table_name)  # create table
    random_records = generate_random_data()  # generate 2 random records
    for record in random_records:
        db.add_record(table_name=table_name, data=record)  # add records to database
    db_records = db.get_last_two_records(table_name=table_name)  # fetch last 2 records from database
    hubspot = HubSpot()  # establish connection with hubspot
    for db_record in db_records:
        response = hubspot.create_or_update_contact(
            {
                'first_name': db_record[1],
                'last_name': db_record[2],
                'email': db_record[3]
            }
        )  # add or update record in hubspot
        if response.status_code == 200:
            db.update_record(table_name=table_name, data={
                'vid': str(response.json()['vid']),
                'email': db_record[3]
            })  # update vid in database
    db.close_connection()
    print("-------> End   <-------")


if __name__ == '__main__':
    main()
