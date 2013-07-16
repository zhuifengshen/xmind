#XMind SDK for python

**XMind SDK for python** to help python developers to easily work with XMind file and build XMind extensions.

##Install XMind SDK for python

Clone repository to local working directory

	git clone https://github.com/xmindltd/xmind-sdk-python.git
	
right now, you got directory named `xmind-sdk-python` under current directory. Change to directory `xmind-sdk-python` and install **XMind SDK for python**.

	python setup.py install
	
*We're highly recommend to install **XMind SDK for python** under isolate python environment using [virtualenv](https://pypi.python.org/pypi/virtualenv)*

##Usage

Open XMind file from exists path or create new XMind file and will placed to path

	import xmind
	workbook = xmind.load(/path/to/file/)
	
Save XMind file to given path, if path not given then will save to path that set to workbook

	xmind.save(workbook)

or given path:
	
	xmind.save(workbook, /save/file/to/path)