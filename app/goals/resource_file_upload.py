############### uploade resource files ##############

#FROM https://www.tutorialspoint.com/flask/flask_file_uploading.htm
# and FROM https://www.youtube.com/watch?v=TLgVEBuQURA

from flask import Flask, render_template, request
from werkzeug import secure_filename

@app.route('/resource_upload_file', methods = ['GET', 'POST'])
def resource_upload_file():
	if request.method == 'GET':
		return render_template('resource_upload_file.html')

	uploaded_file = request.files['file']
	uploaded_file.save(secure_filename(uploaded_file.filename))
	
	new_file = File(uploaded_file.name, uploaded_file.read())
	db.session.add(new_file)
	db.session.commit()
	return 'file' + new_file.name + ' uploaded successfully'	
		
############### uploade resource files ##############
