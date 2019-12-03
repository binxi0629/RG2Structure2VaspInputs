import os, re, json, random
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
    # NB: noly run once at the very beginning

    # >>>> rg2_data_info_dict.json
    # 'W': Waiting for running
    # 'R: Relaxing
    # 'BS': Calculating the Band Structure
    # 'ERROR': Errors occur
    # 'F': Finished successfully

    _root_path = 'rg2_cubic'
    # initialize
    data_dict = {}
    data_info = {}
    target_sg_dict = {
        195: 0, 196: 0, 199: 0, 200: 0, 201: 0, 202: 0, 203: 0, 204: 0,
        206: 0, 207: 0, 208: 0, 209: 0, 210: 0, 212: 0, 213: 0, 214: 0,
        215: 0, 218: 0, 219: 0, 220: 0, 222: 0, 224: 0, 226: 0, 228: 0,
        229: 0, 230: 0
    }
    num_uppper_bound = 100
    data_info['structure_info'] = {}
    name_id_map = []

    rg2_id = 1
    invalid_count = 0
    for i in range(195, 231):
        data_dict[i] = 0

    for root, dirs, files in os.walk(root_dir):
        num_files = len(files)

        # shuffle the directory
        print(f'before: {files}')

        random.shuffle(files)

        print(f'After: {files}')
        for file in range(num_files):

            sg, num_atoms, elements = split_data_info(files[file])

            invalid_count += 1 if num_atoms > 130 else 0
            sg_number = int(sg)

            # if sg_number in range(195, 231):
            if sg_number in target_sg_dict.keys():

                if target_sg_dict[sg_number] < num_uppper_bound:
                    target_sg_dict[sg_number] += 1
                    tmp_array = []

                    sg_dir = f'sg_{sg_number}'
                    sub_path_name = f'rg2_{rg2_id}'
                    os.mkdir(os.path.join(_root_path, sg_dir, sub_path_name))

                    target_file_name = f'rg2_raw_data_{rg2_id}.vasp'
                    dest_path = os.path.join(_root_path, sg_dir, sub_path_name, target_file_name)
                    # dest_path = os.path.join(_root_path, sg_dir, sub_path_name)
                    parent_path = os.path.join(_root_path, sg_dir, sub_path_name)
                    copyfile(os.path.join(root_dir, files[file]), dest_path)

                    data_info['structure_info'][files[file]] = {}
                    data_info['structure_info'][files[file]]['path'] = dest_path
                    data_info['structure_info'][files[file]]['parent_path'] = parent_path
                    data_info['structure_info'][files[file]]['rg_id'] = rg2_id
                    data_info['structure_info'][files[file]]['spacegroup_number'] = sg_number
                    data_info['structure_info'][files[file]]['state'] = 'W'  # W: waiting for running

                    data_dict[sg_number] += 1

                    tmp_array.append(files[file])
                    tmp_array.append(rg2_id)

                    name_id_map.append(tmp_array)

                    print(f'\r\tSucessfully copied: {rg2_id}|{num_files}', end='')
                    rg2_id += 1

    data_info['map'] = name_id_map

    with open('rg2_data_info_dict.json', 'w') as f:
        json.dump(data_info, f, indent=2)
    print('\nSuccessfully saved rg2_data_info_dict.json!')
    print(data_dict)
    print(invalid_count)
    print(target_sg_dict)
    pass


def gen_vaspinputs(root_dir='rg2_cubic', scripts_dir='scripts'):

    count = 1

    with open('rg2_data_info_dict.json', 'r') as f:
        data_info = json.load(f)

    for this_datum in data_info['structure_info']:
        file_path = data_info['structure_info'][this_datum]['path']
        rg2_id = data_info['structure_info'][this_datum]['rg_id']
        sg_number = data_info['structure_info'][this_datum]['spacegroup_number']
        # root_path = re.split('raw_data', file_path)[0]
        # print(file_path)
        rg2_data = structure_from_rg2.RG2Structure(rg2_id=rg2_id,
                                                   poscar_input=file_path,
                                                   sg_number=sg_number)

        rg2_data.write_poscar_with_standard_primitive(poscar_output='POSCAR_prim')  # back up
        rg2_data.write_poscar_with_standard_primitive(poscar_output='POSCAR')
        rg2_data.write_incar(relax=True)
        rg2_data.write_kpoints(number_of_kps=9)
        rg2_data.write_potcar()
        rg2_data.create_bs_working_dir()
        rg2_data.copy_scripts_to_working_dir(scripts_dir=scripts_dir)

        print(f"\rAutogenerate Vasp Inputs, finished:    {count}", end='')
        count += 1


def main():

    create_cubic_dir()
    data_processing()
    gen_vaspinputs()


if __name__ == '__main__':
    main()
