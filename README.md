# Blender-UnrealTools

Vertex Animation-
This script creates a new panel in the object mode tool shelf as well as a new operator.

When called the operator will take all selected mesh objects in the active scene and copy their mesh data per frame.
The difference in each vertex location and normals in world space is then stored as color data in two images respectfully.
A new mesh is created for export with it's second UV channel's vertices spaced evenly across the V axis.

Paint Selection Sequence is used as follow. Create a series of meshes and select them. The script will sort them alphabetically. Then press Paint Selection Sequence button. The script will store their selection sequence in the meshes uvs. Use the ''SequencePainter_SequenceFlipbook'' material function, in UE4, to retrieve the values." You can follow this tutorial to handle the UE import procedure https://docs.unrealengine.com/en-us/Engine/Animation/Tools/VertexAnimationTool/VAT_KF_Meshes

Unfold Anim-
If you have an animated mesh and you need to 'bake' each frame as a independent mesh. To be used with Paint Selection Sequence.

Mesh Morpher-
This script creates a new panel in the object mode tool shelf as well as a new operator.
When called the operator will (based on user settings) store shape key vertex offset data in a mesh's UV channels, and store normal data in it's vertex colors.
