import os
print(os.getcwd())

# -*- coding: utf-8 -*-
import random
import math
import logging
import pandas as pd
import numpy as np
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from pathlib import Path
import glob
from PIL import Image, ImageFont, ImageDraw 

class ImageText(object):
    def __init__(self, filename_or_size, mode='RGBA', background=(0, 0, 0, 0),
                 encoding='utf8'):
        if isinstance(filename_or_size, str):
            self.filename = filename_or_size
            self.image = Image.open(self.filename)
            self.size = self.image.size
        elif isinstance(filename_or_size, (list, tuple)):
            self.size = filename_or_size
            self.image = Image.new(mode, self.size, color=background)
            self.filename = None
        self.load = self.image.load
        self.im = self.image.im
        self.draw = ImageDraw.Draw(self.image)
        self.encoding = encoding

    def get_image(self):
	    return self.image   

    def save(self, filename=None):
        self.image.save(filename or self.filename)

    def get_font_size(self, text, font, max_width=None, max_height=None):
        if max_width is None and max_height is None:
            raise ValueError('You need to pass max_width or max_height')
        font_size = 1
        text_size = self.get_text_size(font, font_size, text)
        if (max_width is not None and text_size[0] > max_width) or \
           (max_height is not None and text_size[1] > max_height):
            raise ValueError("Text can't be filled in only (%dpx, %dpx)" % \
                    text_size)
        while True:
            if (max_width is not None and text_size[0] >= max_width) or \
               (max_height is not None and text_size[1] >= max_height):
                return font_size - 1
            font_size += 1
            text_size = self.get_text_size(font, font_size, text)

    def write_text(self, x, y, text, font_filename, font_size=11,
                   color=(0, 0, 0), max_width=None, max_height=None):
        if font_size == 'fill' and \
           (max_width is not None or max_height is not None):
            font_size = self.get_font_size(text, font_filename, max_width,
                                           max_height)
        text_size = self.get_text_size(font_filename, font_size, text)
        font = ImageFont.truetype(font_filename, font_size)
        if x == 'center':
            x = (self.size[0] - text_size[0]) / 2
        if y == 'center':
            y = (self.size[1] - text_size[1]) / 2
        self.draw.text((x, y), text, font=font, fill=color)
        return text_size

    def get_text_size(self, font_filename, font_size, text):
        font = ImageFont.truetype(font_filename, font_size)
        return font.getsize(text)

    def write_text_box(self, x, y, text, box_width, font_filename,
                       font_size=11, color=(0, 0, 0), place='left',
                       justify_last_line=False):
        lines = []
        line = []
        words = text.split(' ')
        for word in words:
            if '\n' in word:
                newline_words = word.split('\n')
                new_line = ' '.join(line + [newline_words[0]])
                size = self.get_text_size(font_filename, font_size, new_line)
                text_height = size[1]
                if size[0] <= box_width:
                    line.append(newline_words[0])
                else:
                    lines.append(line)
                    line = [newline_words[0]]
                lines.append(line)
                if len(word.split('\n')) > 2:
                    for i in range(1, len(word.split('\n'))-1): lines.append([newline_words[i]])
                line = [newline_words[-1]]
            else:				
                new_line = ' '.join(line + [word])
                size = self.get_text_size(font_filename, font_size, new_line)
                text_height = size[1]
                if size[0] <= box_width:
                    line.append(word)
                else:
                    lines.append(line)
                    line = [word]
        if line:
            lines.append(line)
        lines = [' '.join(line) for line in lines]
        height = y
        for index, line in enumerate(lines):
            height += text_height
            if place == 'left':
                self.write_text(x, height, line, font_filename, font_size,
                                color)
            elif place == 'right':
                total_size = self.get_text_size(font_filename, font_size, line)
                x_left = x + box_width - total_size[0]
                self.write_text(x_left, height, line, font_filename,
                                font_size, color)
            elif place == 'center':
                total_size = self.get_text_size(font_filename, font_size, line)
                x_left = int(x + ((box_width - total_size[0]) / 2))
                self.write_text(x_left, height, line, font_filename,
                                font_size, color)
            elif place == 'justify':
                words = line.split()
                if (index == len(lines) - 1 and not justify_last_line) or \
                   len(words) == 1:
                    self.write_text(x, height, line, font_filename, font_size,
                                    color)
                    continue
                line_without_spaces = ''.join(words)
                total_size = self.get_text_size(font_filename, font_size,
                                                line_without_spaces)
                space_width = (box_width - total_size[0]) / (len(words) - 1.0)
                start_x = x
                for word in words[:-1]:
                    self.write_text(start_x, height, word, font_filename,
                                    font_size, color)
                    word_size = self.get_text_size(font_filename, font_size,
                                                    word)
                    start_x += word_size[0] + space_width
                last_word_size = self.get_text_size(font_filename, font_size,
                                                    words[-1])
                last_word_x = x + box_width - last_word_size[0]
                self.write_text(last_word_x, height, words[-1], font_filename,
                                font_size, color)
        return (box_width, height - y)

class InspirationalQuoteImage:

    def __makeDirectory(self, directory):
        Path(directory).mkdir(parents=True, exist_ok=True)

    def makeInspirationalImages(self, saveImages=True, showImages=False):
        """Creates inspirational images based on the images and quotes provided.
           Images: Should be in /data/raw/images
           Quotes: Should be in /data/raw/quotes.csv (two columns: quote, attributed)

        Args:
            saveImages (bool, optional): Whether you want to save the images in /data/processed/images. Defaults to True.
            showImages (bool, optional): Whether you want the images to pop up as it's running. Defaults to False.
        """
        self.__makeDirectory("data/processed/images")
        PADDING=0.1
        BOX_COLOR=(0,0,0)
        OPACITY=50

        # all files
        allimages = glob.glob("data/raw/images/*.jpg")
        allimages = [x.replace("\\", "/") for x in allimages]
        random.shuffle(allimages)

        df = pd.read_csv("data/raw/quotes.csv", dtype={'quote': 'str', 'attributed': 'str', 'publication': 'str'})
        df = df.sample(frac=1).reset_index(drop=True)
        
        for i, row in df.iterrows():

            # Open Image
            imagename = allimages[i].split("/")[-1]
            img = Image.open(allimages[i])
            img = img.convert("RGBA")
            width, height = img.size

            overlay = Image.new('RGBA', img.size, BOX_COLOR+(0,))
            draw = ImageDraw.Draw(overlay)  # Create a context for drawing things on it.
            draw.rectangle(((0, 0), (width, height)), fill=BOX_COLOR+(OPACITY,))

            img = Image.alpha_composite(img, overlay)

            # Calculate font size
            fontsize = int((math.pow(len(row["quote"]), -1) * 3000) + 150)

            # Draw Text Box (with word-wrap)
            quotesaying = ImageText((width, height), background=(0, 0, 0, 30)) # 80 = alpha
            quotesaying.write_text_box(width*PADDING, height*PADDING, f'\"{row["quote"]}\"', box_width=(width - ((width*PADDING) * 2)), font_filename="CascadiaCode.ttf",
                            font_size=fontsize, color=(255,255,255), place='center')

            # combine quote with original image.
            img = Image.alpha_composite(img, quotesaying)

            if(pd.notnull(row["attributed"])):
                byline = ImageText((width, height), background=(0, 0, 0, 0)) # 200 = alpha
                byline.write_text_box(width*PADDING, ((height - (height*PADDING)) - 140), f'>> {row["attributed"]}', box_width=(width - ((width*PADDING) * 2)), font_filename="CascadiaCode.ttf",
                                font_size=140, color=(255,255,255), place='center')
                img = Image.alpha_composite(img, byline)

            if(showImages):
                img.show()

            if(saveImages):
                img = img.convert("RGB")
                img.save(f"data/processed/images/{imagename}")


def main():
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('Making inspirational quote images...')
    us = InspirationalQuoteImage()
    us.makeInspirationalImages()


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
