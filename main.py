import cv2
from PIL import Image
import pixel_one as pl
import glob
import os

input_path = "F:\\PythonProj\\Pixelator\\testpic\\b2\\"
# input_path = "D:\\project_paper\\process\\0407001\\"
output_folder = "result\\"

outH = int(input('请输入目标输出高 H 的分辨率：'))
outW = int(input('请输入目标输出宽 W 的分辨率：'))

# 在当前目录自动生成用于保存的文件夹
if not os.path.exists(input_path+output_folder):
    os.makedirs(input_path+output_folder)

imgfile = glob.glob(input_path + "*.png")
totalfile = len(imgfile)
i = 0
for f in imgfile:
    i = i + 1
    img = cv2.imread(f)
    image = Image.open(f)
    (filepath, filename) = os.path.split(f)
    (shotname, extension) = os.path.splitext(filename)
    print("当前正在处理 %d/%d :%s" % (i, totalfile, filename))

    colors = pl.get_colors(image)
    H = pl.get_colors_H(colors)
    Y = pl.get_colors_Y(colors)
    C_H_Y = pl.get_maincolors(colors, H, Y)
    image01, pixel_img = pl.box_pixelation(img, C_H_Y, outW, outH)

    # 原图分辨率的像素图输出
    outfile = input_path + output_folder + filename
    cv2.imwrite(outfile, image01)

    # 实际大小像素图输出,加分辨率后缀
    h, w = pixel_img.shape[0], pixel_img.shape[1]
    outfile = input_path + output_folder + shotname + "_" + str(h) + "_" + str(w) + extension
    cv2.imwrite(outfile, pixel_img)