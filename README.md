# sqlalchemy-challenge
Data visualization SQLAlchemy project

This project contains the following:
Resource folder containing the dataset of Hawaiian weather information in a SQLite db and csv file.
app.py: utilizes sqlalchemy to query a SQLITE db and flask to build a site to expose 4 APIs:
1.     precipitation : returns JSON of  date and precip amount for all dates available in the dataset
2.     stations: returns JSON of all the station data(id, station, name, elevation, latitude, longitude) from the dataset
3.     "tobs": returns JSON of tobs (Observed temperature) and date for the most active station in the dataset
4.     start_date: returns JSON of minimum, average and maximum temps calculated for all dates greater than and equal to the start date
5.     start_date/end_date: returns JSON of minimum, average and maximum temps calculated for all dates greater than and equal to the start date and less than or eqal to the end date.  

climate.ipynb : utilizes matplotlib, pandas, and sqlalchemy.
A year's worth of precipitation is plotted for the most active station in the dataset.The min, max and avg temps are calculated.  A histogram of the observed temps (tobs) values are plotted for the most active station

temp_analysis_bonus_1_starter.ipynb : Uses pandas to identify datasets for 2 different months and run a ttest on the resulting collections.

temp_analysis_bonus_2_starter.ipynb : Using a supplied function (calc_temps) to calculate the min, avg, max temps for a given week of vacation dates and then plot them as a whiskered bar plot.
