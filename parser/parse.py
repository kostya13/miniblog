from xml.etree.ElementTree import ElementTree
import codecs
separator = "@@@@@%%%^^(((&&&)))^^%%%@@@@@"
tree = ElementTree()
tree.parse("wp.xml")
channel = tree.find("channel")
out = codecs.open("database.txt", "w", "utf-8")
for item in channel:
    if item.tag == 'item':
        post = False
        category = []
        for i in item:
            if i.tag == '{http://purl.org/rss/1.0/modules/content/}encoded':
                content = i.text
            if i.tag == 'title':
                title = i.text
            if i.tag == 'category' and i.attrib['domain'] == 'category':
                category.append(i.text)
            if i.tag == '{http://wordpress.org/export/1.2/}post_date':
                date =  i.text
#2015-10-23 06:17:49
                post_date = "{}{}{}{}{}{}".format(date[0:4], date[5:7], date[8:10], date[11:13], date[14:16], date[17:19])
            if i.tag == '{http://wordpress.org/export/1.2/}post_type' and i.text == 'post':
                post = True
        if post:
#            print type(title)
            out.write(post_date + '\n' + title + '\n' + ','.join(category )+ '\n' + content + '\n' + separator + '\n')
out.close()
