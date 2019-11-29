import json
import os
import re, subprocess

_ROOT_PATH = '/home/bxi/RG2_gen'  # <<<<<<
_rg2_data_info_dict_name = 'rg2_data_info_dict.json'

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


if __name__ == '__main__':
    state = check_current_state()
    _rg2_data_info_dict_path = os.path.join(_ROOT_PATH, _rg2_data_info_dict_name)
    this_file_name = get_file_name()

    with open(_rg2_data_info_dict_path, 'r+') as df:
        data = json.load(df)

        tmp = data[this_file_name]['state']
        data[this_file_name]['state'] = state

        df.write(json.dumps(data))
