import os
import glob
import subprocess
import re
import shutil
from threading import Thread
from queue import Queue
from pprint import pprint as pp

def removeFiles(path, mode='remove'):
	inifiles = glob.glob(path)
	for files in inifiles:
		print(files)
		if mode == 'rmtree':
			shutil.rmtree(files)
		else:
			os.remove(files)

paths_dict = {
"remove" : [
	"I:/asset_texture/*/*/publish/maps/hi/*.ini",
	"I:/asset_texture/*/*/publish/maps/hi/*thumb*",
	"I:/asset_texture/*/*/publish/maps/hi/*.db*",
	],
"rmtree" : [
	"I:/asset_texture/*/*/publish/maps/hi/.mayaSwatches*",
	]
}

for key in paths_dict.keys():
	print(paths_dict[key])
	paths = paths_dict[key]
	print (type(paths))
	if type(paths) is list:
		print("List indeed!")
		for path in paths:
			print(path," ", key)
			removeFiles(path,mode=key)

####### Generate all the LOW and MID folders for the lower res textures ######
result = glob.glob("I:/asset_texture/*/*/publish/maps/hi")
for path in result:
	lowdir = os.path.abspath(path.replace("hi","low"))
	middir = os.path.abspath(path.replace("hi","mid"))
	isExist = os.path.exists(lowdir)
	isExist = os.path.exists(middir)
	if not isExist:
		os.makedirs(lowdir)
	if not isExist:
		os.makedirs(middir)

###### Uses ImageMagick to convert the MID textures to 1024*1024 and LOW to 512*512, writes out the file ######
texfiles = glob.glob("I:/asset_texture/*/*/publish/maps/hi/*")
for hiinfile in texfiles:
	if os.path.splitext(hiinfile)[1] in ['.jpg','.png','.tif','.exr']:
		lowoutfiles = os.path.abspath(hiinfile.replace("hi","low"))
		midoutfiles = os.path.abspath(hiinfile.replace("hi","mid"))
		midexist = os.path.exists(midoutfiles)

		if not midexist:
			subprocess.call(['C:/Program Files/ImageMagick-6.9.12-Q16/convert.exe', hiinfile, '-resize', '1024x1024', midoutfiles])
			confirmmid = "___________________________{filename} - has been copied and rezised correctly___________________________".format(filename = midoutfiles)
			print(confirmmid)
		else:
			midexists = "{} already exists!".format(midoutfiles)
			print(midexists)


		lowexist = os.path.exists(lowoutfiles)
		if not lowexist:
			subprocess.call(['C:/Program Files/ImageMagick-6.9.12-Q16/convert.exe', hiinfile, '-resize', '512x512', lowoutfiles])
			confirmlow = "___________________________{filename} - has been copied and rezised correctly___________________________".format(filename = lowoutfiles)
			print(confirmlow)
		else:
			lowexists = "{} already exists!".format(lowoutfiles)
			print(lowexists)

print('#_________________________________________________LOW and MID folders created, FILES resized___________________#')

#________________________________________________________#
#_____________________create folders_____________________#
#________________________________________________________#

result = glob.glob("I:\\asset_texture\\*\\*\\publish\\maps\\*")
for tx in result:
	source = os.path.abspath(tx)
	project = 'P:\\AndreJukebox\\assets\\'
	b=tx.split('\\')
	distdir = "{projectdir}{type}\\{asset}\\{pub}\\{texdir}\\{res}".format(projectdir=project,type=b[2],asset=b[3],pub=b[4],texdir=b[5],res=b[6])
	isExist = os.path.exists(distdir)
	
	if not isExist:
		os.makedirs(distdir)
		dircreated = "{dircreatedok} created!".format(dircreatedok=distdir)
		print(dircreated)
	else:
		dexistconfirm = "_____________________________{diristhere} already exist. Skipping._____________________________".format(diristhere=distdir)
		print(dexistconfirm)

#_________________________________________________#
#_____________________MAKE TX_____________________#
#_________________________________________________#

def cmd_open(jobinput):
	while not jobinput.empty():
		command = jobinput.get()
		subprocess.call(command)
		print("Value: ", command)
		jobinput.task_done()
jobs = Queue()

paths = glob.glob("I:\\asset_texture\\*\\*\\publish\\maps\\*\\*")

for tex in paths:
	if os.path.splitext(hiinfile)[1] in ['.jpg', '.png', '.tif', '.exr']:
		extension = tex.split('.')
		removecspace = extension[0].rsplit('_',1)[0]
		txpath = '{filename}.{extension}'.format(filename=removecspace,extension='tx')
		txout = os.path.abspath(txpath.replace("I:\\asset_texture\\","P:\\AndreJukebox\\assets\\"))
		findspace = extension[0].split("_")[-1]
		colorspace = re.search(findspace, tex)
		convert = colorspace.group(0)
		print(txout)
		print(convert)
		colorspace_dict = {
				'rec709':'linear',
				'linear':'linear',
				'raw':'raw'
		}

		ocio_cspace = colorspace_dict.get(convert)
		colorconfig = "P:/AndreJukebox/pipe/ocio/filmic/config.ocio"
		command = 'P:/AndreJukebox/pipe/ktoa/ktoa4.1.2.1_kat5/bin/maketx.exe -v -u --colorconfig {ocio} --colorconvert {orig} {cspace} --oiio {textin} -o {txdest}'.format(ocio=colorconfig,cspace=ocio_cspace,textin=tex,txdest=txout,orig=convert)
		txexist = os.path.exists(txout)
		print(command)
		if not txexist:
			jobs.put(command)
		else:
			print('TX file already exists. Skipping')

for i in range(10):
	worker = Thread(target=cmd_open, args=(jobs,))
	worker.start()
print("waiting for queue to complete", jobs.qsize(), "tasks")
jobs.join()


print('#_________________________________________________TX FILES DONE_________________________________________________#')