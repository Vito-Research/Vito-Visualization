import random
import pandas as pd
from datetime import datetime
from datetime import timedelta
def createRandomData(min, max, step, amount):
    df = pd.DataFrame()
    randomData =[]
    randomDate =[]
    randomTime =[]
    for i in range(amount):
        randomHR = random.randrange(min, max, step)
        randomData.append(randomHR)
        
        time_str = '23/2/2020 11:12:22.234513'
        date_format_str = '%d/%m/%Y %H:%M:%S.%f'
        given_time = datetime.strptime(time_str, date_format_str)
        final_time = given_time + timedelta(hours=i)
        randomDate.append(final_time.date())
        randomTime.append(final_time.strftime('%H:%M:%S'))
   
    
    df["Heartrate"]  = randomData
    df["Start_Date"] = randomDate
    df["Start_Time"] = randomTime
    with open("random.csv", 'w') as f:
        df.to_csv(f)

# createRandomData(60, 100, 2, 500)

