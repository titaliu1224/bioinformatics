from flask import Flask,render_template, request
import os, matplotlib

app = Flask(__name__)
SAVE_PATH = "/tmp"
sequences = []
sequences_file = None
image_format = ''

@app.route('/')
def webSite():
    return render_template('index.html')

@app.route('/generate_logo', methods=['GET', 'POST'])
def generate_logo():
    if request.method == 'POST':
        # delete old file (no need in vercel)
        # for filename in os.listdir(SAVE_PATH): 
        #     file_path = os.path.join(SAVE_PATH, filename)
        #     os.remove(file_path)

        # get input from form
        global sequences, sequences_file, image_format
        sequences_input = request.form['sequences-input']
        sequences = sequences_input.split('\r\n')
        sequences_file = request.files['sequences-file']
        image_format = request.form['image-format']
        print(sequences, sequences_file, image_format)

        # save sequences file
        if sequences_file:
            # save new file
            file_path = os.path.join(SAVE_PATH, 'sequences.txt')
            sequences_file.save(file_path)

            # read sequences file
            with open(file_path, 'r') as file:
                sequences_input = file.read()
                sequences = sequences_input.split('\n')

        # generate logo
        matplotlib.use('agg') # 因為在 flask 中使用，所以要加這行
        visualize_sequence_logo(sequences, SAVE_PATH, image_format)

        sequence_length = max([len(sequence) for sequence in sequences])
        print(sequences_input)
        return render_template('logo.html', logo_img = os.path.join(save_path, 'logo.' + image_format), sequence_number = len(sequences), sequence_length = sequence_length, sequences_input = str(sequences_input))
    else:
        return render_template('index.html')

def getInputData():
    global sequences, image_format
    return sequences, image_format

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

if __name__ == '__main__':
    app.run()
