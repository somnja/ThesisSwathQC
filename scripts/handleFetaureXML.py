import pyopenms
import argparse
import sys

parser = argparse.ArgumentParser(description="Create HTML report for Swatchworkflow, pyprophet and output")
parser.add_argument('-in', help="featureXML file", dest='infile')
parser.add_argument('-traml', help="library in traml fromat", dest='library')
# parse arguments

args = parser.parse_args(sys.argv[1:])
infile = args.infile.encode('utf-8')
lib = args.library  #.encode('utf-8')

features = pyopenms.FeatureMap()
fh = pyopenms.FileHandler()
fh.loadFeatures(infile, features)

keys = []

features[0].getKeys(keys)
header = [
    "transition_group_id",
    "run_id",
    "filename",
    "RT",
    "id",
    "Sequence",
    "FullPeptideName",
    "Charge",
    "m/z",
    "Intensity",
    "ProteinName",
    "decoy"]
keys = [i.decode('utf-8') for i in keys]
header.extend(keys)
print(header)

