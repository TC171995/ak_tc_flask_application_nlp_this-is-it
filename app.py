'''
  @Script-Name: Flask application - 02
  @Python-Version: Python 3.5.2
  @Authors of this script: AmandeepSinghKhanna and Theepan Chakkravarthy S
'''

import os # For operating system functionality.
from flask import Flask, render_template, request, redirect, session # For flask-server functions.
from werkzeug.utils import secure_filename # For secure filenames on file uploads.
import pandas as pd # For handling dataframes.
import re # For regular expression functions.
import PyPDF2 # For reading pdf files. 
from sklearn.feature_extraction.text import CountVectorizer # For feature extraction from the text.

# Initialising the accepted file formats.
accepted_file_formats = ['.xlsx','.csv','.txt','.pdf','.json']

'''
  User-defined functions begins here:
'''

# Function to check if the uploaded file format is accepted:

def file_acceptance_checker(x):
    x_format = x[-5:]
    for i in accepted_file_formats:
        if str(i) in str(x_format):
            Format_found=True
            break
        else:
            Format_found=False
    return Format_found

# Function to retrive the file format:

def file_format_checker(x):
    x_format = x[-5:]
    for format in accepted_file_formats:
        if format in x_format:
            return format

# Function to pre-process the pdf text:

def pdf_pre_process(text):
    new_text = []
    for t in text:
        t = t.lower()
        t = re.sub(r'\n', '', t)
        new_text.append(t)
    return new_text

'''
  User-defined functions end here:
'''

'''
  Flask application begins here:
'''

# Flask application object:
app = Flask(__name__)

'''
  Flask app routes begins here: 
'''

# Index / Landing page:
@app.route('/')
def index():
  return render_template('index.html')

# File upload request based on file upload-format:
@app.route('/file_upload', methods=['POST'])
def file_upload():
  try:
    file = request.files['file']
    filename = secure_filename(file.filename)
    session['filename']=filename
    format_check = file_acceptance_checker(filename)
    if format_check == False:
      return 'Please enter a valid file format. The accepted file formats are: ' + str(accepted_file_formats)
    else:
        file.save(str(filename))
        file_format = file_format_checker(filename)
        if file_format == '.xlsx':
          uploaded_file = pd.read_excel(filename)
          column_list = list(uploaded_file.columns)
          return render_template('Excelfiles.html', column_list=column_list)
        elif file_format == '.csv':
          uploaded_file = pd.read_csv(filename)
          column_list = list(uploaded_file.columns)
          return render_template('Excelfiles.html', column_list=column_list)
        elif file_format == '.txt':
          uploaded_file = pd.read_table(filename)
          column_list=list(uploaded_file.columns)
          return render_template('Excelfiles',column_list=column_list)
        elif file_format == '.json':
          return ".json support is still in progress, Please try again later!"
        elif file_format == '.pdf':
          pdf_file =  open(filename, 'rb')
          pdf_reader =  PyPDF2.PdfFileReader(pdf_file)
          pdf_contents = []
          for i in range(pdf_reader.numPages):
            page_object = pdf_reader.getPage(i)
            temp = page_object.extractText()
            pdf_contents.append(temp)
            del temp
            pdf_file.close()
            pdf_contents = pdf_pre_process(pdf_contents)
            return str(pdf_contents)

  except Exception as e:
    return str(e)

# File attribute checks:
@app.route('/file_attributes_check', methods=['GET','POST'])
def file_attributes_check():
  column_list = request.form['colours']
  number_of_clusters = request.form['number_of_clusters']
  vechile = request.form['vehicle']
  session['vehicle']=vechile
  print(column_list)
  print(number_of_clusters)
  return str(column_list) + " " + str(number_of_clusters) + " " + str(vechile)

# T-SNE output web-page:
@app.route('/t_sne_output')
def t_sne_output():
  pass
  #k = session.get('vehicle')
  #return(str(k))


'''
  Flask app routes end here:
'''

# Run command for the flask application:
if __name__ == '__main__':
  app.secret_key = 'This is a secret key'
  app.run(debug=True)

'''
  Flask application ends here:
'''
