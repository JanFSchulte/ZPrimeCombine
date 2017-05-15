import subprocess, os


def main():

	path = "submission/crab_projects"

	crabDirs = os.listdir(path)

	for dir in crabDirs:
		command = ["crab","resubmit","%s/%s"%(path,dir)]
		subprocess.call(command)


main()
