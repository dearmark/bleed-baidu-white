#-*- coding:utf-8 -*-

from flask import Flask, g, request, render_template
from bs4 import BeautifulSoup

app = Flask(__name__)
app.debug = True
 
@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/baidu/<id>/<uk>')
def baidu(id,uk):
	import urllib,urllib2
	from bs4 import BeautifulSoup
	from flask import jsonify
	app.logger.warning('Request id:'+id)
	app.logger.warning('Request uk:'+uk)
	url = 'http://pan.baidu.com/share/link?shareid=%s&uk=%s' %(id,uk)
	header = {
		'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.8.1.14) Gecko/20080404 (FoxPlus) Firefox/2.0.0.14',
	}
	request = urllib2.Request(url= url,headers = header)
	html_code = urllib2.urlopen(request).read()
	soup = BeautifulSoup(html_code)
	results = soup.find_all('a',attrs={"class": "new-dbtn"})

	for result in results:
		return jsonify(
				id=id,
				uk=uk,
				error=False,
				link=result.get('href'),
				type='baidu'
			)
	return jsonify(
			id=id,
			uk=uk,
			error=True,
			type='baidu'
		)
 
from bae.core.wsgi import WSGIApplication
application = WSGIApplication(app)

