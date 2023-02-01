import re
import pickle
from operator import mul
import json
import subprocess


AA = {'TTT': 'F', 'TTC': 'F', 'TTA': 'L', 'TTG': 'L', 'TCT':'S', 'TCC':'S', 'TCA': 'S', 'TCG': 'S', 'TAT': 'Y',
      'TAC': 'Y', 'TAA': '0', 'TAG': '0', 'TGT': 'C', 'TGC': 'C', 'TGA': '0', 'TGG': 'W', 'CTT': 'L',
      'CTC': 'L', 'CTA': 'L', 'CTG': 'L', 'CCT': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P', 'CAT': 'H', 'CAC': 'H',
      'CAA': 'Q', 'CAG': 'Q', 'CGT': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R', 'ATT': 'I', 'ATC': 'I', 'ATA': 'I',
      'ATG': 'M', 'ACT': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T', 'AAT': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
      'AGT': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R', 'GTT': 'V', 'GTC': 'V', 'GTA': 'V', 'GTG': 'V', 'GCT': 'A',
      'GCC': 'A', 'GCA': 'A', 'GCG': 'A', 'GAT': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E', 'GGT': 'G', 'GGC': 'G',
      'GGA': 'G', 'GGG': 'G'}


# load the tx dictionary
class txdict:
    def __init__(self, file_name):
        with open(file_name, 'rb') as f:
            self.tx_dict = pickle.load(f)


# get rotation txs
class rotationTx:
    def __init__(self, tx):
        self.tx = tx
        self.rotation1 = self.tx[0]
        for i in range(len(self.tx)):
            self.rotation1 += self.tx[i]  # backward

        self.rotation2 = self.tx[1]
        for i in range(len(self.tx) - 2):
            self.rotation2 += self.tx[i + 2]  # forward

    def get_rotationTx(self):
        return self.tx, self.rotation1, self.rotation2


# translation
class translation:
    def __init__(self, txs):
        self.txs = txs
        self.rotation_aa = []
        for tx in self.txs:
            i = 0
            aaseq = ''
            while i < len(tx):
                codon = tx[i:i+3]
                i = i + 3
                if len(codon) == 3:
                    aaseq += AA[codon]
            self.rotation_aa.append(aaseq)
        self.aa_seq = {'normal': self.rotation_aa[0], 'backward': self.rotation_aa[1], 'forward': self.rotation_aa[2]}

    def get_rotationAA(self):
        return self.aa_seq


class peptide_to_tx:
    def __init__(self, translations, peptide):
        self.translation_tx = translations
        self.peptide = peptide
        self.pepre = re.compile(fr"{self.peptide}")
        self.positions = {}
        for key in self.translation_tx:
            results = re.finditer(self.pepre, self.translation_tx[key])
            if results:
                for result in results:
                    position = tuple(map(mul, (result.start(), result.end()), (3, 3)))
                    if key == 'forward':
                        position = tuple(map(lambda i, j: i + j, position, (1, 1)))
                    elif key == 'backward':
                        position = tuple(map(lambda i, j: i - j, position, (1, 1)))
                    if key in self.positions:
                        self.positions[key] += position
                    else:
                        self.positions[key] = position

    def get_positions(self):
        return self.positions


class tx_to_genome:
    def __init__(self, list_to_r):
        self.list = list_to_r

        # Convert the list to a json string
        json_str = json.dumps(self.list)

        # Write the json string to a file
        with open("input.json", "w") as f:
            f.write(json_str + '\n')

        # Use the subprocess module to call the R script and pass the input file as an argument
        result = subprocess.run(["Rscript", "get_genome_coordinate.R", "input.json"], capture_output=True, text=True)
        r_output = str(result.stdout)

        gnre = re.compile(r'\d+')
        self.output = gnre.findall(r_output)
        # print(result.returncode)
        # print(result.stdout)
        # print(result.stderr)

    def get_gn_coordinate(self):
        return self.output
