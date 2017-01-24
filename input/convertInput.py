
def main():
	fname = "dimuon_13TeV_FullDataset.txt" 
	with open(fname) as f:
    		content = f.readlines()	
	for line in content:
		print line.split(" ")[1]

main()
