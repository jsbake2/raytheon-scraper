import time
from scrapy.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.http.request import Request
from raytheon.items import RaytheonItem
from scrapy.http import HtmlResponse
import json
from scrapy.exceptions import CloseSpider


class RaytheonspiderSpider(CrawlSpider):

    name = "raytheonJobsStart"
    page = 150
    ajaxURL = "https://jobs.raytheon.com/search-jobs/results?ActiveFacetID=0&RecordsPerPage=15&Distance=50&RadiusUnitType=0&Keywords=&Location=&Latitude=&Longitude=&ShowRadius=False&CustomFacetName=&FacetTerm=&FacetType=0&SearchResultsModuleName=Search+Results&SearchFiltersModuleName=Search+Filters&SortCriteria=5&SortDirection=1&SearchType=5&CategoryFacetTerm=&CategoryFacetType=&LocationFacetTerm=&LocationFacetType=&KeywordType=&LocationType=&LocationPath=&OrganizationIds=&CurrentPage="

    def start_requests(self):
      yield Request(self.ajaxURL + str(self.page), callback=self.parse_listings)

    def parse_listings(self, response):
      resp = json.loads(response.body)
      response = Selector(text = resp['results'])
      jobs = response.xpath('//*[@id="search-results-list"]/ul/*/a/@href').extract()
      if jobs:
        for job_url in jobs:
          print("This is a fucking stupid issue... FIX IT:     "+job_url)
          job_url = "https://jobs.raytheon.com" + self.__normalise(job_url)
          yield Request(url=job_url, callback=self.parse_details)
      else:
        raise CloseSpider("No more pages... exiting...")
      # go to next page...
      self.page = self.page + 1
      yield Request(self.ajaxURL + str(self.page), callback=self.parse_listings)


    def parse_details(self, response):
      print("This is a fucking stupid issue... FIX IT:     "+str(response))
      sel = Selector(response)
      job = sel.xpath('//*[@id="content"]')
      item = RaytheonItem()
      # Populate job fields
      item['title'] = job.xpath('//*[@id="content"]/section[1]/div/h1/text()').extract()
      jobTitle=job.xpath('//*[@id="content"]/section[1]/div/h1/text()').extract()
      item['reqid'] = job.xpath('//*[@id="content"]/section[1]/div/span[1]/text()').extract()
      item['location'] = job.xpath('//*[@id="content"]/section[1]/div/span[last()]/text()').extract()
      item['applink'] = job.xpath('//*[@id="content"]/section[1]/div/a[2]/@href').extract()
      item['description'] = job.xpath('//*[@id="content"]/section[1]/div/div').extract()
      item['clearance'] = job.xpath('//*[@id="content"]/section[1]/div/span[5]').re(r'Type</b> <br>\r\n            (.*)</span>')
      item['clearanceAndJunk'] = job.xpath('//*[@id="content"]/section[1]/div/span[5]').extract()
      #item['page_url'] = response.url
      item = self.__normalise_item(item, response.url)
      return item

    def __normalise_item(self, item, base_url):
      '''
      Standardise and format item fields
      '''

      # Loop item fields to sanitise data and standardise data types
      for key, value in vars(item).values()[0].iteritems():
        item[key] = self.__normalise(item[key])

      # Convert job URL from relative to absolute URL
      #item['job_url'] = self.__to_absolute_url(base_url, item['job_url'])
      return item

    def __normalise(self, value):
      print self,value
      # Convert list to string
      value = value if type(value) is not list else ' '.join(value)
      # Trim leading and trailing special characters (Whitespaces, newlines, spaces, tabs, carriage returns)
      value = value.strip()
      return value

    def __to_absolute_url(self, base_url, link):
      '''
      Convert relative URL to absolute URL
      '''
      import urlparse

      link = urlparse.urljoin(base_url, link)

      return link

    def __to_int(self, value):
      '''
      Convert value to integer type
      '''

      try:
        value = int(value)
      except ValueError:
        value = 0

      return value

    def __to_float(self, value):
      '''
      Convert value to float type
      '''

      try:
        value = float(value)
      except ValueError:
        value = 0.0

      return value
