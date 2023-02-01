import peptides_locator as pl


def main():
    # load the dictionary
    tx_dict = pl.txdict('tx_dic.pkl').tx_dict

    # put in a transcript
    tx = 'ENST00000379328'
    x = tx_dict[tx]
    print(f'The length of this tx is {len(x)}')

    # rotate the transcript a base forward and backward. Output is a list.
    rotation_tx = pl.rotationTx(tx=x).get_rotationTx()

    # translate the rotated transcripts. Output is a dictionary with three keys ('normal', 'backward', 'forward').
    rotation_aas = pl.translation(txs=rotation_tx).get_rotationAA()

    peptide = 'ATLQRSSLW'

    # get the peptide position in the transcript
    # the peptide_to_tx method returns a dict, where the keys are "normal", "forward", and "backward".
    # The values are the corresponding position of the peptide in the tx.
    peptide_positions = pl.peptide_to_tx(translations=rotation_aas, peptide=peptide).get_positions()

    for key in peptide_positions:
        list_to_r = [tx, peptide_positions[key][0], peptide_positions[key][1] - peptide_positions[key][0]]
        print(list_to_r)

        output = pl.tx_to_genome(list_to_r=list_to_r).get_gn_coordinate()
        print(output)


if __name__ == '__main__':
    main()