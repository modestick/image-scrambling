import numpy as np
import cv2
import random
import sys

def logistic_map_key(s):
    h, w = s[0], s[1]
    all_pixels = h * w
    x = random.uniform(0.11 , 0.99)
    skip = 1111
    r = 4
    for _ in range(skip):
        x = r * x * (1 - x)
    array = []
    for _ in range(all_pixels):
        x = r * x * (1 - x)
        array.append(x)
    return np.argsort(array)

def scram(img, k):
    flat = img.reshape((-1, 3))
    scrambled = flat[k]
    return scrambled.reshape(img.shape)

def unscram(scrambled_img, k):
    flat = scrambled_img.reshape((-1, 3))
    reverse_k = np.empty_like(k)
    reverse_k[k] = np.arange(len(k))
    restored = flat[reverse_k]             
    return restored.reshape(scrambled_img.shape)

def load_image(pic):
    img = cv2.imread(pic)
    if img is None:
        print(f"Image '{pic}' not found.")
        sys.exit(1)
    print("Image shape:", img.shape)
    return img

def main():
    pic = "myPicture.png"
    img = load_image(pic)
    lmkey = logistic_map_key(img.shape)
    s = scram(img, lmkey)
    us = unscram(s, lmkey)
    cv2.imwrite("scrambled.png", s)
    cv2.imwrite("unscrambled.png", us)
    print("Default scramble/unscramble completed for 'myPicture.png'.")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        main()
    else:
        cmd = sys.argv[1].lower()
        if cmd == "scramble":
            if len(sys.argv) < 3:
                print("Usage: python script.py scramble <image_path>")
                sys.exit(1)
            pic = sys.argv[2]
            img = load_image(pic)
            lmkey = logistic_map_key(img.shape)
            np.save("key.npy", lmkey)
            s = scram(img, lmkey)
            cv2.imwrite("scrambled.png", s)
            print(f"Image '{pic}' scrambled and saved as 'scrambled.png'. Key saved as 'key.npy'.")
        elif cmd == "unscramble":
            if len(sys.argv) < 3:
                print("Usage: python script.py unscramble <image_path>")
                sys.exit(1)
            pic = sys.argv[2]
            img = load_image(pic)
            try:
                lmkey = np.load("key.npy")
            except FileNotFoundError:
                print("Key file 'key.npy' not found. Cannot unscramble.")
                sys.exit(1)
            us = unscram(img, lmkey)
            cv2.imwrite("unscrambled.png", us)
            print(f"Image '{pic}' unscrambled and saved as 'unscrambled.png'.")
        else:
            print("Invalid argument. Use 'scramble' or 'unscramble' followed by the image filename.")