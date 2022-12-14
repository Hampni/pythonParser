import redis

# Read from standalone REDIS
rd = redis.Redis(host='localhost',
                 port=6379)


for i in range(3881):
	rd.lpop('letter_links')

print('letter links: ')
print(rd.llen('letter_links'))
print('bad links: ')
print(rd.llen('bad_links'))

# # print(rd.lpop('letter_links'))


