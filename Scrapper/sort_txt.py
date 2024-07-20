def sorted_file(file_to_sort, sorted_file_name):
    with open(file_to_sort, 'r') as file:
        # every row is deveded by \n charecter
        rows = file.read().split('\n')

    # Need to seperate the values in columns
    for ind, string in enumerate(rows):
        rows[ind] = string.split(':')

        if rows[ind]:
            for sub_ind, value in enumerate(rows[ind]):
                try:
                    rows[ind][sub_ind] = int(value)
                except ValueError:
                    pass

    rows = rows[:-1]

    # Quick sort algorythm    
    def partition_array(array, low, high):
        pivot = array[low][0]
        i = low+1 # to sotre the vlaues of numbers with values higher than the pivot
        for j in range(low+1, high+1):
            if array[j][0]<=pivot:
                array[i], array[j] = array[j], array[i]
                i+=1
        array[low], array[i-1] = array[i-1], array[low] # Swwapping the pivot to its correct value
        return i-1 # returing the index of the pivot

    def quicksort(array, low, high):
        if low < high:
            pivot_ind = partition_array(array, low, high)
            quicksort(array, low, pivot_ind-1)
            quicksort(array, pivot_ind+1, high)

    quicksort(rows, 0, len(rows)-1)

    # writing the sorted list to a new text file
    with open(sorted_file_name, 'a') as file:
        string = ''
        for row in rows:
            for data in row:
                if type(data) == int:
                    string += str(data)+':'
                else:
                    string += data+':'
            string = string[:-1]
            file.write(string+'\n')  
            string = ''

