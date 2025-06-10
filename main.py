import sqlite3
import time
from utils import is_in_office, get_office_location
from db import populate_month_days, create_tables, is_current_day_tracked, insert_default_tracked_day, increment_office_minutes, increment_other_minutes, is_current_day_office_set, is_office_entry_time_set, set_current_day_office, update_current_day_office_entry_time, update_current_day_office_exit_time

def main():
    # Initialize database connection
    conn = sqlite3.connect('work_tracker.db')
    
    # Create tables if they do not exist
    create_tables(conn)

    # Populate the month days if they are not already tracked in the database
    populate_month_days(conn)

    # Check if the current day is already tracked
    if not is_current_day_tracked(conn):
        # Insert a default tracked day if not already tracked
        insert_default_tracked_day(conn)

    if is_in_office():
        office_location = get_office_location()
        
        # Check if the office location is already set for today
        if not is_current_day_office_set(conn):
            set_current_day_office(conn, office_location)

        # Check if the office entry time is already set for today
        if not is_office_entry_time_set(conn):
            # Set the office entry time to the current time
            update_current_day_office_entry_time(conn)
        
        # Increment office minutes
        increment_office_minutes(conn, 1)

        # Update office exit time if the user is still in the office
        update_current_day_office_exit_time(conn)

    else:
        # Increment other minutes if not in the office
        increment_other_minutes(conn, 1)

    # Close the database connection 
    conn.close()

if __name__ == "__main__":
    # Run the main function ever minute    
    # while True:
    #     main()
    #     time.sleep(60)  # Sleep for 60 seconds before the next run
    main()