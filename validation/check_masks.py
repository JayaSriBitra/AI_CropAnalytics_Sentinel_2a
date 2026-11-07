"""Inspect a Sentinel-2 image GeoTIFF and its label-mask GeoTIFF."""
import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", required=True, help="Path to image GeoTIFF")
    parser.add_argument("--mask", required=True, help="Path to label-mask GeoTIFF")
    parser.add_argument("--nodata", type=float, default=None,
                        help="Optional mask NoData value to exclude from value listing")
    args = parser.parse_args()

    try:
        import numpy as np
        import rasterio
    except ImportError:
        print("Install dependencies first: pip install rasterio numpy", file=sys.stderr)
        return 2

    with rasterio.open(args.image) as image, rasterio.open(args.mask) as mask:
        print(f"Image: bands={image.count}, size={image.width}x{image.height}")
        print(f"Mask:  bands={mask.count}, size={mask.width}x{mask.height}")
        print(f"Image CRS: {image.crs}")
        print(f"Mask CRS:  {mask.crs}")
        print(f"Image transform: {image.transform}")
        print(f"Mask transform:  {mask.transform}")
        print(f"Image bounds: {image.bounds}")
        print(f"Mask bounds:  {mask.bounds}")

        problems = []
        if image.width != mask.width or image.height != mask.height:
            problems.append("Image and mask dimensions differ")
        if image.crs != mask.crs:
            problems.append("Image and mask CRS differ")
        if image.transform != mask.transform:
            problems.append("Image and mask transforms differ")
        if mask.count != 1:
            problems.append("Expected a single-band class-label mask")

        values = set()
        for _, window in mask.block_windows(1):
            block = mask.read(1, window=window)
            values.update(np.unique(block).tolist())
        if args.nodata is not None:
            values.discard(args.nodata)

        print(f"Mask values (after optional NoData exclusion): {sorted(values)}")
        if problems:
            print("CHECK REQUIRED:")
            for problem in problems:
                print(f"- {problem}")
            return 1

        print("Basic grid checks passed. This does not verify label correctness.")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
