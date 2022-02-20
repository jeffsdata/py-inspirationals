# Getting Started
0. Install dependencies from requirements.txt
    - `pip install -r requirements.txt`
1. Create a list of quotes - in /data/raw/quotes.csv (a demo file is provided)
    - Should have two columns: "quote" and "attributed".
    <img src="./readme-images/quotes-data.png">

2. Create an account on Unsplash and get ClientID
    - Go to: [Unsplash Developers](https://unsplash.com/developers)
    - Sign up
    - Under "Your Apps", create an app and get ClientID (aka: "Access Key")
    - Create a .env file in the root of the project.
    - Create an env variable: `UNSPLASH_CLIENTID=c238cg3ge9g9e_cedusgidicdsc929g29g2972e32df` (this is not a valid client id)
    - Note: There are two levels of app:
        - Dev: Allows 50 calls per hour (plenty for this project - to get up to 1500 images from a topic to work with)
        - Prod: Allows 50,000 calls per hour... obviously, this is probably excessive.

3. Create nature images - to be the base of your inspirational messages.
    - Run /src/data/unsplash
    - in the main() method, `us.getRandomImagesForTopic("nature", 150)`
        - "nature" is the topic - you can pick a different topic if you'd like (explore unsplash.com)
        - 150 is the number of images to save (save enough images for the number of quotes you have in quotes.csv). 
        - wideOnly (bool, optional): Whether you only want to return wide aspect images. Defaults to True.
        - saveFiles (bool, optional): Whether you want to save the files to /data/raw/images. Defaults to True.
    - in the getRandomImagesForTopic() method, `allimages = self.getImagesForTopic(topic, 30)`
        - If you have more than 450 quotes, you'll want to adjust this. The "30" will get 30 pages of 30 images each - 900 images. If you want only horizontal images, then you may not have enoguh after it filters them. Adjust this to get more images to work with if you're not getting enough.

4. Create the inspirational images
    - Run /src/data/imagemaker
    - Will combine the quotes and images, making inspirational images, like below. 


## Examples:
<img src="./readme-images/_7pntVTqEoo.jpg">
<img src="./readme-images/0YG1nfI77T4.jpg">
<img src="./readme-images/9Nn21mIKP1w.jpg">
<img src="./readme-images/9Nn21mIKP1w.jpg">