from launch_rendering import convert_config
from converter import parse_vray_text
config = parse_vray_text.generate_config("543", "420042")
asset = parse_vray_text.get_config_asset(config)
if not asset:
    convert_config(config)
asset = parse_vray_text.get_config_asset(config)

import vray
renderer = vray.Renderer()
renderer.load('templates/preview_2018/preview_2018.vrscene')
from renderer.VRayFurniture import VRayFurniture
furniture = VRayFurniture(renderer=renderer, config_data=asset)
renderer.start()
renderer.waitForRenderEnd()
