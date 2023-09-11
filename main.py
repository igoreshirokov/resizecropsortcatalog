import os
import sys
import csv
from PIL import Image, ImageDraw
import unittest
import shutil
import re

class ImageEditor:
    def __init__(self, folder):
        self.folder = folder
        self.sizes = (1200,1200)
        
    def start(self):
        self.fileList = self.getListFiles()
        for file in self.fileList:
            file = self.renameFileUppercase(file)
            self.crop(file)
            self.resize(file)
            self.createDir(file)
        
        self.rename_files_in_directories()

        
    def getListFiles(self):
        return [file for file in os.listdir(self.folder)]

    def start(self, folder):
        pass

    def rename_files_in_directories(self):
        for root, _, files in os.walk(self.folder):
            for index, file_name in enumerate(files, start=1):
                new_file_name = f'{os.path.basename(root)}_{index:02d}.jpg'
                source_path = os.path.join(root, file_name)
                new_path = os.path.join(root, new_file_name)
                
                os.rename(source_path, new_path)
                
                print(f'Переименован файл: {source_path} -> {new_path}')

    def createDir(self, file):
        sku = re.match(r'П-\d{1,3}', file)
        
        if sku is not None:
            sku = sku[0]
        else:
            sku = file
                
        if not os.path.exists(os.path.join(self.folder, sku)):
            os.mkdir(os.path.join(self.folder, sku))
        
        shutil.move(os.path.join(self.folder, file), os.path.join(self.folder, sku))
        
        print(os.path.join(self.folder, file))
        
    def sort(self, file):
        pass
    
    def crop(self, file):
        # Откройте изображение
        image = Image.open(os.path.join(self.folder, file))  # Замените "input_image.jpg" на ваш путь к изображению

        # Определите, какая сторона больше: ширина или высота
        if image.width > image.height:
            # Если ширина больше, используйте высоту для обрезки
            size = image.height
        else:
            # Если высота больше или равна ширине, используйте ширину для обрезки
            size = image.width

        # Вычислите координаты верхнего левого и нижнего правого углов для обрезки
        left = (image.width - size) // 2
        top = (image.height - size) // 2
        right = left + size
        bottom = top + size

        # Обрежьте изображение с сохранением соотношения сторон
        cropped_image = image.crop((left, top, right, bottom))

        # Сохраните обрезанное изображение
        cropped_image.save(os.path.join(self.folder, file))  # Замените на путь для сохранения

        # Закройте изображение (по завершении)
        image.close()

        print("Изображение обрезано в соотношение сторон 1 к 1")
    
    def resize(self, file):
        image = Image.open(os.path.join(self.folder, file))
        
        if image.size[0] < self.sizes[0]:
            print(f'Изображение {file} не может быть уменьшено, так как его размер меньше')
            print(image.size)
            image.close()
            return
        
        resizedImage = image.resize(self.sizes)
        resizedImage.save(os.path.join(self.folder, file))
        image.close()
        print(f'Размер изображения изменен {file} 1200х1200')
        
    def renameFileUppercase(self, file):
        new_name = file.upper()
        os.rename(os.path.join(self.folder, file), 
                  os.path.join(self.folder, new_name))
        return new_name
    
    
if __name__ == '__main__':
    imageEditor = ImageEditor('test_dir2')
    imageEditor.test()