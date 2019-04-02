# USAGE
# python sendLine.py -u <userid> -t "Hello, World"
#
# HELP
# python sendLine.py -h

# import the necessary packages
from __future__ import print_function
from config import main_config as config
from utils import LINENotifier
import argparse
import sys

# construct the argument parse and parse the arguments
# sample1:
# ap.add_argument("-p", "--prefix", type=str, default="image",
#        help="output filename prefix")
# sample2:
# ap.add_argument("-o", "--output", required=True,
#       help="path to output directory to store augmentation examples")

ap = argparse.ArgumentParser()
ap.add_argument("-u", "--userid", help="LINE userid")
ap.add_argument("-g", "--groupid", help="LINE groupid")
ap.add_argument("-t", "--text", help="Message to send")
ap.add_argument("-i", "--image", help="Image to send")
args = vars(ap.parse_args())

if args["userid"] is None and args["groupid"] is None:
	ap.print_help()
	sys.exit(1)

uid = args["userid"]
gid = args["groupid"]
txt = args["text"]
img = args["image"]

ln = LINENotifier(config)

if img is not None:
	if uid is not None:
		ln.sendPush(img, uid, 'IMG')

	if gid is not None:
		ln.sendPush(img, gid, 'IMG')

if txt is not None:
	if uid is not None:
		ln.sendPush(txt, uid, 'TXT')

	if gid is not None:
		ln.sendPush(txt, gid, 'TXT')

