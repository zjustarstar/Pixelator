import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from collections import Counter
import glob

def get_colors(infile):  #获得图片颜色
    image = Image.open(infile)
    result = image.convert("P", palette=Image.ADAPTIVE)

    palette = result.getpalette()
    colors = list()

    color_counts = sorted(result.getcolors(), reverse=True)
    for i in range(len(color_counts)):
        palette_index = color_counts[i][1]
        dominant_color = palette[palette_index * 3: palette_index * 3 + 3]
        colors.append(tuple(dominant_color))

    main_colors = list()
    thres = 15
    for i, color in enumerate(colors):
        flag = 0
        if (main_colors != []):
            for temp_color in main_colors:
                if ((abs(color[0] - temp_color[0]) <= thres and abs(color[1] - temp_color[1]) <= thres)
                        or (abs(color[1] - temp_color[1]) <= thres and abs(color[2] - temp_color[2]) <= thres)
                        or (abs(color[0] - temp_color[0]) <= thres and abs(color[2] - temp_color[2]) <= thres)
                        or (abs(color[0] - temp_color[0]) <= thres and abs(color[1] - temp_color[1]) <= thres
                            and abs(color[2] - temp_color[2]) <= thres)):
                    flag = 1
        if (flag == 0):
            main_colors.append(color)

    return main_colors

def get_colors_H(colors):#计算获得的颜色对应的色相（H值）
    H=list()
    for i in range(len(colors)):
        r = colors[i][0]/255
        g = colors[i][1]/255
        b = colors[i][2]/255
        Max = max(r,g,b)
        Min = min(r,g,b)
        C = Max - Min
        if C == 0:
            h = 0
        elif Max == r:
            if g >= b:
                h= ((g-b)/C) * 60
            else:
                h = ((g-b)/C) * 60 + 360
        elif Max == g :
            h = ((b-r)/C) * 60 + 120
        elif Max == b:
            h = ((r-g)/C) * 60 +240
        h0 = h/2
        H.append(h0)

    return H

def get_colors_Y(colors):#获得主要颜色对应的YUV中的Y值
    Y = list()
    for i in range(len(colors)):
        r = colors[i][0]
        g = colors[i][1]
        b = colors[i][2]
        y = 0.299*r + 0.587*g + 0.114*b
        Y.append(y)
    return Y

def get_CHY(colors,H,Y):
    sorted_Y = sorted(enumerate(Y), key=lambda x: x[1])
    idx_Y = [i[0] for i in sorted_Y]
    Y = [i[1] for i in sorted_Y]

    sorted_colors = list()
    sorted_H = list()
    for idx in idx_Y:
        sorted_colors.append(colors[idx])
        sorted_H.append(H[idx])
    CHY=(sorted_colors,sorted_H,Y)
    return CHY

def box_pixelation(image,CHY,outw,outh):#图片像素画处理
    h0 = image.shape[0]  # 高
    w0 = image.shape[1]  # 宽
    if h0 <= w0:
        for n in range(1000):
            if 100 * (n - 1) <= h0  < 100 * n:
                grid_h0 = n
        for m in range(1000):
            if 50 * (m-1)<= outh < 50*m:
                grid_outh = m
        grid = round((grid_h0 + grid_outh)/2)
        h = grid * outh
        w = grid * outw

    elif h0 > w0:
        for z in range(1000):
            if 100 * (z - 1) <= w0 < 100 * z:
                grid_w0 = z
        for x in range(1000):
            if 50 * (x - 1) <= outw < 50 * x:
                grid_outw = x
        grid = round((grid_w0 + grid_outw) / 2)
        h = grid * outh
        w = grid * outw

    reimage = cv2.resize(image, (w, h))
    row = int(h / grid)
    col = int(w / grid)

    for i in range(row):
        for j in range(col):
            grid_image = reimage[i * grid:(i + 1) * grid, j * grid:(j + 1) * grid]

            row_grid = grid_image.shape[0]
            col_grid = grid_image.shape[1]

            Y = 256
            B = 0
            G = 0
            R = 0
            for n in range(row_grid):
                for m in range(col_grid):
                    pixel_B = grid_image[n, m, 0]
                    pixel_G = grid_image[n, m, 1]
                    pixel_R = grid_image[n, m, 2]
                    pixel_Y = 0.299 * pixel_R + 0.587 * pixel_G + 0.114 * pixel_B
                    if pixel_Y < Y:
                        Y = pixel_Y
                        B = pixel_B
                        G = pixel_G
                        R = pixel_R

            R1 = R / 255
            G1 = G / 255
            B1 = B / 255
            Max = max(R1, G1, B1)
            Min = min(R1, G1, B1)
            C = Max - Min
            if C == 0:
                h0 = 0
            elif Max == R1:
                if G1 >= B1:
                    h0 = ((G1 - B1) / C) * 60
                else:
                    h0 = ((G1 - B1) / C) * 60 + 360
            elif Max == G:
                h0 = ((B1 - R1) / C) * 60 + 120
            elif Max == B:
                h0 = ((R1 - G1) / C) * 60 + 240
            H = h0 / 2

            main_colors = CHY[0]
            main_H = CHY[1]
            main_Y = CHY[2]
            r_c0 = abs(main_colors[0][0] - R)
            g_c0 = abs(main_colors[0][1] - G)
            b_c0 = abs(main_colors[0][2] - B)

            r_c1 = abs(main_colors[1][0] - R)
            g_c1 = abs(main_colors[1][1] - G)
            b_c1 = abs(main_colors[1][2] - B)

            if R==G==B<50:
                M_color = (0,0,0)
            elif Y<= main_Y[1]:
                if (r_c0<15 and g_c0<15) or (r_c0<15 and b_c0<15) or (g_c0<15 and b_c0<15):
                    mcolor = main_colors[0]
                # elif (r_c1<15 and g_c1<15) or (r_c1<15 and b_c1<15) or (g_c1<15 and b_c1<15):
                #     mcolor = main_colors[1]
                elif (r_c0 < r_c1 and g_c0 < g_c1) or (r_c0 < r_c1 and b_c0 < b_c1) or (g_c0 < g_c1 and b_c0 < b_c1)\
                        or (r_c0 < r_c1 and g_c0 < g_c1 and b_c0 < b_c1):
                    mcolor = main_colors[0]
                # elif (r_c0 > r_c1 and g_c0 > g_c1) or (r_c0 > r_c1 and b_c0 > b_c1) or (g_c0 > g_c1 and b_c0 > b_c1) \
                #         or (r_c0 > r_c1 and g_c0 > g_c1 and b_c0 > b_c1):
                #     mcolor = main_colors[1]

                else:
                    continue
                M_color = mcolor
            # elif main_Y[0]< Y <= main_Y[1]:
            #     if (r_c1<15 and g_c1<15) or (r_c1<15 and b_c1<15) or (g_c1<15 and b_c1<15):
            #         mcolor = main_colors[1]
            #     elif (r_c0<15 and g_c0<15) or (r_c0<15 and b_c0<15) or (g_c0<15 and b_c0<15):
            #         mcolor = main_colors[0]
            #     elif (r_c0 < r_c1 and g_c0 < g_c1) or (r_c0 < r_c1 and b_c0 < b_c1) or (g_c0 < g_c1 and b_c0 < b_c1)\
            #             or (r_c0 < r_c1 and g_c0 < g_c1 and b_c0 < b_c1):
            #         mcolor = main_colors[0]
            #     elif (r_c0 > r_c1 and g_c0 > g_c1) or (r_c0 > r_c1 and b_c0 > b_c1) or (g_c0 > g_c1 and b_c0 > b_c1) \
            #             or (r_c0 > r_c1 and g_c0 > g_c1 and b_c0 > b_c1):
            #         mcolor = main_colors[1]
            #     else:
            #         continue
            #     M_color=mcolor
            else:
                continue

            main_R = M_color[0]
            main_G = M_color[1]
            main_B = M_color[2]

            grid_image[:, :, 2] = main_R
            grid_image[:, :, 1] = main_G
            grid_image[:, :, 0] = main_B
    return reimage

# image_path = "D:\\project_paper\\process\\colors\\A010.png"
# outw = 50
# outh = 50
#
# img = cv2.imread("D:\\project_paper\\process\\0407001\\A010.jpg")
# # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# colors = get_colors(image_path )
# H = get_colors_H(colors)
# Y = get_colors_Y(colors)
# CHY = get_CHY(colors,H,Y)
# pixel_image = box_pixelation(img,CHY,outw,outh)
#
# cv2.imwrite("D:\\project_paper\\process\\0225process\\B010.png", pixel_image, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])