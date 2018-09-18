
import mechanize

# feed the input data to the http://quid.hpl.hp.com:9081/cacti/index.y?new
# then store back to the current location
def power(cache):
	m=0
#configuration changed
	name=""
	cache_size=[]
	assoc=[]
	cache_size1=[32768,65536]
	assoc1=[1,2]
	cache_size2=[131072,262144]
	assoc2=[4,8]
	if(cache==1):
		cache_size=cache_size1
		assoc=assoc1
		name="outputl1.htm"
	if(cache==2):
		cache_size=cache_size2
		assoc=assoc2	
		name="outputl2.htm"	
	for i in range(2):
		for k in range(2):
			br = mechanize.Browser()
			br.set_handle_robots(False)
	# Add User-Agent
			br.addheaders = [("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36")]
			br.open('http://quid.hpl.hp.com:9081/cacti/index.y?new')
			#select form
			br.select_form(nr=0)
			m=m+1
			br["cache_size"]=str(cache_size[k])
			br["line_size"]="64"
			br["assoc"]=str(assoc[i])
			br["nrbanks"]="1"
			br["technode"]="90"
			br.submit()
			br.response().get_data()
			with open(str(m)+name,"w") as f:
				f.write(br.response().get_data())
def main():

	power(1)
	power(2)
	br = mechanize.Browser()
	br.set_handle_robots(False)
	# Add User-Agent
	br.addheaders = [("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36")]
	br.open('http://quid.hpl.hp.com:9081/cacti/index.y?new')
	#select form
	br.select_form(nr=0)
	# fill in blank
	br["cache_size"]="4194304"
	br["line_size"]="64"
	br["assoc"]="16"
	br["nrbanks"]="1"
	br["technode"]="90"
	br.submit()
	br.response().get_data()
	with open("l3.html","w") as f:
		f.write(br.response().get_data())
if __name__ == "__main__":
        main()

