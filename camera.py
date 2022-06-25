from flask import Flask, render_template, request, make_response
import cv2
import numpy as np
import datetime
import os



app = Flask(__name__, template_folder='templates')

def frames():


    ######## Taking out Frames from video file ##################
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    ##create a user folder to save the frames
    parent_dir = os.path.join(BASE_DIR, "images") #BASE_DIR + "/images/{}".format(userId)
    try:
        return os.mkdir(parent_dir)
    except OSError as error: 
        pass



@app.route('/')
def index():
    return render_template('recorder_up.html')

def send_file_data(data, mimetype='image/jpeg', filename='output.jpg'):
    # https://stackoverflow.com/questions/11017466/flask-to-return-image-stored-in-database/11017839

    response = make_response(data)
    response.headers.set('Content-Type', mimetype)
    response.headers.set('Content-Disposition', 'attachment', filename=filename)

    return response

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    frames()

    #print(request.files,request.form)
    #path = os.path.join(base_dir, "images", request.form["fname"]+".jpg")#base_dir + "/VideoUpload/{}.webm".format(request.form["fname"])
    #video file has been saved to the folder VideoUpload
    #request.files['data'].save(path)
    if request.method == 'POST':
        
        file = request.files.get('snap')
        
        if file:

            img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
            height, width = 240, 320
            dsize = (width,height)
            img = cv2.resize(img, dsize)
            

            text = datetime.datetime.now().strftime('%Y.%m.%d %H.%M.%S.%f')
            img = cv2.putText(img, text, (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            path = os.path.sep.join([base_dir,"images", "frame{}.png".format(str(text).replace(":",' '))])
            cv2.imwrite(path, img)
            ret, buf = cv2.imencode('.jpg', img)

            
            return send_file_data(buf.tobytes())
        else:
            return 'You forgot Snap!'
    return None

@app.route('/verifying')
def verification():
    return render_template("index.html")


if __name__ == '__main__':
    # camera can work with HTTP only on 127.0.0.1
    # for 0.0.0.0 it needs HTTPS so it needs `ssl_context='adhoc'` (and in browser it need to accept untrusted HTTPS
    #app.run(host='127.0.0.1', port=5000)#, debug=True)
    app.run(host='127.0.0.1', port=5000, debug=True)