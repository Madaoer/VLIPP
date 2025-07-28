import argparse
from VLIPP.stage1 import get_recaption_and_label, detect_and_segment, vlm_planning, VideoSimulator 
from VLIPP.utils.helpers import io_from_json
from pathlib import Path
from sam2.build_sam import build_sam2
from sam2.sam2_image_predictor import SAM2ImagePredictor
from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection


def parse_args():
    parser = argparse.ArgumentParser(description="A simple argument parser example.")
    
    parser.add_argument('--exp_name', type=str, required=True, help='Name of the experiment')
    parser.add_argument('--prompt', type=str, required=True, help='Text prompt that describes the video')
    parser.add_argument('--data_root', required=True, help='dataset root')
    parser.add_argument('--first_frame_path', required=True, help='File path to the first frame image of the video sequence')
    parser.add_argument('--grounding_model_path', required=True, help='File path to the first frame image of the video sequence')
    parser.add_argument('--sam2_checkpoint', required=True, help='File path to the first frame image of the video sequence')
    parser.add_argument('--sam2_model_config', default="configs/sam2.1/sam2.1_hiera_l.yaml", help='File path to the first frame image of the video sequence')
    
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()
    
    exp_name = args.exp_name
    prompt = args.prompt
    data_root = Path(args.data_root)
    first_frame_path = args.first_frame_path

    output_json_path = data_root / 'json' / f'{exp_name}.json'
    output_json_root = output_json_path.parent
    output_json_root.mkdir(parents=True, exist_ok=True)

    # --- step 1 ---
    data_dict = get_recaption_and_label(prompt, first_frame_path, exp_name)
    
    # --- step 2 ---
    data_dict['first_frame'] = first_frame_path
    sam2_model_config = args.sam2_model_config
    sam2_checkpoint = args.sam2_checkpoint
    grounding_model_path = args.grounding_model_path
    detection_root = data_root / 'detections'
    output_root = detection_root / f'{exp_name}'
    
    DEVICE = "cuda"
    sam2_model = build_sam2(sam2_model_config, sam2_checkpoint, device=DEVICE)
    sam2_predictor = SAM2ImagePredictor(sam2_model)

    processor = AutoProcessor.from_pretrained(grounding_model_path)
    grounding_model = AutoModelForZeroShotObjectDetection.from_pretrained(grounding_model_path).to(DEVICE)
    data_dict = detect_and_segment(data_dict, output_root=output_root, sam2_predictor=sam2_predictor, processor=processor, grounding_model=grounding_model)
    
    # --- step 3 ---
    data_dict = vlm_planning(data_dict)
    io_from_json(output_json_path, data_dict, io_type='w')
    
    # --- step 4 ---
    simulator = VideoSimulator(frame_width=720, frame_height=480)
    output_dir = data_root / 'animation_video'
    output_dir.mkdir(parents=True, exist_ok=True)
    output_video_path = output_dir / f'{exp_name}.mp4'
    sim_data = data_dict['vlm_planning']
    simulate_video_path = simulator.process_simulation(
        sim_data, first_frame_path, output_video_path
    )