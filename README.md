# Chaotic Image Scrambler

A simple command-line tool that scrambles and restores images using a logistic map - a classic example of a chaotic system. Each scramble produces a unique pixel permutation driven by a randomly seeded sequence, and a key file is saved so the image can be perfectly restored later.

---

## How it works

The scrambler uses the logistic map `x = r * x * (1 - x)` with `r = 4` to generate a long sequence of pseudo-random values. Those values are sorted to produce a permutation index, which is then used to shuffle every pixel in the image. To unscramble, the inverse permutation is computed and applied.

Because the initial seed is random each time, two scrambles of the same image will produce different results. The key file is the only thing that ties a scrambled image back to its original - keep it around.

---

## Requirements

Install dependencies with:

```
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## Usage

### Scramble an image

```
python scrambler.py scramble <input> <output> --keyfile <keyfile>
```

**Arguments:**

- `input` - path to the original image
- `output` - where to save the scrambled image
- `--keyfile` - path where the key will be saved (as a `.npy` file)
---

### Unscramble an image

```
python scrambler.py unscramble <input> <output> --keyfile <keyfile>
```

**Arguments:**

- `input` - path to the scrambled image
- `output` - where to save the restored image
- `--keyfile` - path to the key file generated during scrambling

---
