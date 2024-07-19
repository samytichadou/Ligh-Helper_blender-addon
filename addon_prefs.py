import bpy


# addon preferences
class LIGHTHELPER_PF_addon_prefs(bpy.types.AddonPreferences):
    bl_idname = __package__

    def draw(self, context):
        layout = self.layout

        # donate
        op=layout.operator("wm.url_open", text="Donate", icon="FUND")
        op.url="https://ko-fi.com/tonton_blender"


### REGISTER ---
def register():
    bpy.utils.register_class(LIGHTHELPER_PF_addon_prefs)
def unregister():
    bpy.utils.unregister_class(LIGHTHELPER_PF_addon_prefs)
