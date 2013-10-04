######
# This script replaces values for max flow in a HEC-HMS input file
# This is hardwired to replace all loc- and in- elements
#
# Steve Skripnik
# Started: 2013-10-02
# V1
########################

import shutil, sys, csv

BASINFILE = 'BDale_detailed.basin'
EDITLIST = 'inletdata.csv'
OUTFILE = BASINFILE.split('.')[0]+'_new.basin'
DIVTABLENAME = 'dummy diversion'
LOGFILE = BASINFILE+'.log'

ok = raw_input('Modifying '+BASINFILE+' based on '+EDITLIST+' and saving as '+OUTFILE+'. Okay to continue? [Y]: ')

if ok.lower() <> 'y':
	print "Exiting program"
	sys.exit()

#read inlet list
f = open(EDITLIST,'rb')
inletlist=[]
a = csv.reader(f)
for i, line in enumerate(a):
	if i>0:
		f1,f2,f3,f4 = line
		inletlist.append((f1,f2,f3,f4))
f.close()


f = open(BASINFILE,'r')
basin_data = f.readlines()
f.close()

o = open(OUTFILE,'w')

#first, replace all diversion table names
print '* Replacing data.'
for row in inletlist:
	nname = row[0]
	nflow = row[3]
	print nname

	inLoc = False
	#errorcode = 0
	for i,row2 in enumerate(basin_data[:]):
		#print row2
		if inLoc == False:
			if 'diversion: '+nname.lower() in row2.lower():
				inLoc = True
				print "Found Diversion {}".format(nname)
		else:
			#print row2
			if "Maximum Diversion Flow:" in row2:
				
				newrow = "     Maximum Diversion Flow: {}\n".format(nflow)
				basin_data[i]=newrow
				print "Replaced {} diversion flow".format(nname)
			elif "Inflow Diversion Table Name:" in row2:
				
				newrow = "     Inflow Diversion Table Name: {}\n".format(DIVTABLENAME)
				basin_data[i]=newrow
				print "Replaced {} diversion table".format(nname)
			elif "End:" in row2:
				print "End of {} block".format(nname)
				inLoc = False
o.writelines(basin_data)
o.close()





