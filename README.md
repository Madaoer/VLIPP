# VLIPP: Towards Physically Plausible Video Generation with Vision and Language Informed Physical Prior
### [Project Page](https://madaoer.github.io/projects/physically_plausible_video_generation/) | [Paper](https://arxiv.org/abs/2503.23368) | [机器之心](https://mp.weixin.qq.com/s/6XddT1q0_yFO0hhQvmEwAQ)

> VLIPP: Towards Physically Plausible Video Generation with Vision and Language Informed Physical Prior\
> [Xindi Yang](#)<sup>\*</sup>,
[Baolu Li](https://libaolu312.github.io/)<sup>\*</sup>,
[Yiming Zhang](#),
[Zhenfei Yin](https://yinzhenfei.github.io/)<sup>†</sup>,
[Lei Bai](http://leibai.site/)<sup>†</sup>,
[Liqian Ma](https://charliememory.github.io/),
[Zhiyong Wang](https://www.sydney.edu.au/engineering/about/our-people/academic-staff/zhiyong-wang.html) \,
[Jianfei Cai](https://jianfei-cai.github.io/),
[Tien-Tsin Wong](https://ttwong12.github.io/myself.html),
[Huchuan Lu](https://scholar.google.com/citations?user=D3nE0agAAAAJ&hl=zh-CN&oi=sra),
[Xu Jia](https://stephenjia.github.io/)<sup>†</sup> \
> ICCV 2025

<p align="center">
    <video src="https://github.com/user-attachments/assets/c253cf1d-a4c8-4c24-b966-a1ecdf754a72" controls autoplay loop muted></video>
</p>


## Installation

#### Tested on Ubuntu 22.04 + Python 3.10 + Pytorch 2.5.1 + cu12.4

Prepare environment:
```
conda create -n vlipp python=3.10
pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu124
conda activate vlipp
mkdir data
```
You need to install GroundedSAM2 follow the instruction in [Grounded-SAM-2](https://github.com/IDEA-Research/Grounded-SAM-2).

Install requirements:
```
pip install -r requirements.txt
```

## Data Structure
<details>
  <summary> (click to expand) </summary>

      data/
      ├── animation_video/      # Synthetic motion videos
      │   └── {exp_name}.mp4
      ├── detections/           # Segmentation of the first frame
      │   └── {exp_name}
      ├── first_frames/         # First frame images
      │   └── {exp_name}.jpg
      ├── json/                 # Metadata in JSON format
      │   └── {exp_name}.json
      └── results/              # Output results
          └── {exp_name}



</details>

## Quick Start
### Stage1: Coarse-Level Motion Planning
If you have an OpenAI API key, you can put the API key in scripts/inference/run_stage1.sh or set OPENAI_API_KEY environment variable. Then you can use OpenAI's API for planning a physically plausible motion trajectory, with GPT-4o as an example:
```
bash scripts/inference/run_stage1.sh
```
### Stage2: Fine-Level Motion Synthesis
Then, you can use the coarse-level motion planned by the VLM in the previous stage to guide the video diffusion model in synthesizing a physically plausible video.
```
bash scripts/inference/run_stage2.sh
```

Note that since we provide some caches for stage 1, you don't need to run stage 1 on your own for cached prompts that we provide (i.e., you don't need an OpenAI API key).

```
bash scripts/cached_example/ball_cube_collide.sh
bash scripts/cached_example/pour_juice.sh
bash scripts/cached_example/mug_fall.sh
```

## Coarse Motion Guidance for Physically Plausible Video Generation

Coarse motion trajectories planned by the VLM can serve as motion priors, guiding video-diffusion models to generate physically plausible videos.


<p align="center">
    <video src="https://github.com/user-attachments/assets/301ac1c7-87cf-4167-84b5-d4f4a015efb9" controls autoplay loop muted></video>
</p>

## Citation
If you find our code or paper helps, please consider citing:
```
@article{yang2025vlipp,
  title={VLIPP: Towards Physically Plausible Video Generation with Vision and Language Informed Physical Prior},
  author={Yang, Xindi and Li, Baolu and Zhang, Yiming and Yin, Zhenfei and Bai, Lei and Ma, Liqian and Wang, Zhiyong and Cai, Jianfei and Wong, Tien-Tsin and Lu, Huchuan and others},
  journal={arXiv preprint arXiv:2503.23368},
  year={2025}
}
```

## Acknowledgement
The code base is adapted from [Go-with-the-Flow](https://github.com/Eyeline-Research/Go-with-the-Flow) and [Grounded-SAM-2](https://github.com/IDEA-Research/Grounded-SAM-2), thanks for their great work!
