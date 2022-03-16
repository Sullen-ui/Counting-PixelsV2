import os
from flask import Flask, request, redirect ,flash, session
from flask.templating import render_template
from PIL import Image, ImageColor
import numpy as np

#Путь для картинок
UPLOAD_FOLDER = './static/pic'

server = Flask(__name__)
server.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg'])
server.config['SESSION_TYPE'] = 'memcached'
server.config['SECRET_KEY'] = 'super secret key'

# Функция проверки расширения файла 
def allowed_file(filename):
        return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def countBW(path):             
            # Берем картинку и считаем белые и чёрные пиксели
            original = np.array(Image.open(path).convert('RGB')) 
            
            black = [0, 0, 0]
            white = [255, 255, 255]
            numblacks = numwhites = 0
            numblacks = np.count_nonzero(np.all(original==black, axis=2))
            numwhites = np.count_nonzero(np.all(original==white, axis=2)) 
            # Заносим переменные в библиотеку сессии для использования в других функциях
            session['white'] = numwhites  
            session['black'] = numblacks 
            #Сравниваю каких пикселей больше и так-же заношу в библиотекуds
            result = max(numwhites,numblacks)
            if result == numwhites:
                phrase = 'Белых пикселей больше'
            else:
                phrase = 'Черных пикселей больше'
            session['phrase'] = phrase
            return render_template ("index.html", black=numblacks, white=numwhites, path=path, phrase=phrase )


        
@server.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # проверим, передается ли в запросе файл 
        if 'file' not in request.files:
            # После перенаправления на страницу загрузки
            # покажем сообщение пользователю 
            flash('Не могу прочитать файл')
            return redirect(request.url)
        file = request.files['file']
        # Если файл не выбран, то браузер может
        # отправить пустой файл без имени.
        if file.filename == '':
            flash('Нет выбранного файла')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # безопасно извлекаем оригинальное имя файла
            filename = file.filename
            # сохраняем файл
            path=(os.path.join(server.config['UPLOAD_FOLDER'], filename))
            file.save(path)
            session['path']= path
            return countBW(path)
          
    return render_template ("index.html")     

    
@server.route('/hex', methods=['GET', 'POST'])
# Считаем писели по HEX коду
def countHex():
        if request.method == 'POST':
            hex = request.form.get('hex')
            color=ImageColor.getrgb(hex)
            original = np.array(Image.open(session['path']).convert('RGB')) 
            numpixels = 0
            numpixels = np.count_nonzero(np.all(original==color, axis=2))
            return render_template ("index.html", hex=numpixels, path=session['path'], white =session['white'] , black =session['black'], phrase=session['phrase'])    
        return render_template ("index.html")    
           