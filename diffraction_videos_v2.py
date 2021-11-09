import numpy as np
from matplotlib import pyplot as plt
import os
import glob
import pandas as pd
import cv2

l = 0.14235

video_name = 'Tathiane.avi'
image_folder = 'images_folder'

for filename in os.listdir(os.getcwd()):
    if filename[-4:] == ".chi":
        aq = pd.DataFrame()

        aq = pd.read_csv(filename, skiprows=4, delim_whitespace=True)
        aq.columns = ["angle", "intensity"]
        aq["d_spacing"] = l/(2*np.sin(((aq["angle"]*np.pi)/180)/2))
        # aq["intensity"] = aq["intensity"]/aq["intensity"].max()

        fig = plt.figure()
        ax = fig.add_axes([.12, .12, .85, .85])
        ax.plot(aq["d_spacing"], aq["intensity"]/aq["intensity"].max(), c="k")
        ax.set_xlabel(r"Interplanar Spacing ($\AA$)", size=13)
        ax.set_ylabel("Normalized Intensity", size=13)
        ax.set_xlim(2.3, 1.7)
        # ax.set_ylim(3,10)
        ax.annotate(f'TC_11Mn', xy=(1.9, .82), xytext=(1.9, .82))
        ax.annotate(f'Acquisition: {filename[-8:-4]}', xy=(1.9, .72), xytext=(1.9, .72))
        # ax.annotate(f'QUEM É TEU DEUS ?!', xy=(30,630), xytext=(30, 630))
        del aq
        if int(filename[-7:-4]) in range(1, 10):
            plt.savefig("images_folder/" +
                        filename[:-6] + "000" + filename[-5:-4] + ".jpg", dpi=75)
        elif int(filename[-7:-4]) in range(10, 100):
            plt.savefig("images_folder/" +
                        filename[:-7] + "00" + filename[-6:-4] + ".jpg", dpi=75)
        elif int(filename[-7:-4]) in range(100, 1000):
            plt.savefig("images_folder/" +
                        filename[:-8] + "0" + filename[-7:-4] + ".jpg", dpi=75)


images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
images.sort()
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, 0, 20, (width, height))

for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
cvDestroyAllWindows
video.release()


# l = 0.14235
# aq = pd.read_csv("TC_11Mn_S1_1-00315.chi", skiprows=4, delim_whitespace=True)
# aq.columns = ["angle", "intensity"]
# aq["d_spacing"] = l/(2*np.sin(((aq["angle"]*np.pi)/180)/2))
# # aq["intensity"] = aq["intensity"]/aq["intensity"].max()

# fig = plt.figure()
# ax = fig.add_axes([.12,.12,.85,.85])
# ax.plot(aq["d_spacing"], aq["intensity"]/aq["intensity"].max(), c="k")
# ax.set_xlabel(r"Interplanar Spacing ($\AA$)", size=13)
# ax.set_ylabel("Intensity (log)", size=13)
# ax.set_xlim(2.3,1.7)
# ax.annotate('TC_11Mn', xy=(1.9,.82), xytext=(1.9,.82))
# ax.annotate('Acquisition:', xy=(1.9,.72), xytext=(1.9,.72))
# # ax.set_ylim(4,10)

# plt.show()
