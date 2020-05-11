# chain_store_scraper: get branch locations for global chain store brands

Most of the global chains have a store locator in their website. This locator usually allows for searching by zip codes, which enables us to collect location information by region. All we need is a list of zip codes for the destination of interest, and a scraper that can scrape the locator page. 
- I began by compiling a list of zip codes for each city of interest. I wrote a scraper to collect zip codes from [WorldPostalCode](https://worldpostalcode.com/united-states/washington/seattle), which displays zip codes by city in a clean format. Zip code scraper can be found [here](https://github.com/ruilinchen/chain_store_scraper/blob/master/zip_code_scraper.ipynb). All the collected zip codes are stored in a single file called "[zip_codes_in_the_world.csv](https://github.com/ruilinchen/chain_store_scraper/blob/master/data/zip_codes_in_the_world.csv)", which can be found in the [data folder](https://github.com/ruilinchen/chain_store_scraper/tree/master/data). <ins> This scraper does not work well for Baltimore, Maryland, as the data format used to display zip codes of this city is different from the rest, but works for other places. </ins>
- Next, I wrote a scraper using Selenium to collect search results by zip codes. 
  - A prelimiary scraper is available [here](https://github.com/ruilinchen/chain_store_scraper/blob/master/mcdonalds_locator.py). It can now successfully:
    - enter zip code as search term
    - submit search request
    - display all the returned results in a single webpage. 
    - extract store info from this webpage for each zip code
    - loop through all the zip codes
  - Future steps:
    - Drop repeated records
    - Exception handler -- bypass a survey prompt

With the scraper, I can loop through zip codes and collect stores by city. So far, I have scraped the following cities. Store information is stored in a single file called "[store_locations.csv](https://github.com/ruilinchen/chain_store_scraper/blob/master/data/store_locations.csv)", which can be found in the [data folder](https://github.com/ruilinchen/chain_store_scraper/tree/master/data). <ins> Note that there might be repeated records. </ins>
- Baltimore
- Phoenix
- Seattle
