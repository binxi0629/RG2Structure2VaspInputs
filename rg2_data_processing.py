import os, re, json
from shutil import copyfile

import structure_from_rg2


def create_cubic_dir():
    # NB: noly run once at the very beigining
    root_name = 'rg2_cubic'
    os.mkdir(root_name)

    for i in range(195, 231):
        subdir_path = 'sg_'+str(i)
        path = os.path.join(root_name, subdir_path)
        os.mkdir(path)


def split_data_info(file_name):
    split = re.split('-', file_name)
    sg = split[0]
    num_atoms = int(split[2])
    elements = split[3]

    return sg, num_atoms, elements


def data_processing(root_dir='out'):
    # NB: noly run once at the very beigining

    _root_path = 'rg2_cubic'
    data_dict = {}
    data_info ={}
    rg2_id = 1
    invalid_count = 0
    for i in range(195, 231):
        data_dict[i] = 0

    for root, dirs, files in os.walk(root_dir):
        num_files = len(files)
        for file in range(num_files):

            sg, num_atoms, elements = split_data_info(files[file])

            invalid_count += 1 if num_atoms > 130 else 0
            sg_number = int(sg)

            if sg_number in range(195, 231):
                sg_dir = f'sg_{sg_number}'
                sub_path_name = f'rg2_{rg2_id}'
                os.mkdir(os.path.join(_root_path, sg_dir, sub_path_name))

                target_file_name = f'rg2_raw_data_{rg2_id}.vasp'
                dest_path = os.path.join(_root_path, sg_dir, sub_path_name, target_file_name)

                copyfile(os.path.join(root_dir, files[file]), dest_path)

                data_info[files[file]] = [dest_path, rg2_id, sg_number]
                data_dict[sg_number] += 1

                print(f'\r\tSucessfully copied: {rg2_id}|{num_files}', end='')
                rg2_id += 1

    with open('rg2_data_info_dict.json', 'w') as f:
        json.dump(data_info, f, indent=2)
    print('\nSuccessfully saved rg2_data_info_dict.json!')
    print(data_dict)
    print(invalid_count)
    pass


def gen_vaspinputs(root_dir='rg2_cubic'):

    count = 1

    with open('rg2_data_info_dict.json', 'r') as f:
        data_info = json.load(f)

    for this_datum in data_info:
        file_path = data_info[this_datum][0]
        rg2_id = data_info[this_datum][1]
        sg_number = data_info[this_datum][2]
        # root_path = re.split('raw_data', file_path)[0]
        # print(file_path)
        rg2_data = structure_from_rg2.RG2Structure(rg2_id=rg2_id, poscar_input=file_path, sg_number=sg_number)
        rg2_data.write_poscar_with_standard_primitive()
        rg2_data.write_incar(relax=True)
        rg2_data.write_kpoints(number_of_kps=9)
        rg2_data.write_potcar()

        print(f"\rAutogenerate Vasp Inputs, finished:    {count}|521", end='')
        count += 1


def main():

    create_cubic_dir()
    data_processing()
    gen_vaspinputs()


if __name__ == '__main__':
        main()
