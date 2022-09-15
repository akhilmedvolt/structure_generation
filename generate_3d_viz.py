import MDAnalysis as mda
import prolif as plf
import pandas as pd
import numpy as np
import py3Dmol

from rdkit import Geometry, Chem

import os

colors = {
    "HBAcceptor": "yellow",
    "HBDonor": "yellow",
    "PiCation": "green",
    "PiStacking": "purple",
    "Hydrophobic": "black"

}

# JavaScript functions
resid_hover = """function(atom,viewer) {{
    if(!atom.label) {{
        atom.label = viewer.addLabel('{0}:'+atom.atom+atom.serial,
            {{position: atom, backgroundColor: 'mintcream', fontColor:'black'}});
    }}
}}"""
hover_func = """
function(atom,viewer) {
    if(!atom.label) {
        atom.label = viewer.addLabel(atom.interaction,
            {position: atom, backgroundColor: 'black', fontColor:'white'});
    }
}"""
unhover_func = """
function(atom,viewer) {
    if(atom.label) {
        viewer.removeLabel(atom.label);
        delete atom.label;
    }
}"""


def generate_3d_viz(file):
    try:
        os.system(f"grep 'ATOM' {file} > prot.pdb")
        os.system(f"grep 'HETATM' {file} > lig.pdb")

        os.system('obabel prot.pdb -opdb -O proth.pdb -h')
        os.system('obabel lig.pdb -opdb -O ligh.pdb -h')

        prot = mda.Universe("proth.pdb")
        lig = mda.Universe("ligh.pdb")

        prot_mol = plf.Molecule.from_mda(prot)
        lig_mol = plf.Molecule.from_mda(lig)

        fp = plf.Fingerprint()
        fp.run_from_iterable([lig_mol], prot_mol)
        df: pd.DataFrame = fp.to_dataframe(return_atoms=True)

        f_name = file.split(".")[0]

        v = py3Dmol.view(650, 600)
        v.removeAllModels()
        models = {}
        mid = -1

        for i, row in df.T.iterrows():
            lresid, presid, interaction = i
            lindex, pindex = row[0]
            lres = lig_mol[lresid]
            pres = prot_mol[presid]
            print(lres, pres)

            # set model ids for reusing later
            for resid, res, style in [
                (lresid, lres, {"colorscheme": "cyanCarbon"}),
                (presid, pres, {}),
            ]:
                if resid not in models.keys():
                    mid += 1
                    v.addModel(Chem.MolToMolBlock(res), "sdf")
                    model = v.getModel()
                    model.setStyle({}, {"stick": style})
                    # add residue label
                    model.setHoverable(
                        {}, True, resid_hover.format(resid), unhover_func
                    )
                    models[resid] = mid

            p1 = lres.GetConformer().GetAtomPosition(lindex)
            p2 = pres.GetConformer().GetAtomPosition(pindex)

            v.addCylinder(
                {
                    "start": dict(x=p1.x, y=p1.y, z=p1.z),
                    "end": dict(x=p2.x, y=p2.y, z=p2.z),
                    "color": colors[interaction],
                    "radius": 0.15,
                    "dashed": True,
                    "fromCap": 1,
                    "toCap": 1,
                }
            )

            c = Geometry.Point3D(*plf.utils.get_centroid([p1, p2]))
            modelID = models[lresid]
            model = v.getModel(modelID)
            model.addAtoms(
                [
                    {
                        "elem": "Z",
                        "x": c.x,
                        "y": c.y,
                        "z": c.z,
                        "interaction": interaction,
                    }
                ]
            )

            model.setStyle(
                {"interaction": interaction}, {"clicksphere": {"radius": 0.5}}
            )
            model.setHoverable(
                {"interaction": interaction}, True, hover_func, unhover_func
            )

        order = np.argsort(
            [atom.GetIntProp("_MDAnalysis_index") for atom in prot_mol.GetAtoms()]
        )
        mol = Chem.RenumberAtoms(prot_mol, order.astype(int).tolist())
        mol = Chem.RemoveAllHs(mol)
        pdb = Chem.MolToPDBBlock(mol, flavor=(0x20 | 0x10))

        v.addModel(pdb, "pdb")
        model = v.getModel()
        model.setStyle({}, {"cartoon": {"style": "edged"}})

        v.zoomTo({"model": list(models.values())})

        f_name = file.split(".")[0]
        # Generate HTML
        markup = v.startjs + v.endjs
        with open(f"output3D/{f_name}_viz3d.html", "w") as f:
            f.write(markup)

        try:
            os.remove("lig.pdb")
            os.remove("prot.pdb")
            os.remove("ligh.pdb")
            os.remove("proth.pdb")
        except:
            pass
        print(f"3D Generation Complete for {f_name}")
    except Exception as e:
        print(e)
        pass


