from datetime import timedelta,datetime,timezone
import datetime as dt





def get_return_date(issue_date):
    return (datetime.now()+timedelta(days=15)).date()