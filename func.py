list = [[3, 3, 0], [0, 3, 3]]
#list = [[6, 6, 6, 6]]
#list = [[7, 7], [7, 7]]
list =  [[6, 6, 6, 6]]
print(list)
print(f" высота = {len(list)}  ширина = {len(list[0])}")
for index, row in enumerate(list):
    print(f"Index: {index}, Row: {row}")
    print(len(row))


# Возвращает повернутую фигуру
list2 = [ [ list[y][x] for y in range(len(list)) ] for x in range(len(list[0]) - 1, -1, -1) ]
print(list2)
print(f" высота = {len(list2)}  ширина = {len(list2[0])}")
