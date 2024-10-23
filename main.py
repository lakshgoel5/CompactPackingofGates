from visualize_gates import draw_gate_packing

def make_two_new_empty_spaces(L, index, key , w, h, bounding_box):
    temp_w = L[index][0]
    temp_h = L[index][1]
    (x, y) = (L[index][2], L[index][3])
    gates[key] = (x,y)
    if abs((temp_h * (temp_w - w)) - (w * (temp_h - h))) > abs(
            (temp_w * (temp_h - h)) - (h * (temp_w - w))):
        if (temp_h * temp_w - w) >= (w * temp_h - h):
            smaller_space = (w, temp_h - h,x,y+h)
            larger_space = ( temp_w - w, temp_h,x+w, y)

        else:
            larger_space = ( w, temp_h - h, x, y+h)
            smaller_space = ( temp_w - w, temp_h, x+w, y)
    else:
        if (temp_w * temp_h - h) >= (h * temp_w - w):
            smaller_space = (temp_w - w, h, x+w, y)
            larger_space = (temp_w, temp_h - h, x, y+h)
        else:
            larger_space = (temp_w - w, h, x+w, y)
            smaller_space = (temp_w, temp_h - h, x,y+h)
    i = index+1
    n = len(L)
    while i<n and L[i][0]*L[i][1] > larger_space[0]*larger_space[1]:
        L[i-1]= L[i]
        i+=1
    L[i-1] = larger_space
    L.append(smaller_space)
    i = n-1
    while i>=0 and L[i][0]*L[i][1] < smaller_space[0]*smaller_space[1]:
        L[i+1]= L[i]
        i-=1
    L[i+1] = smaller_space
def add_new_block_up(L,key, width_block, height_block, bounding_box):
    width_reached = bounding_box[0]
    height_reached = bounding_box[1]
    gates[key] = (0, height_reached)
    new_block= (width_reached-width_block, height_block, width_block , height_reached)
    new_block_area= new_block[0]*new_block[1]
    n = len(L)
    i = n-1
    L.append(new_block)
    while i >= 0 and L[i][0]*L[i][1] < new_block_area:
        L[i+1]=L[i]
        i-=1
    L[i+1] = new_block
    bounding_box[1] = height_block+ height_reached

def add_new_block_right(L,key, width_block, height_block, bounding_box):
    width_reached= bounding_box[0]
    height_reached= bounding_box[1]
    gates[key] = (width_reached,0)
    new_block= (width_block, height_reached-height_block, width_reached , height_block)
    new_block_area= new_block[0]*new_block[1]
    n = len(L)
    i = n-1
    L.append(new_block)
    while i >= 0 and L[i][0]*L[i][1] < new_block_area:
        L[i+1]=L[i]
        i-=1
    L[i+1] = new_block
    bounding_box[0] =  width_reached+width_block

def add_new_block (L , key , width_block, height_block , bounding_box):
    width_reached = bounding_box[0]
    height_reached = bounding_box[1]
    width_small = (width_block <= width_reached)
    height_small = (height_block <= height_reached)
    if width_small and height_small:
        if (width_reached-width_block)*height_block < (height_reached-height_block)*width_block:
            add_new_block_up(L,key, width_block, height_block, bounding_box)
        else :
            add_new_block_right(L,key, width_block, height_block, bounding_box)
    elif width_small:
        add_new_block_up(L,key, width_block, height_block, bounding_box)
    else :
        add_new_block_right(L,key, width_block, height_block, bounding_box)
def find_fitting_node ( L, width_block, height_block):
    n = len(L)
    i = n-1
    while i >= 0 :
        if L[i][0] >= width_block and L[i][1] >= height_block :
            return i
        else :
            i -= 1
    if i < 0:
        return -1

gate_dimensions = {}
with open("input.txt", "r") as file:
    lines = file.readlines()
    for line in lines:
        gate_info = line.split()
        if len(gate_info) != 3:
            print(f"Skipping line in dimensions file: {line.strip()}")
            continue
        name = gate_info[0]
        width = int(gate_info[1])
        height = int(gate_info[2])
        gate_dimensions[name] = (width, height)

gate_dimensions = dict(sorted(gate_dimensions.items(), key=lambda item: max(item[1][1],item[1][0]), reverse=True))


gates={}
key = list(gate_dimensions.keys())[0]
L = []
L.append((gate_dimensions[key][0],gate_dimensions[key][1],0,0))
bounding_box = [gate_dimensions[key][0], gate_dimensions[key][1]]
for key in gate_dimensions:
    w = gate_dimensions[key][0]
    h = gate_dimensions[key][1]
    fit_index= find_fitting_node(L , w, h)
    if fit_index == -1:
        add_new_block (L , key ,w , h, bounding_box)
    else :
        make_two_new_empty_spaces(L, fit_index , key , w, h, bounding_box )
gates = dict(sorted(gates.items(), key=lambda item: int(item[0][1:])))
with open("output.txt", "w") as file:
    file.write("bounding_box " + str(bounding_box[0]) + " " + str(bounding_box[1]) + "\n")
    for key in gates:
        file.write(key + " " + str(gates[key][0]) + " " + str(gates[key][1]) + "\n")

total_area=0
for key in gates:
    total_area+=gate_dimensions[key][1]*gate_dimensions[key][0]
