import json
import os
import re, subprocess

_ROOT_PATH = '/home/bxi/RG2_gen'  # <<<<<<
_rg2_data_info_dict_name = 'rg2_data_info_dict.json'
_file_name_format = 'rg2_raw_data_'  # rg2_raw_data_<rg2-id>.json

# >>>> rg2_data_info_dict.json
# 'W': Waiting for running
# 'Q: Queuing
# 'R: Relaxing
# 'BS': Calculating the Band Structure
# 'ERROR': Errors occur
# 'F': Finished successfully


def get_file_name():
    return str(subprocess.check_output('ls | grep .vasp', shell=True))


def check_current_state(file_name='tmp') -> str:
    if os.path.isfile(file_name):
        with open(file_name, 'r') as f:
            current_state = f.readline()
        return current_state
    else:
        return 'W'


def get_rg2_id():
    file_name = get_file_name()
    tmp_name = re.split(_file_name_format, file_name)[1]
    rg2_id = re.split('.vasp', tmp_name)[0]  # string
    return rg2_id


if __name__ == '__main__':
    state = check_current_state()
    _rg2_data_info_dict_path = os.path.join(_ROOT_PATH, _rg2_data_info_dict_name)
    this_rg2_id = get_rg2_id()

    with open(_rg2_data_info_dict_path, 'r+') as df:
        data = json.load(df)

        total_map = data['map']
        tmp_array = total_map[this_rg2_id-1]
        if this_rg2_id == str(tmp_array[1]):
            this_file_name = tmp_array[0]
        else:
            for each_array in total_map:
                if this_rg2_id == str(each_array[1]):
                    this_file_name = each_array[0]

        data[this_file_name]['state'] = state
        df.write(json.dumps(data))
