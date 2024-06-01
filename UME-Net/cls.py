import os

# 获取当前文件夹名称
folder_name = os.path.basename(os.getcwd())

# 遍历当前文件夹中的文件，保存所有文件名到train_result.txt中
with open("{}.txt".format(folder_name), "a+") as f:
    f.write("\n\n=========================\n\n")
    for filename in os.listdir('./output_result/'):
        if 'epoch' not in filename:
            continue
        f.write(filename + "\n")

# 找出文件名数字最大的文件
filenames = os.listdir('./output_result/')

max_psnr = {}
max_ssim = {}
exits = list()
for d in filenames:
    if 'epoch' not in d:
        continue
    cls = d.split('_')[-1].split('.')[0]
    psnr = d.split('_')[2]
    ssim = d.split('_')[3]

    if cls not in max_psnr:
        max_psnr[cls] = (d, psnr)
    else:
        if psnr > max_psnr[cls][1]:
            max_psnr[cls] = (d, psnr)

    if cls not in max_ssim:
        max_ssim[cls] = (d, ssim)
    else:
        if ssim > max_ssim[cls][1]:
            max_ssim[cls] = (d, ssim)

    for cls, (d, psnr) in max_psnr.items():
        if d not in exits:
            exits.append(d)

    for cls, (d, ssim) in max_ssim.items():
        if d not in exits:
            exits.append(d)

# 删除除了文件名数字最大的其他文件
for filename in os.listdir('./output_result/'):
    if 'epoch' not in filename:
        continue
    if filename not in d:
        os.remove(os.path.join('./output_result/', filename))
