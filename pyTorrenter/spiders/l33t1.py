# -*- coding: utf-8 -*-
import scrapy
from tabulate import tabulate 
import texttable

class L33tSpider(scrapy.Spider):
	name = 'l33t1'
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
		ibox = response.css('ul.list')
		row_head = ibox.css('li strong::text').extract()
		row_val = ibox.css('li span::text').extract()
		r_len = len(row_head)

		tab = texttable.Texttable()

		for x in range(r_len):
			tab.add_row([row_head[x], row_val[x]])
		s = tab.draw()
		print(s)


		dlbox = response.css('.download-links-dontblock')
		dl_head = dlbox.css('li a::text').extract()
		dl_val = dlbox.css('li a::attr(href)').extract()
		table_links = [list(x) for x in zip (dl_head, dl_val)]

		title = response.css('h1::text').extract()
		title = [x.strip() for x in title]
		title = ''.join(title)

		descript = response.css('#description p::text').extract()
		descript = ''.join(descript)
		descript = descript.replace('\r', ' - ')

		files = response.css('#files li::text').extract()
		magnet = magnet = response.xpath("//a[contains(., 'Magnet Down')]/@href").extract()

		infotab = texttable.Texttable()
		mheader = ["Torrent | " + title]
		infotab.header(mheader)
		infotab.add_row([descript])
		infotab.add_row([magnet])
		a = infotab.draw()
		print(a)


		