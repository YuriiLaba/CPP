from concurrent.futures import ThreadPoolExecutor, as_completed
from string import punctuation

'''
if __name__ == "__main__":
    pool = ThreadPoolExecutor(1)
    future = pool.submit(f, 1)
    future1 = pool.submit(f, 2)
    print(future.done())
    print(future1.done())
    print(future.result())
    print(future1.result())
'''

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


def words_counting(words_list, word_counter):

    local_dict = {}
    for word in words_list:
        if word not in local_dict:
            local_dict[word] = 1
        else:
            local_dict[word] =+ 1

    return local_dict


input_list = read_file('text.txt')
threads = 3
avg = len(input_list) / threads
last = 0
word_counter = {}
results = []

with ThreadPoolExecutor(max_workers=5) as pool:
    while last < len(input_list):
        results.append(pool.submit(words_counting, input_list[int(last):int(last + avg)], word_counter))
        last += avg

    for future in results:
        for word in future.result().keys():
            if word in word_counter.keys():
                word_counter[word] += future.result()[word]

            else:
                word_counter[word] = future.result()[word]


write_file(word_counter, 'result.txt')