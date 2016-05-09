from PIL import Image
import pytesseract
 
def img_crop():
    base_img      = '/usr/local/lib/python2.7/dist-packages/pytesseract/mysquad'
    file_format   = '.png'
    SQUAD_IMAGE   = base_img + file_format
    IMAGE_CROPPED_GK = '/usr/local/lib/python2.7/dist-packages/pytesseract/mysquadcrop_gk.png'
    IMAGE_CROPPED_DEF = '/usr/local/lib/python2.7/dist-packages/pytesseract/mysquadcrop_def.png'
    img      = Image.open(SQUAD_IMAGE)
    width    = img.size[0]
    height   = img.size[1]
    img_gk   = img.crop((width -2280, height - 1020, width -1790, height - 945 ))
    GK_IMAGE = base_img + '_gk' + file_format
    img_gk.save(GK_IMAGE)
    img_def  = img.crop((width -2500, height - 785, width -1590, height - 710 ))
    DEF_IMAGE = base_img + '_def' + file_format
    img_def.save(DEF_IMAGE)
    img_mid  = img.crop((width -2500, height - 544, width -1590, height - 469 ))
    MID_IMAGE = base_img + '_mid' + file_format
    img_mid.save(MID_IMAGE)
    img_fwd  = img.crop((width -2314, height - 301, width -1750, height - 225 ))
    FWD_IMAGE = base_img + '_fwd' + file_format
    img_fwd.save(FWD_IMAGE) 
    

def img_to_text():
    IMAGE_CROPPED = '/usr/local/lib/python2.7/dist-packages/pytesseract/mysquad_mid.png'
    #detect words in image
    words = pytesseract.image_to_string(Image.open(IMAGE_CROPPED))
    print words

img_to_text()
#img_crop()
