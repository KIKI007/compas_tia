from compas.datastructures import Mesh
from numba import jit
import numpy as np
from numba.typed import List

__all__ = ['tia_mesh', "tia_assembly"]
class tia_mesh:
    faces_boundary = List()
    faces_normal = List()
    def __init__(self, compas_mesh):
        for f in compas_mesh.faces():
            face_loop = List()
            for v in compas_mesh.face_vertices(f):
                pos = compas_mesh.vertex_coordinates(v)
                face_loop.append(List([pos[0], pos[1], pos[2]]))
            normal = compas_mesh.face_normal(f)
            self.faces_normal.append(List([normal[0], normal[1], normal[2]]))
            self.faces_boundary.append(face_loop)

from numba import jit
@jit(nopython=True)
def f(x):
    tmp = [] # defined empty
    for i in range(x):
        tmp.append(i) # list type can be inferred from the type of `i`
    return tmp

@jit(nopython=True)
def compute_faces_data(parts_faces_normals):
    faces_data = List()
    num_of_parts = len(parts_faces_normals)
    for partID in range(num_of_parts):
        part = parts_faces_normals[partID]
        num_of_faces = len(part)
        for faceID in range(num_of_faces):
            faces_data.append(List([partID, faceID]))
            faces_data.append(List([partID, faceID]))
    return faces_data

@jit(nopython=True)
def compute_faces_plane(parts_faces_boundary, parts_faces_normals):
    faces_plane = List()
    faces_data = List()
    num_of_parts = len(parts_faces_boundary)
    for partID in range(num_of_parts):
        part = parts_faces_boundary[partID]
        num_of_faces = len(part)
        for faceID in range(num_of_faces):
            normal = parts_faces_normals[partID][faceID]
            v0 = parts_faces_boundary[partID][faceID][0]
            intercept = -(normal[0] * v0[0] + normal[1] * v0[1] + normal[2] * v0[2])
            plane = List([normal[0], normal[1], normal[2], intercept])
            faces_plane.append(plane)
            faces_data.append(List([partID, faceID]))
            plane = List([-normal[0], -normal[1], -normal[2], -intercept])
            faces_plane.append(plane)
            faces_data.append(List([partID, faceID]))
    return faces_plane


#@jit(nopython=True)
def compute_incontact_plane(parts_faces_plane,
                            parts_faces_data,
                            digit_epsilon = 1E-2,
                            angle_epsilon = 1E-2,
                            intercept_epsilon = 1E-2):

    incontact_plane_index = []
    for index in range(0, 4):
        plane_digits = [[parts_faces_plane[planeID][index], int(planeID)] for planeID in range(len(parts_faces_plane))]
        plane_digits.sort(key=lambda k: k[0])
        for planeID in range(len(plane_digits)):
            plane_index = []
            curr_plane_index = plane_digits[planeID][1]
            digit_plane = plane_digits[planeID][0]
            # index before planeID
            for beforePlaneID in range(planeID - 1, -1, -1):
                digit_before = plane_digits[beforePlaneID][0]
                if digit_plane - digit_before < digit_epsilon:
                    plane_index_before = plane_digits[beforePlaneID][1]
                    plane_index.append(plane_index_before)
                else:
                    break

            # index after planeID
            for afterPlaneID in range(planeID + 1, len(plane_digits)):
                digit_after = plane_digits[afterPlaneID][0]
                if digit_after - digit_plane < digit_epsilon:
                    plane_index_after = plane_digits[afterPlaneID][1]
                    plane_index.append(plane_index_after)
                else:
                    break

            # set intersection
            if index == 0:
                incontact_plane_index.append(plane_index)
            else:
                a = incontact_plane_index[curr_plane_index]
                b = plane_index
                incontact_plane_index[curr_plane_index] = list(set(a) & set(b))

    plane_pairs = []
    for id in range(int(len(incontact_plane_index) / 2)):
        planeIDA = 2 * id
        a = incontact_plane_index[id * 2]
        b = incontact_plane_index[id * 2 + 1]
        combine_incontact_planes = list(set.union(set(a), set(b)))
        for planeIDB in combine_incontact_planes:
            if planeIDB % 2 == 0:
                partIDA = parts_faces_data[planeIDA][0]
                partIDB = parts_faces_data[planeIDB][0]
                if partIDA != partIDB:
                    normalA = parts_faces_plane[planeIDA][0:3]
                    normalB = parts_faces_plane[planeIDB][0:3]
                    delta_angle = 1 + (normalA[0] * normalB[0] + normalA[1] * normalB[1] + normalA[2] * normalB[2])
                    delta_intercept = parts_faces_plane[planeIDA][3] + parts_faces_plane[planeIDB][3]
                    if delta_angle < angle_epsilon and delta_intercept < intercept_epsilon and delta_intercept > -1E-4:
                        plane_pairs.append([int(planeIDA / 2), int(planeIDB / 2)])
                        print(parts_faces_plane[planeIDA], parts_faces_plane[planeIDB])


    print(plane_pairs)


class tia_assembly:

    parts_ = []

    parts_faces_boundary_ = List()
    parts_faces_normals_ = List()

    parts_faces_planes_ = List()
    parts_faces_data_ = List()

    def __init__(self, tia_meshes):
        self.parts_ = tia_meshes
        self.parts_faces_boundary_ = List([part.faces_boundary for part in self.parts_])
        self.parts_faces_normals_ = List([part.faces_normal for part in self.parts_])
        self.parts_faces_planes_ = compute_faces_plane(self.parts_faces_boundary_, self.parts_faces_normals_)
        self.parts_faces_data_ = compute_faces_data(self.parts_faces_normals_)


    def compute_contacts(self):
        compute_incontact_plane(self.parts_faces_planes_, self.parts_faces_data_)



