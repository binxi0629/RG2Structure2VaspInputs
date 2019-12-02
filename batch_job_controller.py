import json, os

_root_path = '/home/bxi/RG2_gen'
# last_stop = 0
_default_data_info_file = 'rg2_data_info_dict.json'


def submit_batch_jobs_by_num(number_jobs=20, last_stop=0):
    with open(_default_data_info_file, 'r') as f:
        rg2_info = json.load(f)
        data_map = rg2_info['map']
        structure_info = rg2_info['structure_info']

    job_list = []
    count = 0
    start_index = last_stop + 1
    i = start_index

    while count < number_jobs:

        job = data_map[i-1]
        job_name = job[0]
        job_rg2_id = job[1]

        if structure_info[job_name]['state'] is 'W':
            shell_script_path = os.path.join(_root_path, structure_info[job_name]['parent_path'])
            shell_script = 'relax.sh'
            # print(shell_script_path)
            # os.system(f'cd {shell_script_path}')

            os.system(f'cd {shell_script_path} && qsub -N {job_rg2_id} {shell_script} && cd -')
            # os.system(f'qsub -N {job_rg2_id} {shell_script}')
            # os.system('cd -')
            count += 1
            job_list.append(job_rg2_id)

        i += 1

    print(f'{number_jobs} jobs successfully submitted, job list:')
    print(job_list)


def main():
    submit_batch_jobs_by_num(number_jobs=10, last_stop=10)


if __name__ == '__main__':
    main()