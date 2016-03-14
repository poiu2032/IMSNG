#parallel python example for multi-core process usage for serial works
#import parallel python
import pp



#ready for ppserver 
ppservers=()
#ncpus
ncpus=4
#make job_server
#job_server = pp.Server(ncpus, ppservers=ppservers)
job_server = pp.Server(ppservers=ppservers)


'''
if len(sys.argv) > 1:
    ncpus = int(sys.argv[1])
    # Creates jobserver with ncpus workers
    job_server = pp.Server(ncpus, ppservers=ppservers)
else:
    # Creates jobserver with automatically detected number of workers
    job_server = pp.Server(ppservers=ppservers)
'''


#function 
def lacosmic(filename) :


#submit funtions to job server
jobs = [(input, job_server.submit(lacosmic, args=(input, ),modules=("cosmics", ))) for input in lists]



# for loop of function in job using multi-core
for input, job in jobs:
	job()


