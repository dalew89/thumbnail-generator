#!/usr/bin/env python
from __future__ import unicode_literals, print_function
import argparse
import ffmpeg
import sys
import os

parser = argparse.ArgumentParser(description='Generate video thumbnail')
parser.add_argument('input_dir', help='Directory that contains the video files')
parser.add_argument('output_dir', help='The directory of the generated thumbnails')
parser.add_argument(
    '--time', type=int, default=0.5, help='Time offset')
parser.add_argument(
    '--width', type=str, default='640x360',
    help='Width of output thumbnail (height automatically determined by aspect ratio)')


def generate_thumbnail(in_filename, out_filename, time, dimensions):
    try:
        (
            ffmpeg
            .input(in_filename, ss=time)
            .filter('scale', dimensions)
            .output(out_filename, vframes=1)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        print(e.stderr.decode(), file=sys.stderr)
        sys.exit(1)


def gen_thumbnails(input_dir, output_dir):
    video_directory = os.listdir(input_dir)
    for video in video_directory:
        generate_thumbnail(os.path.join(input_dir, video), os.path.join(input_dir, (os.path.splitext(video)[0]+".png")),
                           args.time, args.width)


if __name__ == '__main__':
    args = parser.parse_args()
    gen_thumbnails(args.input_dir, args.output_dir)
