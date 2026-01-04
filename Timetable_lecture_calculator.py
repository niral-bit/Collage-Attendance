import pandas as pd
from numpy import ceil as roundup

def calculate_lectures(start_date, end_date, holidays, timetable):
    # 1. Generate academic days (excluding weekends)
    all_days = pd.date_range(start=start_date, end=end_date, freq='B')
    holiday_dates = pd.to_datetime(holidays)
    academic_days = all_days[~all_days.isin(holiday_dates)]
    
    # 2. Create DataFrame
    df_days = pd.DataFrame({'Date': academic_days})
    df_days['DayOfWeek'] = df_days['Date'].dt.day_name()
    
    # 3. Calculate counts using the new Day-wise input
    # Get the frequency of each day of the week in the period
    day_counts = df_days['DayOfWeek'].value_counts()
    
    report = {}
    # Iterate through the days defined in your timetable
    for day, subjects in timetable.items():
        count_for_this_day = day_counts.get(day, 0)
        
        for subject in subjects:
            # Add the count to the subject
            report[subject] = report.get(subject, 0) + count_for_this_day
        
    return report 


# Config
start = "2026-01-05"
end = "2026-03-31"
attendance_critaria = 80 # for the minimum criterial attendance percentage need

# List your specific holiday dates here (YYYY-MM-DD)
my_holidays = [
    "2026-01-26", # Republic Day (Example)
    "2026-02-10", #Festival
    "2026-02-11", #Festival
]

# Map your subjects to the days they occur
# If you have Two time the same lecture in a day , write it two time in that day
# In this example i have mix lecture name with abbrivation and without it
# If you use Abbrivation but want see full name in csv file then add the name of lecture as shown below
my_timetable = {
    "Monday":    ["MATH","CAD"],
    "Tuesday":   ["PHY","CAD"],
    "Wednesday": ["CHEM","HL","MATH"],
    "Thursday":  ["ENG","ECO"],
    "Friday":    ["CHEM","ECO","AI"]
}

# Lecture Full name
Abbrivation ={
    "CAD": "Computer Aid Drawing",
    "PHY": "Physic",
    "ENG": "English",
    "ECO": "Economic"
}

# Define a function for the creating csv 
def Report_csv(output_calulated_lecture: dict,csv_filename: str= "output.csv",is_abbrivation: bool = False,abbrivation: dict = Abbrivation):
    if(is_abbrivation == False):
        lecture_dict = dict(sorted(output_calulated_lecture.items()))
        result = pd.DataFrame([lecture_dict],index=["Total Lecture"]).transpose()
    else:
        lecture_dict = dict(sorted({abbrivation.get(k,k):v for k,v in output_calulated_lecture.items()}.items()))
        result = pd.DataFrame([lecture_dict],index=["Total Lecture"]).transpose()
    result[f"{attendance_critaria}% (round up)"] = result['Total Lecture'].transform(lambda x : roundup(x * attendance_critaria/100))
    result["Can be missed"] = result['Total Lecture'] - result[f"{attendance_critaria}% (round up)"]
    result.to_csv(csv_filename,index_label="Lecture Name")

lecture_counts = calculate_lectures(start, end, my_holidays, my_timetable)

#Example without abbrivation
Report_csv(lecture_counts,"lecture.csv")
#Example with abbrivation
Report_csv(lecture_counts,"lecture_abbrivated.csv",True)


## For debugging
if __name__ == "__main__":
    print(f"Lecture Report from {start} to {end}")
    print("-" * 40)
    for subject, count in lecture_counts.items():
        print(f"{subject}: {count} Lecture")