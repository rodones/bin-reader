
import os
import sys
import collections
import json
from matrix import Matrix
from read_bin import read_images_binary, read_points_binary
from vector import Point3f

ImageEntity = collections.namedtuple(
    "ImageEntity", ["name", "point"])

matrix: 'Matrix'


def check_file(filename: str) -> bool:
    return os.path.isfile(filename)


def is_bin(filename: str) -> bool:
    return check_file(filename) and (filename.endswith(".bin"))


def matrix_selection():
    global matrix
    print("Provide values row by row and space seperated")
    mat = []

    for i in range(1, 5):
        row = input("Row "+str(i)+" : ")
        mat.append([float(a) for a in row.split(" ")])

    print("Selected matrix: "+str(mat))

    if len(mat) == 4:
        matrix = Matrix(mat)
    else:
        matrix = Matrix()


def main():
    global matrix
    if(len(sys.argv) < 3):
        print("usage\n\tpython app.py <point bin file> <image bin file>")
        exit(0)

    if(not is_bin(sys.argv[1])):
        print("provide a valid point bin file")
        exit(0)

    if(not is_bin(sys.argv[2])):
        print("provide a valid image bin file")
        exit(0)

    print("Translation matrix init step")
    yN = input("if no identity selected y/N: ")

    if yN == "N":
        matrix = Matrix()
    elif yN == "y":
        matrix_selection()
    else:
        print("Provide a valid input")
        exit(0)

    print("Entity init step:")

    images = read_images_binary(sys.argv[2])
    points = read_points_binary(sys.argv[1])
    entites: 'list[ImageEntity]' = []

    for i in images:

        vals = Point3f(0, 0, 0)
        lenVals = 0
        for a in images[i].point3D_ids:
            if(a >= 0):
                if(points[a].obj is not int):
                    lenVals += 1
                    vals += (matrix*points[a].obj)
        entites.append(ImageEntity(images[i].name,
                                   vals*float(1/lenVals))._asdict())

    f = open("request.json", "w")

    f.write(json.dumps(entites, default=vars))
    f.close()
    exit(1)


if __name__ == "__main__":
    main()
