import bpy

class LIGHTSETTER_PR_object_props(bpy.types.PropertyGroup):
    hide_panel: bpy.props.BoolProperty(name='Hide Light Object panel', default=True)
    hidden_viewport: bpy.props.BoolProperty()
    hidden_render: bpy.props.BoolProperty()

class LIGHTSETTER_PR_scene_props(bpy.types.PropertyGroup):
    isolated_light: bpy.props.PointerProperty(type=bpy.types.Object, name="Isolated Light")
    include_world: bpy.props.BoolProperty(
        name="Include World",
        description="Include World for Isolation operators",
    )
    hidden_world: bpy.props.PointerProperty(type=bpy.types.World, name="Hidden World")
    hidden_world_fake_user: bpy.props.BoolProperty()
    
### REGISTER ---

def register():
    bpy.utils.register_class(LIGHTSETTER_PR_object_props)
    bpy.utils.register_class(LIGHTSETTER_PR_scene_props)
    bpy.types.Object.lightsetter_object_properties = \
        bpy.props.PointerProperty(type = LIGHTSETTER_PR_object_props, name="Light Helper Object Properties")
    bpy.types.Scene.lightsetter_scene_properties = \
        bpy.props.PointerProperty(type = LIGHTSETTER_PR_scene_props, name="Light Helper Scene Properties")

def unregister():
    bpy.utils.unregister_class(LIGHTSETTER_PR_object_props)
    bpy.utils.unregister_class(LIGHTSETTER_PR_scene_props)
    del bpy.types.Object.lightsetter_object_properties
    del bpy.types.Scene.lightsetter_scene_properties
