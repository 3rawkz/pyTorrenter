# -*- coding: utf-8 -*-
import scrapy
from tabulate import tabulate 


class L33tSpider(scrapy.Spider):
	name = 'l33t'
	allowed_domains = ['1337x.to']

	def start_requests(self):
		yield scrapy.Request('https://1337x.to/search/%s/1/'% self.search)

	def parse(self, response):
		for href in response.css('.table-list td.coll-1.name a::attr(href)').re('.*torrent.*'):
			yield scrapy.Request(response.urljoin(href),
								 callback=self.parse_page)

		for next in response.xpath("//a[contains(., '>>')]/@href").extract():
			yield scrapy.Request(response.urljoin(href),
								 callback=self.parse)

	def parse_page(self, response):
		title = response.css('h1::text').extract_first()
		descript = response.css('#description p::text').extract()
		files = response.css('#files li::text').extract()
		magnet = response.css('a.dbabbedb.btn.btn-bbecfcfa::attr(href)').extract_first()

		#info = ["TITLE: ", title],["Description: ", descript],["Files: ", files]
		info = [["TITLE: "],[title]]
		print tabulate(info, tablefmt="grid")
		#print(info)


		ibox = response.css('ul.list')
		row_head = ibox.css('li strong::text').extract()
		row_val = ibox.css('li span::text').extract()
		table = [list(x) for x in zip (row_head, row_val)]

		print tabulate(table, tablefmt="grid")

		#print(table)

		dlbox = response.css('.download-links-dontblock')
		dl_head = dlbox.css('li a::text').extract()
		dl_val = dlbox.css('li a::attr(href)').extract()
		table_links = [list(x) for x in zip (dl_head, dl_val)]

		