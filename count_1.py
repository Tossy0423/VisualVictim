# -*- coding: utf-8
import numpy as np


def main():
    img1 = np.array([[1,1,1],[0,0,0]])
    img2 = np.array([[1,0,0],[0,0,1]])
    img1 = np.reshape(img1,-1)
    img2 = np.reshape(img2,-1)
    diff = img1 - img2
    dis =  len(np.where(diff==0)[0])
    
    print("img1:{}".format(img1))
    print("img2:{}".format(img2))
    print("diff:{}".format(diff))
    print("dis:{}".format(dis))
if __name__ == "__main__":
    main()
