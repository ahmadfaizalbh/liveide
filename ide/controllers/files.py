import os
import json
import uuid

from ide.bottle import *
from ide.bottleauth import User
from ide import settings
from ide import models
from ide.decorators import login_required


@login_required
@get('/files/')
def files_list():
	'''
	Returns list of files in user top dir.
	E.g., files not assigned to any project.
	'''

	user_id = User().id
	path = "%s%i/" % (settings.PROJECTS_ROOT, user_id)

	f = {}
	for (dirpath, dirname, filenames) in os.walk(path):
		# TODO: consider to read content of file
		# File ID: uuid.uuid4().hex is one time ID for file
		# to make it possible to handle it in UI
		f = [{
			"id": uuid.uuid4().hex,
			"title": x,
			"path": x, # this is files in user's ROOT so path is filename
			"dir": ""
		} for x in filenames]

		break
	
	return json.dumps(f)


@login_required
@post('/file_create/')
def file_create():
	'''
	Adds new file for loggedin user.
	Creates file on FS.
	File can be assigned to project or not assigned.
	'''
	
	title = request.POST.get("title")
	content = request.POST.get("content", "")
	rel_dir = request.POST.get("dir", "")
	file_path = rel_dir + "/" + title

	user_id = User().id
	project_id = request.POST.get("project")

	path = "%s%i/" % (settings.PROJECTS_ROOT, user_id)
	
	if project_id:
		project = models.Project.find_one({"id": project_id})

	if not os.path.exists(path + file_path):
		try:
			fo = open(path + file_path, "wb")
			fo.write(content)
		except:
			return json.dumps({"msg": "Error creating file!"})
		finally:
			fo.close()

		# uuid.uuid4().hex is just one time ID for file, for UI usage only
		c = {
			"id": uuid.uuid4().hex,
			"title": title,
			"project": project_id,
			"content": content,
			"path": file_path,
			"dir": rel_dir,
		}

		return json.dumps(c)

	return json.dumps({"msg": "File exists!"})


@login_required
@post('/file_remove/')
def file_remove():
	'''
	Removes file from FS.
	NOT REVERTABLE.
	'''

	user_id = User().id
	path = "%s%i/" % (settings.PROJECTS_ROOT, user_id)
	file_path = request.POST.get("path")

	if not file_path:
		return json.dumps({"msg": "Specify file name!"})

	# Remove on FS
	if os.path.exists(path + file_path):
		try:
			os.remove(path + file_path)
		except:
			return json.dumps({"msg": "Removing on FS failed!"})

	return "{}"


@login_required
@get("/file_content/")
def file_content():
	'''
	Reads file on FS
	'''

	content = ""
	user_id = User().id
	path = "%s%i/" % (settings.PROJECTS_ROOT, user_id)
	file_path = request.GET.get("path")

	if not file_path:
		return "Specify file name!"

	try:
		fo = open(path + file_path, "rb")
		content = fo.read()
	except:
		content = "Error reading file!"
	finally:
		fo.close()

	return content


@login_required
@post("/file_save/")
def file_save():
	'''
	Save file on FS
	'''

	user_id = User().id
	path = "%s%i/" % (settings.PROJECTS_ROOT, user_id)
	file_path = request.POST.get("path")
	content = request.POST.get("content")

	if not file_path:
		return json.dumps({"msg": "Specify file name!"})

	try:
		fo = open(path + file_path, "wb")
		fo.write(content)
	except:
		return json.dumps({"msg": "Error writing file!"})
	finally:
		fo.close()

	return "{}"