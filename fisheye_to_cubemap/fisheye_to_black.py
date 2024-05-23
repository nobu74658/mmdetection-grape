import sys
import os 
import numpy as np
import vrProjector
import cv2
from mpmath import mp

#画像の読み込み.入力画像が左側か右側か知っておく必要あり．

def rotate_fisheye(input_img, output_img):
    side = 'right'
    img_size = 480


    if( (side != 'right') and (side !='left') ):
        print( '3rd argument must be "right" or "left"' ) 
        sys.exit()

    fisheye_raw = cv2.imread( input_img, cv2.IMREAD_COLOR )
    blanc_img = np.zeros( (fisheye_raw.shape[0], fisheye_raw.shape[1], 3 ), np.uint8 )
    dualfisheye = cv2.hconcat( [blanc_img, fisheye_raw ] )
    
    #一時保存
    cv2.imwrite( 'dualfish_fix.png', dualfisheye )

    #キューブマップにしてみる
    source = vrProjector.SideBySideFisheyeProjection()
    source.loadImage('dualfish_fix.png')

    # theta_offset: 垂直方向の回転角度
    # phi_offset: 水平方向の回転角度
    source.reprojectToThis(source, theta_offset= mp.pi /4, phi_offset= mp.pi/3)
    source.saveImage_half('rotate_fisheye.png', side)

    # out = vrProjector.CubemapProjection()
    # out.initImages(img_size,img_size)
    # out.reprojectToThis(source)

    # if( side == 'right' ):
    #     out.saveImages("front.png", output_img, "back.png", "left.png", "top.png", "bottom.png")
    # else:
    #     out.saveImages("front.png", "right.png", "back.png", output_img, "top.png", "bottom.png")

def fisheye_to_cubemap_folder(input_folder, output_folder):
    for image_path in os.listdir(input_folder):
        rotate_fisheye(input_folder + image_path, output_folder + image_path)

# input_folder = '/mmdetection/grape/data/fisheye/'
# output_folder = '/mmdetection/grape/data/cubemap/'
# fisheye_to_cubemap_folder(input_folder, output_folder)
        
rotate_fisheye('/Users/nobu/research/mmdetection-grape/fisheye_to_cubemap/test.png', '/Users/nobu/research/mmdetection-grape/fisheye_to_cubemap/hoge_half_rotate.png')