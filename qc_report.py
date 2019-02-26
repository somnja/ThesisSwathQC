#! /usr/bin/env python

import argparse

def run(args):
    from Bio import SeqIO

    #args.input

    # make fastq
    with open(fa_path, "r") as fasta, open(fq_path, "w") as fastq:
        for record in SeqIO.parse(fasta, "fasta"):
            record.letter_annotations["phred_quality"] = [40] * len(record)
            SeqIO.write(record, fastq, "fastq")


def main():
    # create argument parser
    parser=argparse.ArgumentParser(description="Create HTML report for Swatchworkflow, pyprophet and TRIC output")
    # add arguments
    # add up to three inout files: tsv from pyprophet (merged.tsv)
    #                              tsv from TRIC: (aligned.tsv)
    #                              json from OpenSwathWorkflow -out_qc
    parser.add_argument('-i', "--in",help="input in .tsv or json format" , dest='input', type=str, nargs='+')
    parser.add_argument('-o', "--out",help="output destination", dest="output", type=str, required=False)

    parser.add_argument('-l', '--library', help='library file in tsv format, not pqp', dest='lib', type=str, required=False)

    parser.add_argument('-s', '--species', help='spiecies tags in library?', dest='species', type=str, nargs='+', required=False)

    parser.set_defaults(func=run)
    args=parser.parse_args()
    args.func(args)


if __name__=="__main__":
    main()
