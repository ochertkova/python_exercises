import PIL
from PIL import Image, ImageEnhance, ImageDraw, ImageFont


# read image and convert to RGB
image=Image.open("readonly/msi_recruitment.gif")
image=image.convert('RGB')



images=[] #create a list for images
intense=[0.1,0.5,0.9] #create a list for intensity
channels = image.split() #write channels into tuple


#function for merging text rectangle with the image
def image_layout(image,channel,intense_rate):

    #create black rectangle image

    im_size = image.size
    w = int(im_size[0]) #use width of the initial image
    h = 50
    img_rec = Image.new("RGB", (w, h))
    rec = ImageDraw.Draw(img_rec)

    #adding text

    text = "channel {} intensity {}".format(i,intense_rate)
    font = ImageFont.truetype("readonly/fanwood-webfont.ttf", 55)
    text_coord = (0,int(h-55))
    rec.text(text_coord, text, fill=None, font=font)


    #create contact image with black rectangle

    x = 0
    y = 0
    contact_image=PIL.Image.new(image.mode, (image.width,image.height + h)) #create contact image canvas
    contact_image.paste(image, (x, y) ) #paste image
    contact_image.paste(img_rec, (x, im_size[1]) ) #paste black rectangle with text


    return contact_image


#function for modifying channels (RGB tuple)

def replace_channel(channels,new_ch_value, i):
    new_channels = list(channels)#converting tuple to list in order to modify
    new_channels[i] = new_ch_value

    return tuple(new_channels) #returning modified RGB channels

#main logic: creating a list of 9 images with different channels and intensity

i = 0
for channel in channels: #iterating through channels
    for intense_rate in intense:  #iterating through rates of intensity
        new_img=image_layout(image,i,intense_rate) #invoke function to merge image with text rectangle
        new_channels = new_img.split() #getting channel values of modified image (with text)
        #changing channel and intensity
        new_img = Image.merge('RGB',replace_channel(new_channels,
                                                    new_channels[i].point(lambda i: i*intense_rate),
                                                    i))
        images.append(new_img)
    i = i+1



# create a contact sheet
first_image=images[0]
contact_sheet=PIL.Image.new(first_image.mode, (first_image.width*3,first_image.height*3))
x=0
y=0

for img in images:
    # Lets paste the current image into the contact sheet
    contact_sheet.paste(img, (x, y) )
    # Now we update our X position. If it is going to be the width of the image, then we set it to 0
    # and update Y as well to point to the next "line" of the contact sheet.
    if x+first_image.width == contact_sheet.width:
        x=0
        y=y+first_image.height
    else:
        x=x+first_image.width

# resize and display the contact sheet
contact_sheet = contact_sheet.resize((int(contact_sheet.width/2),int(contact_sheet.height/2) ))
display(contact_sheet)
