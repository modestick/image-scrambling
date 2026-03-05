import numpy as np
import cv2
import random
import argparse
import sys
import os


def logistic_map_key(s):
    h, w = s[0], s[1]
    all_pixels = h * w
    x = random.uniform(0.11, 0.99)
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
    if os.path.isdir(args.input):
        os.makedirs(args.output, exist_ok=True)
        for filename in os.listdir(args.input):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                input_path = os.path.join(args.input, filename)
                basename = os.path.splitext(filename)[0]
                output_path = os.path.join(args.output, f"scrambled_{basename}.png")
                keyfile_path = os.path.join(args.output, f"key_{basename}.npy")
                img = load_image(input_path)
                key = logistic_map_key(img.shape)
                scrambled_img = scram(img, key)
                cv2.imwrite(output_path, scrambled_img)
                np.save(keyfile_path, key)
                print(f"Image '{filename}' scrambled and saved to '{output_path}'. Key saved to '{keyfile_path}'.")
    else:
        if args.keyfile is None:
            basename = os.path.splitext(args.output)[0]
            keyfile_path = f"{basename}.npy"
        else:
            keyfile_path = args.keyfile
        img = load_image(args.input)
        key = logistic_map_key(img.shape)
        scrambled_img = scram(img, key)
        cv2.imwrite(args.output, scrambled_img)
        np.save(keyfile_path, key)
        print(f"Image scrambled and saved to '{args.output}'. Key saved to '{keyfile_path}'.")


def unscramble_command(args):
    if os.path.isdir(args.input):
        os.makedirs(args.output, exist_ok=True)
        for filename in os.listdir(args.input):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                input_path = os.path.join(args.input, filename)
                basename = os.path.splitext(filename)[0]
                output_path = os.path.join(args.output, f"restored_{basename}.png")
                if filename.startswith("scrambled_"):
                    original_name = filename[len("scrambled_"):]
                else:
                    original_name = filename
                original_basename = os.path.splitext(original_name)[0]
                keyfile_path = os.path.join(args.input, f"key_{original_basename}.npy")
                if not os.path.exists(keyfile_path):
                    print(f"Key file '{keyfile_path}' not found, skipping '{filename}'.")
                    continue
                scrambled_img = load_image(input_path)
                key = np.load(keyfile_path)
                restored_img = unscram(scrambled_img, key)
                cv2.imwrite(output_path, restored_img)
                print(f"Image '{filename}' unscrambled and saved to '{output_path}'.")
    else:
        if args.keyfile is None:
            print("Error: --keyfile is required when unscrambling a single file.")
            sys.exit(1)
        scrambled_img = load_image(args.input)
        key = np.load(args.keyfile)
        restored_img = unscram(scrambled_img, key)
        cv2.imwrite(args.output, restored_img)
        print(f"Image unscrambled and saved to '{args.output}'.")


def main():
    parser = argparse.ArgumentParser(description="Chaotic Image Scrambler")
    subparsers = parser.add_subparsers(required=True)

    scramble_parser = subparsers.add_parser("scramble")
    scramble_parser.add_argument("input", help="Input image or directory of images")
    scramble_parser.add_argument("output", help="Output scrambled image or directory")
    scramble_parser.add_argument("--keyfile", help="File to store generated key (single file mode only; auto-derived if omitted)")
    scramble_parser.set_defaults(func=scramble_command)

    unscramble_parser = subparsers.add_parser("unscramble")
    unscramble_parser.add_argument("input", help="Scrambled image or directory of scrambled images")
    unscramble_parser.add_argument("output", help="Restored image or directory")
    unscramble_parser.add_argument("--keyfile", help="Key file (single file mode only; auto-located in directory mode)")
    unscramble_parser.set_defaults(func=unscramble_command)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()