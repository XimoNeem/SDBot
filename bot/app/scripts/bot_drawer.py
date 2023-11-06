from scripts.bot_pages import *
from scripts.bot_config import config_requestUrl, config_negativePrompt
import asyncio
import requests_async as requests
import scripts.bot_db_handler

async def draw_image(user_id:int, prompts:str, action_onFailure, action_arg1, action_arg2, action_arg3) -> str:
    print(user_id)
    user = scripts.bot_db_handler.get_user(user_id)

    if user.tockens < 1:
        await action_onFailure(user_id, action_arg1)
        await action_onFailure(user_id, action_arg2)
        return None
    else:
        payload = {
            "prompt": prompts,
            "negative_prompt": config_negativePrompt,
        }

        try:    
            response = await requests.post(url=config_requestUrl, json=payload)

            if response.status_code == 200:
                user.subtract_tocken()

                return response.json['images'][0]
            else:
                print('[ERROR] no host')
                await action_onFailure(user_id, action_arg3)


        except:
            print('[ERROR] no host')
            await action_onFailure(user_id, action_arg3)




# {
#   "prompt": "",
#   "negative_prompt": "",
#   "styles": [
#     "string"
#   ],
#   "seed": -1,
#   "subseed": -1,
#   "subseed_strength": 0,
#   "seed_resize_from_h": -1,
#   "seed_resize_from_w": -1,
#   "sampler_name": "string",
#   "batch_size": 1,
#   "n_iter": 1,
#   "steps": 50,
#   "cfg_scale": 7,
#   "width": 512,
#   "height": 512,
#   "restore_faces": true,
#   "tiling": true,
#   "do_not_save_samples": false,
#   "do_not_save_grid": false,
#   "eta": 0,
#   "denoising_strength": 0,
#   "s_min_uncond": 0,
#   "s_churn": 0,
#   "s_tmax": 0,
#   "s_tmin": 0,
#   "s_noise": 0,
#   "override_settings": {},
#   "override_settings_restore_afterwards": true,
#   "refiner_checkpoint": "string",
#   "refiner_switch_at": 0,
#   "disable_extra_networks": false,
#   "comments": {},
#   "enable_hr": false,
#   "firstphase_width": 0,
#   "firstphase_height": 0,
#   "hr_scale": 2,
#   "hr_upscaler": "string",
#   "hr_second_pass_steps": 0,
#   "hr_resize_x": 0,
#   "hr_resize_y": 0,
#   "hr_checkpoint_name": "string",
#   "hr_sampler_name": "string",
#   "hr_prompt": "",
#   "hr_negative_prompt": "",
#   "sampler_index": "Euler",
#   "script_name": "string",
#   "script_args": [],
#   "send_images": true,
#   "save_images": false,
#   "alwayson_scripts": {}
# }