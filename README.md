# scrape_libraryofjuggling


Extract juggling trick data (name, difficulty, prerequisites) from http://libraryofjuggling.com/ with python and scrapy.

The scraped data is written to a csv file, every row representing a trick in the format:

`<Name`>,`<NumBalls>`,`<Difficulty`>,`<Prerequisites-list`>

NelsonsNemesis,5,Columns,RubensteinsRevenge

A trick may also have several prerequisites which are recommended to train before learning this one.
If a trick is a variation of some trick, such as 'Reverse Chops' is a variation of 'Chops',
we add the prefix [<Parent_Name>] to a trick name. But only in the first column.
Prerequisites are not named with the parent prefix.

You can find the data in 'juggling_tricks.csv'

This code was written in order to use the extracted data for another project.

Install: `pip install scrapy`
Run with 'scrapy crawl loj'
