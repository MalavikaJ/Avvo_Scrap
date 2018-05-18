import scrapy
from scrapy.http import Request


class Start(scrapy.Spider):
   name="start"
   start_urls=['https://www.avvo.com/all-lawyers/ny/new_york.html',]

   #scraping the first city in New York i.e. Accord
   def parse(self,response):
      for city in response.xpath('//div[@class="text-columns text-columns-narrowest text-columns-max-4 u-margin-bottom-0"]'):
         yield{'City':city.xpath('//ol[@class="unstyled-list"]/li[1]/a/text()').extract_first(),}

      #moving to the following page which contains the lawyers of Accord
      next_page=response.xpath('//div[@class="text-columns text-columns-narrowest text-columns-max-4 u-margin-bottom-0"]/ol/li[1]/a/@href').extract_first()
      print("url",next_page)
      if next_page is not None:
         yield response.follow(next_page,self.lawyers)#invokes method 'lawyer'
         print("success"),



   #follows the URL of each lawyer and scraps the corresponding data 
   def lawyers(self,response):
      print("y")
      lawyer_page=response.xpath('//div[@class="gtm-context"]/ul/li//div/figure/a/@href').extract()
      print("url=",lawyer_page)
      lawyer_page=list(set(lawyer_page))
      for url in lawyer_page:
         yield scrapy.Request(response.urljoin(url),callback=self.profile)#invokes method 'profile' which scraps the data
      for page in self.pagination(response):
         yield from self.pagination(response)#invokes method 'pagination' which follows the next page containing lawyers


   #follows the next page containing lawyers
   def pagination(self,response):         
      pagination_url=response.xpath('//li[@class="pagination-next"]/a/@href').extract_first()
      print("urlpp=",pagination_url)
      if pagination_url is not None:
         pagination_url=response.urljoin(pagination_url)
         yield scrapy.Request(pagination_url,callback=self.lawyers)#invokes method 'lawyer'


   #scraps the data for each lawyer
   def profile(self,response):
      for req in response.xpath('//div[@class="col-xs-8 col-sm-10 col-md-8"]'):
         yield{'Name':req.xpath('//h1[@class="u-vertical-margin-0"]/span/text()').extract_first(),}
         yield{'Client_Reviews':req.xpath('//span[@class="small"]/text()').extract_first(),
               'Client_Rating':req.xpath('//span[@class="sr-only"]/text()').extract_first(),
               'Avvo_Rating':req.xpath('//span[@class="h3"]/span/span[2]/span/text()').extract_first(),}

         
      for lic in response.css('ul.icon-list'):
         yield{'License':lic.xpath('//time/text()').extract_first(),}


      for img in response.xpath('//div[@class="card gtm-context overridable-lawyer-phone"]'):
         yield{'Image':img.xpath('//div[@class="col-xs-4 col-sm-2 col-md-4 remove-right-gutter"]//figure/img/@src').extract_first(),}


      for abt in response.xpath('//div[@class="col-xs-12 col-md-8 v-profile-layout"]'):
         yield{'About_Me':abt.xpath('//div[@class="card"]/div[1]/text()').extract_first(),}


      for prac in response.xpath('//div[@class="col-xs-12 col-sm-8"]'):
         yield{'Practice_Area':prac.xpath('//ol[@class="v-chart-legend-list unstyled-list"]/li//a/text()').extract(),}

      
      for adr in response.xpath('//div[@class="js-context js-map-container"]'):
         yield{'Street_Address':adr.xpath('//address[@class="js-context js-address js-v-address"]/span/p/span[1]/text()').extract_first(),
               'Address_Locality':adr.xpath('//address[@class="js-context js-address js-v-address"]/span/p/span[2]/text()').extract_first(),
               'Address_Region':adr.xpath('//address[@class="js-context js-address js-v-address"]/span/p/span[4]/text()').extract_first(),
               'Postal_code':adr.xpath('//address[@class="js-context js-address js-v-address"]/span/p/span[6]/text()').extract_first(),}

         yield{'Office':adr.xpath('//address[@class="js-context js-address js-v-address"]/span/div[1]/span[2]/a/span/text()').extract_first(),
               'Fax':adr.xpath('//address[@class="js-context js-address js-v-address"]/span/div[2]/span[2]/a/span/text()').extract_first(),}

      current_URL=response.request.url
      print("url="+current_URL)
      yield{'URL':current_URL}
      

     
            
