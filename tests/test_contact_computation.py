import compas_tia.tia_contact_computation
from compas_tia import tia_mesh
from compas_tia import tia_assembly
import pytest
from compas.datastructures import Mesh
from numba.typed import List


class TestContactComputation:
    class test_input():
        mesh_compas0 = Mesh.from_obj("../data/passiveAfterBoolean.obj")
        mesh0 = tia_mesh(mesh_compas0)
        mesh_compas1 = Mesh.from_obj("../data/activeAfterBoolean.obj")
        mesh1 = tia_mesh(mesh_compas1)
        assembly = tia_assembly([mesh0, mesh1])
        assembly.compute_contacts()


