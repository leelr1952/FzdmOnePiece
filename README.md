# FzdmOnePiece
风之动漫的版本是台版，其他动漫网上的几乎是大陆版，个人喜欢台版的翻译。。。

爬取基于scrapy基本模板；爬取的路径保存于mysql，在停止爬虫重新启动后可以检索数据库，跳过已爬过的url；有尝试使用imagepipeline，不过无法接受item信息，所以还是用普通pipeline，用urllib.request.urlretrieve处理图片保存