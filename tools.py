from pymatgen.core import Structure
from pymatgen.symmetry.bandstructure import HighSymmKpath

import re, json, os


# Write POSCAR_test to std POSCAR_test

# def write_POSCAR_with_standard_primitive(POSCAR_input="POSCAR_1", POSCAR_output="POSCAR_1.lobster", symprec=0.01):
#     """
#     writes a POSCAR_1 with the standard primitive cell. This is needed to arrive at the correct kpath
#     Args:
#         POSCAR_input (str): filename of input POSCAR_1
#         POSCAR_output (str): filename of output POSCAR_1
#         symprec (float): precision to find symmetry
#     """
#     structure = Structure.from_file(POSCAR_input)
#     kpath = HighSymmKpath(structure, symprec=symprec)
#     new_structure = kpath.prim
#     new_structure.to(fmt='POSCAR', filename=POSCAR_output)


def get_rg2_structure(poscar_input='POSCAR') -> Structure:

    return Structure.from_file(poscar_input)


def get_rg2_elements(poscar_input='POSCAR'):

    # NB: all the elements should be required in elements_map.json
    _map_name = 'elements_map.json'
    elements_map = []
    elements_list = []

    f = open(poscar_input, 'r')
    contents = f.readlines()
    line = contents[5]
    tmp_list = re.split(r"\s", line)

    for c in tmp_list:
        if c != '':
            elements_list.append(c)

    with open(_map_name, 'r') as f_map:
        e_map = json.load(f_map)

    # #>>>Exception may occur here
    [elements_map.append(e_map[e]) for e in elements_list]

    return elements_map


def get_rg2_number_of_atoms():
    return 0

# write_POSCAR_with_standard_primitive('./POSCAR_test', './si_std_2')


def count(root_dir='out'):
    data_list = []
    sg_list = []

    for i in range(36):
        data_list.append(0)
        sg_list.append(195+i)

    for root, dirs, files in os.walk(root_dir):
        num_files = len(files)
        for file in range(num_files):
            sg_number = int(re.split('-', files[file])[0])
            if sg_number in range(195, 231):
                index = get_index(sg_number)
                data_list[index] += 1

    import matplotlib.pyplot as plt

    plt.bar(sg_list, data_list)
    plt.show()


def get_index(sg_num: int):
    return sg_num - 195


if __name__ == '__main__':
    count()