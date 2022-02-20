# -*- coding: utf-8 -*-
import os
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
import requests
import urllib.request
from random import sample
from pathlib import Path

class ImageAPI:
    """ Unsplash Image API
        - Note: Development-level accounts are limited to 50 calls per hour.
    """

    def __makeDirectory(self, directory):
        Path(directory).mkdir(parents=True, exist_ok=True)

    def __saveUnsplashImages(self, allimages):
        self.__makeDirectory("data/raw/images")
        for img in allimages:
            filetype = img.get("urls").get("regular").split("?")[1]
            filetype = [x.replace("fm=", "") for x in filetype.split("&") if "fm=" in x]
            if(len(filetype) > 0):
                filetype = filetype[0]
                urllib.request.urlretrieve(img.get("urls").get("full"), f'data/raw/images/{img.get("id")}.{filetype}')

    def getImagesForTopic(self, topic, pages=30):
        """ Retrieve a list of images for a particular topic from unsplash. 

        Args:
            topic (string): An id or slug for a topic.
            pages (int, optional): The number of pages to return. 30 images per page. Defaults to 30.

        Returns:
            List: A list of images from unsplash
        """
        logger = logging.getLogger(__name__)
        logger.info(f'Getting all images for topic {topic}...')
        allimages = []
        for i in range(pages):
            page = i + 1
            r = requests.get(f'https://api.unsplash.com/topics/{topic}/photos?page={page}&per_page=30', 
                            headers={'Authorization': f'Client-ID {os.getenv("UNSPLASH_CLIENTID")}'})
            if(r.status_code==200):
                allimages.extend(r.json())
        return allimages

    def getRandomImagesForTopic(self, topic, count, pages, wideOnly=True, saveFiles=True):
        """ Get random images from the top 30 pages of a given topic (ie: from 900 images)

        Args:
            topic (string): An id or slug for a topic.
            count (int): The number of images to return/save.
            pages (int): The number of pages to get from Unsplash. Be aware of your API limits.
            wideOnly (bool, optional): Whether you only want to return wide aspect images. Defaults to True.
            saveFiles (bool, optional): Whether you want to save the files to /data/raw/images. Defaults to True.

        Returns:
            _type_: _description_
        """
        logger = logging.getLogger(__name__)
        logger.info(f'Working on getting random {topic} images...')
        allimages = self.getImagesForTopic(topic, pages)
        
        # Filter to wide images?
        if(wideOnly):
            logger.warning(f'Filter: Filtering to wide aspect images.')
            allimages = [x for x in allimages if x.get("width") > x.get("height")]

        # Random sample
        if(len(allimages)<count):
            logger.warning(f'Sampling: The sample ({count}) was larger than the total images ({len(allimages)}), so returning all items.')
        else:
            logger.info(f'Sampling: Getting {count} out of {len(allimages)} from images...')
            allimages = sample(allimages,count)

        # Should I save the images?
        if(saveFiles):
            logger.info("Save: Saving images...")
            self.__saveUnsplashImages(allimages)

        return allimages


def main():
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('Getting unsplash images.')
    us = ImageAPI()
    us.getRandomImagesForTopic("nature", 150, 30)
    logger.info("All done.")


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
