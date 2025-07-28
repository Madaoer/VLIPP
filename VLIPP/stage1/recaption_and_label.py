from openai import OpenAI
from pathlib import Path
import json
import re
import os
import argparse
from VLIPP.utils.helpers import encode_image, get_vlm_plan_to_json, io_from_json
from VLIPP.utils.template import messages

def get_recaption_and_label(prompt, first_frame_path, exp_name):
    '''
    Generates a refined video description, identifies key physical objects, 
    and assigns a category label based on an input prompt and first-frame image.

    Parameters:
        prompt (str): The input text describing the video scene.
        first_frame_path (str): Path to the first frame image, used for visual context.
        exp_name (str): The experiment name for logging or identification.

    Returns:
        dict: A dictionary containing:
            - "recaption": The refined video prompt.
            - "key_physic_object": Identified important object(s) in the scene.
            - "category": The semantic category for the scene.
            - "exp_name": The experiment name passed as input.
    '''

    openai_api_key = os.getenv("OPENAI_API_KEY")

    # Initialize the OpenAI API client
    client = OpenAI(
        api_key=openai_api_key,
        base_url="https://api.openai.com/v1"
    )

    # Convert the first frame image to a base64-encoded string
    first_frame_b64_str = encode_image(first_frame_path)

    # Inject the image and prompt into the last message template
    messages[-1]['content'][0]['image'] = first_frame_b64_str
    messages[-1]["content"][-1]["text"] = f"""{prompt}"""

    print("Processing: ", prompt)

    # Send the prompt and image to the GPT-4o model for interpretation
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
    )

    # Extract the model's response text
    output_string = response.choices[0].message.content

    # Use regular expressions to extract the desired fields from the output
    refine_video_prompt_match = re.search(
        r'refine_video_prompt:\s*(.*?)\s*(?=key_physic_object:)', 
        output_string, re.DOTALL
    )
    key_physic_object_match = re.search(
        r'key_physic_object:\s*"(.*?)"', 
        output_string
    )
    category_match = re.search(
        r'category:\s*(.*)', 
        output_string
    )

    # Extract matched groups or default to empty strings
    refine_video_prompt = refine_video_prompt_match.group(1).strip() if refine_video_prompt_match else ""
    key_physic_object = key_physic_object_match.group(1).strip() if key_physic_object_match else ""
    category = category_match.group(1).strip() if category_match else ""

    # Construct the final result dictionary
    info_dict = {
        "recaption": refine_video_prompt,
        "key_physic_object": key_physic_object,
        "category": category,
        "exp_name": exp_name
    }

    return info_dict


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recaption and label video prompts.")
    parser.add_argument("--prompt", type=str, required=True, help="The input prompt for the video scene.")
    parser.add_argument("--data_root", type=str, required=True, help="The input prompt for the video scene.")
    parser.add_argument("--exp_name", type=str, required=True, help="The input prompt for the video scene.")
    parser.add_argument("--first_frame_path", type=str, required=True, help="The input prompt for the video scene.")
    
    args = parser.parse_args()
    
    prompt = args.prompt
    data_root = Path(args.data_root)
    exp_name = args.exp_name
    first_frame_path = args.first_frame_path
    
    output_json_path = data_root / 'json' / f'{exp_name}.json'
    output_json_root = output_json_path.parent
    output_json_root.mkdir(parents=True, exist_ok=True)

    prompt = 'Pouring orange juice into a glass.'
    result = get_recaption_and_label(prompt, first_frame_path, exp_name)
    io_from_json(output_json_path, data=result, io_type='w')
    