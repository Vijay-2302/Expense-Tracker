import datetime

class DateTime:
    
    def __init__(self):
        self.date = datetime.datetime.now()
        self.day = self.date.strftime('%d')

    def get_week(self):
        date_lst = []
        for i in range(7):
            date_lst.append((self.date - datetime.timedelta(days=i)).strftime('%Y-%m-%d'))
        
        return date_lst
sc = DateTime()
sc.get_week()