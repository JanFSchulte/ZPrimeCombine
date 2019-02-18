
def main():
	fname = "eventList.txt" 
	with open(fname) as f:
    		content = f.readlines()	
	for line in content:
		if float(line.split()[2]) > 1.2:
			print line.split()[1]

main()
