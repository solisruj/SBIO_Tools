#!/usr/bin/python

# This is a crude re-array program that needs to be written. 

# Importing modules: pandas, numpy, and sys.
import pandas as pd
import numpy as np
import sys
import os

Input_CSV = sys.argv[1]
Number_Plates = sys.argv[2]
Destination_Plate = sys.argv[3]

Input_CSV = "candidate_problem_1_input.csv"
# I minus one here from Number_plates to match the number of input plates that tubes are being pulled from to match RI-1 and RI2 configurations. 
Number_Plates = (6)-1
Destination_Plate = "SA00507956"

data_file = pd.read_table(Input_CSV, sep=",")

Source_Rack_ID = data_file.iloc[:,0].copy()
Unique_SRID = Source_Rack_ID.drop_duplicates().copy()
USRID = Unique_SRID.reset_index(drop=True)

Alpha = [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
wells = []
for i in Alpha:
	for c in range(1,12):
		w_ids = i+str(c).zfill(2)
		wells.append(w_ids)

DesPLate = pd.DataFrame(data=wells)

DP = []
for r in range(0, len(data_file)):
	df_items = data_file.iloc[r:r+1,]
	x = df_items.values.tolist()
	DP_items = DesPLate.iloc[r:r+1]
	c = DP_items.values.tolist()
	#DP_items = DesPLate[r:r+1,]
	#print str(x[0][0]),"\t",str(x[0][1]), "\t", str(x[0][2]), "\t", Destination_Plate, "\t",str(c[0][0]), "\t", str(x[0][2])
	R_ =  x[0][0],x[0][1],x[0][2],Destination_Plate,c[0][0],x[0][2]
	DP.append(R_)

DF_M = pd.DataFrame(data=DP)
DF_M.columns = ['Source Rack ID','Source Tube','Sorce Barcode', 'Destination Rack ID', 'Destination Tube', 'Destination Barcode']


# Variables set to zero for counting. 
fc = 0
c_ = 0
fn = []
while True: 
	# Setting the file name and opening the first file. 
	file_name = Destination_Plate+"_"+str(c_)+".csv"
	fn.append(file_name)
	file = open(file_name, mode="w")
	file.write('Source Rack ID,Source Tube,Sorce Barcode,Destination Rack ID,Destination Tube,Destination Barcode,\n')
	# IDc (ID counter) variable set to zero for counting. 
	IDc = 0
	# For loop that reads throug each source barcode in USRID.
	for n in range(0, len(USRID)):
		# For loop that reads through DF_M dataframe. 
		for r_ in range(0, len(DF_M)):
			# Conditional statement to check if USRID equals the DF_M column source rack id, and if it mataches writes to open working file.
			if(USRID.iloc[n:n+1,].values[0] == DF_M.iloc[r_:r_+1,].values[0][0]):
				line = str(DF_M.iloc[r_:r_+1,].values[0][0])+","+str(DF_M.iloc[r_:r_+1,].values[0][1])+","+str(DF_M.iloc[r_:r_+1,].values[0][2])+","+str(DF_M.iloc[r_:r_+1,].values[0][3])+","+str(DF_M.iloc[r_:r_+1,].values[0][4])+","+str(DF_M.iloc[r_:r_+1,].values[0][5])+"\n"
				file.write(line)
		# IDc variable that adds one to iteself. 
		IDc = IDc + 1
		# This if conditional statement checks if IDC is equal to the number of plates robot instrument can handle, and if it is equal to Number_Plates it closes the file, resets IDc, and adds one to C_ counter.
		# The conditional also opens a new file to write information to and adds the approriate header. It also appends the file names to the fn (file name) list. 
		if(IDc==Number_Plates):
			file.close()
			IDc = 0
			c_ = c_ + 1
			file_name = Destination_Plate+"_"+str(c_)+".csv"
			#print "New file: "  + file_name
			fn.append(file_name)
			file = open(file_name, mode="w")
			file.write('Source Rack ID,Source Tube,Sorce Barcode,Destination Rack ID,Destination Tube,Destination Barcode,\n')
			
	if(fc <= 1 ):
		break		
# This line close the remaining open file.  
file.close()

for n in range(0, len(fn)):
	if(os.stat(fn[n]).st_size == 0):
		os.remove(fn[n])

