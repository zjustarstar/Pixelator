import cv2
import numpy as np

def process001(img, outH, outW): #对轮廓区域进行处理
    image = img
    h0 = image.shape[0]  # 高
    w0 = image.shape[1]  # 宽

    if h0 == w0 and h0 % outH ==0: #正方形整除关系
        Grid = h0/ outH
        if Grid < 40:
            pixel = Grid
            h = int(pixel * outH)
            w = int(pixel * outW)
        elif 40<= Grid <80:
            pixel = int(Grid/2)
            h = int(pixel * 2 * outH)
            w = int(pixel * 2 * outW)
        elif 80<= Grid <160:
            pixel = int(Grid/4)
            h = int(pixel * 4 * outH)
            w = int(pixel * 4 * outW)
        elif 160<= Grid <320:
            pixel = int(Grid/8)
            h = int(pixel * 8 * outH)
            w = int(pixel * 4 * outW)

    elif h0 == w0 and h0 % outH !=0: #正方形不整除关系
        Grid = int(h0 / outH) + 1 # 达到放大原图效果
        if Grid < 40:
            pixel = Grid
            h = int(pixel * outH)
            w = int(pixel * outW)
        elif 40 <= Grid < 80:
            pixel = int(Grid / 2) +1
            h = int(pixel * 2 * outH)
            w = int(pixel * 2 * outW)
        elif 80 <= Grid < 160:
            pixel = int(Grid / 4) +1
            h = int(pixel * 4 * outH)
            w = int(pixel * 4 * outW)
        elif 160 <= Grid < 320:
            pixel = int(Grid / 8) +1
            h = int(pixel * 8 * outH)
            w = int(pixel * 4 * outW)

    elif h0 != w0 and h0 % outH ==0 and w0 % outW ==0: #长方形整除关系
        if h0 > w0: #以短边计算Grid
            Grid = w0/ outW
            if Grid < 40:
                pixel = Grid
                h = int(pixel * outH)
                w = int(pixel * outW)
            elif 40<= Grid <80:
                pixel = int(Grid/2)
                h = int(pixel * 2 * outH)
                w = int(pixel * 2 * outW)
            elif 80<= Grid <160:
                pixel = int(Grid/4)
                h = int(pixel * 4 * outH)
                w = int(pixel * 4 * outW)
            elif 160<= Grid <320:
                pixel = int(Grid/8)
                h = int(pixel * 8 * outH)
                w = int(pixel * 4 * outW)

        elif h0 < w0: #以短边计算Grid
            Grid = h0/ outH
            if Grid < 40:
                pixel = Grid
                h = int(pixel * outH)
                w = int(pixel * outW)
            elif 40<= Grid <80:
                pixel = int(Grid/2)
                h = int(pixel * 2 * outH)
                w = int(pixel * 2 * outW)
            elif 80<= Grid <160:
                pixel = int(Grid/4)
                h = int(pixel * 4 * outH)
                w = int(pixel * 4 * outW)
            elif 160<= Grid <320:
                pixel = int(Grid/8)
                h = int(pixel * 8 * outH)
                w = int(pixel * 4 * outW)

    elif h0 != w0 and h0 % outH !=0 or w0 % outW !=0: #长方形不能整除关系
        if h0 > w0:  # 以短边计算Grid
            Grid = int(w0 / outW) +1
            if Grid < 40:
                pixel = Grid
                h = int(pixel * outH)
                w = int(pixel * outW)
            elif 40 <= Grid < 80:
                pixel = int(Grid / 2) +1
                h = int(pixel * 2 * outH)
                w = int(pixel * 2 * outW)
            elif 80 <= Grid < 160:
                pixel = int(Grid / 4) +1
                h = int(pixel * 4 * outH)
                w = int(pixel * 4 * outW)
            elif 160 <= Grid < 320:
                pixel = int(Grid / 8) +1
                h = int(pixel * 8 * outH)
                w = int(pixel * 4 * outW)

        elif h0 < w0:  # 以短边计算Grid
            Grid = int(h0 / outH) +1
            if Grid < 40:
                pixel = Grid
                h = int(pixel * outH)
                w = int(pixel * outW)
            elif 40 <= Grid < 80:
                pixel = int(Grid / 2) +1
                h = int(pixel * 2 * outH)
                w = int(pixel * 2 * outW)
            elif 80 <= Grid < 160:
                pixel = int(Grid / 4) +1
                h = int(pixel * 4 * outH)
                w = int(pixel * 4 * outW)
            elif 160 <= Grid < 320:
                pixel = int(Grid / 8) +1
                h = int(pixel * 8 * outH)
                w = int(pixel * 4 * outW)

    reimage = cv2.resize(image, (w, h))
    row = int(h / pixel)
    col = int(w / pixel)
    # 用于保存最终的目标像素图
    final_pixelImg = np.ones([row, col], np.uint8) * 255

    #以上是对原图进行格子划分，确定格子分辨率，和将原图划分为几行几列
    #以下是对每个格子进行处理，主要是从图像轮廓颜色入手，通过计算格子中某颜色像素点占比而确定格子的处理放式

    for i in range(row):
        for j in range(col):
            pixel_image = reimage[int(i * pixel) : int((i + 1) * pixel), int(j * pixel) : int((j + 1) * pixel)]

            W = pixel_image.shape[0]
            H = pixel_image.shape[1]

            colorB = 0
            colorW = 0
            for row1 in range(0, H):
                for col1 in range(0, W):
                    B = pixel_image[row1, col1, 0]
                    G = pixel_image[row1, col1, 1]
                    R = pixel_image[row1, col1, 2]
                    if B==G==R and R != 255 and G != 255 and B != 255:
                        colorB += 1
                    else:
                        colorW += 1

            if colorB/(pixel*pixel) > 0.09:
                pixel_image[:,:]= 0
                final_pixelImg[i, j] = 0

    return reimage, final_pixelImg


def process002(img, outH, outW): #对非轮廓区域进行处理
    image=img
    h = image.shape[0]  # 高
    w = image.shape[1]  # 宽

    pixelH = int(h/outH)
    pixelW = int(w/outW)

    if h == w:
        Pixel = pixelH
    elif h > w:
        Pixel = pixelW
    elif h < w:
        Pixel = pixelH

    if Pixel<40:
        pixel=Pixel
    elif 40<= Pixel < 80:
        pixel=int(Pixel/2)
    elif 80<= Pixel < 160:
        pixel=int(Pixel/4)
    elif 160<= Pixel < 320:
        pixel=int(Pixel/8)

    row = int(h / pixel)
    col = int(w / pixel)

    for i in range(row):
        for j in range(col):
            pixel_image = image[i * pixel:(i + 1) * pixel, j * pixel:(j + 1) * pixel]
            unique, counts = np.unique(pixel_image.reshape(-1, 3), axis=0, return_counts=True)
            pixel_image[:, :, 0], pixel_image[:, :, 1], pixel_image[:, :, 2] = unique[np.argmax(counts)]

    return image