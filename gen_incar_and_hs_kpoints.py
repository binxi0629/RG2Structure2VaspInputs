from pymatgen.core import Structure
from pymatgen.symmetry.bandstructure import HighSymmKpath
from pymatgen.io.vasp.inputs import Incar, Poscar, Potcar, Kpoints, VaspInput


def gen_incar(incar_config={}):

    _default_incar_config = {
        'ALGO': 'Fast',
        'ICHARG': '2',
        'PREC': 'Normal',
        'EDIFF': '1E-5',
        'ENCUT': '520',
        'ISMEAR': '0',
        'IBRION': '-1',
        'ISIF': '0',
        'NELM': '200',
        'NSW': '0',
        'SIGMA': '0.1',
        'ISYM': '2',
    }
    _default_incar_config.update(incar_config)
    Incar(_default_incar_config).write_file('INCAR')


def gen_hs_kpoints(structure):
    kpath = HighSymmKpath(structure)
    kpts = Kpoints.automatic_linemode(divisions=5, ibz=kpath)
    kpts.write_file('KPOINTS')


def main():
    structure = Structure.from_file('POSCAR')
    gen_hs_kpoints(structure)
    gen_incar()


if __name__ == '__main__':
    main()
