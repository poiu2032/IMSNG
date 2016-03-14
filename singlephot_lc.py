# Still writing 2015/09/18
# Changsu choi
# Light curve making code


from astropy.io import ascii
import matplotlib.pyplot as plt
import os

os.system('sh singlephot_process.sh')

bphot= ascii.read('ATEL7987-B-phot.txt')
vphot= ascii.read('ATEL7987-B-phot.txt')
rphot= ascii.read('ATEL7987-B-phot.txt')

bmjd,bap3mag,bap3err=bphot[''],bphot[''],bphot['']
vmjd,vap3mag,vap3err=vphot[''],vphot[''],vphot['']
rmjd,rap3mag,rap3err=rphot[''],rphot[''],rphot['']


fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(tt,snmag, marker='.',color='b',s=5)
#ax.set_ylim(2,4)
ax.grid(True)
ax.set_title('Light curve of NGC2442 in B band')
ax.set_xlabel('MJD')
ax.set_ylabel('MAG NOMAD catalog calibrated')

fig.savefig("lc_B.pdf")

