from zipfile import ZipFile


def save_all(file_name, iter, suffix="log"):
    with ZipFile(file_name, "w") as f:
        for name, data in iter:
            full_name = "%s.%s" % (name, suffix)
            f.writestr(full_name, data)
