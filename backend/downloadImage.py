import requests

import random
import string

def get_random_string(length):
    # Random string with the combination of lower and upper case
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def downloadImage(url):
	print(url)
	deco = get_random_string(10)
	filename = 'E:/js/exten/rmads/backend/image/{}.jpg'.format(deco)
	f = open(filename,'wb')
	f.write(requests.get(url).content)
	f.close
	return filename,'{}.jpg'.format(deco)