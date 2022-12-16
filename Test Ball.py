# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 14:38:40 2021

@author: lection
"""

import pychrono.core as chrono
import pychrono.irrlicht as chronoirr
import pychrono.fea as fea

def AddFallingItems(sys):
    # Shared contact materials for falling objects
    sph_mat = chrono.ChMaterialSurfaceNSC()
    sph_mat.SetFriction(1)
    col_1 = chrono.ChColorAsset()
    col_1.SetColor(chrono.ChColor(0.6, 0, 0))
    # Create falling rigid bodies (spheres and boxes etc.)
    for bi in range(800):
        msphereBody = chrono.ChBodyEasySphere(0.8,      # radius size
                                              1000,     # density
                                              True,     # visualization?
                                              True,     # collision?
                                              sph_mat)  # contact material
        msphereBody.SetPos(chrono.ChVectorD(-5 + chrono.ChRandom() * 10, 0, -5 + chrono.ChRandom() * 10))
        msphereBody.AddAsset(col_1)
        sys.Add(msphereBody)

        mtexture = chrono.ChTexture()
        mtexture.SetTextureFilename(chrono.GetChronoDataFile("bluwhite.png"))
        msphereBody.AddAsset(mtexture)


def AddContainer(sys):
    # Contact material for container
    ground_mat = chrono.ChMaterialSurfaceNSC()
    
    floorBody = chrono.ChBodyEasyBox(20, 1, 20, 1000, False, True, ground_mat)
    floorBody.SetPos(chrono.ChVectorD(0, -5, 0))
    floorBody.SetBodyFixed(True)
    sys.Add(floorBody)

    wallBody1 = chrono.ChBodyEasyBox(1, 10, 20, 1000, False, True, ground_mat)
    wallBody1.SetPos(chrono.ChVectorD(-10, 0, 0))
    wallBody1.SetBodyFixed(True)
    sys.Add(wallBody1)

    wallBody2 = chrono.ChBodyEasyBox(1, 10, 20, 1000, False, True, ground_mat)
    wallBody2.SetPos(chrono.ChVectorD(10, 0, 0))
    wallBody2.SetBodyFixed(True)
    sys.Add(wallBody2)

    wallBody3 = chrono.ChBodyEasyBox(20, 10, 1, 1000, False, True, ground_mat)
    wallBody3.SetPos(chrono.ChVectorD(0, 0, -10))
    wallBody3.SetBodyFixed(True)
    sys.Add(wallBody3)

    wallBody4 = chrono.ChBodyEasyBox(20, 10, 1, 1000, False, True, ground_mat)
    wallBody4.SetPos(chrono.ChVectorD(0, 0, 10))
    wallBody4.SetBodyFixed(True)
    sys.Add(wallBody4)



# ---------------------------------------------------------------------
#  Create the simulation system and add items

mysystem = chrono.ChSystemNSC()

# ---------------------------------------------------------------------
#  Create an Irrlicht application to visualize the system

myapplication = chronoirr.ChIrrApp(mysystem, 'Test balls', chronoirr.dimension2du(1024,768))

myapplication.AddTypicalSky()
myapplication.AddTypicalLogo(chrono.GetChronoDataFile('logo_pychrono_alpha.png'))
myapplication.AddTypicalCamera(chronoirr.vector3df(0, 20 , -20))
myapplication.AddTypicalLights()

mixer = AddContainer(mysystem)
AddFallingItems(mysystem)


myapplication.AssetBindAll()
myapplication.AssetUpdateAll()

# Modify some setting of the physical syustem for the simulation, if you want
mysystem.SetSolverType(chrono.ChSolver.Type_PSOR)
mysystem.SetSolverMaxIterations(20)

stepper = chrono.ChTimestepperHHT(mysystem)
mysystem.SetTimestepper(stepper)

stepper.SetAlpha(-0.2)
stepper.SetAbsTolerances(1e-5)
stepper.SetMode(chrono.ChTimestepperHHT.POSITION)
stepper.SetScaling(True)
stepper.SetStepControl(True)
stepper.SetMinStepSize(1e-5)


myapplication.SetTimestep(0.02)
myapplication.SetTryRealtime(True)


while(myapplication.GetDevice().run()):
    myapplication.BeginScene()
    myapplication.DrawAll()
    myapplication.DoStep()
    myapplication.EndScene()
   





