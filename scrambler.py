import numpy as np
import cv2
import random
import argparse


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


def scramble_command(args):
    img = load_image(args.input)
    key = logistic_map_key(img.shape)
    scrambled_img = scram(img, key)
    cv2.imwrite(args.output, scrambled_img)
    np.save(args.keyfile, key)
    print(f"Image scrambled and saved to '{args.output}'. Key saved to '{args.keyfile}'.")

def unscramble_command(args):
    scrambled_img = load_image(args.input)
    key = np.load(args.keyfile)
    restored_img = unscram(scrambled_img, key)
    cv2.imwrite(args.output, restored_img)
    print(f"Image unscrambled and saved to '{args.output}'.")




def main():
    parser = argparse.ArgumentParser(description="Chaotic Image Scrambler")

    subparsers = parser.add_subparsers(required=True)

    
    scramble_parser = subparsers.add_parser("scramble")
    scramble_parser.add_argument("input", help="Input image")
    scramble_parser.add_argument("output", help="Output scrambled image")
    scramble_parser.add_argument("--keyfile", required=True, help="File to store generated key")
    scramble_parser.set_defaults(func=scramble_command)

    
    unscramble_parser = subparsers.add_parser("unscramble")
    unscramble_parser.add_argument("input", help="Scrambled image")
    unscramble_parser.add_argument("output", help="Restored image")
    unscramble_parser.add_argument("--keyfile", required=True,
                                   help="Key file used during scrambling")
    unscramble_parser.set_defaults(func=unscramble_command)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()