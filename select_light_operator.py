import bpy

from .gui import get_lights_objects

def unisolate(target_light, light_list, scn):
    scn_props=scn.lightsetter_scene_properties
    target_light.hide_viewport=target_light.lightsetter_object_properties.hidden_viewport
    target_light.hide_render=target_light.lightsetter_object_properties.hidden_render

    for ob in light_list:
        if ob!=target_light:
            ob.hide_viewport=ob.lightsetter_object_properties.hidden_viewport
            ob.hide_render=ob.lightsetter_object_properties.hidden_render
    scn_props.isolated_light=None

    # World
    if scn_props.hidden_world:
        scn.world=scn_props.hidden_world
        scn.world.use_fake_user=scn_props.hidden_world_fake_user
        scn_props.hidden_world=None


class LIGHTSETTER_OT_select_isolate_light(bpy.types.Operator):
    """Click - Select \nShift Click - Add to Selection\nAlt Click - Isolate"""
    bl_idname = "lightsetter.select_isolate_light"
    bl_label = "Select/Isolate Light"
    bl_options = {"UNDO","INTERNAL"}

    light_name: bpy.props.StringProperty()
    shift=False
    alt=False

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        if event.alt:
            self.alt=True
        elif event.shift:
            self.shift=True
        return self.execute(context)
 
    def execute(self, context):
        light_list=get_lights_objects(context)
        scn=context.scene
        scn_props=scn.lightsetter_scene_properties

        # Unisolate
        if self.light_name=="":
            target_light=scn_props.isolated_light
            unisolate(target_light,light_list,scn)
            self.report({'INFO'}, "Lights restored")
            return {'FINISHED'}

        # Selection
        if not self.alt:
            # Get light if exists
            chk_exist=False
            for ob in light_list:
                if ob.name==self.light_name:
                    ob.select_set(True)
                    context.view_layer.objects.active=ob
                    chk_exist=True
                    break

            # Check if light exists
            if not chk_exist:
                self.report({'WARNING'}, "Unable to find light")
                return {'FINISHED'}

            # Deselect all other objects
            if not self.shift:
                for ob in light_list:
                    if ob.name!=self.light_name:
                        ob.select_set(False)

            self.report({'INFO'}, "%s selected" % self.light_name)

        # Isolation
        else:
            target_light=None
            de_isolate=False

            # Get light if exists
            for ob in light_list:
                if ob.name==self.light_name:
                    target_light=ob
                    break

            # Check if light exists
            if target_light is None:
                self.report({'WARNING'}, "Unable to find light")
                return {'FINISHED'}

            # Check for isolate toggle
            if scn_props.isolated_light==target_light:
                de_isolate=True

            # De Isolate
            if de_isolate:
                unisolate(target_light,light_list,scn)
                self.report({'INFO'}, "Lights restored")

            # Isolate
            else:

                # Lights
                if scn_props.isolated_light is None:
                    target_light.lightsetter_object_properties.hidden_viewport=target_light.hide_viewport
                    target_light.lightsetter_object_properties.hidden_render=target_light.hide_render
                target_light.hide_viewport=target_light.hide_render=False

                for ob in light_list:
                    if ob!=target_light:
                        if scn_props.isolated_light is None:
                            ob.lightsetter_object_properties.hidden_viewport=ob.hide_viewport
                            ob.lightsetter_object_properties.hidden_render=ob.hide_render
                        ob.hide_viewport=ob.hide_render=True

                scn_props.isolated_light=target_light

                # World
                if scn_props.include_world:
                    if scn.world:
                        scn_props.hidden_world=scn.world
                        scn_props.hidden_world_fake_user=scn.world.use_fake_user
                        scn.world.use_fake_user=True
                        scn.world=None

                self.report({'INFO'}, "%s isolated" % self.light_name)

        return {'FINISHED'}


def register():
    bpy.utils.register_class(LIGHTSETTER_OT_select_isolate_light)

def unregister():
    bpy.utils.unregister_class(LIGHTSETTER_OT_select_isolate_light)
