EXP_NAME="pour_juice"
DATA_ROOT="cached_example"

python -m VLIPP.stage2.make_warped_noise "$DATA_ROOT" --exp_name "$EXP_NAME"

python -m VLIPP.stage2.generate_video "$DATA_ROOT" \
    --exp_name "$EXP_NAME" \
    --device "cuda" \
    --num_inference_steps 30 \
    