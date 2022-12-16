# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 17:01:29 2021

@author: lection
"""
import pychrono as chrono
import pychrono.fea as fea
import pychrono.irrlicht as chronoirr

# Create a Engine physical system
my_system = chrono.ChSystemSMC()

## Create a mesh
my_mesh = fea.ChMesh();

## Create a section
msection = fea.ChBeamSectionEulerAdvanced()
#C45 Concrete
beam_wy = 0.01
beam_wz = 0.02
beam_L = 0.1
msection.SetAsRectangularSection(beam_wy, beam_wz)
msection.SetYoungModulus(3.35e7)
msection.SetGshearModulus(3.35e7 * 0.4)
msection.SetBeamRaleyghDamping(0.000)

# Add some BEAMS:

hnode1 = fea.ChNodeFEAxyzrot(chrono.ChFrameD(chrono.ChVectorD(0, 0, 0)))
hnode2 = fea.ChNodeFEAxyzrot(chrono.ChFrameD(chrono.ChVectorD(beam_L, 0, 0)))
hnode3 = fea.ChNodeFEAxyzrot(chrono.ChFrameD(chrono.ChVectorD(beam_L * 2, 0, 0)))

hnode4 = fea.ChNodeFEAxyzrot(chrono.ChFrameD(chrono.ChVectorD(0, 0, 0.01)))
hnode5 = fea.ChNodeFEAxyzrot(chrono.ChFrameD(chrono.ChVectorD(beam_L, 0, 0.01)))
hnode6 = fea.ChNodeFEAxyzrot(chrono.ChFrameD(chrono.ChVectorD(beam_L * 2, 0, 0.01)))

my_mesh.AddNode(hnode1)
my_mesh.AddNode(hnode2)
my_mesh.AddNode(hnode3)

my_mesh.AddNode(hnode4)
my_mesh.AddNode(hnode5)
my_mesh.AddNode(hnode6)

belement1 = fea.ChElementBeamEuler()
belement1.SetNodes(hnode1, hnode2)
belement1.SetSection(msection)
my_mesh.AddElement(belement1)

belement2 = fea.ChElementBeamEuler()
belement2.SetNodes(hnode2, hnode3)
belement2.SetSection(msection)
my_mesh.AddElement(belement2);

belement3 = fea.ChElementBeamEuler()
belement3.SetNodes(hnode4, hnode5)
belement3.SetSection(msection)
my_mesh.AddElement(belement3)

belement4 = fea.ChElementBeamEuler()
belement4.SetNodes(hnode5, hnode6)
belement4.SetSection(msection)
my_mesh.AddElement(belement4);

# Apply a shear force to a node:
hnode2.SetForce(chrono.ChVectorD(0, 15, 0))
hnode5.SetForce(chrono.ChVectorD(0, 15, 0))

# Fix a node to ground:

mtruss = chrono.ChBody()
mtruss.SetBodyFixed(True)
my_system.Add(mtruss)

constr_bc = chrono.ChLinkMateGeneric()
constr_bc.Initialize(hnode3, mtruss, False, hnode3.Frame(), hnode3.Frame())
my_system.Add(constr_bc)
constr_bc.SetConstrainedCoords(True, True, True,   # x, y, z
                               True, True, True)   # Rx, Ry, Rz

constr_d = chrono.ChLinkMateGeneric()
constr_d.Initialize(hnode1, mtruss, False, hnode1.Frame(), hnode1.Frame())
my_system.Add(constr_d)
constr_d.SetConstrainedCoords(True, True, True,   # x, y, z
                               True, True, True)   # Rx, Ry, Rz

constr_ef = chrono.ChLinkMateGeneric()
constr_ef.Initialize(hnode6, mtruss, False, hnode6.Frame(), hnode6.Frame())
my_system.Add(constr_ef)
constr_ef.SetConstrainedCoords(True, True, True,   # x, y, z
                               True, True, True)   # Rx, Ry, Rz


constr_g = chrono.ChLinkMateGeneric()
constr_g.Initialize(hnode4, mtruss, False, hnode4.Frame(), hnode4.Frame())
my_system.Add(constr_g)
constr_g.SetConstrainedCoords(True, True, True,   # x, y, z
                               True, True, True)   # Rx, Ry, Rz


# Ignore the Gravity
my_mesh.SetAutomaticGravity(False);

# Add the mesh to the system
my_system.Add(my_mesh)

# ==Asset== attach a visualization of the FEM mesh.

mvisualizebeamA = fea.ChVisualizationFEAmesh(my_mesh)
mvisualizebeamA.SetFEMdataType(fea.ChVisualizationFEAmesh.E_PLOT_ELEM_BEAM_MZ)
mvisualizebeamA.SetColorscaleMinMax(-0.4, 0.4)
mvisualizebeamA.SetSmoothFaces(True)
mvisualizebeamA.SetWireframe(False)
my_mesh.AddAsset(mvisualizebeamA)

# Create the Irrlicht visualization 
myapplication = chronoirr.ChIrrApp(my_system, 'Test beams', chronoirr.dimension2du(1024,768))

#application.AddTypicalLogo()
myapplication.AddTypicalSky()
myapplication.AddTypicalLogo(chrono.GetChronoDataFile('logo_pychrono_alpha.png'))
myapplication.AddTypicalCamera(chronoirr.vector3df(0.1,0.1,0.2))
myapplication.AddTypicalLights()

#
myapplication.AssetBindAll()

#
myapplication.AssetUpdateAll()

# solver
msolver = chrono.ChSolverMINRES()
my_system.SetSolver(msolver)
msolver.EnableDiagonalPreconditioner(True)

my_system.SetSolverMaxIterations(100)
my_system.SetSolverForceTolerance(1e-10)

stepper = chrono.ChTimestepperHHT(my_system)
my_system.SetTimestepper(stepper)

stepper.SetAlpha(-0.2)
stepper.SetMaxiters(5)
stepper.SetAbsTolerances(1e-8)
stepper.SetMode(chrono.ChTimestepperHHT.POSITION)
stepper.SetScaling(True)
stepper.SetStepControl(True)
stepper.SetMinStepSize(1e-8)

myapplication.SetTimestep(0.0038);
#	application.GetSystem().DoStaticLinear()
 
while(myapplication.GetDevice().run()):
    myapplication.BeginScene()
    myapplication.DrawAll()
    myapplication.DoStep()
    myapplication.EndScene()
    
   