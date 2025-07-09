export OPENAI_API_KEY="{Your OpenAI Key here}"

EXP_NAME="{Your exp name here}"
PROMPT="{Your prompt here}"
DATA_ROOT="data"
FIRST_FRAME_PATH="{Your first frame path here}"
GROUNDING_MODEL_PATH="IDEA-Research/grounding-dino-tiny"
SAM2_CHECKPOINT="./checkpoints/sam2.1_hiera_large.pt"

python -m VLIPP.stage1.stage1 --prompt "$PROMPT" \
               --data_root "$DATA_ROOT" \
               --first_frame_path "$FIRST_FRAME_PATH" \
               --exp_name "$EXP_NAME" \
               --grounding_model_path "$GROUNDING_MODEL_PATH" \
               --sam2_checkpoint "$SAM2_CHECKPOINT"