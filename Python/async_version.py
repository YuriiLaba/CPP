import asyncio
import time
import functools
from string import punctuation

def read_file(file_name):
    words_list = []
    for line in open(file_name, 'r'):
        for word in line.translate(line.maketrans("", "", punctuation)).lower().split():
            words_list.append(word)

    return words_list

def list_divider(list_of_words, parts):
    avg = len(list_of_words) / parts
    result = []
    last = 0

    while last < len(list_of_words):
        result.append(list_of_words[int(last):int(last + avg)])
        last += avg

    return result

async def words_counting(words_list, word_counter):

    local_dict = {}
    for word in words_list:
        if word not in local_dict:
            local_dict[word] = 1
        else:
            local_dict[word] =+ 1

    for i in local_dict.keys():
        if i in word_counter.keys():
            word_counter[i] += local_dict[i]

        else:
            word_counter[i] = local_dict[i]

    return word_counter


def print_result(word_counter):
    for (word, occurance) in word_counter.items():
        print('{:15} {:3}\n'.format(word, occurance))


number_of_threads = 4
input_list = list_divider(read_file('text1.txt'), number_of_threads)
word_counter = {}


if __name__ == "__main__":
    start = time.time()

    loop = asyncio.get_event_loop()
    temp_futures = {asyncio.ensure_future(words_counting(part_of_list, word_counter)): part_of_list for part_of_list in input_list}
    for fr in temp_futures:
        fr.add_done_callback(functools.partial(print_result, word_counter=temp_futures[fr]))

    loop.run_until_complete(asyncio.wait(list(temp_futures.keys())))

    loop.close()
    print("Got {} temps in {} seconds".format(len(input_list), time.time() - start))

