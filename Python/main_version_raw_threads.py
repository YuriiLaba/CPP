from time import time, process_time
from string import punctuation
from collections import Counter
from multiprocessing import Process

def read_file(file_name):
    words_list = []
    for line in open(file_name, 'r'):
        for word in line.translate(line.maketrans("", "", punctuation)).lower().split():
            words_list.append(word)

    return words_list


def write_file(word_counter, file_name):
    with open(file_name, 'w') as file:
        for (word, occurance) in word_counter.items():
            file.write('{:15} {:3}\n'.format(word, occurance))



class WordsCount(Process):
    word_counter = Counter({})

    def __init__(self, words_list, word_counter):
        super().__init__()
        self.words_list = words_list

    def run(self):
        local_dict = Counter({})
        for word in self.words_list:
            if word not in local_dict:
                local_dict[word] = 1
            else:
                local_dict[word] =+ 1

        WordsCount.word_counter += local_dict
        print(WordsCount.word_counter)


def launch_program():
    word_counter = Counter({})
    threads = []
    input_list = read_file('text.txt')
    avg = len(input_list) / 10
    last = 0

    while last < len(input_list):
        threads.append(WordsCount(input_list[int(last):int(last + avg)], word_counter))
        last += avg

    start_time = time()

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print(process_time())

    print('Got {} threads in {} seconds'.format(len(threads), time() - start_time))
    write_file(word_counter, 'result.txt')


launch_program()


