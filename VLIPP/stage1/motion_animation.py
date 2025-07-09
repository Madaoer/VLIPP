import os
import cv2
import numpy as np
import json
import argparse
import ast
from typing import Dict, List, Tuple, Optional
from pathlib import Path
from VLIPP.utils.helpers import io_from_json


class VideoSimulator:
    def __init__(self, frame_width: int = 720, frame_height: int = 480):
        """Initialize the simulator with the target frame size."""
        self.frame_width = frame_width
        self.frame_height = frame_height

    def clip_bbox(self, bbox: List[float]) -> Optional[List[float]]:
        """
        Clip a bounding box to stay within image boundaries.
        If the box lies completely outside, return None.
        """
        x1, y1, x2, y2 = bbox
        x1, x2 = min(x1, x2), max(x1, x2)
        y1, y2 = min(y1, y2), max(y1, y2)

        x1 = max(0, min(x1, self.frame_width))
        y1 = max(0, min(y1, self.frame_height))
        x2 = max(0, min(x2, self.frame_width))
        y2 = max(0, min(y2, self.frame_height))

        if x1 >= x2 or y1 >= y2:
            return None
        return [x1, y1, x2, y2]

    def read_bbox_json(self, sim_data: Dict) -> Tuple[Dict, Dict]:
        """
        Parse bounding boxes from JSON, supporting dynamic object appearance.

        Returns:
            frames (dict): Maps frame number to list of objects with valid bboxes.
            object_appearance (dict): Maps object ID to the first frame it appears in.
        """
        frames = {}
        object_appearance = {}
        raw_frames = sim_data.get("Frames", {})

        for frame_str, objects in raw_frames.items():
            try:
                frame_no = int(frame_str)
            except Exception as e:
                print(f"Failed to parse frame number {frame_str}: {e}")
                continue

            frame_objects = []
            for obj in objects:
                bbox = obj.get("bbox", obj.get("box"))
                if not bbox or len(bbox) != 4:
                    print(f"Invalid object data: {obj}")
                    continue

                x, y, w, h = bbox
                new_bbox = self.clip_bbox([x, y, x + w, y + h])
                if new_bbox is None:
                    continue

                obj["bbox"] = new_bbox
                obj_id = obj.get("id", str(hash(str(obj))))

                if obj_id not in object_appearance:
                    object_appearance[obj_id] = frame_no

                frame_objects.append(obj)

            frames[frame_no] = frame_objects

        return frames, object_appearance

    def build_bbox_array(self, frames: Dict, object_appearance: Dict) -> np.ndarray:
        """
        Construct a 3D array of bounding boxes with shape (num_frames, num_objects, 4).
        Missing objects in a frame are filled with zeros.
        """
        all_frame_nos = sorted(frames.keys())
        all_object_ids = sorted(object_appearance.keys())
        num_frames = len(all_frame_nos)
        num_objects = len(all_object_ids)

        bboxes = np.zeros((num_frames, num_objects, 4), dtype=np.float32)
        frame_idx_map = {frame_no: idx for idx, frame_no in enumerate(all_frame_nos)}

        for obj_idx, obj_id in enumerate(all_object_ids):
            first_frame = object_appearance[obj_id]
            for frame_no in range(first_frame, all_frame_nos[-1] + 1):
                if frame_no not in frames:
                    continue
                for obj in frames[frame_no]:
                    if obj.get("id", str(hash(str(obj)))) == obj_id:
                        frame_idx = frame_idx_map[frame_no]
                        bboxes[frame_idx, obj_idx] = obj["bbox"]
                        break

        return bboxes

    def interpolate_bboxes(self, bboxes: np.ndarray, target_frames: int = 49) -> np.ndarray:
        """
        Interpolate bounding box positions over the specified number of target frames.
        Missing values are interpolated linearly across time.
        """
        num_frames, object_count, _ = bboxes.shape
        interpolated = np.zeros((target_frames, object_count, 4), dtype=np.float32)
        orig_indices = np.linspace(0, target_frames - 1, num=num_frames)
        target_indices = np.arange(target_frames)

        for obj in range(object_count):
            for coord in range(4):
                valid_indices = np.where(bboxes[:, obj, coord] != 0)[0]
                if len(valid_indices) > 1:
                    interpolated[:, obj, coord] = np.interp(
                        target_indices,
                        orig_indices[valid_indices],
                        bboxes[valid_indices, obj, coord]
                    )
        return interpolated

    def inpaint_frame(self, frame: np.ndarray, bbox_list: List[List[float]]) -> np.ndarray:
        """
        Remove objects from the frame using OpenCV inpainting.
        This is used to create a clean background.
        """
        mask = np.zeros(frame.shape[:2], dtype=np.uint8)
        for bbox in bbox_list:
            x1, y1, x2, y2 = [int(round(v)) for v in bbox]
            cv2.rectangle(mask, (x1, y1), (x2, y2), 255, thickness=-1)
        inpainted = cv2.inpaint(frame, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)
        return inpainted

    def extract_object(self, frame: np.ndarray, bbox: List[float]) -> Optional[np.ndarray]:
        """
        Crop an object from the frame using the bounding box.
        Returns None if the box is invalid.
        """
        x1, y1, x2, y2 = [int(round(v)) for v in bbox]
        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(frame.shape[1], x2)
        y2 = min(frame.shape[0], y2)

        if x1 >= x2 or y1 >= y2:
            return None

        return frame[y1:y2, x1:x2]

    def process_simulation(
        self,
        sim_data: Dict,
        first_frame_path: str,
        output_video_path: str,
        total_frames: int = 49,
        fps: int = 16
    ) -> Optional[str]:
        """
        Generate a video by animating object movement using interpolated bounding boxes.

        Steps:
        - Load and parse input JSON
        - Extract and inpaint the background
        - Crop object images
        - Paste each object at its new location in each frame
        - Write out a video

        Returns:
            str: Path to the saved video, or None on failure.
        """
        frames, object_appearance = self.read_bbox_json(sim_data)
        if not frames:
            print(f"{sim_data.get('video_id')} contains no valid frame data.")
            return None

        try:
            bboxes = self.build_bbox_array(frames, object_appearance)
        except Exception as e:
            print(f"Failed to build bbox array: {e}")
            return None

        first_frame = cv2.imread(first_frame_path)
        if first_frame is None:
            print(f"Failed to load image: {first_frame_path}")
            return None

        first_frame = cv2.resize(first_frame, (self.frame_width, self.frame_height))
        height, width = first_frame.shape[:2]

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

        all_object_ids = sorted(object_appearance.keys())
        num_objects = len(all_object_ids)

        object_images = [None] * num_objects
        object_initial_bboxes = [None] * num_objects

        for obj_idx, obj_id in enumerate(all_object_ids):
            first_frame_no = object_appearance[obj_id]
            if first_frame_no in frames:
                for obj in frames[first_frame_no]:
                    if obj.get("id", str(hash(str(obj)))) == obj_id:
                        bbox = obj["bbox"]
                        object_initial_bboxes[obj_idx] = bbox
                        object_images[obj_idx] = self.extract_object(first_frame, bbox)
                        break

        interpolated_bboxes = self.interpolate_bboxes(bboxes, target_frames=total_frames)

        background_bboxes = [bbox for bbox in object_initial_bboxes if bbox is not None]
        background = self.inpaint_frame(first_frame, background_bboxes)

        for frame_index in range(total_frames):
            frame = background.copy()

            for obj_idx in range(num_objects):
                bbox = interpolated_bboxes[frame_index, obj_idx]
                if np.all(bbox == 0) or object_images[obj_idx] is None:
                    continue

                x1, y1, x2, y2 = bbox
                new_x = int(round(x1))
                new_y = int(round(y1))
                new_w = int(round(x2 - x1))
                new_h = int(round(y2 - y1))

                if new_w <= 0 or new_h <= 0:
                    continue

                try:
                    resized_obj = cv2.resize(object_images[obj_idx], (new_w, new_h))
                except:
                    continue

                if (new_y >= height or new_x >= width or 
                    new_y + new_h <= 0 or new_x + new_w <= 0):
                    continue

                paste_y1 = max(0, new_y)
                paste_x1 = max(0, new_x)
                paste_y2 = min(height, new_y + new_h)
                paste_x2 = min(width, new_x + new_w)

                obj_y1 = max(0, -new_y)
                obj_x1 = max(0, -new_x)
                obj_y2 = min(new_h, height - new_y)
                obj_x2 = min(new_w, width - new_x)

                if (obj_x1 >= obj_x2 or obj_y1 >= obj_y2 or 
                    paste_x1 >= paste_x2 or paste_y1 >= paste_y2):
                    continue

                frame[paste_y1:paste_y2, paste_x1:paste_x2] = \
                    resized_obj[obj_y1:obj_y2, obj_x1:obj_x2]

            writer.write(frame)

        writer.release()
        print(f"Video saved to {output_video_path}")
        return output_video_path





if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Recaption and label video prompts.")
    parser.add_argument("--data_root", type=str, required=True, help="The input prompt for the video scene.")
    parser.add_argument("--exp_name", type=str, required=True, help="The input prompt for the video scene.")
    
    args = parser.parse_args()
    
    data_root = Path(args.data_root)
    exp_name = args.exp_name
    
    simulator = VideoSimulator(frame_width=720, frame_height=480)
    
    output_dir = data_root / 'animation_video'
    output_dir.mkdir(parents=True, exist_ok=True)
    

    input_json_path = data_root / 'json' / f'{exp_name}_3.json'
    info_json = io_from_json(input_json_path, io_type='r')
    exp_name = info_json['exp_name']
    output_video_path = output_dir / f'{exp_name}.mp4'
    
    sim_data = info_json['vlm_planning']
    first_frame_path = info_json['first_frame']
    simulate_video_path = simulator.process_simulation(
        sim_data, first_frame_path, output_video_path
    )