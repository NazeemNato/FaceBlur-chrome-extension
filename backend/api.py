from flask import Flask,request,send_file
from flask_restful import Resource, Api
from flask_cors import CORS
from werkzeug.utils import secure_filename
from face_blur import anonymize_face_pixelate,anonymize_face_simple
import numpy as np
import cv2
import os
from downloadImage import *
app = Flask(__name__)
api = Api(app)
CORS(app)
prototxtPath = 'face_detector/deploy.prototxt'
weightsPath = 'face_detector/res10_300x300_ssd_iter_140000.caffemodel'
net = cv2.dnn.readNet(prototxtPath, weightsPath)
IMAGELOCATION = 'E:/js/exten/rmads/backend/image/out/'


class GetImage(Resource):
	def get(self):
		return {'name':'test api'}
	def post(self):
		imgUrl = request.get_json()
		try:
			loc,filename = downloadImage(imgUrl)
			image = cv2.imread(loc)
			(h,w) = image.shape[:2]
			blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300),(104.0, 177.0, 123.0))
			net.setInput(blob)
			detections = net.forward()
			for i in range(0, detections.shape[2]):
				confidence = detections[0, 0, i, 2]
				if confidence > 0.5:
					box =detections[0, 0, i, 3:7] * np.array([w, h, w, h])
					(startX, startY, endX, endY) = box.astype("int")
					face = image[startY:endY, startX:endX]
					face = anonymize_face_simple(face, factor=1.5)
					image[startY:endY, startX:endX] = face
			cv2.imwrite(os.path.join(IMAGELOCATION , filename), image)
			return {'image':'http://127.0.0.1:5000/output/{}'.format(filename)},201
		except Exception as e:
			print(e)
			return {'image':imgUrl},201

@app.route('/output/<filename>')

def display_image(filename):
	file = IMAGELOCATION+ filename
	return send_file(file, mimetype='image/gif')

api.add_resource(GetImage,'/')
if __name__ == '__main__':
	app.run(debug=True)