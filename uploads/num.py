list_a = [5, 2, 9, 1, 7]
largest = list_a[0]
smallest = list_a[0]
for num in list_a:
    if num > largest:
        largest = num
    elif num < smallest:
        smallest = num
print("Largest number:", largest)
print("Smallest number:", smallest)
