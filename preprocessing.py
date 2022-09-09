from cloudpathlib import CloudPath


def s3_download(link, download_folder):
    cp = CloudPath(link)
    print("Downloading files")
    cp.download_to(download_folder)


if __name__ == "__main__":
    link = "s3://medvolt-drp/results/client_6/workspace_1/project_1/experiment_1/C1CCC(C(C1)/"
    download_folder = link.split("/")[8]
    s3_download(link, download_folder)
