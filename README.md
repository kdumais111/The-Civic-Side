
## The Civic Side

The Civic Side dashboard explores several measures of civic engagement across Chicago. It pairs mayoral campaigns contributions data scraped from the [Illinois Board of Elections website](https://www.elections.il.gov/CampaignDisclosure/ContributionSearchByCommittees.aspx) with voter turnout and [311 non-emergency service calls](https://www.chicago.gov/city/en/depts/311.html) data from the city of Chicago to investigate how different zip codes engage in political processes and access civic services. (Note that all data are from 2019, to correspond with the most recent completed mayoral election cycle at the time of project development in early 2023.) Read more about the Civic Side in our project paper.

### To launch the dashboard:

• Download the [Civic Side GitHub repository](https://github.com/uchicago-capp122-spring23/30122-project-the-civic-side)

• Navigate to the top-level directory, `30122-project-the-civic-side`

• Run `poetry install` from the command line to active the virtual environment

• Run `poetry run python3 civic_side/prep_data.py` to scrape, clean, and merge the dashboard data

• Run `poetry run python3 civic_side/dashboard.py` to active the dashboard and follow the resulting link from the terminal to the browser-based dashboard

### To interact with the dashhboard:

• Pick your metrics of choice from the map drop-down menus – compare the maps side-by-side to see which metrics do (and don't) correlate with each other

• Use the table drop-down menu to display more 311 call and campaign finance data for the city of Chicago as a whole or a zip code of your choice

### Enjoy exploring the Civic Side!
