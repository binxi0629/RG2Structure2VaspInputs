from pymatgen.core import Structure
from pymatgen.symmetry.bandstructure import HighSymmKpath
from pymatgen.io.vasp.inputs import Incar, Poscar, Potcar, Kpoints, VaspInput

import tools
import os,json
from shutil import copyfile


class RG2Structure:

    def __init__(self, rg2_id, sg_number, poscar_input='POSCAR', fmt='POSCAR'):

        # initialize the required info
        self.rg2_structure = tools.get_rg2_structure(poscar_input)
        self.elements = tools.get_rg2_elements(poscar_input)
        self.rg2_id = rg2_id
        self.sg_number = sg_number
        # self.number_of_atoms = tools.get_rg2_number_of_atoms()
        self.path_name = poscar_input

        # default path to save vaspinputs files:
        # ./rg2_cubic/sg_<spacegroup_number>/rg2_<rg2_id>/rg2_raw_data_<rg2_id>.vasp
        self._json_file_name = f'rg2_raw_data_{self.rg2_id}.json'

        self._save_to_path = os.path.join('rg2_cubic', f'sg_{self.sg_number}', f'rg2_{self.rg2_id}')
        self.dict = {}

    def record_rg2_structure_info(self):
        pass

    def write_poscar_with_standard_primitive(self, poscar_output="POSCAR", symprec=0.01):
        """
        writes a POSCAR file with the standard primitive cell. This is needed to arrive at the correct kpath
        Args:
            poscar_output (str): filename of output POSCAR_1
            symprec (float): precision to find symmetry
        """

        kpath = HighSymmKpath(self.rg2_structure, symprec=symprec)
        new_structure = kpath.prim
        poscar_file_name = os.path.join(self._save_to_path, poscar_output)
        new_structure.to(fmt='POSCAR', filename=poscar_file_name)

    def write_incar(self, relax: bool, incar_config: dict = {}):
        """
        writes an INCAR file with some default settings, and also can modify the tags
        :param relax:
                --True: writes an INCAR for relax use
                --False: wirtes an INCAR only supporting static run
        :param incar_config: customized incar settings
        """

        incar_file_name = os.path.join(self._save_to_path, 'INCAR')

        _default_incar_config = {
            'ALGO': 'ALL',
            'ICHARG': '2',
            'PREC': 'Normal',
            'EDIFF': '1E-5',
            'EDIFFG': '-0.1',
            'ENCUT': '520',
            'ISMEAR': '0',
            'IBRION': '-1',
            'ISIF': '0',
            'NELM': '200',
            'NSW': '0',
            'SIGMA': '0.1',
            'ISYM': '2',
        }
        if relax:
            relax_incar_config = {
                'IBRION': '2',
                'NSW': '100',
                'ISIF': '3',  # only cell will move, the atoms won't move
            }
            _default_incar_config.update(relax_incar_config)

        _default_incar_config.update(incar_config)

        Incar(_default_incar_config).write_file(incar_file_name)

    def write_potcar(self):
        # NEED check if correct
        # TODO:
        # Every time when changing running environment, need uncomment the following two lines
        # os.system('pmg config --add PMG_VASP_PSP_DIR G:/pseudo-potential/')

        potcar_file_name = os.path.join(self._save_to_path, 'POTCAR')
        # Vasp functional set as potpaw_GGA
        Potcar(symbols=self.elements, functional='PW91').write_file(potcar_file_name)

    def write_kpoints(self, number_of_kps: int = 7):
        """
        wirtes a KPOINTS file for relaxiation use
        :param number_of_kps: e.g. 7 7 7
        """
        kpoints_file_name = os. path.join(self._save_to_path, 'KPOINTS')

        with open(kpoints_file_name, 'w') as kps:
            kps.write('KPOINTS file generated automatically\n')
            kps.write('0\n')
            kps.write('Gamma\n')
            kps.write(f'{number_of_kps} {number_of_kps} {number_of_kps}\n')
            kps.write('0 0 0')

    def write_kpoints_along_hs_path(self, divisions=5):
        """
        writes a KPOINTS file for band structure calculation  use
        """
        hs_kpoints_file_name = os.path.join(self._save_to_path, 'KPOINTS')

        structure = Structure.from_file(os.path.join(self._save_to_path, 'POSCAR'))
        kpath = HighSymmKpath(structure)
        kpts = Kpoints.automatic_linemode(divisions=divisions, ibz=kpath)
        kpts.write_file(hs_kpoints_file_name)

    def create_bs_working_dir(self):
        bs_working_dir = os.path.join(self._save_to_path, 'bandStructure')
        os.mkdir(bs_working_dir)

    def copy_scripts_to_working_dir(self, scripts_dir):

        _r_scripts = ['relax.sh', 'check_state.py']
        _bs_scripts = ['bs.sh', 'gen_incar_and_hs_kpoints.py', 'vasprun2json.py']

        working_dir = self._save_to_path
        for r_scripts in _r_scripts:
            copyfile(os.path.join(scripts_dir, r_scripts), os.path.join(working_dir, r_scripts))

        bs_working_dir = os.path.join(self._save_to_path, 'bandStructure')

        for bs_scripts in _bs_scripts:
            copyfile(os.path.join(scripts_dir, bs_scripts), os.path.join(bs_working_dir, bs_scripts))

    def generate_json_file(self):
        working_dir = os.path.join(self._save_to_path, 'bandStructure')
        _json_file_name = f'rg2_raw_data_{str(self.rg2_id)}.json'

        self.dict['rg2_id'] = self.rg2_id

        with open(os.path.join(working_dir, _json_file_name), 'w') as f:
            json.dump(self.dict, f, indent=2)
