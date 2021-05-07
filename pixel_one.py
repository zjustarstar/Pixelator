from PIL import Image
import numpy as np
import cv2

def get_colors(image):  #获得图片主要颜色
    # image = Image.open(infile)
    # reimage = image.resize((100,100))
    result = image.convert("P", palette=Image.ADAPTIVE)

    # 找到主要的颜色
    palette = result.getpalette()
    colors = list()

    color_counts = sorted(result.getcolors(), reverse=True)
    if len(color_counts)>30:
        for i in range(30):
            palette_index = color_counts[i][1]
            dominant_color = palette[palette_index * 3: palette_index * 3 + 3]
            colors.append(tuple(dominant_color))
    elif len(color_counts)<= 30:
        for i in range(len(color_counts)):
            palette_index = color_counts[i][1]
            dominant_color = palette[palette_index * 3: palette_index * 3 + 3]
            colors.append(tuple(dominant_color))

    return colors

def get_colors_H(colors):
    H = list()
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
        h0=h/2
        H.append(h0)

    return H

def get_colors_Y(colors):
    Y = list()
    for i in range(len(colors)):
        r = colors[i][0]
        g = colors[i][1]
        b = colors[i][2]
        y = 0.299*r + 0.587*g + 0.114*b
        Y.append(y)
    return Y

def get_maincolors(colors,H,Y):
    H0=list()
    C0=list()
    Y0=list()
    for i in range(len(H)):
        if H[i] not in H0:
            H0.append(H[i])
            C0.append(colors[i])
            Y0.append(Y[i])
    color30 = list()
    H30=list()
    Y30=list()
    color60 = list()
    H60 = list()
    Y60 = list()
    color90 = list()
    H90 = list()
    Y90 = list()
    color120 = list()
    H120 = list()
    Y120 = list()
    color150 = list()
    H150 = list()
    Y150 = list()
    color180 = list()
    H180 = list()
    Y180 = list()
    color210 = list()
    H210 = list()
    Y210 = list()
    color240 = list()
    H240 = list()
    Y240 = list()
    color270 = list()
    H270 = list()
    Y270 = list()
    color300 = list()
    H300 = list()
    Y300 = list()
    color330 = list()
    H330 = list()
    Y330 = list()
    color360 = list()
    H360 = list()
    Y360= list()
    for j in range(len(H0)):
        H1 = H0[j]
        C1 = C0[j]
        Y1 = Y0[j]
        if 0 <= H1 <30:
            color30.append(C1)
            H30.append(H1)
            Y30.append(Y1)
        elif 30 <= H1 <60:
            color60.append(C1)
            H60.append(H1)
            Y60.append(Y1)
        elif 60 <= H1 <90:
            color90.append(C1)
            H90.append(H1)
            Y90.append(Y1)
        elif 90 <= H1 <120:
            color120.append(C1)
            H120.append(H1)
            Y120.append(Y1)
        elif 120 <= H1 <150:
            color150.append(C1)
            H150.append(H1)
            Y150.append(Y1)
        elif 150 <= H1 <180:
            color180.append(C1)
            H180.append(H1)
            Y180.append(Y1)
        elif 180 <= H1 <210:
            color210.append(C1)
            H210.append(H1)
            Y210.append(Y1)
        elif 210 <= H1 <240:
            color240.append(C1)
            H240.append(H1)
            Y240.append(Y1)
        elif 240 <= H1 <270:
            color270.append(C1)
            H270.append(H1)
            Y270.append(Y1)
        elif 270 <= H1 <300:
            color300.append(C1)
            H300.append(H1)
            Y300.append(Y1)
        elif 300 <= H1 <330:
            color330.append(C1)
            H330.append(H1)
            Y330.append(Y1)
        elif 330 <= H1 <360:
            color360.append(C1)
            H360.append(H1)
            Y360.append(Y1)
    Dcolors = (color30, color60, color90, color120, color150, color180, color210, color240, color270, color300, color330, color360)
    maincolors = [x for x in Dcolors if x]
    DH = (H30,H60,H90,H120,H150,H180,H210,H240,H270,H300,H330,H360)
    mainH = [z for z in DH if z]
    DY = (Y30,Y60,Y90,Y120,Y150,Y180,Y210,Y240,Y270,Y300,Y330,Y360)
    mainY = [v for v in DY if v]
    # colors_H_Y=(maincolors,mainH,mainY)
    colors_H_Y=(Dcolors,DH,DY)
    # print(maincolors)
    # print(mainH)
    # print(mainH)

    return colors_H_Y

def box_pixelation(image,colors_H_Y,outw,outh):
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

    # 用于保存最终的目标像素图
    final_pixelImg = np.ones([row, col], np.uint8) * 255

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

            R1 = R/255
            G1 = G/255
            B1 = B/255
            Max = max(R1, G1, B1)
            Min = min(R1, G1, B1)
            C = Max - Min
            if C == 0:
                h0 = 0
            elif Max == R1:
                if G1>= B1:
                    h0 = ((G1 - B1) / C) * 60
                else:
                    h0 = ((G1 - B1) / C) * 60 + 360
            elif Max == G:
                h0 = ((B1 - R1) / C) * 60 + 120
            elif Max == B:
                h0 = ((R1 - G1) / C) * 60 + 240
            H = h0

            if R>200 and G>200 and B>200:
                color=(255,255,255)
            elif R==G==B>50:
                color=(255,255,255)
            elif R==G==B<=50:
                color=(0,0,0)
            else:
                color_one=colors_H_Y[0]
                H_one=colors_H_Y[1]
                Y_one=colors_H_Y[2]


                for x in range(12):
                    if 30*x <= H <30*(x+1):
                        s_one = x
                if len(H_one[x])==0:
                    color=(R,G,B)
                elif len(H_one[x])!=0:
                    color_two = color_one[s_one]
                    H_two = H_one[s_one]
                    Y_two = Y_one[s_one]

                    Cmh_two=list()
                    for z in range(len(H_two)):
                        mh_two=abs(H_two[z] - H)
                        Cmh_two.append(mh_two)
                    for u in range(len(Cmh_two)):
                        for v in range(len(Cmh_two)):
                            if Cmh_two[u] ==Cmh_two[v]==min(Cmh_two) and u<=v and Y_two[u]<=Y_two[v]:
                                s_two = u
                            elif Cmh_two[u] ==Cmh_two[v]==min(Cmh_two) and u<=v and Y_two[u]>Y_two[v]:
                                s_two = v
                    color_three = color_two[s_two]
                    color = color_three

            main_R = color[0]
            main_G = color[1]
            main_B = color[2]

            grid_image[:, :, 2] = main_R
            grid_image[:, :, 1] = main_G
            grid_image[:, :, 0] = main_B

            final_pixelImg[i, j] = color[0]

    # 转为RGB格式，方便在其它程序中使用;
    final_pixelImg = cv2.cvtColor(final_pixelImg, cv2.COLOR_GRAY2BGR)

    return reimage, final_pixelImg

