import os
import shutil
from flask import Flask,request,flash,redirect,url_for,render_template,session
from werkzeug.utils import secure_filename
import matplotlib.pyplot as plt
#import setup
#import Image_augmentation


#setup.install_missing()

UPLOAD_FOLDER = r'D:\Assignment\Image_Augmentation\Data\train'
ALLOWED_EXTENSIONS = {'jpg','png','jpeg','gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Define secret key to enable session
app.secret_key = 'This is your secret key to utilize session in Flask'

@app.route('/')
def main():
    return render_template('Index.html')

@app.route('/upload',methods = ['POST','GET'])
def upload_file():
    if request.method == 'POST':
        file_names = []
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist("file")
        for file in files:
            print(os.getcwd())
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                #filename = file.filename
                file_names.append(filename)
                print(filename)
                file.save(filename)
                shutil.move(os.path.join(os.getcwd(),filename),os.path.join(os.getcwd(),'static',filename))
                session['uploaded_img_file_path'] = os.path.join(os.getcwd(),'static')
                session['file_list'] = file_names
                #return redirect(url_for('/augmentations', name=filename))
        return render_template('index2.html')
        

@app.route('/display',methods = ['POST'])
def display():
    image_file_path = session.get('uploaded_img_file_path',None)
    image_files = session.get('file_list')
    # Display image in Flask application web page
    return render_template('image_processing.html',user_image_path = image_file_path,files = image_files)

@app.route('/augmentations',methods = ['POST','GET'])
def augmentations():
    image_file_path = session.get('uploaded_img_file_path',None)
    image_files = session.get('file_list')
    

if __name__ == '__main__':
    app.run(debug=True)