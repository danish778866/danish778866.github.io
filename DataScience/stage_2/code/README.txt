Please execute the following commands sequentially to replicate our setup:
Note: The commands setup a virtual environment and assume that you've downloaded 
the files imdb_spider.py, tmdb_spider.py and placed it in the directory where
the commands are being executed.

virtualenv myenv
source myenv/bin/activate
pip install Scrapy
scrapy startproject movies_crawler
mv imdb_spider.py movies_crawler/movies_crawler/spiders
mv tmdb_spider.py movies_crawler/movies_crawler/spiders
cd movies_crawler/movies_crawler
scrapy crawl IMDb -a num_tuples=5000 -a id=0 -o mdb.csv -t csv
scrapy crawl TMDb -a num_pages=250 -a id=0 -o tmdb.csv -t csv
