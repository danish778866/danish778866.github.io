import scrapy

class IMDbSpider(scrapy.Spider):
    name = "IMDb"
    start_urls = [
        'https://www.imdb.com/search/title?genres=sci-fi&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=75c37eae-37a7-4027-a7ca-3fd76067dd90&pf_rd_r=VF5X0WNXR03BP5XNGZHY&pf_rd_s=center-1&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr1_i_2',
    ]

    def validate_attributes(self, name, year, duration, genre, certificate, stars):
        ignore_movie = False
        if certificate is None or certificate.startswith("TV"):
            ignore_movie = True
        if name is None or name == "":
            ignore_movie = True
        if year is None or len(year) > 1 or len(year) == 0:
            ignore_movie = True
        if duration is None or duration == "":
            ignore_movie = True
        if genre is None or genre == "":
            ignore_movie = True
        if stars is None or len(stars) == 0:
            ignore_movie = True
        return ignore_movie

    def parse(self, response):
        for movie in response.css("div.lister-item"):
            name = movie.css("h3.lister-item-header a::text").get()
            year = movie.css("span.lister-item-year::text").re('\d+')
            duration = movie.css("span.runtime::text").get()
            genre = movie.css("span.genre::text").get().strip()
            stars_para = movie.xpath("./div/p[contains(., 'Stars:')]")
            ghost_span = stars_para.xpath(".//span[@class='ghost']")
            certificate = movie.css("span.certificate::text").get()
            if len(ghost_span) == 0:
                stars = stars_para.xpath(".//a/text()").getall()
            else:
                stars = stars_para.xpath(".//span[@class='ghost']/following-sibling::a/text()").getall()
            ignore_movie = self.validate_attributes(name, year, duration, genre, certificate, stars)
            if not ignore_movie and int(self.id) < int(self.num_tuples):
                self.id = int(self.id) + 1
                yield {
                    'id': self.id,
                    'name': name, 
                    'year': year, 
                    'duration': duration, 
                    'genre': genre, 
                    'actors': stars,
                }

        if int(self.id) < int(self.num_tuples):
            next_page = response.css("a.next-page::attr(href)").get()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)
