import logomaker
import matplotlib.pyplot as plt
import os, matplotlib
import numpy as np
# from Bio import SeqIO

def visualize_sequence_logo(sequences, save_path=None, image_format=None, show_img=False):
    # 產生 logo
    matrix = logomaker.alignment_to_matrix(sequences, to_type='counts')
    row_sums = np.sum(matrix, axis=1)
    frequency_matrix = matrix / np.array(row_sums)[:, np.newaxis].astype(float)
    logo = logomaker.Logo(frequency_matrix, color_scheme='skylign_protein')
    logo.style_spines(visible=False)
    logo.style_spines(spines=['left', 'bottom'], visible=True)
    logo.style_xticks(rotation=0, fmt='%d', anchor=0)
    plt.ylabel("Frequency")
    #logo.ax.set_ylim(0, len(sequences))

    # 直接顯示圖片，debug用
    if show_img: 
        plt.show()
        return
    
    # 儲存 logo
    plt_path = os.path.join(save_path, 'logo.' + image_format)
    plt.savefig(plt_path)
    print("saved image: ", plt_path)

# sequences = []
# fasta_file = "test.fasta"
# for record in SeqIO.parse(fasta_file, "fasta"):
#     sequences.append(str(record.seq))
# visualize_sequence_logo(sequences)

if __name__ == '__main__':
    sequence = ['GDLGAGKTT', 'GDLGAGKTT', 'GPLGAGKTS', 'GDLGAGKTS', 'GDLGAGKTT', 'GDLGAGKTT', 'GEVGSGKTT', 'GELGAGKTT', 'GDLGAGKTT', 'GNLGAGKTT', 'GELGAGKTT', 'GTLGAGKTT', 'GDLGAGKTT', 'GDLGAGKTT', 'GDLGAGKTT', 'GDLGAGKTT', 'GDLGAGKTT']
    visualize_sequence_logo(sequence)
