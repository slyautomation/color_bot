# Easy Color Bot Project Guide

<img src="https://user-images.githubusercontent.com/81003470/187099489-426bc3af-9415-407d-8981-09fe1031a38b.png" width="120">

```
img = Image.open(filename)
```
Opens the file namely the 'test.png' file.

<img src="https://user-images.githubusercontent.com/81003470/187099244-5c4d4910-7a64-4771-8068-9f8116e0f3ba.png" width="55">

```
w, h = img.size
```
Returns 2 values the height and width in pixels.

```
img = img.convert('RGBA') # 
```
converts the image so we can read the data as rgba values; 'A' is for alpha or transparency level.

<img src="https://user-images.githubusercontent.com/81003470/187099175-d5eda19e-a9b0-497c-bf55-0bb6835eb451.png" width="55">

```
data = img.getdata() # 
```
Imagine the image file as a matrix of pixels in rows and columns and each single cell has meta data that meta data is the rbg value.

<img src="https://user-images.githubusercontent.com/81003470/187099353-ddbd5fe9-8eda-4500-8e23-242ff9398021.png" width="55">

```
image = cv2.imread(filename) # 
```
Reads the file but using opencv for later use.

<img src="https://user-images.githubusercontent.com/81003470/187099458-3995bc95-aec6-423b-9a17-ad3e6a133982.png" width="55">

```
i = 0
```
A counter and it will be used to get the index of our loop function in order to identify the location of the desired pixel colour’s location.

<img src="https://user-images.githubusercontent.com/81003470/187099469-138c26c4-d59a-4bd3-b619-8dc21ab7e635.png" width="55">

```
For item in data: 
```
loop function and will iterate through each pixel and determine if the meta rgb value is the desired color we need. 

<img src="https://user-images.githubusercontent.com/81003470/187099570-fa29070a-0b6b-4393-a03b-e4f233df68cd.png" width="55">

First to visualise the data print item prints the value of each pixels color represented as a tuple value 255, 255 , 255 is a white pixel.

```
if item[0] == rgb[0] and item[1] == rgb[1] and item[2] == rgb[2]: 
```
Comparing the tuple value which is storing the rgb value for each pixel and comparing our color to see if all values match with the pixel color. 
```
print(True)
print("index:", [i])
```
If it does we have found the first pixel that matches our color
So print true and print the index so we know what the position the pixel found on.

<img src="https://user-images.githubusercontent.com/81003470/187099640-7d81650b-170c-452f-8e98-ef4ae6b24fec.png" width="55"> <img src="https://user-images.githubusercontent.com/81003470/187099632-db41f5c5-bc78-4a28-a5b9-2b24da41bdc3.png" width="55">

```
print("img height:", h, "| img width:", w)
```
so this is print the pixel width and height of our image which is needed to find the x and y coordinate of the matching pixel color.
I’ll go over to excel so we can visualise what is happening.
```
print("row:", i/w, "column:", (i/w % 1)*w)
```
Get the y; divide the index by the width
For the x it is the left over decimal values of index divided by width.
```
p2 = round(i/w)
p1 = round((i/w % 1)*w)
```
```
image = cv2.rectangle(image, pt1=(p1 - 2, p2 - 2), pt2=(p1 + 2, p2 + 2), color=(0, 0, 0), thickness=1)
cv2.imwrite("textshot.png", image)
```
Draw a rectangle around the matching pixel color and it will save the result as textshot.png
```
return True
```
Return true if the color pixel is found
```
i += 1 
```
The counter at the end of loop which is incremented at each loop
```
print(False)
return False
```
if no matching color pixel was found print and return false

_Images provided by https://www.flaticon.com/_
