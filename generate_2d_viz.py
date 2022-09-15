import os
import MDAnalysis as mda
import prolif as plf
import pandas as pd

from prolif.plotting.network import LigNetwork


def generate_2d_viz(file):
    try:
        f_name = file.split(".")[0]

        os.system(f"grep 'ATOM' {file} > prot.pdb")
        os.system(f"grep 'HETATM' {file} > lig.pdb")

        os.system(f'obabel prot.pdb -opdb -O {f_name}_proth.pdb -h')
        os.system(f'obabel lig.pdb -opdb -O {f_name}_ligh.pdb -h')

        prot = mda.Universe(f"{f_name}_proth.pdb")
        lig = mda.Universe(f"{f_name}_ligh.pdb")

        prot_mol = plf.Molecule.from_mda(prot)
        lig_mol = plf.Molecule.from_mda(lig)

        fp = plf.Fingerprint()

        fp.run_from_iterable([lig_mol], prot_mol)

        df: pd.DataFrame = fp.to_dataframe(return_atoms=True)

        f_name = file.split(".")[0]
        df.to_csv(f"./dataframes/{f_name}_df.csv")
        net = LigNetwork.from_ifp(df, lig_mol,
                                  kind="frame", frame=0)

        net.save(f"output2D/{f_name}_viz2d.html")

        try:
            os.remove("lig.pdb")
            os.remove("prot.pdb")
            os.remove(f"{f_name}_ligh.pdb")
            os.remove(f"{f_name}_proth.pdb")
        except:
            pass
        print(f"2D Generation Complete for {f_name}")
    except Exception as e:
        print(e)
        pass
