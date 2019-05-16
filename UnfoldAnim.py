# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Unfold Animation",
    "author": "Santamaria Nicolas",
    "version": (1, 0),
    "blender": (2, 78, 0),
    "location": "View3D > Tool Shelf > Unreal Tools",
    "description": "Unfold keyframes of an animated mesh into separate meshes",
    "warning": "Each keyframe will be a new mesh.",
    "wiki_url": "",
    "category": "Unreal Tools",
    }

import bpy
import bmesh
import mathutils
from bpy.types import Operator, Panel
from mathutils import Vector

#gets mesh data from an object in world coordinates with modifiers and transforms applied
def copyMeshData(data, object, newBmesh, scene):
    meshData = object.to_mesh(scene, True, 'PREVIEW')
    
    for vert in meshData.vertices:
        vert.co = object.matrix_world * vert.co
    
    newBmesh.from_mesh(meshData)
    data.meshes.remove(meshData)
    
    return newBmesh


def unfold_mesh(data, scene, obj):
    anim = obj.animation_data
    #if anim is not None and anim.action is not None:
    print('has animation');
    for f in range(scene.frame_start, (scene.frame_end +1), scene.frame_step):
        scene.frame_set(f)
        
        newMesh = data.meshes.new("mesh")
        
        newBmesh = bmesh.new()
        newBmesh = copyMeshData(data, obj, newBmesh, scene)
        newBmesh.to_mesh(newMesh)
        newBmesh.free()
        newMesh.calc_normals()
        newObject = data.objects.new("{0:s}_Frame_{1:03d}".format(obj.name,f), newMesh)
        scene.objects.link(newObject)

def main(context):
    scene = context.scene
    data = bpy.data
    selectedObjects = context.selected_objects
    for obj in selectedObjects:
        unfold_mesh(data, scene, obj)
                    
    scene.frame_set(1)
    return 0

#create operator class for panel button    
class UT_ProcessAnimOperator(Operator):
    bl_label = "Unfold Animated Mesh"
    bl_idname = "unreal_tools.unfold_anim"
    
    @classmethod
    def poll(cls, context):
        return True in [object.type == 'MESH' for object in context.selected_objects] and context.mode == 'OBJECT' and len(context.selected_objects) == 1
    
    def execute(self, context):
        units = context.scene.unit_settings
        
        if units.system != 'METRIC' or round(units.scale_length, 2) != 0.01:
            
            self.report({'ERROR'}, "Scene units must be Metric with a Unit Scale of 0.01!")
        
            return {'CANCELLED'}
                        
        else:
            main(context)
            
            return {'FINISHED'}
        
#create panel class for UI in object mode tool shelf
class UT_UnfoldAnimPanel(Panel):
    bl_label = "Mesh Animation"
    bl_idname = "ut_unfold_anim_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Unreal Tools"
    bl_context = "objectmode"
    
    def draw(self, context):
        scene = context.scene
        layout = self.layout
        
        col = layout.column(align = True)
        col.prop(scene, "frame_start")
        col.prop(scene, "frame_end")
        col.prop(scene, "frame_step")
      
        row = layout.row()
        row.scale_y = 1.5
        row.operator("unreal_tools.unfold_anim")

#create register functions for adding and removing script          
def register():
    bpy.utils.register_class(UT_UnfoldAnimPanel)
    bpy.utils.register_class(UT_ProcessAnimOperator)
    
def unregister():
    bpy.utils.unregister_class(UT_UnfoldAnimPanel)
    bpy.utils.unregister_class(UT_ProcessAnimOperator)
    
if __name__ == "__main__":
    register()
