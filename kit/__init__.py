import re
import  string
import random


EMAIL_VALID = re.compile(r'^\w+[-+.\w]*@\w+([-.]\w+)*\.\w+([-.]\w+)*$')

Random = lambda x: ''.join(random.sample(string.ascii_letters + string.digits, x))

SMALL_KV = {}