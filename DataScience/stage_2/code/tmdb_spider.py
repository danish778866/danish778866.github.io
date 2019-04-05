import scrapy

class TMDbSpider(scrapy.Spider):
    name = "TMDb"
    start_urls = ['https://www.themoviedb.org/movie']

    def parse(self, response):
        for href in response.css("p.view_more a::attr(href)"):
            yield response.follow(href, self.parse_movie)
        self.num_pages = int(self.num_pages) - 1
        if self.num_pages > 0:
            for href in response.css("a.next_page::attr(href)").getall():
                yield response.follow(href, self.parse)

    def parse_movie(self, response):
        name = response.css("div.title a h2::text").get()
        year = response.css("div.title span span.release_date::text").re('\d+')
        genre_column = response.css("section.genres")
        genre = genre_column.css("li a::text").getall()
        panel = response.css("section.panel")
        stars = panel.css("ol li p a::text").getall()
        split_column = column = response.css("section.split_column")
        duration = split_column.xpath("//parent::*[*/bdi[contains(text(), 'Runtime')]]/text()").get().strip()
        self.id = int(self.id) + 1

        yield {
            'id': self.id,
            'name': name,
            'year': year,
            'duration': duration,
            'genre': genre,
            'actors': stars,
        }
