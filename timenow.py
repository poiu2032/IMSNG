#linux : 
# %> date '+%F  %r'

import time
now = time.localtime()


print "Year  : %d" % (now.tm_year)
print "Month : %d" % (now.tm_mon)
print "Day   : %d" % (now.tm_mday)

print "$$$$:$$:$$ T$$:$$:$$ format"
print '%d'% now.tm_year+':'+'%2d.'%now.tm_mon+':'+'%2d'%now.tm_mday+': T'+'%2d'%now.tm_hour+':'+'%2d'%now.tm_min+':'+'%2d'%now.tm_sec+'local time'


#vis= '{:4s}:{:2f}:{:2f} T{:2f}:{2f}:{:2f}'.format(str(now.tm_year), now.tm_mon, now.tm_mday, now.tm_hour,now.tm_min,now.tm_sec)

print "Hour   : %d" % (now.tm_hour)         # 24hour
print "Minute : %d" % (now.tm_min)
print "Second : %d" % (now.tm_sec)

print

print "Weekday                     : %d"  % (now.tm_wday)  # Monday = 0
print "Days from First day of year : %d"  % (now.tm_yday)  # 01/01 = 1
print "Day time saving             : %d"  % (now.tm_isdst) # noDTS = 0

