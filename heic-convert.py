#!/usr/bin/env python3

# Import the necessary libraries
from tqdm import tqdm
import os
import pyheif
import piexif
import sys
import argparse
from pathlib import Path
from PIL import Image

# This is our main function that does the actual conversion
def main(files):
    # This iterates over all of the file names we give it
    for f in tqdm(files):
        # Read in the image
        heif_file = pyheif.read(f)
        # Create the image from the heic file
        image = Image.frombytes(
                heif_file.mode,
                heif_file.size,
                heif_file.data,
                "raw",
                heif_file.mode,
                heif_file.stride,
            )
        # Write out the metadata
        for metadata in heif_file.metadata or []:
            if metadata['type'] == 'Exif':
                exif_dict = piexif.load(metadata['data'])

        # Clean up some of the data
        exif_dict['0th'][274] = 0
        exif_bytes = piexif.dump(exif_dict)
        # Export name
        exportName = Path(f).stem + '.jpg'
        # Save the image
        image.save(exportName, "JPEG", exif=exif_bytes)
        image.close()


# This is the function that allows us to pass command line arguments to the
# rest of the script
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('file', nargs='+', help='path to the file')
    args_namespace = parser.parse_args()
    args = vars(args_namespace)['file']
    main(args)
