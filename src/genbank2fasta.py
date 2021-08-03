import re
import textwrap
import argparse

def genbank_reader(genbank_file):
    with open(genbank_file, 'r') as filin:
        genbank_id = ''
        genbank_dict = {}
        is_seq = False
        assert genbank_file.split('.')[1] in ['fasta', 'faa', 'fna'], "Incorrect input file extension. See genbank2fasta.py --help"
        for line in filin:
            if line[0:9] == 'ACCESSION':
                genbank_id = line.split()[1]
                genbank_dict[genbank_id] = ''
            elif line[0:6] == 'ORIGIN':
                is_seq = True
                continue
            elif line[0:2] == '//':
                is_seq = False
            if is_seq:
                cleaned_line = re.sub(pattern='[0-9]', repl='', string=line.strip()).replace(' ', '').upper()
                genbank_dict[genbank_id] += cleaned_line
        assert len(genbank_id) > 0, "Incorrect format for input file, missing 'ACCESSION' field."
        return genbank_dict

def genbank2fasta(input_genbank, output_fasta='genbank2fasta.fasta'):
    genbank_dict = genbank_reader(input_genbank)
    with open(output_fasta, 'w') as filout:
        for key in genbank_dict:
            filout.write(f">{key}\n")
            filout.write(f'{textwrap.fill(text=genbank_dict[key], width=60)}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--genbank", help='Genbank input file to convert')
    parser.add_argument("-o", "--fasta", help='Fasta output file (valid extensions: .fasta, .faa, .fna)')
    args = parser.parse_args()
    if args.fasta:
        print(f"\nConverting your genbank file into {args.fasta} file...")
        genbank2fasta(args.genbank, output_fasta=args.fasta)
    else:
        print("\nConverting your genbank file into genbank2fasta.fasta file...")
        genbank2fasta(args.genbank)

    print("Done !")