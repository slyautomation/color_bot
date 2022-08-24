# color_bot
```
img = Image.open(filename)
```
Opens the file namely the 'test.png' file
```
w, h = img.size
```
Returns 2 values the height and width in pixels

img = img.convert('RGBA') # converts the image so we can read the data as rgba values a
# is for alpha or transparency level
data = img.getdata() # imagine the image file as a matrix of pixels in rows and columns
# and each single cell has meta data that meta data is the rbg value,
# we'll use the excel document later to visualise this concept
image = cv2.imread(filename) # reads the file but using opencv for later use
i = 0 # this is a counter and it will be used to get the index of our loop function in order to identify the location of the desired pixel colour’s location.

For item in data # this is the lloop function and will iterate through each pixel and determine if the meta rgb value is the desired color we need. 
First to visualise the data print item prints the value of each pixels color represented as a tuple value 255, 255 , 255 is a white pixel.
if item[0] == rgb[0] and item[1] == rgb[1] and item[2] == rgb[2]: 
so we are comparing the tuple value which is storing the rgb value for each pixel and comparing  our color to see if all values match with the pixel color. 
            print(True)
            print("index:", [i])
If it does we have found the first pixel that matches our color
So print true and print the index so we know what the position the pixel found on.
            print("img height:", h, "| img width:", w)
so this is print the pixel width and height of our image which is needed to find the x and y coordinate of the matching pixel color.
I’ll go over to excel so we can visualise what is happening.
            print("row:", i/w, "column:", (i/w % 1)*w)
so to get the y we divide the index by the width and for the x it is the left over decimal values of index divided by width percentage 1. Which takes the fractional parts of the integer and we multiply that by the width. 
            p2 = round(i/w)
            p1 = round((i/w % 1)*w)
            image = cv2.rectangle(image, pt1=(p1 - 2, p2 - 2), pt2=(p1 + 2, p2 + 2), color=(0, 0, 0), thickness=1)
            cv2.imwrite("textshot.png", image)
this part is where the script will draw a rectangle around the matching pixel color and it will save the result as textshot.png
            return True # return true if the color pixel is found
        i += 1 this is the counter at the end of loop which is incremented at each loop
    print(False)
    return False
if no matching color pixel was found print and return false

