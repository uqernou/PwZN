import pandas as pd
import matplotlib.pyplot as plt

covid_19 = pd.read_csv('covid-19_Data.csv', sep=';', header=0,
                       usecols=['iso_code', 'continent', 'location', 'total_cases', 'total_deaths'])
print(covid_19)
covid_19_per_continent = covid_19.groupby(['continent']).sum(numeric_only=True)
print(covid_19_per_continent)
covid_19_per_continent.plot(kind='bar')
plt.show()