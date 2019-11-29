import xml.etree.ElementTree as ElementTree
import numpy, json, re, os
import subprocess
from typing import List, Dict, Union

_ROOT_PATH = '~/Work_Use'  # <<<<<< Modify each time one changes the environment
_rg2_data_info_dict_name = 'rg2_data_info_dict.json'
_file_name_format = 'rg2_raw_data_'  # rg2_raw_data_<rg2-id>.json


def get_vasprun_root(vasprun_path: str) -> ElementTree:
    tree = ElementTree.parse(vasprun_path)
    return tree.getroot()


def get_kpoints(vasprun_root: ElementTree) -> numpy.ndarray:
    return numpy.asarray([kpoint.text.split() for kpoint in vasprun_root.find("kpoints/varray")], float)


def get_eigenvalues(vasprun_root: ElementTree) -> numpy.ndarray:
    eigenvalues_tree_list = vasprun_root.findall("calculation/eigenvalues/array/set/set/set")
    return numpy.asarray([[eigenvalues.text.split()[0]
                           for eigenvalues in eigenvalues_tree]
                          for eigenvalues_tree in eigenvalues_tree_list], float)


def get_kpoints_labels(kpoints_path: str) -> List[Dict[str, Union[int, str]]]:
    with open(kpoints_path, "r") as file:
        kpoints = numpy.array([line.split() for line in file])
    division = int(kpoints[1][0])
    kpoints = kpoints[4:]
    labels = [kpoint[4] for kpoint in kpoints if kpoint]
    branches = []
    for i in range(int(len(labels) / 2)):
        branches.append({
            "start_index": i * division,
            "end_index": (i + 1) * division - 1,
            "name": labels[i * 2] + "-" + labels[i * 2 + 1]
        })
    return branches


def get_file_name():

    return str(subprocess.check_output('ls | grep .vasp', shell=True))


def get_rg2_id():
    this_file_name = get_file_name()
    tmp = re.split(_file_name_format, this_file_name)[1]
    rg2_id = re.split('.vasp', tmp)[0]  # string
    return rg2_id


def wirte2json():

    _default_dir = '..'
    rg2_id = get_rg2_id()
    file_name = f'{_file_name_format}{rg2_id}.json'

    vasprun_root = get_vasprun_root("vasprun.xml")
    eigenvalues = get_eigenvalues(vasprun_root)
    kpoints = get_kpoints(vasprun_root)
    kpoints_labels = get_kpoints_labels("KPOINTS")
    # print(eigenvalues.shape)
    # print(kpoints.shape)
    # print(len(kpoints_labels))
    # print(eigenvalues.transpose())
    # print(kpoints)
    # print(kpoints_labels)

    data = {}
    data['band'] = {}
    data['rg2_id'] = rg2_id
    data['band']['bands'] = eigenvalues.transpose()
    data['band']['branches'] = kpoints_labels
    data['band']['kpoints'] = kpoints
    with open(os.path.join(_default_dir, file_name), 'w') as f:
        json.dump(data, f, indent=2, cls=NumpyEncoder)


def main():
    wirte2json()


class NumpyEncoder(json.JSONEncoder):
    """
        to solve Error: NumPy array is not JSON serializable
        see: https://stackoverflow.com/questions/26646362/numpy-array-is-not-json-serializable
    """
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


if __name__ == '__main__':
    main()
