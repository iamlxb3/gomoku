def convert_number_to_one_hot_list(index, length):
    new_list = [0 for x in range(length)]
    new_list[index] = 1
    return new_list