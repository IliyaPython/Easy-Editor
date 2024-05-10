#создай тут фоторедактор Easy Editor!
import os
from PyQt5.QtWidgets import (
   QApplication, QWidget,
   QFileDialog, QInputDialog,
   QLabel, QPushButton, QListWidget,
   QHBoxLayout, QVBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt # нужна константа Qt.KeepAspectRatio для изменения размеров с сохранением пропорций
from PyQt5.QtGui import QPixmap, QIcon # оптимизированная для показа на экране картинка


from PIL import Image
from PIL.ImageQt import ImageQt # для перевода графики из Pillow в Qt 
from PIL import ImageFilter, ImageEnhance
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
   GaussianBlur, UnsharpMask
)

workdir = ''
def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()
    img_label.setPixmap(QPixmap(None))
def filter(files, extensions):
    result = []
    for file in files:
        for extension in extensions:
            if file.endswith(extension):
                result.append(file)
    return result
def showFilenamesList():
    extensions = ['.jpg','.jpeg', '.png', '.gif', '.bmp']
    chooseWorkdir()
    try:
        print(workdir)
        filenames = filter(os.listdir(workdir), extensions)
    except IOError:
        warning('Папка для работы не найдена!')
        filenames = []
    imgs_list.clear()
    for image in filenames:
        imgs_list.addItem(image)

def showChosenImage():
    if imgs_list.currentRow() >= 0:
        filename = imgs_list.currentItem().text()
        workimage.loadImage(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)
def warning(warn_text, error=0):
    warning = QMessageBox()
    if error == 9090:
        warning.addButton(QMessageBox.No) # Здесь можно пользоваться кнопкакми из класса QMessageBox!
        warning.addButton(QMessageBox.Ok) # И это тоже супер / P.S. Класс начинается со страницы 6635 :0
    warning.setWindowTitle('Предупреждение')
    warning.setText(warn_text)
    warning.exec_()
    return warning.buttons(), warning.clickedButton() # Возвращаем списко всех кнопок и нажатую кнопку

class ImageProccesor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Edit_Images/"
    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        imagePath = os.path.join(dir, filename)
        self.image = Image.open(imagePath)
        self.edit_image = self.image
    def showImage(self, path):
        img_label.hide()
        pixmapimage = QPixmap(path)
        w, h = img_label.width(), img_label.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        img_label.setPixmap(pixmapimage)
        img_label.show()
    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not (os.path.exists(path)): # or os.path.isdir(path))
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.edit_image.save(image_path)
    def edit_BaW(self):
        try:
            if btn_BaW.text() == 'Чёрно-белый':
                self.back_step = self.edit_image
                self.edit_image = self.edit_image.convert('L')
                btn_BaW.setText('Цветной')
            else:
                self.edit_image = self.back_step
                btn_BaW.setText('Чёрно-белый')
            self.saveImage()
            image_path = os.path.join(self.dir, self.save_dir, self.filename)
            self.showImage(image_path)
        except AttributeError:
            warning('Картинка для обработки не выбрана!')
        except TypeError:
            warning('Картинка для обработки не выбрана!')
    def edit_mirror(self):
        try:
            self.back_step = None; btn_BaW.setText('Чёрно-белый') # Плохая строка, из-за того, что по другому никак :,(
            self.edit_image = self.edit_image.transpose(Image.FLIP_LEFT_RIGHT)
            self.saveImage()
            image_path = os.path.join(self.dir, self.save_dir, self.filename)
            self.showImage(image_path)
        except AttributeError:
            warning('Картинка для обработки не выбрана!')
        except TypeError:
            warning('Картинка для обработки не выбрана!')
    def edit_lefted(self):
        try:
            self.back_step = None; btn_BaW.setText('Чёрно-белый') # Плохая строка, из-за того, что по другому никак :,(
            self.edit_image = self.edit_image.transpose(Image.ROTATE_270)
            self.saveImage()
            image_path = os.path.join(self.dir, self.save_dir, self.filename)
            self.showImage(image_path)
        except AttributeError:
            warning('Картинка для обработки не выбрана!')
        except TypeError:
            warning('Картинка для обработки не выбрана!')
    def edit_right(self):
        try:
            self.back_step = None; btn_BaW.setText('Чёрно-белый') # Плохая строка, из-за того, что по другому никак :,(
            self.edit_image = self.edit_image.transpose(Image.ROTATE_90)
            self.saveImage()
            image_path = os.path.join(self.dir, self.save_dir, self.filename)
            self.showImage(image_path)
        except AttributeError:
            warning('Картинка для обработки не выбрана!')
        except TypeError:
            warning('Картинка для обработки не выбрана!')
    def edit_contrast(self):
        try:
            self.back_step = None; btn_BaW.setText('Чёрно-белый') # Плохая строка, из-за того, что по другому никак :,(
            self.edit_image = ImageEnhance.Contrast(self.edit_image)
            self.edit_image = self.edit_image.enhance(2)
            self.saveImage()
            image_path = os.path.join(self.dir, self.save_dir, self.filename)
            self.showImage(image_path)
        except AttributeError:
            warning('Картинка для обработки не выбрана!')
        except TypeError:
            warning('Картинка для обработки не выбрана!')
    def blured(self):
        try:
            self.back_step = None; btn_BaW.setText('Чёрно-белый') # Плохая строка, из-за того, что по другому никак :,(
            self.edit_image = self.edit_image.filter(ImageFilter.BLUR)
            self.saveImage()
            image_path = os.path.join(self.dir, self.save_dir, self.filename)
            self.showImage(image_path)
        except AttributeError:
            warning('Картинка для обработки не выбрана!')
        except TypeError:
            warning('Картинка для обработки не выбрана!')
    def contour(self):
        try:
            self.back_step = None; btn_BaW.setText('Чёрно-белый') # Плохая строка, из-за того, что по другому никак :,(
            self.edit_image = self.edit_image.filter(ImageFilter.CONTOUR)
            self.saveImage()
            image_path = os.path.join(self.dir, self.save_dir, self.filename)
            self.showImage(image_path)
        except AttributeError:
            warning('Картинка для обработки не выбрана!')
        except TypeError:
            warning('Картинка для обработки не выбрана!')
    def flip_TOP_BOT(self):
        try:
            self.back_step = None; btn_BaW.setText('Чёрно-белый') # Плохая строка, из-за того, что по другому никак :,(
            self.edit_image = self.edit_image.transpose(Image.FLIP_TOP_BOTTOM)
            self.saveImage()
            image_path = os.path.join(self.dir, self.save_dir, self.filename)
            self.showImage(image_path)
        except AttributeError:
            warning('Картинка для обработки не выбрана!')
        except TypeError:
            warning('Картинка для обработки не выбрана!')
    def clear_of_all(self):
        try:
            self.back_step = None; btn_BaW.setText('Чёрно-белый') # Плохая строка, из-за того, что по другому никак :,(
            self.edit_image = self.edit_image.filter(ImageFilter.EMBOSS)
            self.saveImage()
            image_path = os.path.join(self.dir, self.save_dir, self.filename)
            self.showImage(image_path)
        except AttributeError:
            warning('Картинка для обработки не выбрана!')
        except TypeError:
            warning('Картинка для обработки не выбрана!')
    def unsharpMask(self):
        try:
            self.back_step = None; btn_BaW.setText('Чёрно-белый') # Плохая строка, из-за того, что по другому никак :,(
            self.edit_image = self.edit_image.filter(ImageFilter.UnsharpMask)
            self.saveImage()
            image_path = os.path.join(self.dir, self.save_dir, self.filename)
            self.showImage(image_path)
        except AttributeError:
            warning('Картинка для обработки не выбрана!')
        except TypeError:
            warning('Картинка для обработки не выбрана!')
    def cropped(self):
        try:
            self.back_step = None; btn_BaW.setText('Чёрно-белый') # Плохая строка, из-за того, что по другому никак :,(
            box, result = QInputDialog.getText(EasyEd, 'Обрезать картинку', f'Размеры файла:{self.image.size}\nВведите данные (лево, вверх право, низ)')
            print(box)
            try:
                box = tuple(map(int, box.split(', ')))
                print(box)
            except ValueError:
                warning('Извините, во время ввода вы указали не число!')
            else:
                try:
                    self.edit_image = self.edit_image.crop(box)
                    self.saveImage()
                    image_path = os.path.join(self.dir, self.save_dir, self.filename)
                    self.showImage(image_path)
                except SystemError:
                    warning('Смотрите, размер картинки определяется так:\n У нас есть (лево, вверх, право, вниз)\n Тогда размер картинки будет (Право-Лево, Вниз-Вверх)\n Программе нужно, чтобы Право и Вниз были больше, чем Лево и Вверх.')
        except AttributeError:
            warning('Картинка для обработки не выбрана!')
        except TypeError:
            warning('Картинка для обработки не выбрана!')
        
    def reset(self):
        if imgs_list.selectedItems():# Снизу мы принимаем список кнопок и нажатую кнопку
            buttons, clicked = warning('Вы хотите удалить сбросить свои прошлые обработки?', 9090) # И это тоже супер
            path = workdir +'/'+ self.save_dir
            self.back_step = None; btn_BaW.setText('Чёрно-белый') # Плохая строка, из-за того, что по другому никак :,(
            if clicked == buttons[0]: # Нам известно, что кнопка Ok находится первее No, следовательно
                # кнопка Ok будет первой [0] в списке
                if os.path.exists(path): # or os.path.isdir(path))
                    while os.listdir(path):
                        for file in os.listdir(path):
                            try:
                                os.remove(path + file)
                            except PermissionError:
                                os.rmdir(path + file)
                    os.rmdir(path)
            try:
                image_path = os.path.join(self.dir, self.filename)
            except AttributeError:
                warning('Картинка для сброса не выбрана!')
            except TypeError:
                warning('Картинка для сброса не выбрана!')
            else:
                if os.path.isfile(path + self.filename):
                    os.remove(path + self.filename)
                self.loadImage(workdir, self.filename)
                self.showImage(image_path)
        else:
            warning('Картинка для сброса не выбрана!')
app = QApplication([])
app.setWindowIcon(QIcon('images.ico'))
EasyEd = QWidget()
EasyEd.setWindowIcon(QIcon('images.ico'))
EasyEd.setWindowTitle('Easy Editor')
EasyEd.resize(700, 500)
# Создание виджетов
btn_dir = QPushButton('Папка')
imgs_list = QListWidget()
img_label = QLabel('Картинка')
btn_lefted = QPushButton('Лево')
btn_righted = QPushButton('Право')
btn_mirror = QPushButton('Зеркало Л ↔ П')
btn_contrast = QPushButton('Резкость')
btn_BaW = QPushButton('Чёрно-белый')
btn_reset = QPushButton('Сбросить изменения')
btn_blur = QPushButton('Размытие')
btn_contour = QPushButton('Выделить контуры')
btn_clear = QPushButton('Отчистить от цветов')
btn_mask = QPushButton('Нерезкая маска')
btn_cropped = QPushButton('Обрезать')
btn_flipTB = QPushButton('Зеркало Верх ↕ Низ')
# Создание лэйаутов
main_layout = QHBoxLayout()
midlle_VLayout1 = QVBoxLayout()
midlle_VLayout2 = QVBoxLayout()
junior_HLayout1 = QHBoxLayout()
junior_HLayout2 = QHBoxLayout()
 # Насаживание виджетов
  # Средний 1
midlle_VLayout1.addWidget(btn_dir)
midlle_VLayout1.addWidget(imgs_list)
  # Средний 2
midlle_VLayout2.addWidget(img_label)
midlle_VLayout2.addLayout(junior_HLayout1)
midlle_VLayout2.addLayout(junior_HLayout2)
    # Младший 1
junior_HLayout1.addWidget(btn_lefted)
junior_HLayout1.addWidget(btn_righted)
junior_HLayout1.addWidget(btn_mirror)
junior_HLayout1.addWidget(btn_contrast)
junior_HLayout1.addWidget(btn_BaW)
junior_HLayout1.addWidget(btn_reset)
    # Младший 2
junior_HLayout2.addWidget(btn_blur)
junior_HLayout2.addWidget(btn_contour)
junior_HLayout2.addWidget(btn_flipTB)
junior_HLayout2.addWidget(btn_clear)
junior_HLayout2.addWidget(btn_mask)
junior_HLayout2.addWidget(btn_cropped)

 # Закрпеление лэйаутов
main_layout.addLayout(midlle_VLayout1)
main_layout.addLayout(midlle_VLayout2)
main_layout.setSpacing(15)
EasyEd.setLayout(main_layout)
# Рабочее изорбражение
workimage = ImageProccesor()
# Функции-обработчики
imgs_list.currentRowChanged.connect(showChosenImage)
btn_dir.clicked.connect(showFilenamesList)
btn_BaW.clicked.connect(workimage.edit_BaW)
btn_lefted.clicked.connect(workimage.edit_lefted)
btn_righted.clicked.connect(workimage.edit_right)
btn_mirror.clicked.connect(workimage.edit_mirror)
btn_reset.clicked.connect(workimage.reset)
btn_contrast.clicked.connect(workimage.edit_contrast)
btn_blur.clicked.connect(workimage.blured)
btn_contour.clicked.connect(workimage.contour)
btn_clear.clicked.connect(workimage.clear_of_all)
btn_mask.clicked.connect(workimage.unsharpMask)
btn_cropped.clicked.connect(workimage.cropped)
btn_flipTB.clicked.connect(workimage.flip_TOP_BOT)
# Запуск приложения! "Поехали!"
EasyEd.show()
app.exec_()