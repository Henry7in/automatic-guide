import bpy
import re
import os
import json
import urllib.request
import urllib.error

def get_api_key(context, addon_name):
    preferences = context.preferences
    addon_prefs = preferences.addons[addon_name].preferences
    return addon_prefs.api_key


def init_props():
    bpy.types.Scene.gpt4_chat_history = bpy.props.CollectionProperty(type=bpy.types.PropertyGroup)
    bpy.types.Scene.gpt4_model = bpy.props.EnumProperty(
        name="Model",
        description="Select the model to use",
        items=[
            ("deepseek-chat", "DeepSeek Chat (fast)", "Use DeepSeek Chat model"),
            ("deepseek-reasoner", "DeepSeek Reasoner (smart)", "Use DeepSeek Reasoner model"),
        ],
        default="deepseek-chat",
    )
    bpy.types.Scene.gpt4_chat_input = bpy.props.StringProperty(
        name="Message",
        description="Enter your message",
        default="",
    )
    bpy.types.Scene.gpt4_button_pressed = bpy.props.BoolProperty(default=False)
    bpy.types.PropertyGroup.type = bpy.props.StringProperty()
    bpy.types.PropertyGroup.content = bpy.props.StringProperty()

def clear_props():
    del bpy.types.Scene.gpt4_chat_history
    del bpy.types.Scene.gpt4_chat_input
    del bpy.types.Scene.gpt4_button_pressed


def generate_blender_code(prompt, chat_history, context, system_prompt, addon_name=None):
    if not addon_name:
        addon_name = __name__.rsplit('.', 1)[0]
    
    api_key = get_api_key(context, addon_name)
    if not api_key:
        api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise Exception("No API key. Set DeepSeek API Key in addon preferences.")

    model = context.scene.gpt4_model

    # Build messages
    messages = [{"role": "system", "content": system_prompt}]
    for message in chat_history[-10:]:
        if message.type == "assistant":
            messages.append({"role": "assistant", "content": "```\n" + message.content + "\n```"})
        else:
            messages.append({"role": message.type.lower(), "content": message.content})

    messages.append({"role": "user", "content": "Can you please write Blender code for me that accomplishes the following task: " + prompt + "? Do not respond with anything that is not Python code."})

    # Setup request
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": messages,
        "stream": True,
        "max_tokens": 1500,
    }

    if model == "deepseek-reasoner":
        payload["max_completion_tokens"] = 4000

    api_url = "https://api.deepseek.com/chat/completions"

    # Make request using urllib
    req = urllib.request.Request(api_url, data=json.dumps(payload).encode('utf-8'), headers=headers)
    
    completion_text = ""
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            for line in response:
                line = line.decode('utf-8').strip()
                if not line or not line.startswith("data: "):
                    continue
                data_str = line[6:]
                if data_str == "[DONE]":
                    break
                try:
                    data = json.loads(data_str)
                    delta = data.get("choices", [{}])[0].get("delta", {})
                    content = delta.get("content", "")
                    if content:
                        completion_text += content
                        print(completion_text, flush=True, end="\r")
                except:
                    continue

        # Extract code
        code_blocks = re.findall(r'```(?:python)?(.*?)```', completion_text, re.DOTALL)
        if code_blocks:
            return code_blocks[0].strip()
        return None
    except urllib.error.HTTPError as e:
        error_text = e.read().decode('utf-8')
        try:
            err_json = json.loads(error_text)
            error_msg = err_json.get("error", {}).get("message", error_text)
        except:
            error_msg = error_text
        raise Exception(f"DeepSeek API error ({e.code}): {error_msg}")
    except Exception as e:
        raise Exception(f"Failed: {str(e)}")


def split_area_to_text_editor(context):
    area = context.area
    for region in area.regions:
        if region.type == 'WINDOW':
            override = {'area': area, 'region': region}
            bpy.ops.screen.area_split(override, direction='VERTICAL', factor=0.5)
            break

    new_area = context.screen.areas[-1]
    new_area.type = 'TEXT_EDITOR'
    return new_area
