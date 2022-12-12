import time
import os
from re import A, T
from app import app
from flask import  request, render_template, jsonify, send_file
from werkzeug.utils import secure_filename
import detect
import argparse
from json import JSONEncoder
import json
import numpy
from PIL import Image as im
parser = argparse.ArgumentParser()
parser.add_argument('image_path', help='path to image')


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'mp4'])

list_to_string= lambda x: "".join(map(str, x))


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
	return render_template('upload.html')


@app.route('/uploader', methods = ['POST'])
def load_image():
	# check if the post request has the file part

	class NumpyArrayEncoder(JSONEncoder):
		def default(self, obj):
			if isinstance(obj, numpy.ndarray):
				return obj.tolist()
			return JSONEncoder.default(self, obj)

	if 'file' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	file = request.files['file']
	if file.filename == '':
		resp = jsonify({'message' : 'No file selected for uploading'})
		resp.status_code = 400
		return resp






	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(filename)
		t0=time.time()
		output = detect.run(source = file.filename)

		if output is None:
			resp = jsonify({'error':'Unable to detect display'})
			os.remove(file.filename)
			resp.status_code = 400
			return resp
		else :
			#resp = jsonify({'image': output})
			numpyData = {'output': output}
			print("serialize NumPy array into JSON and write into a file")

			data = im.fromarray(output)
			data.save('output.jpg')
			print(f'Total Time required. ({time.time() - t0:.3f}s)',flush=True)
			os.remove(file.filename)
			#resp.status_code = 201
			return send_file('output.jpg', mimetype='image/gif')

	else:
		resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
		resp.status_code = 400
		return resp


if __name__ == '__main__':
	app.run(host="0.0.0.0", debug=True)