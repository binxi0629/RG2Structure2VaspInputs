import json
import os
import re, subprocess

_ROOT_PATH = '~/RG2_gen'  # <<<<<<
_rg2_data_info_dict_name = 'rg2_data_info_dict.json'
_file_name_format = 'rg2_raw_data_'  # rg2_raw_data_<rg2-id>.json

# >>>> rg2_data_info_dict.json
# 'W': Waiting for running
# 'Q: Queuing
# 'R: Relaxing
# 'BS': Calculating the Band Structure
# 'ERROR': Errors occur
# 'F': Finished successfully


def get_file_name() -> str:

    try:
        return str(subprocess.check_output('ls | grep .vasp', shell=True))
    except Exception:
        return str(subprocess.check_output('ls ../ | grep .vasp', shell=True))


def check_current_state(file_name='tmp') -> str:

    def read_state_from_file(fun_file_name='tmp') -> str:
        with open(fun_file_name, 'r') as file:
            this_line = file.readline()
            current_state = re.split('\n', this_line)[0]
        return current_state

    if os.path.isfile(file_name):
        return read_state_from_file(file_name)
    elif os.path.isfile(f'../{file_name}'):
        file_name = f'../{file_name}'
        return read_state_from_file(file_name)
    else:
        return 'W'


def get_rg2_id() -> str:
    file_name = get_file_name()
    tmp_name = re.split(_file_name_format, file_name)[1]
    rg2_id = re.split('.vasp', tmp_name)[0]  # string
    return rg2_id


if __name__ == '__main__':
    state = check_current_state()
    _rg2_data_info_dict_path = os.path.join(_ROOT_PATH, _rg2_data_info_dict_name)
    this_rg2_id = get_rg2_id()

    # print(state)
    with open(_rg2_data_info_dict_path, 'r') as df:
        data = json.load(df)

    data1 = data
    total_map = data1['map']

    tmp_array = total_map[int(this_rg2_id)-1]
    if this_rg2_id == str(tmp_array[1]):
        this_file_name = tmp_array[0]
    else:
        for each_array in total_map:
            if this_rg2_id == str(each_array[1]):
                this_file_name = each_array[0]

    with open(_rg2_data_info_dict_path, 'w') as f:
        data1['structure_info'][this_file_name]['state'] = state
        json.dump(data1, f, indent=2)
