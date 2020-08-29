import os
import math
from PIL import Image
import PIL.Image

class ImageResizer:
    @staticmethod
    def getImageRatio(image_height, image_width):
        # get the ratio of image
        return float(image_width/image_height)

    @staticmethod
    def ifTargetSourceRatioEqual(target_height, target_width, source_height, source_width):
        # check if ratio is the same between the source image and the target image.
        source_ratio = ImageResizer.getImageRatio(source_height, source_width)
        target_ratio = ImageResizer.getImageRatio(target_height, target_width)

        return (True if source_ratio == target_ratio else False)

    @staticmethod
    def getHeightWithRatio(image_width, image_ratio):
        return math.ceil(image_width / image_ratio)

    @staticmethod
    def getWidthWithRatio(image_height, image_ratio):
        return math.ceil(image_height * image_ratio)

    @staticmethod
    def resizeImage(image, target_height, target_width):
        size = (target_width, target_height)
        image = image.resize(size, PIL.Image.ANTIALIAS)
        return image

    @staticmethod
    def resize(image, max_height, max_width, min_height, min_width):
        source_ratio = ImageResizer.getImageRatio(image.height, image.width)
        target_ratio = ImageResizer.getImageRatio(max_height, max_width)
        return image

    @staticmethod
    def resizePipeline(image, max_height, max_width, min_height, min_width, option='aspect', bg_color=(255,255,255)):
        # source image's ratio
        source_ratio = ImageResizer.getImageRatio(image.height, image.width)
        output_image = None 

        if max_height == -1:
            # set max_height
            max_height = ImageResizer.getHeightWithRatio(max_width, source_ratio)
        if max_width == -1:
            # set max_width
            max_width = ImageResizer.getWidthWithRatio(max_height, source_ratio)

        if min_height == -1: min_height = image.height
        if min_width == -1: min_width = image.width

        TARGET_SOURCE_RATIO_EQUAL = ImageResizer.ifTargetSourceRatioEqual(max_height, max_width, image.height, image.width)      
        # target's ratio
        target_ratio = ImageResizer.getImageRatio(max_height, max_width) 
        
        # Judging the size
        if (image.width > max_width) or (image.height > max_height):
            # Need to scale size
            if source_ratio >= 1: # 橫圖
                target_width = max_width
                # get expect target height 
                expected_target_height = ImageResizer.getHeightWithRatio(target_width, source_ratio)
                if expected_target_height > max_height:
                    target_width = min_width
                target_height = ImageResizer.getHeightWithRatio(target_width, source_ratio)
            else:  # 直圖
                target_height = max_height
                 # get expect target width 
                expected_target_width = ImageResizer.getWidthWithRatio(target_height, source_ratio)
                if expected_target_width > max_width:
                    target_height = min_height
                target_width = ImageResizer.getWidthWithRatio(target_height, source_ratio)

            # Resize Image
            image = ImageResizer.resizeImage(image, target_height, target_width)

        if (image.width < min_width) or (image.height < min_height):
            # 需要縮至 target_size
            if source_ratio >=1: # 橫圖
                target_width = min_width
                # get expected target height 
                expected_target_height = ImageResizer.getHeightWithRatio(target_width, source_ratio)
                if expected_target_height < min_height:
                    target_width = max_width
                target_height = ImageResizer.getHeightWithRatio(target_width, source_ratio)
            else: # 直圖
                target_height = min_height
                # get expected target width 
                expected_target_width = ImageResizer.getWidthWithRatio(target_height, source_ratio)
                if expected_target_width < min_width:
                    target_height = max_width
                target_width = ImageResizer.getWidthWithRatio(target_height, source_ratio)
            # Resize image
            image = ImageResizer.resizeImage(image, target_height, target_width)
        
        if TARGET_SOURCE_RATIO_EQUAL: # source, target ratio eq without cropping or filling..
            return image
        
        # source, target ratio not eq. According to the option parameter `crop` or `fill bg`
        if option == 'crop': # crop image
            source_width = image.width
            source_height = image.height

            aspect_ratio = float(source_width)/float(source_height)
            if(aspect_ratio > target_ratio):
                #crop left and right
                target_height = source_height
                target_width = round(source_height * target_ratio)
                dx = round(source_width - target_width)
                left_x = dx/2
                resize = (left_x, 0, left_x + target_width, target_height)
            else:
                #crop top and bottom
                target_width = source_width
                target_height = round(source_width / target_ratio)
                dy = source_height - target_height
                top_y = round(dy/2)
                resize = (0, top_y, target_width, top_y+target_height)
            output_image = image.crop(resize)
    
        elif option == 'fill': # fill backgroud
            # fill bakcgroud color
            if (source_ratio> target_ratio): # fill top and bottom.
                area_width = image.width # match width
                area_height = ImageResizer.getHeightWithRatio(image.width, target_ratio)
                output_image = Image.new('RGB', (int(area_width),int(area_height)), bg_color)

                # fit image into center along Y axis
                y_pos = float(area_height - image.height) / 2.0
                output_image.paste(image, (0, int(y_pos)))
                
            else: # fill left and right
                area_height = image.height # match height
                area_width = ImageResizer.getWidthWithRatio(image.height, target_ratio)

                output_image = Image.new('RGB', (int(area_width),int(area_height)) ,bg_color)

                # fit image into center along X axis
                x_pos = float(area_width - image.width) / 2.0
                output_image.paste(image, (int(x_pos), 0))

        elif option == 'aspect':
            return image

        if not output_image is None:
            image = output_image

        return image

if __name__ == '__main__':
    image = Image.open("./path_to_image.jpg")
    image = ImageResizer.resizePipeline(image, max_height=1000, max_width=1000, min_height=500, min_width=500, option="aspect", bg_color=(0,255,255))
    image.show()
