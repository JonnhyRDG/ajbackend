import os
import glob
import subprocess
import re
import shutil
from threading import Thread
from queue import Queue
from pprint import pprint as pp

jobs = Queue()
paths_dict = {
"remove" : [
	"P:\\AndreJukebox_dev\\asset_texture\\*\\*\\publish\\maps\\hi\\*.ini",
	"P:\\AndreJukebox_dev\\asset_texture\\*\\*\\publish\\maps\\hi\\*thumb*",
	"P:\\AndreJukebox_dev\\asset_texture\\*\\*\\publish\\maps\\hi\\*.db*",
	],
"rmtree" : [
	"P:\\AndreJukebox_dev\\asset_texture\\*\\*\\publish\\maps\\hi\\.mayaSwatches*",
	]
}

def removeFiles(path, mode='remove'):
	inifiles = glob.glob(path)
	for files in inifiles:
		print(files)
		if mode == 'rmtree':
			shutil.rmtree(files)
		else:
			os.remove(files)

	for key in paths_dict.keys():
		print(paths_dict[key])
		paths = paths_dict[key]
		print (type(paths))
		if type(paths) is list:
			for path in paths:
				print(path," ", key)
				removeFiles(path,mode=key)

	

def cmd_open(jobinput):
	while not jobinput.empty():
		command = jobinput.get()
		subprocess.call(command)
		print("Value: ", command)
		jobinput.task_done()

def maketx(texture):
	if os.path.splitext(texture)[1] in ['.jpg', '.png', '.tif', '.exr']:
		extension = texture.split('.')
		removecspace = extension[0].rsplit('_',1)[0]
		txpath = '{filename}.{extension}'.format(filename=removecspace,extension='tx')
		txout = os.path.abspath(txpath.replace("P:\\AndreJukebox_dev\\asset_texture","P:\\AndreJukebox\\assets\\"))
		findspace = extension[0].split("_")[-1]
		colorspace = re.search(findspace, texture)
		convert = colorspace.group(0)
		colorspace_dict = {
				'rec709':'linear',
				'linear':'linear',
				'raw':'raw'
		}

		ocio_cspace = colorspace_dict.get(convert)
		colorconfig = "P:\\AndreJukebox\\pipe\\ocio\\filmic\\config.ocio"
		command = f'P:\\AndreJukebox\\pipe\\ktoa\\ktoa4.2.3.2_kat6\\bin\\maketx.exe -v -u --colorconfig {colorconfig} --colorconvert {convert} {ocio_cspace} --oiio {texture} -o {txout}'
		print(command)
		jobs.put(command)
		

def maketxjobs():
	for i in range(32):
		worker = Thread(target=cmd_open, args=(jobs,))
		worker.start()
	print("waiting for queue to complete", jobs.qsize(), "tasks")
	jobs.join()

def makeAllTx():
	texfiles = glob.glob("P:\\AndreJukebox_dev\\asset_texture\\*\\*\\publish\\maps\\hi\\*")
	for tex in texfiles:
		maketx(texture=tex)
	maketxjobs()

def makeTxAsset(asset,object):
	if object == '':
		assetpath = f'P:\\AndreJukebox_dev\\asset_texture\\*\\{asset}\\publish\\maps\\hi\\*'
	else:
		assetpath = f'P:\\AndreJukebox_dev\\asset_texture\\*\\{asset}\\publish\\maps\\hi\\{asset}_{object}_*'
	assettextures = glob.glob(assetpath)
	print(assetpath)
	for t in assettextures:
		maketx(t)
	maketxjobs()

makeTxAsset('skysc00','interior')