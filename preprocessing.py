from cloudpathlib import CloudPath


def s3_download(link):
    root = CloudPath(link)
    print("Downloading files")
    iter_ = 0
    for f in root.rglob('/*.pdb'):
        if "complex" in f.name:
            filename = f.name.replace('/', '_')
            print(f"{str(iter_)}:", filename)
            f.download_to("./pdbid/" + filename)
        else:
            pass
        iter_ += 1


if __name__ == "__main__":
    link = "s3://medvolt-drp/results/client_6/workspace_1/project_1/experiment_1/C1CCC(C(C1)/"
    download_folder = link.split("/")[8]
    s3_download(link)
