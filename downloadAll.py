import subprocess

widths = ['050','075','100','125','150','175','200','225','250','275','300','325','350']
#widths = ['275','300','325','350']
#widths = ['200']

for width in widths:
	#command = ['python' , 'harvestCRABResults.py', '-c',  'ICHEP_width%s'%width, '-t', 'forDM' ,'-u', 'jan']
	#subprocess.call(command)
	#command = ['python' , 'harvestCRABResults.py', '-c',  'ICHEPDimuon_width%s'%width, '-t', 'forDM' ,'-u', 'jan']
	#subprocess.call(command)
	command = ['python' , 'harvestCRABResults.py', '-c',  'ICHEPDielectron_width%s'%width, '-t', 'forDM' ,'-u', 'jan','--merge']
	subprocess.call(command)
