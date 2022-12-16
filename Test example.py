# -*- coding: utf-8 -*-
"""
Created on Thu Jul  1 13:27:02 2021

@author: lection
"""

import pychrono.core as chrono
import pychrono.irrlicht as chronoirr
import pychrono.fea as fea

def CastNode(nb):
    feaNB = fea.CastToChNodeFEAbase(nb)
    nodeFead = fea.CastToChNodeFEAxyzD(feaNB)
    return nodeFead

time_step = 1e-3
mysystem  = chrono.ChSystemSMC()
mysystem .Set_G_acc(chrono.ChVectorD(0, 0, -9.8))

application = chronoirr.ChIrrApp(mysystem , "Test Module", chronoirr.dimension2du(800, 600), False, True)

application.AddTypicalLogo()
application.AddTypicalSky()
application.AddTypicalLights()
application.AddTypicalCamera(chronoirr.vector3df(0, 0, 5),  
                             chronoirr.vector3df(0, 0, 3))  

# Create a mesh
my_mesh = fea.ChMesh()
numFlexBody = 1

plate_lenght_x = 5
plate_lenght_y = 5
plate_lenght_z = 0.01

numDiv_x = 10
numDiv_y = 10
N_x = numDiv_x + 1
N_y = numDiv_y + 1

# Number of elements
TotalNumElements = numDiv_x * numDiv_y
TotalNumNodes = N_x * N_y
# For uniform mesh
dx = plate_lenght_x / numDiv_x
dy = plate_lenght_y / numDiv_y
dz = plate_lenght_z

# Create and add the nodes
for i in range(TotalNumNodes) :
    # Node location
    loc_x = (i % N_x) * dx;
    loc_y = (i // N_x) % N_y * dy;
    loc_z = 0;

    # Node direction
    dir_x = 0
    dir_y = 0
    dir_z = 1

    # Create the node
    node = fea.ChNodeFEAxyzD(chrono.ChVectorD(loc_x, loc_y, loc_z), chrono.ChVectorD(dir_x, dir_y, dir_z))

    node.SetMass(0)

    # Fix all nodes along the axis X=0
    if (i == 0) or (i==10) or (i==110) or(i==120):
        node.SetFixed(True)

    # Add node to mesh
    my_mesh.AddNode(node)

# Get a handle to the tip node.
tempnode = my_mesh.GetNode(TotalNumNodes - 1)
tempfeanode = fea.CastToChNodeFEAbase(tempnode)
nodetip = fea.CastToChNodeFEAxyzD(tempfeanode)

# Create an orthotropic material.
rho = 1000
E = chrono.ChVectorD(2.1e7, 2.1e7, 2.1e7)
nu = chrono.ChVectorD(0.3, 0.3, 0.3)
G = chrono.ChVectorD(8.0769231e6, 8.0769231e6, 8.0769231e6)
mat = fea.ChMaterialShellANCF(rho, E, nu, G)

# Create the elements
for i in range(TotalNumElements):
    # Adjacent nodes
    node0 = (i // numDiv_x) * N_x + i % numDiv_x
    node1 = (i // numDiv_x) * N_x + i % numDiv_x + 1
    node2 = (i // numDiv_x) * N_x + i % numDiv_x + 1 + N_x
    node3 = (i // numDiv_x) * N_x + i % numDiv_x + N_x

    # Create the element and set its nodes.
    element = fea.ChElementShellANCF()
    element.SetNodes(CastNode(my_mesh.GetNode(node0)),
                      CastNode(my_mesh.GetNode(node1)),
                      CastNode(my_mesh.GetNode(node2)),
                      CastNode(my_mesh.GetNode(node3)))

    # Set element dimensions
    element.SetDimensions(dx, dy)

    # Add a single layers with a fiber angle of 0 degrees.
    element.AddLayer(dz, 0 * chrono.CH_C_DEG_TO_RAD, mat)

    # Set other element properties
    element.SetAlphaDamp(0.1)    # Structural damping for this element
    element.SetGravityOn(False)  # turn internal gravitational force calculation off
    
    # Add element to mesh
    my_mesh.AddElement(element)

# Add the mesh to the system
mysystem.Add(my_mesh)

def AddFallingItems(sys):
    # Shared contact materials for falling objects
    sph_mat = chrono.ChMaterialSurfaceNSC()
    sph_mat.SetFriction(1)
    col_1 = chrono.ChColorAsset()
    col_1.SetColor(chrono.ChColor(0.6, 0, 0))
    # Create falling rigid bodies (spheres and boxes etc.)
    for bi in range(20):
        msphereBody = chrono.ChBodyEasySphere(0.3,      # radius size
                                              500,     # density
                                              True,     # visualization?
                                              True,     # collision?
                                              sph_mat)  # contact material
        msphereBody.SetPos(chrono.ChVectorD(chrono.ChRandom() * 3,chrono.ChRandom() * 3, 2))
        msphereBody.AddAsset(col_1)
        sys.Add(msphereBody)

        mtexture = chrono.ChTexture()
        mtexture.SetTextureFilename(chrono.GetChronoDataFile("bluwhite.png"))
        msphereBody.AddAsset(mtexture)
        
#visualization
visualizemeshA = fea.ChVisualizationFEAmesh(my_mesh)
visualizemeshA.SetFEMdataType(fea.ChVisualizationFEAmesh.E_PLOT_NODE_SPEED_NORM)
visualizemeshA.SetColorscaleMinMax(0.0, 5.50)
visualizemeshA.SetShrinkElements(True, 0.85)
visualizemeshA.SetSmoothFaces(True)
my_mesh.AddAsset(visualizemeshA)

visualizemeshB = fea.ChVisualizationFEAmesh(my_mesh)
visualizemeshB.SetFEMdataType(fea.ChVisualizationFEAmesh.E_PLOT_SURFACE)
visualizemeshB.SetWireframe(True)
visualizemeshB.SetDrawInUndeformedReference(True)
my_mesh.AddAsset(visualizemeshB)

visualizemeshC = fea.ChVisualizationFEAmesh(my_mesh)
visualizemeshC.SetFEMglyphType(fea.ChVisualizationFEAmesh.E_GLYPH_NODE_DOT_POS)
visualizemeshC.SetFEMdataType(fea.ChVisualizationFEAmesh.E_PLOT_NONE)
visualizemeshC.SetSymbolsThickness(0.004)
my_mesh.AddAsset(visualizemeshC)

visualizemeshD = fea.ChVisualizationFEAmesh(my_mesh)
visualizemeshD.SetFEMglyphType(fea.ChVisualizationFEAmesh.E_GLYPH_ELEM_TENS_STRAIN)
visualizemeshD.SetFEMdataType(fea.ChVisualizationFEAmesh.E_PLOT_NONE)
visualizemeshD.SetSymbolsScale(1)
visualizemeshD.SetColorscaleMinMax(-0.5, 5)
visualizemeshD.SetZbufferHide(False)
my_mesh.AddAsset(visualizemeshD)

AddFallingItems(mysystem)

application.AssetBindAll()
application.AssetUpdateAll()
#
solver = chrono.ChSolverMINRES()
mysystem.SetSolver(solver)

solver.EnableDiagonalPreconditioner(True)
#solver.SetVerbose(True)
mysystem.SetSolverMaxIterations(100)
mysystem.SetSolverForceTolerance(1e-10)


while(application.GetDevice().run()):
    application.BeginScene()
    application.DrawAll()
    application.DoStep()
    application.EndScene()
        