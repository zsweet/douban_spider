# -*- coding: utf-8 -*-
import pymongo
import scrapy
from bson import ObjectId
from cqc_douban.items import CqcDoubanItem
from scrapy import Request


class DoubanSpider(scrapy.Spider):
    name = "douban"
   # allowed_domains = ["movie.douban.com/subject/1291549/"]
   # start_urls = ['http://movie.douban.com/subject/1291549//']
   # id = 'defaulte'

    def parse(self, response):
        item = CqcDoubanItem()
        item['id'] = response.meta['data']['id']
        item['source'] = response.meta['data']['source']
        item['content'] = response.meta['data']['content']
        item['title'] = response.meta['data']['title']
        item['tags'] = response.meta['data']['tags']
        item['url'] = response.meta['data']['url']

        item['actors'] = actors = response.css('div[id="info"] .actor .attrs a::text').extract()  #主演
        item['director'] = director = response.css('div[id="info"] .attrs a[rel="v:directedBy"]::text').extract_first()  #导演
        country = response.xpath(u'//span[contains(./text(), "制片国家/地区:")]/following::text()[1]').extract_first()
        if country != None :
            item['country'] = country.split('/')
        else:
            item['country'] = ''
        item['dateCountry'] = dateCountry = response.css('div[id="info"]  span[property="v:initialReleaseDate"]::text').extract()  # 上映时间和国家
        language = response.xpath(u'//span[contains(./text(), "语言:")]/following::text()[1]').extract_first()
        if language != None :
            item['language'] = language.split('/')
        else:
            item['language'] = ''
        item['duration'] = duration = response.css('div[id="info"] span[property="v:runtime"]::text').extract_first()  # shijian
        if item['duration'] == None :
            item['duration'] = response.xpath(u'//span[contains(./text(), "单集片长:")]/following::text()[1]').extract_first()
            if item['duration']!= None :
                item['duration'] = item['duration']+'（单集）'
        nickname = response.xpath(u'//span[contains(./text(), "又名:")]/following::text()[1]').extract_first()
        if nickname!=None :
            item['nickname'] = nickname.split('/')
        else:
            item['nickname'] = ''

        #item['imdb'] = imdb = response.css('div[id="info"] a[rel="nofollow"]::text').extract_first()  # 导演
        item['imdb'] = imdb = response.xpath(u'//span[contains(./text(), "IMDb链接:")]/following::text()[2]').extract_first()
        item['kind'] = kind = response.css('div[id="info"] span[property="v:genre"]::text').extract()  # 导演
        item['comments'] = comments = response.css('div[id="comments-section"] div[id="hot-comments"] .comment-item p::text').extract()  #导演
        reviews = response.css('section[class="reviews mod movie-content"] div[class="review-list"] div[class="main-bd"] div[class="short-content"]::text').extract()  #导演
        item['rating'] = rating = response.css('div[id="interest_sectl"] strong[class="ll rating_num"]::text').extract_first()
        item['rating_sum'] = rating_sum = response.css('div[id="interest_sectl"] .rating_sum span::text').extract_first()
        item['rating_per'] = rating_weight_stars = response.css('div[id="interest_sectl"] .ratings-on-weight .item .rating_per::text').extract()
        item['rating_betterthan'] = rating_betterthan = response.css('div[id="interest_sectl"] .rating_betterthan a::text').extract()

        infospan = response.css('div[id="info"] span')
        screenwriter = ''
        for index in range(len(infospan)):
            if infospan[index].css('span::text').extract() == ['编剧'] :
                screenwriter = infospan[index+1].css('a::text').extract()
        item['screenwriter'] = screenwriter

        item['reviews'] = []
        for index in range(0,len(reviews),3):
            item['reviews'].append(reviews[index])

        #
        # infos = response.xpath('//div[@id="info"]/*')
        # print(infos.extract())
        # for index in range(len(infos)):
        #     if infos[index].xpath('text()').extract() == ['制片国家/地区:']:
        #         print(infos[index+1])
        #         country = infos[index+1].xpath('text()')
     #   screenwriter = response.css('div[id="info"] span [a::text="编剧"]').extract()
       # country = response.css('div[id="info"] span ').extract()
       # print ('infos:')
       # print(infos)
       #  print('actors:')
       #  print(actors)
       #  print('director:')
       #  print(director)
       #  print('screenwriter:')
       #  print(screenwriter)
       #  print('country:')
       #  print(country)
       #  print('dateCountry:')
       #  print(dateCountry)
       #  print('language:')
       #  print(language)
       #  print('nickname:')
       #  print(nickname)
       #  print('duration:')
       #  print(duration)
       #  print('imdb:')
       #  print(imdb)
       #  print('kind:')
       #  print(kind)
       #  print('comments:')
       #  print(comments)
       #  print('reviews:')
       #  print(item['reviews'])
       #  print('rating:')
       #  print(rating)
       #  print('rating_sum:')
       #  print(rating_sum)
       #  print('rating_weight_stars:')
       #  print(rating_weight_stars)
       #  print('rating_betterthan:')
       #  print(rating_betterthan)
      #  for review in reviews:
           # print "!! %s"%(review)
        yield item


    def start_requests(self):
        try:
            client = pymongo.MongoClient(self.settings.get('MONGO_URI'))
            db = client[self.settings.get('MONGO_DB')]
            collection = db[self.settings.get('MONGO_COL')]
        except BaseException as e:
            print('！！！Reason in connect database:')
            print(e)
      #  try:
     # #       if client.get_database(self.settings.get('MONGO_DB')):
     #            print("Connection Successful!")
     #    except:
     #        print ("Failed to connect to server")
     #        print (self.settings.get('MONGO_URI'))


        #db = client[ self.settings.get('MONGO_DB')]
        #print(db.name)
     #   print('这是名字')
       # collection = db[self.settings.get('MONGO_COL')]
        #print( collection.find().count()    )

       # print("GGGGGGGGGGGGGGGGGGGGGGGGG!!!!")
       # yield  Request("https://movie.douban.com/subject/1291549/",self.parse)
        #print("数据库连接状态 %d " % collection.status())
        for tmp in  collection.find():#.skip(21600):#.limit(3).skip(2315)
            print(tmp['id'])
            yield Request(tmp['url'],self.parse,meta={'data':tmp})


# 现在已经爬下来了一批豆瓣电影数据，需要更详细的信息，这里需要你来爬一下，顺便练练手。
# 字段
# 简介 introduction
# 主演 actors   (list形式)
# 导演  director
# 编剧 screenwriter
# 国家 country
# 上映日期  date
# 上映国家
# 语言  language
# 片长 duration
# IMDB  imdb
# 类型 kind  (list形式)
# 评分 score
# 评论 comments (list形式)
# 影评 reviews (list形式)
# 把这些内容存回MongoDB里面。
# 可能有的英文表示不好，也可能有些list形式没标全，你具体看看哪些string，哪些 list
# MongoDB
#
# 优先用主：mongodb://root:job123buaa@106.14.147.212:3718/admin
#
# 如果遇到主挂了的情况，再用从：mongodb://root:job123buaa@106.14.147.212:3717/admin
#
# 两个加一个try except 判断吧。
#
# 数据在 douban movies
#
# 里面有数据了，但是缺上面的字段，你爬一下，然后存进来，两万多个，爬完增加这些字段即可，还是存在这里面，使用Mongo $set 操作增加这些字段即可。
#
# 建议：提前做好备份！！
#
# 使用 MongoChef 可视化管理工具