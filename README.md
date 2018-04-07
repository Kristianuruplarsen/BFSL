# Scraping borgerforslag.dk

Borgerforslag.dk is a website where danish citizens an submit and vote on policy suggestions. Any suggestion that reaches more than 50.000 votes is to be debated in the danish Parliament.

Make sure to get the STATUSDATA.pickle file if you use this repo. There are a lot of gaps in the ordering of suggestion urls (i.e. theres a http://.../FT-00005 but the next in line is FT-00034), STATUSDATA.pickle contains information on which html's actually contain a suggestion, speeding up scraping significantly. 
