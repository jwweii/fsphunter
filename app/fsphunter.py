import sys
import peptides_locator as pl


def main():

    # load the dictionary
    tx_dict = pl.txdict('tx_dic.pkl').tx_dict

    # put in a transcript
    tx = sys.argv[1]
    x = tx_dict[tx]
    print(f'The length of this tx is {len(x)}')

    # rotate the transcript a base forward and backward. Output is a list.
    rotation_tx = pl.rotationTx(tx=x).get_rotationTx()

    # translate the rotated transcripts. Output is a dictionary with three keys ('normal', 'backward', 'forward').
    rotation_aas = pl.translation(txs=rotation_tx).get_rotationAA()

    peptide = sys.argv[2]

    # get the peptide position in the transcript
    # the peptide_to_tx method returns a dict, where the keys are "normal", "forward", and "backward".
    # The values are the corresponding position of the peptide in the tx.
    pep_positions = pl.peptide_to_tx(translations=rotation_aas, peptide=peptide).get_positions()

    # to get the genome coordinate:
    # first, make the tx, start position of the peptide, and width to a list.
    # second, pass the list to the tx_to_genome method to get the output.
    # The output is a list, where elements are integers presented as strings.
    for key in pep_positions:
        width = pep_positions[key][1] - pep_positions[key][0]
        list_to_r = [tx, pep_positions[key][0], width]
        print(f'The peptide is at a {key} tx from {pep_positions[key][0]} to {pep_positions[key][1]}')

        output = pl.tx_to_genome(list_to_r=list_to_r).get_gn_coordinate()
        gn_cor = [int(i) for i in output]
        print(f'The genome coordinate is at chr{gn_cor[0]} from {gn_cor[1]} to {gn_cor[1] + width} ')


if __name__ == '__main__':
    main()
