from cloudpathlib import CloudPath


def s3_download(link):
    cp = CloudPath(link)
    cp.download_to("lurasidone_results")


if __name__ == "__main__":
    link = "s3://medvolt-nce/dynamic/new_results/lurasidone_results/"
    s3_download(link)
