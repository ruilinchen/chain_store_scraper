# chain_store_scraper: get branch locations for global chain store brands

Most of global chains have a store locator in their website. This locator usually allows for searching by zip codes. Therefore, I begin by compiling a list of zip codes for the destination of interest. Below, I will use Seattle, WA, USA and McDonalds as an example. 
- First, collect zip codes from [WorldPostalCode](https://worldpostalcode.com/united-states/washington/seattle), which lists all the zip codes for cities all over the world. Zip code scraper can be found available [here](https://github.com/ruilinchen/chain_store_scraper/blob/master/zip_code_scraper.ipynb). All the collected zip codes are stored in a single file called "zip_codes_in_the_world.csv", which can be found in the [data folder](https://github.com/ruilinchen/chain_store_scraper/tree/master/data). 
- Second, write a scraper using Selenium to collect search results by zip codes. 
  - A prelimiary scraper is available [here](https://github.com/ruilinchen/chain_store_scraper/blob/master/mcdonalds_locator.py). It can now successfully:
    - enter zip code as search term
    - submit search request
    - display all the returned results in a single webpage. 
  - What is next:
    - collect store info from this webpage for each zip code
    - loop through all the zip codes. 

