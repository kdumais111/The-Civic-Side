
## The Civic Side

The Civic Side dashboard explores several measures of civic engagement across Chicago. It pairs mayoral campaigns contributions data scraped from the [Illinois Board of Elections website](https://www.elections.il.gov/CampaignDisclosure/ContributionSearchByCommittees.aspx) with voter turnout and [311 non-emergency service calls](https://www.chicago.gov/city/en/depts/311.html) data from the city of Chicago to investigate how different zip codes engage in political processes and access civic services. (Note all data are from 2019, to correspond with the most recent completed mayoral election cycle at the time of project development in early 2023. Read more about our data and methods in our project paper.) 

### To launch the dashboard:

1. Download the [Civic Side GitHub repository](https://github.com/uchicago-capp122-spring23/30122-project-the-civic-side)

2. Navigate to the top-level directory, `30122-project-the-civic-side`

3. Run `poetry install` from the command line to active the virtual environment

4. Run `poetry run python3 civic_side/prep_data.py` to scrape, clean, and merge the dashboard data

5. Run `poetry run python3 civic_side/dashboard.py` to active the dashboard and follow the resulting link from the terminal to the browser-based dashboard

### To interact with the dashboard:

**Two side-by-side maps of Chicago are your gateway to the Civic Side. Use the map drop-downs to specify which measure of civic engagement (voting rates, average campaign contributions, 311 utilization, etc.) each map displays.** You can also display average housing prices, used here as a proxy for income, to see how civic engagement relates to socioeconomic status. Zip code colors correspond to values for each measure, with darker zip codes having higher values. Hover over a zip code to display its exact value for the specified measure. Display different measures side-by-side to see how they do – or don't – correlate with each other.

**For example, try selecting 311 Complaints per thousand residents and 311 complaints excluding 60612.** The first map displays a single deep blue zip code in a sea of white. Hover over that zip code to see that it's 60612 with close to 15,600 311 complaints per thousand residents. The second map, which excludes 60612, reveals variation across other zip codes initially obscured by the fact that 60612 had many, many more 311 complaints than any other zip code. With a bit of detective work, you could learn that 60612 is home to a cluster of downtown hospitals, which may be driving this trend.

**Below the maps, several tables display additional details about 311 utilization and campaign contributions in Chicago.** The tables default to city-wide data, but you can use the drop-down to display numbers for a zip code of interest instead. For example, select 60612 to see that the vast majority of 311 calls in the medical district are information only calls, likely from community members seeking information about accessing medical services.

**For those curious about hyperlocal politics, a final table maps wards and precincts to Chicago zip codes.**

### Enjoy exploring the Civic Side!
