import astropy.table as tbl

filename='obsobj.txt'
tt=tbl.Table.read(filename,format='ascii')

ind=np.where(tt['col2']=='B')

#tt.sort(['col2'])

tt[ind].write('bobj.txt',format='ascii',names=('#name', 'filter', 'obj', 'type', 'exp', 'etc'))
