from openai import OpenAI
import openai
import json
import os
import argparse
from pathlib import Path
from PIL import Image
import base64
from VLIPP.utils.template import template_library
from VLIPP.utils.helpers import encode_image, get_vlm_plan_to_json, io_from_json


def vlm_planning(data_dict):
    """
    Performs visual-language model (VLM) based motion planning using GPT-4o,
    conditioned on an input image, segmentation map, and object annotations.

    This function constructs a prompt using visual inputs and a natural language caption,
    sends it to OpenAI's GPT-4o, and parses its structured output to generate
    a frame-by-frame plan of object movements or changes.

    Parameters:
        data_dict (dict): A dictionary containing:
            - 'first_frame': Path to the original image.
            - 'seg_mask_path': Path to the segmentation map.
            - 'annotations': List of object bounding box annotations.
            - 'recaption': Refined caption/description of the scene.
            - 'category': Physics-based tag for selecting prompt templates.

    Returns:
        dict: Updated `data_dict` with an additional field 'vlm_planning', which contains:
            - 'Reasoning': The raw text output from GPT-4o.
            - 'Frames': Parsed frame-by-frame bounding box predictions.
    """
    openai_api_key = os.getenv("OPENAI_API_KEY")

    # Initialize OpenAI API client
    client = OpenAI(
        api_key=openai_api_key,
        base_url="https://api.openai.com/v1"
    )

    # Load image paths
    first_frame = data_dict['first_frame']
    first_frame_seg = data_dict['seg_mask_path']

    # Construct bounding box list with IDs and names
    first_frame_box = []
    for idx, annotation in enumerate(data_dict['annotations']):
        box_info = {
            "id": idx,
            "name": annotation['class_name'],
            "box": annotation['bbox']
        }
        first_frame_box.append(box_info)

    # Encode images to base64 strings for use in GPT-4o image input
    first_frame_b64_str = encode_image(first_frame)
    first_frame_seg_b64_str = encode_image(first_frame_seg)

    # Retrieve natural language prompt and physics tag (e.g., "collision", "falling")
    prompt = data_dict['recaption']
    physic_tag = data_dict['category']

    # Load prompt template based on physics category
    messages = template_library[physic_tag]

    messages[-1]['content'][0]['image'] = first_frame_b64_str
    messages[-1]['content'][1]['image'] = first_frame_seg_b64_str

    messages[-1]["content"][2]["text"] = f"""initial_boxes: {first_frame_box}\ncaption: {prompt}"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
    )

    # Extract the text response from GPT
    output_text = response.choices[0].message.content

    # Parse the GPT response into a structured format
    bboxs = get_vlm_plan_to_json(output_text)

    # Compose the result dictionary
    results = {
        "Reasoning": output_text,
        "Frames":  bboxs
    }

    # Add VLM planning result to the original input dictionary
    data_dict['vlm_planning'] = results

    return data_dict


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recaption and label video prompts.")
    parser.add_argument("--exp_name", type=str, required=True, help="The input prompt for the video scene.")
    parser.add_argument("--data_root", type=str, required=True, help="The input prompt for the video scene.")
    # parser.add_argument("--openai_api_key", type=str, required=True, help="OpenAI API key for authentication.")
    
    args = parser.parse_args()
    
    exp_name = args.exp_name
    data_root = Path(args.data_root)
    
        
    input_json_path = data_root / 'json' / f'{exp_name}_2.json'
    output_json_path = data_root / 'json' / f'{exp_name}_3.json'
            
    info_json = io_from_json(input_json_path, io_type='r')

    openai_api_key = os.getenv("OPENAI_API_KEY")

    client = OpenAI(
        api_key=openai_api_key,
        base_url="https://api.openai.com/v1"
    )


    first_frame = info_json['first_frame']
    first_frame_seg = info_json['seg_mask_path']
    
    
    first_frame_box = []
    for idx, annotation in enumerate(info_json['annotations']):
        box_info = {
            "id": idx,
            "name": annotation['class_name'],
            "box": annotation['bbox']
        }
        first_frame_box.append(box_info)

    img_type = "image/jpeg"
    first_frame_b64_str = encode_image(first_frame)
    first_frame_seg_b64_str = encode_image(first_frame_seg)
    
    prompt = info_json['recaption']
    physic_tag = info_json['category']
    messages = template_library[physic_tag]
    
    messages[-1]['content'][0]['image'] = first_frame_b64_str
    messages[-1]['content'][1]['image'] = first_frame_seg_b64_str
    messages[-1]["content"][2]["text"] = f"""initial_boxes: {first_frame_box}\ncaption: {prompt}"""
    
    
    response = client.chat.completions.create(
        model="gpt-4o", 
        messages=messages,
    )

    output_text = response.choices[0].message.content
    
    bboxs = get_vlm_plan_to_json(output_text)
    
    results = {
        "Reasoning": output_text,
        "Frames":  bboxs
    }
    
    info_json['vlm_planning'] = results
    io_from_json(output_json_path, data=info_json, io_type='w')
        
        

