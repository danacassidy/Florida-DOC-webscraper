# Florida-DOC-webscraper

This is a web scraper I built during my internship at the Miami Herald in 2021. I built it using python, selenium, and beautiful soup tin order to find and categorizes information from multiple sites on thousands of Florida Department of Corrections inmates who died each fiscal year. 

The program is published on here with a Jupyter notebook for clarity and easier reading. The website automatically opens a browser and collects the data from each listed inmate. It then goes one step further and *clicks* on a desired hyperlink of an inmate’s “DC Number” and collects the data from the second link, as well.


The collected data is then transferred to a CSV file and used to analyze further. My go-to analysis method is Pandas. 

Web scraping is important in journalism because it allows reporters to access information that might take too long to request via public records. The Florida Department of Corrections is nearly impossible to get requests filled from. This project taught me how to use Selenium and BeautifulSoup more efficiently in a real-world setting.
