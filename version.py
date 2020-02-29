
import os
import subprocess

# The Major.Minor version of the app
BASE_VERSION = "0.0"

# Calculate the commit count and use it as a build number
proc = subprocess.Popen(
    'git fetch --unshallow origin; '
    'git rev-list --count origin/`git rev-parse --abbrev-ref HEAD`',
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)
stdout, _ = proc.communicate()

commitCount = int(stdout.strip(), 10)

versionNumber = "{}.{}".format(BASE_VERSION, commitCount)

# Update the build number in the setup.py file
dirName = os.path.dirname(__file__)
setupFile = os.path.join(dirName, 'setup.py')

with open(setupFile, 'r') as infile:
    setupFileData = infile.readlines()

for i, line in enumerate(setupFileData):
    if not line.startswith('version = '):
        continue
    setupFileData[i] = "version = '{}'\n".format(versionNumber)
    break

with open(setupFile, 'w') as outfile:
    outfile.writelines(setupFileData)

print(versionNumber)
