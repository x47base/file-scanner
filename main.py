import os

def scan(path: str = "C:\\", file_type_filter: str = "", array: list = []):
    os.listdir(path)
    
    # Getting all files and directorys of the path with or without file extension filter
    if file_type_filter != "":
        content = [(c, f"{path}\\{c}", os.path.getsize(f"{path}\\{c}")) for c in os.listdir(path) if c.endswith(file_type_filter)]
    else:
        content = [(c, f"{path}\\{c}", os.path.getsize(f"{path}\\{c}")) for c in os.listdir(path)]
    
    # scanning all the directories and adding them to the content array
    for dir in os.listdir(path):
        if os.path.isdir(os.path.join(path, dir)):
            content += scan(f"{path}\\{dir}")       # Recursion
    
    # extending the main array by content array
    array.extend(item for item in content if item not in array)
    
    # returning the results
    return array


def filter(array: list):
    """
    Array Heapsort Filter
    -> filtered by file name
    """
    option = 0 # set to 1 to filter by path
    n = len(array)
    def swap(x: int, y: int):
        """
        Swap Array Argument Positions
        """
        _x, _y = array[x], array[y]
        array[y] = _x
        array[x] = _y
    def heapify(arr: list, i: int, heap_size: int):
        """
        Heapify
        """
        left = 2 * i + 1
        right = 2 * i + 2
        largest = i

        if left < heap_size and arr[left][option] > arr[largest][option]:
            largest = left
        if right < heap_size and arr[right][option] > arr[largest][option]:
            largest = right

        if largest != i:
            swap(i, largest)
            heapify(arr, largest, heap_size)

    def build_max_heap(arr: list):
        """
        Build Max Heap
        """
        for i in range(n // 2 - 1, -1, -1):
            heapify(arr, i, n)

    # run the filter
    build_max_heap(array)
    for i in range(n - 1, 0, -1):
        swap(0, i)
        heapify(array, 0, i)

def export(array: list = [], output_file_path: str = "C:\\files-scan-log.txt"):
    """
    Export the files array to an output file.
    """
    with open(file=output_file_path, mode="w+") as file:
        for i in array: file.write(i[0] + ";"); file.write(i[1] + ";"); file.write(str(i[2])); file.write("\n")

def main():
    try:
        # Get path and extension filter
        path = input("Path: ")
        file_type_filter = input("File Extension Filter (Leave blank for no extension filter): ")
        
        # Scan the files and directories
        results = scan(path = path, file_type_filter = file_type_filter, array = [])
    except PermissionError:
        # Invalid permission, Admin permission possibly required for this path
        print("[ERROR] Invalid permission: Admin permissions are possibly required for this path")
        exit(code=403)
    filter(results)
    export(array=results, output_file_path="C:\\files-scan-log.txt")

if __name__ == "__main__":
    main()
