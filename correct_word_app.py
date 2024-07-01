import streamlit as st


def read_file(path_file):
    with open(path_file, 'r') as file:
        file = file.readlines()

    word = sorted(set([line.strip().lower() for line in file]))

    return word


def levenshtien_distance(str1, str2):
    # create matrix
    matrix = [[0 for _ in range(len(str2) + 1)] for _ in range(len(str1) + 1)]

    for i in range(len(str2) + 1):
        matrix[0][i] = i

    for i in range(len(str1) + 1):
        matrix[i][0] = i

    for i in range(1, len(str1) + 1):
        for j in range(1, len(str2) + 1):
            if str1[i-1] == str2[j-1]:
                matrix[i][j] = matrix[i-1][j-1]

            else:
                delete = matrix[i-1][j] + 1
                insert = matrix[i][j-1] + 1
                sub = matrix[i-1][j-1] + 1
                matrix[i][j] = min(delete, insert, sub)
    return matrix[len(str1)][len(str2)]


def main():
    st.title("Word Correction using Levenshtein Distance")
    input_word = st.text_input('Word')

    if st.button("compute"):
        leven_distance = dict()
        vocas = read_file("data/vocab.txt")
        for voca in vocas:
            leven_distance[voca] = levenshtien_distance(input_word, voca)
        print(leven_distance.items())
        sorted_distance = dict(
            sorted(leven_distance.items(), key=lambda item: item[1]))

        correct_word = list(sorted_distance.keys())[0]

        st.write('Correct word : ', correct_word)

        col1, col2 = st.columns(2)
        col1.write('Vocabulary: ')
        col1.write(vocas)

        col2.write('Distance:')
        col2.write(sorted_distance)


if __name__ == "__main__":
    main()
