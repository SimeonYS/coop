import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import CoopItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class CoopSpider(scrapy.Spider):
	name = 'coop'
	start_urls = ['https://coopbank.dk/om-coop-bank/nyheder-og-presse/']

	def parse(self, response):
		post_links = response.xpath('//div[@class="col-sm-6 articlepadding "]//a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//p/em/text() | //h3/text()').get()
		title = ''.join(response.xpath('//h1//text()').getall())
		content = response.xpath('//div[contains(@class,"article")]//text()[not (ancestor::h1) and not (ancestor::p/em)]').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=CoopItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
