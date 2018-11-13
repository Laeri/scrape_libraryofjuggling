# scrape_libraryofjuggling
Extract juggling trick data (name, difficulty, prerequisites) from http://libraryofjuggling.com/ with python and scrapy.

The scraped data is written to a csv file, every row representing a trick in the format:

`<Name`>,`<Difficulty`>,`<Prerequisites-list`>

NelsonsNemesis,5,Columns,RubensteinsRevenge

A trick may also have several prerequisites which are recommended to train before learning this one.

You can find the data in 'juggling_tricks.csv'

This code was written in order to use the extracted data for another project.

Run with 'scrapy crawl loj'
