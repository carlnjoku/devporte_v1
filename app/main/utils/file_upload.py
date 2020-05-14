from flask import Flask, request, jsonify, make_response
import shutil
import os

import datetime
import base64

from werkzeug.utils import secure_filename


from ..config import firebase
storage = firebase.storage()


ALLOWED_EXTENSIONS_ALL_PROFILE = set(['png', 'jpg', 'jpeg', 'gif'])
ALLOWED_EXTENSIONS_ALL = set(['png', 'jpg', 'jpeg', 'gif', 'mp4', 'mp3', 'docx', 'doc'])


UPLOAD_FOLDER = 'media'


UPLOAD_PROJECT_FOLDER = 'project_files'



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_ALL

def allowed_file_profile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_ALL_PROFILE




def upload_profile(file, firstname, userId):
    print(file)
    res={}
    #req_data = request.form.to_dict(flat=True)
    file = request.files['avatarBlob']
    if 'avatarBlob' in request.files and allowed_file_profile(file.filename) :

        firstname = firstname
        uid = userId
        get_filename = secure_filename(file.filename)
        filename, file_extension = os.path.splitext(get_filename)

        # Generate new file name
        filename = uid+'-'+firstname+file_extension

        filename = filename.replace(' ', '-').lower()

        
    else:
        if not 'avatarBlob' in request.files :res["error"] = "No Image"
        
        if not allowed_file_profile(file.filename):res["error"] = "File type not supported"
        
        
        return jsonify({"result": res})

    filename = os.path.join(UPLOAD_FOLDER, filename)

    
    print(filename)

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    

    temp_file = os.path.join(UPLOAD_FOLDER, "temp.jpg")
    
    file.save(temp_file)
    
    storage.child(filename).put(temp_file)
    
    # Get image url from firebase
    img_url = storage.child(filename).get_url(None)
   
    #res["msg"] = "Valid_Image"
    shutil.copy(temp_file,filename)
    file = request.files['avatarBlob']

    
    res["media"] = filename

    print(img_url)
    print(request.files)
    return img_url


def upload_multiple_files(uploaded_files):
    try:

        res={}
        uploaded_files = request.files.getlist("file")
        #print(upload_files)
        filenames = []
        for file in uploaded_files:
            # Check if the file is one of the allowed types/extensions
            if file:
                # Make the filename safe, remove unsupported chars
                get_filename = secure_filename(file.filename)
                filename, file_extension = os.path.splitext(get_filename)

                # Generate new file name
                filename = filename+file_extension

                filename = filename.replace(' ', '-').lower()

                filename = os.path.join(UPLOAD_PROJECT_FOLDER, filename)


                if not os.path.exists(UPLOAD_PROJECT_FOLDER):
                    os.makedirs(UPLOAD_PROJECT_FOLDER)

                temp_file = os.path.join(UPLOAD_PROJECT_FOLDER, "temp"+file_extension)
                
                file.save(temp_file)
                
                storage.child(filename).put(temp_file)
                

                # Get image url from firebase
                img_url = storage.child(filename).get_url(None)

                print(img_url)
                
                shutil.copy(temp_file,filename)
                file = request.files['file']

                res["project_files"] = filename
                
                os.remove(temp_file)

                # Remove the dot in the extension
                original_file_extension = file_extension.replace('.', '')
                #filenames.append(img_url)
                filenames.append({'img_url':img_url, 'filename':get_filename, 'extention':original_file_extension})
        
                print(filenames)
                
        return(filenames)
        

       

    except Exception as e:
        return jsonify({"data": {"error_msg": str(e)}})