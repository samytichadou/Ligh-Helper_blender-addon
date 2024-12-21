import bpy

def get_lights_objects(context):
    light_list=[]
    for obj in context.view_layer.objects:
        if obj.type=='LIGHT':
            light_list.append(obj)
    return light_list

def return_light_icon(data):
    return 'LIGHT_%s' % data.type

def get_selection_icon(ob,context):
    isolated_light=context.scene.lightsetter_scene_properties.isolated_light
    if isolated_light is not None:
        if ob==isolated_light:
            return "OUTLINER_OB_LIGHT"
        else:
            return "DOT"
    if context.view_layer.objects.active==ob:
        if ob.select_get():
            return "PROP_CON"
        else:
            return "PROP_OFF"
    elif ob.select_get():
        return "RADIOBUT_ON"
    else:
        return "RADIOBUT_OFF"

def draw_common_light_props(container, light_data):
    container.prop(light_data.cycles, "max_bounces")
    container.prop(light_data.cycles, "cast_shadow")

def draw_point_light_settings(container, light_data):
    # Radius, Max bounce, Cast shadow
    col=container.column(align=True)

    row=col.row(align=True)
    row.prop(light_data, "shadow_soft_size", text="Radius")

    row=col.row(align=True)
    draw_common_light_props(row, light_data)

def draw_sun_light_settings(container, light_data):
    # Angle, Max bounce, Cast shadow
    col=container.column(align=True)

    row=col.row(align=True)
    row.prop(light_data, "angle")

    row=col.row(align=True)
    draw_common_light_props(row, light_data)

def draw_spot_light_settings(container, light_data):
    # Radius, Max bounce, Cast shadow, Spot size, Spot blend, Show cone
    col=container.column(align=True)

    row=col.row(align=True)
    row.prop(light_data, "shadow_soft_size", text="Radius")
    row.prop(light_data, "spot_size")
    
    row=col.row(align=True)
    row.prop(light_data, "spot_blend")
    row.prop(light_data, "show_cone")
    
    row=col.row(align=True)
    draw_common_light_props(row, light_data)

def draw_area_light_settings(container, light_data):
    # Shape, Size X Y, Max bounce, Cast shadow, Spread
    col=container.column(align=True)

    row=col.row(align=True)
    row.prop(light_data, "shape", text="")
    row.prop(light_data, "size")

    row=col.row(align=True)
    if light_data.shape in {"RECTANGLE","ELLIPSE"}:
        row.prop(light_data, "size_y")
    row.prop(light_data, "spread")
    
    row=col.row(align=True)
    draw_common_light_props(row, light_data)


class LIGHTSETTER_PT_manager(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Lights"
    bl_label = "Light Manager"

    def draw_header(self, context):
        layout = self.layout

        scn_props=context.scene.lightsetter_scene_properties
        if scn_props.isolated_light is None:
            layout.label(text="", icon="LIGHT")
        else:
            layout.alert=True
            op=layout.operator('lightsetter.select_isolate_light',text="",icon="OUTLINER_OB_LIGHT")
            op.light_name=""

    def draw(self, context):
        scn=context.scene
        props=scn.lightsetter_scene_properties
        isolated_light=props.isolated_light
        layout = self.layout

        row=layout.row(align=True)
        if props.hidden_world is not None:
            row.enabled=False
        row.prop(props, "include_world", text="")
        row.template_ID(scn, "world", new="world.new")

        col=layout.column(align=True)

        lights=get_lights_objects(context)
        for light in lights:
            props=light.lightsetter_object_properties

            box=col.box()

            not_isolated=False
            if isolated_light is not None:
                if isolated_light!=light:
                    not_isolated=True
                else:
                    box.alert=True

            row=box.row(align=True)

            if props.hide_panel:
                icon="RIGHTARROW_THIN"
            else:
                icon="DOWNARROW_HLT"
            row.prop(props,'hide_panel',text="",icon=icon,emboss=False)

            # Light Selector
            op=row.operator(
                'lightsetter.select_isolate_light',
                text="",
                icon=get_selection_icon(light,context),
                emboss=False,
            )
            op.light_name=light.name

            # Light Name
            row.prop(light, 'name', text="", icon=return_light_icon(light.data), emboss=True)
            
            # Base props
            row.separator()
            sub=row.row(align=True)
            sub.scale_x=0.25
            sub.prop(light.data, 'color', text="")
            row.prop(light.data, 'energy', text="")
            
            # Hide props
            row.separator()
            sub=row.row()
            sub.scale_x=0.75
            sub.prop(light, 'hide_select', text="", emboss=False)
            sub.prop(light, 'hide_viewport', text="", emboss=False)
            sub.prop(light, 'hide_render', text="", emboss=False)

            if not props.hide_panel:
                # box=col.box()
                if light.data.type=="POINT":
                    draw_point_light_settings(box, light.data)
                elif light.data.type=="SUN":
                    draw_sun_light_settings(box, light.data)
                elif light.data.type=="SPOT":
                    draw_spot_light_settings(box, light.data)
                elif light.data.type=="AREA":
                    draw_area_light_settings(box, light.data)


def register():
    bpy.utils.register_class(LIGHTSETTER_PT_manager)

def unregister():
    bpy.utils.unregister_class(LIGHTSETTER_PT_manager)
