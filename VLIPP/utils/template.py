template_rigid_object = [
    {
        "role": "system",
        "content": [
            {
                "type": "text", 
                "text": """You are an expert in real-world physical motion. Your task is to predict video bounding boxes. You will receive a reference image, its segmentation map, the initial bounding box where motion starts, and a textual description of the video content. Your task is to predict the bounding box coordinates for the next 13 frames.The video frame size is 720x480 (width × height). The top-left coordinate is [0, 0], and the bottom-right coordinate is [720, 480]. When predicting, ensure that different bounding boxes do not overlap or exceed the frame boundaries. \n\nEach frame should be represented as [{'id': unique object identifier, 'name': object name, 'box': [box top-left x-coordinate, box top-left y-coordinate, box width, box height]}, ...]. Each box should not include more than one object. Your predicted frames must encapsulate the whole scenario depicted by the initial information. Your predicted frames must fully represent the entire scenario described by the initial information. The movement of objects in the predicted frames should follow the laws of physics, such as bouncing during collisions, changing directions, and other related phenomena. For example, when two objects collide, their speed and direction will be influenced by the point of impact, and their motion will adjust according to the laws of momentum and energy conservation. \n\nWhen predicting future bounding boxes, objects must not change direction, accelerate, or begin new motion states (such as bouncing, sliding, or stopping) unless a direct physical contact has clearly occurred between their bounding boxes. A collision can only be inferred when the predicted bounding boxes overlap or touch at their edges. If no bounding boxes are in contact, their motion state must continue as expected from prior frames.\n\nYou should check whether the collision condition is satisfied, such as whether the bounding boxes are in contact.\n\nIn the prediction process, you should plan the possible motion of each object in the scene caused by collisions. Additionally, the collision between objects may cause overlap, and their movement trajectories should conform to real-world physical principles, such as the effects of gravity, friction, and other forces. You only need to focus on the objects provided to you in the first frame, and no need to pay attention to anything else. Your predictions should infer which physical laws apply, such as Gravity, Conservation of Momentum, Fluid Mechanics, Thermodynamics, Magnetic Force, etc. For example, under the action of gravity, the ball will accelerate and rebound after colliding with the ground. When two balls move towards each other, the material, volume, density, etc. of each ball must be considered, and the collision process satisfies the law of conservation of momentum. Assume objects move and interact based on real-world physics. The camera follows perspective geometry. Even if an object disappears and reappears, its bounding box should maintain the same ID across frames. If necessary, you may make reasonable assumptions.Before generating bounding box coordinates for each frame, provide step-by-step reasoning. Refer to the examples below for the desired format. Never use markdown or other formats not in the examples. Do not start each frame with `-`. Do not include any comments in your response. 
                !You need to infer the mass relationship between the objects from the input image""" ,
            },
        ],
    },
    {
        "role": "user",
        "content": [
            {
                "type": "text", 
                "text": """initial_boxes:  [{'id': 0, 'name': 'ball', 'box': [303, 82, 108, 108]}]
                Caption: Generate a high-quality video of a wooden ball dropping from a height of about 1 meter onto a smooth, solid table.Capture the physics of the ball's descent, including its acceleration due to gravity, the moment of impact with the table, and the subsequent bounce. Show the ball compressing slightly upon impact, then rebounding, losing a bit of height with each bounce until it comes to rest. Include subtle details like the sound of the impact, the slight vibration of the table, and the ball's rotation as it moves.
                physics: Gravity""",
            },
        ],
    },
    {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": """Reasoning: 
                Step1-Analysis Caption and determine the physical laws to be satisfied: As can be seen from the caption, the topic of this study is about the free fall of a small ball, so this topic needs to satisfy Newton's laws of motion, focusing on the impact of gravity.
                Step2-Analyze the impact of this physical law: In accordance with Newton's laws of motion, gravity will cause the small ball to perform free fall motion, vertically accelerate and hit the table, and rebound after the collision. Due to energy loss, the height of each rebound will decrease, which is in line with the law of conservation of energy and momentum.
                Step3-Analyze the impact on box coordinates: The horizontal motion of the ball is negligible, so the x coordinate remains basically unchanged. Due to the vertical acceleration, the y coordinate of the small ball will gradually increase and the interpolation of the y coordinate between each two frames will also gradually increase. After colliding with the table, the small ball rebounds, the y coordinate decreases, and the small ball decelerates vertically upward. Subsequently, the small ball continues to accelerate vertically and collides with the table for the second time. After the third collision, the small ball is stationary on the table, and the y coordinate remains unchanged. Since the ball is a rigid body, it will be slightly compressed at the moment of collision with the desktop. Therefore, the width in the box coordinates remains unchanged, the height decreases slightly, and then quickly returns to normal. The width and height will not change for the rest of the time.
                Predict the coordinates for the next 13 frames:
                Frame 1: [{'id': 0, 'name': 'wooden ball', 'box': [303, 82, 108, 108]}]
                Frame 2: [{'id': 0, 'name': 'wooden ball', 'box': [303, 137, 108, 108]}]
                Frame 3: [{'id': 0, 'name': 'wooden ball', 'box': [303, 184, 108, 108]}]
                Frame 4: [{'id': 0, 'name': 'wooden ball', 'box': [303, 313, 108, 108]}]
                Frame 5: [{'id': 0, 'name': 'wooden ball', 'box': [303, 255, 108, 108]}]
                Frame 6: [{'id': 0, 'name': 'wooden ball', 'box': [303, 284, 108, 104]}] 
                Frame 7: [{'id': 0, 'name': 'wooden ball', 'box': [303, 313, 108, 108]}]
                Frame 8: [{'id': 0, 'name': 'wooden ball', 'box': [303, 298, 108, 108]}]
                Frame 9: [{'id': 0, 'name': 'wooden ball', 'box': [303, 305, 108, 108]}]
                Frame 10: [{'id': 0, 'name': 'wooden ball', 'box': [303, 313, 108, 104]}]
                Frame 11: [{'id': 0, 'name': 'wooden ball', 'box': [303, 313, 108, 108]}]
                Frame 12: [{'id': 0, 'name': 'wooden ball', 'box': [303, 313, 108, 108]}]
                Frame 13: [{'id': 0, 'name': 'wooden ball', 'box': [303, 313, 108, 104]}]""",
            },
        ],
    },
    
    {
        "role": "user",
        "content": [
            {
                "type": "text", 
                "text": """initial_boxes: [{'id': 0, 'name': 'ball 1', 'box': [200, 240, 50, 50]}, {'id': 1, 'name': 'ball 2', 'box': [520, 240, 50, 50]}]
                Caption: On the left side of the desktop, there is a small, glossy sphere, and on the right side, another small, glossy sphere. Both spheres are identical in size and texture, with a subtle shine that reflects the ambient light. The left sphere begins to roll slowly to the right, while the right sphere rolls slowly to the left. They move at a steady pace, gradually approaching each other. When the two spheres collide in the center of the desktop, there is a subtle, satisfying click sound. Upon impact, the spheres compress slightly, then rebound in opposite directions. The left sphere rolls back to its starting position, and the right sphere does the same, slowing down as they move away from each other. The lighting is soft and even, casting gentle shadows beneath the spheres as they move. The overall atmosphere is calm and precise, with a focus on the physics of the collision and the smooth motion of the spheres. 
                physics: Conservation of Momentum""",
            },
        ],
    },
    {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": """Reasoning: 
                Step1-Analysis Caption and determine the physical laws to be satisfied: From the caption, we can know that the theme of this time is that two rigid balls move towards each other and collide, so the movement must satisfy Newton's laws of motion, and the law of conservation of momentum is satisfied when colliding.
                Step2-Analyze the impact of this physical law: According to Newton's laws of motion, the left and right balls move towards each other with uniform acceleration. The law of conservation of momentum is satisfied when a collision occurs. According to the provided caption and the width and height of the two balls, we know that the two balls are made of the same material and have the same volume. After the collision, the two balls will move in the opposite direction before the collision and decelerate uniformly to a stop.
                Step3-Analyze the impact on box coordinates: The bounding boxes of the two balls are ball1: [200, 240, 50, 50] and ball2: [520, 220, 50, 50], which means [x, y, w, h]. Based on the reasoning, the motion direction of ball1 is [|x2 + w2/2 - x1 - w1/2|, |y2 + h2/2 - y1 - h1/2|] = [320, 20], normalize it to get [0.94, 0.06], which represents the motion direction of the ball. Let's assume that the ball moves 30 units per frame. The condition for the balls to collide is dist((x1, y1), (x2, y2)) < (w + h) / 4. After the collision, the motion direction of the balls will reverse. In the real world, the positions of the two balls will not overlap
                Predict the coordinates for the next 13 frames:
                Frame 1: [{'id': 0, 'name': 'ball 1', 'box': [200, 240, 50, 50]}, {'id': 1, 'name': 'ball 2', 'box': [520, 240, 50, 50]}]
                Frame 2: [{'id': 0, 'name': 'ball 1', 'box': [227, 240, 50, 50]}, {'id': 1, 'name': 'ball 2', 'box': [493, 220, 50, 50]}]
                Frame 3: [{'id': 0, 'name': 'ball 1', 'box': [254, 240, 50, 50]}, {'id': 1, 'name': 'ball 2', 'box': [466, 220, 50, 50]}]
                Frame 4: [{'id': 0, 'name': 'ball 1', 'box': [281, 240, 50, 50]}, {'id': 1, 'name': 'ball 2', 'box': [439, 220, 50, 50]}]
                Frame 5: [{'id': 0, 'name': 'ball 1', 'box': [308, 240, 50, 50]}, {'id': 1, 'name': 'ball 2', 'box': [412, 220, 50, 50]}]
                Frame 6: [{'id': 0, 'name': 'ball 1', 'box': [335, 240, 50, 50]}, {'id': 1, 'name': 'ball 2', 'box': [385, 220, 50, 50]}]
                Frame 6: [{'id': 0, 'name': 'ball 1', 'box': [313, 240, 50, 50]}, {'id': 1, 'name': 'ball 2', 'box': [408, 220, 50, 50]}]
                Frame 7: [{'id': 0, 'name': 'ball 1', 'box': [291, 240, 50, 50]}, {'id': 1, 'name': 'ball 2', 'box': [431, 220, 50, 50]}]
                Frame 8: [{'id': 0, 'name': 'ball 1', 'box': [269, 240, 50, 50]}, {'id': 1, 'name': 'ball 2', 'box': [454, 220, 50, 50]}]
                Frame 9: [{'id': 0, 'name': 'ball 1', 'box': [247, 240, 50, 50]}, {'id': 1, 'name': 'ball 2', 'box': [477, 220, 50, 50]}]
                Frame 10: [{'id': 0, 'name': 'ball 1', 'box': [225, 240, 50, 50]}, {'id': 1, 'name': 'ball 2', 'box': [500, 220, 50, 50]}]
                Frame 11: [{'id': 0, 'name': 'ball 1', 'box': [203, 240, 50, 50]}, {'id': 1, 'name': 'ball 2', 'box': [523, 220, 50, 50]}]
                Frame 12: [{'id': 0, 'name': 'ball 1', 'box': [181, 240, 50, 50]}, {'id': 1, 'name': 'ball 2', 'box': [546, 220, 50, 50]}]
                Frame 13: [{'id': 0, 'name': 'ball 1', 'box': [159, 240, 50, 50]}, {'id': 1, 'name': 'ball 2', 'box': [568, 220, 50, 50]}]
                """,
            },
        ],
    },

    {
        "role": "user",
        "content": [
            {
                "type": "image",
                "image": "",  # first frame
            },
            {
                "type": "image",
                "image": "",  # segmentation map
            },
            {
                "type": "text", 
                "text": """""",
            },
        ],
    },
]

template_fluid = [
    {
        "role": "system",
        "content": [
            {
                "type": "text", 
                "text": """You are an expert in real-world physical motion. Your task is to predict video bounding boxes. You will receive a reference image, its segmentation map, the initial bounding box where motion starts, and a textual description of the video content. Your task is to predict the bounding box coordinates for the next 13 frames.The video frame size is 720x480 (width × height). The top-left coordinate is [0, 0], and the bottom-right coordinate is [720, 480]. When predicting, ensure that different bounding boxes do not overlap or exceed the frame boundaries. \n\nEach frame should be represented as: `[{'id': unique object identifier, 'name': object name, 'box': [box top-left x-coordinate, box top-left y-coordinate, box width, box height]}, ...]`.Your predicted frames must cover the entire described scene. Critical moments in the movement must be included in the predicted sequence, such as the moment of collision.You need to consider the material and properties of the moving objects in the video. You only need to focus on the objects provided to you in the first frame, and no need to pay attention to anything else. Your predictions should infer which physical laws apply, such as Gravity, Conservation of Momentum, Fluid Mechanics, Thermodynamics, Magnetic Force, etc. For example, under the influence of fluid mechanics, when pouring water into a cup, the water level in the cup should rise and ripples should occur. The top boundary of a liquid should move when it's being poured, while the bottom edge of the liquid (for instance, in a container) should stay fixed. When an object (such as a liquid) is in a container and is being poured, the bottom boundary of the liquid typically stays fixed. Assume objects move and interact based on real-world physics. The camera follows perspective geometry. Even if an object disappears and reappears, its bounding box should maintain the same ID across frames. If necessary, you may make reasonable assumptions.Before generating bounding box coordinates for each frame, provide step-by-step reasoning. Refer to the examples below for the desired format. Never use markdown or other formats not in the examples. Do not start each frame with `-`. Do not include any comments in your response.""",
            },
        ],
    },

    {
        "role": "user",
        "content": [
            {
                "type": "text", 
                "text": """initial_boxes: [{'id': 0, 'name': 'tea', 'box': [241.8, 335.3, 165, 88]}]
                Caption: The video shows a close-up of a clear glass being filled with tea. The tea is being poured from above, and we can see the stream of tea hitting the bottom of the glass and causing ripples and splashes. The background is a plain white surface, which contrasts with the transparency of the glass and the clarity of the tea. The glass is cylindrical in shape and appears to be of a standard size for a drinking glass. The tea is clear and appears to be at room temperature. There is no visible branding or logos on the glass, and no other objects or people are present in the frame. The focus is solely on the action of the tea being poured and the resulting movement in the glass.
                physics: Fluid Mechanics""",
            },
        ],
    },
    {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": """Reasoning: 
                Step1-Analysis Caption and determine the physical laws to be satisfied: As can be seen from the caption, the theme of this session is to pour tea into a glass teacup. Therefore, the tea is affected by gravity during its fall, and the state of the tea in the cup satisfies fluid mechanics.
                Step2-Analyze the impact of this physical law: Tea falls into the cup under the influence of gravity. According to fluid mechanics, the water level in the cup will gradually rise, and the water surface will ripple due to the pouring of water.
                Step3-Analyze the impact on box coordinates: When tea is poured into the cup, under the restriction of the cup, the x coordinate of the tea box will not change much. As the water level rises, the y coordinate will gradually decrease. As the water level rises, the overall volume of the tea gradually increases, the height of the box will also increase, and the width will change with the boundary of the cup.
                Predict the coordinates for the next 13 frames:
                Frame 1: [{'id': 0, 'name': 'tea', 'box': [241.8, 335.3, 165, 88]}]
                Frame 2: [{'id': 0, 'name': 'tea', 'box': [241.2, 330.0, 165, 94]}]
                Frame 3: [{'id': 0, 'name': 'tea', 'box': [241.0, 322.2, 165, 102]}]
                Frame 4: [{'id': 0, 'name': 'tea', 'box': [241.3, 317.6, 165, 105]}]
                Frame 5: [{'id': 0, 'name': 'tea', 'box': [240.6, 313.7, 166, 111]}]
                Frame 6: [{'id': 0, 'name': 'tea', 'box': [239.1, 305.6, 167, 118]}]
                Frame 7: [{'id': 0, 'name': 'tea', 'box': [237.7, 301.1, 170, 123]}]
                Frame 8: [{'id': 0, 'name': 'tea', 'box': [236.8, 295.3, 172, 129]}]
                Frame 9: [{'id': 0, 'name': 'tea', 'box': [235.7, 290.2, 172, 134]}]
                Frame 10: [{'id': 0, 'name': 'tea', 'box': [235.1, 283.3, 173, 140]}]
                Frame 11: [{'id': 0, 'name': 'tea', 'box': [234.0, 278.3, 175, 145]}]
                Frame 12: [{'id': 0, 'name': 'tea', 'box': [233.1, 272.0, 177, 152]}]
                Frame 13: [{'id': 0, 'name': 'tea', 'box': [231.7, 268.0, 179, 156]}]""",
            },
        ],
    },

    {
        "role": "user",
        "content": [
            {
                "type": "image",
                "image": "",  # first frame
            },
            {
                "type": "image",
                "image": "",  # segmentation map
            },
            {
                "type": "text", 
                "text": """""",
            },
        ],
    },
]

template_heat = [
    {
        "role": "system",
        "content": [
            {
                "type": "text", 
                "text": """You are an expert in real-world physical motion. Your task is to predict video bounding boxes. You will receive a reference image, its segmentation map, the initial bounding box where motion starts, and a textual description of the video content. Your task is to predict the bounding box coordinates for the next 13 frames.The video frame size is 720x480 (width × height). The top-left coordinate is [0, 0], and the bottom-right coordinate is [720, 480]. When predicting, ensure that different bounding boxes do not overlap or exceed the frame boundaries. \n\nEach frame should be represented as: `[{'id': unique object identifier, 'name': object name, 'box': [box top-left x-coordinate, box top-left y-coordinate, box width, box height]}, ...]`.Your predicted frames must cover the entire described scene. Critical moments in the movement must be included in the predicted sequence, such as the moment of collision.You need to consider the material and properties of the moving objects in the video. You only need to focus on the objects provided to you in the first frame, and no need to pay attention to anything else. Your predictions should infer which physical laws apply, such as Gravity, Conservation of Momentum, Fluid Mechanics, Thermodynamics, Magnetic Force, etc. For example, under the influence of thermodynamics, ice will gradually melt into a pool of water, and flames will tremble in the wind. Assume objects move and interact based on real-world physics. The camera follows perspective geometry. Even if an object disappears and reappears, its bounding box should maintain the same ID across frames. If necessary, you may make reasonable assumptions.Before generating bounding box coordinates for each frame, provide step-by-step reasoning. Refer to the examples below for the desired format. Never use markdown or other formats not in the examples. Do not start each frame with `-`. Do not include any comments in your response.""",
            },
        ],
    },

    {
        "role": "user",
        "content": [
            {
                "type": "text", 
                "text": """initial_boxes: [{'id': 0, 'name': 'fire', 'box': [68.1,1.4,564,474]}]
                Caption: Create a cinematic video of a cozy, dimly lit room with a large floor-to-ceiling window. Outside, the night is dark, with faint moonlight casting soft shadows. Inside, a pile of wooden logs is burning brightly in a fireplace or fire pit near the window. The flames are strong and lively, flickering and dancing, casting warm, golden light across the room. The glow of the fire reflects off the glass of the window, creating a mesmerizing contrast between the warmth inside and the cool darkness outside. The atmosphere is serene and intimate, with subtle smoke rising from the burning wood. Capturing the details of the crackling fire, the texture of the wood, and the interplay of light and shadow.
                physics: Thermodynamics""",
            },
        ],
    },
    {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": """Reasoning: 
                Step1-Analysis Caption and determine the physical laws to be satisfied: As can be seen from the caption, the theme of this time is a pile of firewood burning, so the laws of thermodynamics need to be satisfied.
                Step2-Analyze the impact of this physical law: According to the laws of thermodynamics, This burning fire will result in flickering flames and subtle smoke rising from the wood due to combustion. Because of thermodynamics, the heat will cause convection currents. The flames will flicker slightly but stay within the bounding box of interest, reflecting changes in heat intensity.
                Step3-Analyze the impact on box coordinates: Since the volume of the flame is not fixed, but the overall activity area will not change drastically, the x and y of the box will change unfixedly, and the width and height will also change unfixedly. Hence, XY position remains mostly stable with slight growth and shrinkage height-wise due to flickering flames.
                Predict the coordinates for the next 13 frames:
                Frame 1: [{'id': 0, 'name': 'fire', 'box': [68.1,1.4,564,474]}]
                Frame 2: [{'id': 0, 'name': 'fire', 'box': [67.3,1.4,564,474]}]
                Frame 3: [{'id': 0, 'name': 'fire', 'box': [65.3,50.7,556,424]}]
                Frame 4: [{'id': 0, 'name': 'fire', 'box': [90.2,1.4,542,475]}]
                Frame 5: [{'id': 0, 'name': 'fire', 'box': [92.2,46.2,541,429]}]
                Frame 6: [{'id': 0, 'name': 'fire', 'box': [94.4,97.9,557,377]}]
                Frame 7: [{'id': 0, 'name': 'fire', 'box': [90.6,48.8,537,427]}]
                Frame 8: [{'id': 0, 'name': 'fire', 'box': [84.4,8.3,548,467]}]
                Frame 9: [{'id': 0, 'name': 'fire', 'box': [93.7,1.5,532,474]}]
                Frame 10: [{'id': 0, 'name': 'fire', 'box': [92.0,13.8,541,462]}]
                Frame 11: [{'id': 0, 'name': 'fire', 'box': [88.2,14.4,544,461]}]
                Frame 12: [{'id': 0, 'name': 'fire', 'box': [87.1,58.5,539,417]}]
                Frame 13: [{'id': 0, 'name': 'fire', 'box': [87.1,58.5,539,417]}]""",
            },
        ],
    },
    
    {
        "role": "user",
        "content": [
            {
                "type": "text", 
                "text": """initial_boxes: [{'id': 0, 'name': 'ice', 'box': [393.9,186.1,90,117]}]
                Caption: Generate a close-up video of a clean, minimalist table surface with a smooth, reflective finish. On the table, several clear ice cubes are slowly melting. The ice cubes are partially translucent, with subtle cracks and textures visible inside. Water droplets form and trickle down the sides of the cubes, pooling slightly on the table. The lighting is soft and natural, creating gentle highlights and reflections on the wet surfaces. The scene feels calm and tranquil, with a focus on the gradual transformation of the ice as it melts. The camera captures the details of the melting process, including the shimmering water and the interplay of light on the ice and table.
                physics: Thermodynamics""",
            },
        ],
    },
    {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": """Reasoning: 
                Step1-Analysis Caption and determine the physical laws to be satisfied: As the theme involves ice melting, the process is governed by heat transfer (thermal conduction and convection) and phase transition laws (solid to liquid). Thermodynamics dictates that heat from the surrounding environment flows into the ice until equilibrium is reached.
                Step2-Analyze the impact of this physical law: According to heat transfer principles, the ice block will gradually lose structural integrity as it absorbs energy. Melting will cause water droplets to form on the surface, pooling around the base. Convection currents in the surrounding air/water may create uneven melting patterns, leading to irregular shape changes. The volume of the ice will shrink over time, with liquid water spreading outward, influenced by gravity and surface tension.
                Step3-Analyze the impact on box coordinates: As the ice melts, some water appears near the ice, and the overall area increases, causing the bounding box to grow vertically and horizontally. If the ice slides due to uneven melting or water lubrication, the XY position may shift slightly, but it will usually be fixed at the initial contact point.
                Predict the coordinates for the next 13 frames:
                Frame 1: [{'id': 0, 'name': 'ice', 'box': [393.9,186.1,90,117]}]
                Frame 2: [{'id': 0, 'name': 'ice', 'box': [390.0,186.8,96,117]}]
                Frame 3: [{'id': 0, 'name': 'ice', 'box': [387.5,187.5,102,119]}]
                Frame 4: [{'id': 0, 'name': 'ice', 'box': [384.3,188.2,110,122]}]
                Frame 5: [{'id': 0, 'name': 'ice', 'box': [379.4,188.9,121,124]}]
                Frame 6: [{'id': 0, 'name': 'ice', 'box': [368.7,190.0,147,127]}]
                Frame 7: [{'id': 0, 'name': 'ice', 'box': [364.3,190.8,157,131]}]
                Frame 8: [{'id': 0, 'name': 'ice', 'box': [354.8,191.1,177,133]}]
                Frame 9: [{'id': 0, 'name': 'ice', 'box': [339.4,192.1,215,140]}]
                Frame 10: [{'id': 0, 'name': 'ice', 'box': [326.2,193.2,235,141]}]
                Frame 11: [{'id': 0, 'name': 'ice', 'box': [299.3,197.7,274,166]}]
                Frame 12: [{'id': 0, 'name': 'ice', 'box': [271.9,174.3,316,195]}]
                Frame 13: [{'id': 0, 'name': 'ice', 'box': [271.5,109.6,317,260]}]""",
            },
        ],
    },

    {
        "role": "user",
        "content": [
            {
                "type": "image",
                "image": "",  # first frame
            },
            {
                "type": "image",
                "image": "",  # segmentation map
            },
            {
                "type": "text", 
                "text": """""",
            },
        ],
    },
]

template_magnetic = [
    {
        "role": "system",
        "content": [
            {
                "type": "text", 
                "text": """You are an expert in real-world physical motion. Your task is to predict video bounding boxes. You will receive a reference image, its segmentation map, the initial bounding box where motion starts, and a textual description of the video content. Your task is to predict the bounding box coordinates for the next 13 frames.The video frame size is 720x480 (width × height). The top-left coordinate is [0, 0], and the bottom-right coordinate is [720, 480]. When predicting, ensure that different bounding boxes do not overlap or exceed the frame boundaries. \n\nEach frame should be represented as: `[{'id': unique object identifier, 'name': object name, 'box': [box top-left x-coordinate, box top-left y-coordinate, box width, box height]}, ...]`.Your predicted frames must cover the entire described scene. Critical moments in the movement must be included in the predicted sequence, such as the moment of collision.You need to consider the material and properties of the moving objects in the video. You only need to focus on the objects provided to you in the first frame, and no need to pay attention to anything else. Your predictions should infer which physical laws apply, such as Gravity, Conservation of Momentum, Fluid Mechanics, Thermodynamics, Magnetic Force, etc. For example, under the influence of the magnetic field, two magnets with the same poles repel each other and with opposite poles attract each other, and magnets will attract iron objects.Assume objects move and interact based on real-world physics. The camera follows perspective geometry. Even if an object disappears and reappears, its bounding box should maintain the same ID across frames. If necessary, you may make reasonable assumptions.Before generating bounding box coordinates for each frame, provide step-by-step reasoning. Refer to the examples below for the desired format. Never use markdown or other formats not in the examples. Do not start each frame with `-`. Do not include any comments in your response.""",
            },
        ],
    },

    {
        "role": "user",
        "content": [
            {
                "type": "text", 
                "text": """initial_boxes: [{'id': 0, 'name': 'magnet 1', 'box': [66.2,198.4,286,47]}, {'id': 1, 'name': 'magnet 2', 'box': [394.5,196.7,210,45]}]
                Caption: Generate a video scene featuring a clean, minimalist desktop surface. On the left side of the desktop, place a long, slender bar magnet with its north pole (N) facing to the right. On the right side, place an identical long, slender bar magnet with its north pole (N) facing to the left, directly opposite the first magnet. The right magnet begins to slowly move towards the left magnet. As the two north poles approach each other, the left magnet is visibly repelled and slides away to the left due to the magnetic force. The right magnet pauses briefly, then continues to move closer again, causing the left magnet to be repelled once more, sliding further away. Focus on the smooth, realistic motion of the magnets, the subtle vibrations as they repel each other, and the clean, reflective surface of the desktop. Ensure the lighting is soft and even, highlighting the metallic texture of the magnets and the sleekness of the desktop.
                physics: Magnetic Force""",
            },
        ],
    },
    {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": """Reasoning: 
                Step1-Analysis Caption and determine the physical laws to be satisfied: The scenario involves two bar magnets aligned with like poles (e.g., N-N or S-S) facing each other, governed by magnetostatics and Coulomb’s law for magnetism. Key principles include magnetic repulsion, dipole-dipole interaction, and the conservation of energy in magnetic field systems.
                Step2-Analyze the impact of this physical law: Due to like-pole repulsion, the magnets will experience a mutual force pushing them apart. If unconstrained, they will move to minimize overlap while maintaining a stable equilibrium distance determined by their magnetic strength and external constraints. Magnetic field lines between the poles will diverge outward, creating a region of high magnetic flux density around the gap. If fixed in place, stress and potential torsional motion (e.g., rotation to reduce repulsion) may occur. Energy dissipation through air resistance or friction will dampen oscillations if the system is perturbed.
                Step3-Analyze the impact on box coordinates: The bounding boxes of each magnet will shift away from each other along the axis of alignment (e.g., x-direction), with the distance between boxes increasing until repulsion balances external forces (e.g., friction or clamping).
                Predict the coordinates for the next 13 frames:
                Frame 1: [{'id': 0, 'name': 'magnet 1', 'box': [66.2,198.4,286,47]}, {'id': 1, 'name': 'magnet 2', 'box': [394.5,196.7,210,45]}
                Frame 2: [{'id': 0, 'name': 'magnet 1', 'box': [65.8,197.1,283,52]}, {'id': 1, 'name': 'magnet 2', 'box': [374.1,195.6,259,46]}]
                Frame 3: [{'id': 0, 'name': 'magnet 1', 'box': [52.4,196.1,283,73]}, {'id': 1, 'name': 'magnet 2', 'box': [367.1,195.2,259,47]}]
                Frame 4: [{'id': 0, 'name': 'magnet 1', 'box': [47.3,193.9,281,92]}, {'id': 1, 'name': 'magnet 2', 'box': [362.0,195.7,257,47]}]
                Frame 5: [{'id': 0, 'name': 'magnet 1', 'box': [41.4,193.4,275,132]}, {'id': 1, 'name': 'magnet 2', 'box': [347.6,200.0,261,47]}]
                Frame 6: [{'id': 0, 'name': 'magnet 1', 'box': [39.7,192.7,276,135]}, {'id': 1, 'name': 'magnet 2', 'box': [359.5,228.3,149,48]}]
                Frame 7: [{'id': 0, 'name': 'magnet 1', 'box': [40.2,192.6,276,135]}, {'id': 1, 'name': 'magnet 2', 'box': [398.7,262.7,268,60]}]
                Frame 8: [{'id': 0, 'name': 'magnet 1', 'box': [40.4,192.0,276,136]}, {'id': 1, 'name': 'magnet 2', 'box': [433.8,315.3,178,75]}]
                Frame 9: [{'id': 0, 'name': 'magnet 1', 'box': [40.6,192.6,276,135]}, {'id': 1, 'name': 'magnet 2', 'box': [398.0,320.0,266,100]}]
                Frame 10: [{'id': 0, 'name': 'magnet 1', 'box': [38.3,192.8,277,135]}, {'id': 1, 'name': 'magnet 2', 'box': [356.8,301.2,261,116]}]
                Frame 11: [{'id': 0, 'name': 'magnet 1', 'box': [36.9,192.0,279,136]}, {'id': 1, 'name': 'magnet 2', 'box': [335.2,310.9,260,114]}]
                Frame 12: [{'id': 0, 'name': 'magnet 1', 'box': [29.0,189.0,275,122]}, {'id': 1, 'name': 'magnet 2', 'box': [314.8,312.5,256,113]}]
                Frame 13: [{'id': 0, 'name': 'magnet 1', 'box': [297.8,300.2,149,84]}, {'id': 1, 'name': 'magnet 2', 'box': [17.3,183.0,286,89]}]""",
            },
        ],
    },
    
    {
        "role": "user",
        "content": [
            {
                "type": "text", 
                "text": """initial_boxes: [{'id': 0, 'name': 'magnet 1', 'box': [0.7,247.2,333,63]}, {'id': 1, 'name': 'magnet 2', 'box': [553.7,252.4,165,60]}]
                Caption: Create a video scene featuring a clean, minimalist desktop . On the left side of the desktop, place a long, slender bar magnet with its north pole (N) facing to the right. On the right side, place an identical long, slender bar magnet with its south pole (S) facing to the left, directly opposite the first magnet. The right magnet begins to slowly move towards the left magnet. As the opposite poles (N and S) approach each other, the right magnet is rapidly and smoothly attracted to the left magnet due to the magnetic force, snapping into place and tightly adhering to it. Highlight the sudden acceleration of the right magnet as it is pulled in, the slight vibration upon contact, and the final stable position where the two magnets are firmly attached. Emphasize the clean, polished surface of the desktop, the metallic texture of the magnets, and the soft, even lighting that enhances the realism of the scene.
                physics: Magnetic Force""",
            },
        ],
    },
    {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": """Reasoning: 
                Step1-Analysis Caption and determine the physical laws to be satisfied: The scenario involves two bar magnets aligned with opposite poles (e.g., N-S or S-N) facing each other, governed by magnetostatics, Coulomb's law for magnetism, and magnetic dipole interactions. Key principles include magnetic attraction, field superposition, and energy minimization as the system seeks equilibrium.
                Step2-Analyze the impact of this physical law: Under the influence of the magnetic field, as the right magnet approaches, the opposite poles produce a mutual attraction, pulling the magnets towards each other.
                Step3-Analyze the impact on box coordinates: The right magnet moves toward the left magnet. Since the magnet is a rigid body, its x coordinate gradually decreases, while the y coordinate remains unchanged. As the right magnet approaches the left side, under the action of the magnetic field, the right magnet accelerates and is tightly attracted to the left magnet, remaining motionless.
                Predict the coordinates for the next 13 frames:
                Frame 1: [{'id': 0, 'name': 'magnet 1', 'box': [0.7,247.2,333,63]}, {'id': 1, 'name': 'magnet 2', 'box': [553.7,252.4,165,60]}]
                Frame 2: [{'id': 0, 'name': 'magnet 1', 'box': [0.7,247.3,332,63]}, {'id': 1, 'name': 'magnet 2', 'box': [548.1,252.3,171,61]}]
                Frame 3: [{'id': 0, 'name': 'magnet 1', 'box': [0.7,247.2,332,63]}, {'id': 1, 'name': 'magnet 2', 'box': [472.7,250.8,246,62]}]
                Frame 4: [{'id': 0, 'name': 'magnet 1', 'box': [0.7,247.2,332,63]}, {'id': 1, 'name': 'magnet 2', 'box': [448.3,250.6,271,62]}]
                Frame 5: [{'id': 0, 'name': 'magnet 1', 'box': [0.7,247.3,332,63]}, {'id': 1, 'name': 'magnet 2', 'box': [415.4,250.2,304,63]}]
                Frame 6: [{'id': 0, 'name': 'magnet 1', 'box': [0.6,247.4,332,62]}, {'id': 1, 'name': 'magnet 2', 'box': [394.2,250.1,325,63]}]
                Frame 7: [{'id': 0, 'name': 'magnet 1', 'box': [0.5,247.4,332,62]}, {'id': 1, 'name': 'magnet 2', 'box': [367.1,249.7,332,63]}]
                Frame 8: [{'id': 0, 'name': 'magnet 1', 'box': [0.1,247.8,332,65]}, {'id': 1, 'name': 'magnet 2', 'box': [332.1,247.8,332,65]}]
                Frame 9: [{'id': 0, 'name': 'magnet 1', 'box': [0.1,247.8,332,65]}, {'id': 1, 'name': 'magnet 2', 'box': [332.1,247.8,332,65]}]
                Frame 10: [{'id': 0, 'name': 'magnet 1', 'box': [0.1,247.8,332,65]}, {'id': 1, 'name': 'magnet 2', 'box': [332.1,247.8,332,65]}]
                Frame 11: [{'id': 0, 'name': 'magnet 1', 'box': [0.1,247.8,332,65]}, {'id': 1, 'name': 'magnet 2', 'box': [332.1,247.8,332,65]}]
                Frame 12: [{'id': 0, 'name': 'magnet 1', 'box': [0.1,247.8,332,65]}, {'id': 1, 'name': 'magnet 2', 'box': [332.1,247.8,332,65]}]
                Frame 13: [{'id': 0, 'name': 'magnet 1', 'box': [0.1,247.8,332,65]}, {'id': 1, 'name': 'magnet 2', 'box': [332.1,247.8,332,65]}]""",
            },
        ],
    },

    {
        "role": "user",
        "content": [
            {
                "type": "image",
                "image": "",  # 首帧图
            },
            {
                "type": "image",
                "image": "",  # 分割图
            },
            {
                "type": "text", 
                "text": """""",
            },
        ],
    },
]


template_library = {
    "Solid Mechanics": template_rigid_object,
    "Fluid Dynamics": template_fluid,
    "Thermodynamics": template_heat,
    "Magnetism": template_magnetic,
    "Optics": template_rigid_object
}

messages = [
    {
        "role": "system",
        "content": [
            {
                "type": "text", 
                "text": """You are a physics-aware video scene designer. Perform the following tasks systematically, you have three tasks:
                The first task is Refine Input Prompt into Video Scene Description. You will take a short input prompt and expand it into a detailed video scene description for the video generation model. Please fully describe the entire video scene. During the refinement process, you need to pay attention to the physical phenomena in the video scene, clearly describe the properties of key objects (such as material, shape, etc.), the process of motion (such as before collision, during collision, after collision), and use simple words.
                The second task is to extract the key objects that have physical phenomena in the video scene, such as ball collision, please output 'ball'; if orange juice is poured into a cup, please output 'juice' or 'liquid'; if flames are burning, please output 'fire', if it is related to light and shadow, please output 'light'. The words you extracted will be used in the prediction segmentation model. Please extract carefully and output up to three words. If there is a containment relationship between multiple key objects, please directly output the words of the largest set.
                The third task is to assign physics tags to the video prompt. There are five options: [Solid Mechanics, Fluid Dynamics, Optics, Magnetism, Thermodynamics, Unknow]. If the object in the video is a rigid body (such as a ball collision, a wooden block sliding, etc.), please output 'Solid Mechanics'; if the object in the video is a fluid (such as pouring water, stirring coffee, etc.), please output 'Fluid Dynamics'; if the phenomenon in the video is related to thermodynamics (such as flame burning, ice melting), please output 'Thermodynamics'; if a phenomenon related to magnetism occurs in the video, please output 'Magnetism'; if none of them occurs, please output 'Unknow'. 
                
                You need to infer the mass relationship between the objects from the input image and predict their subsequent motion based on this mass relationship.
                
                Refer to the examples below for the desired format. Never use markdown or other formats not in the examples. Do not include any comments in your response.""",
            },
        ],
    },
    
    {
        "role": "user",
        "content": [
            {
                "type": "text", 
                "text": """prompt:Two balls move towards each other and collide.""",
            },
        ],
    },
    {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": """
                refine_video_prompt: In a high-speed video, two hard balls of contrasting vibrant colors collide dramatically on a smooth wooden tabletop. One ball moves from left to right, while the other moves from right to left. After the collision, the balls bounce off each other, with their directions of motion reversing at the collision point. The collision adheres to the law of conservation of momentum, showcasing a dynamic and energetic interaction. The wooden tabletop is clean and reflective, adding to the visual impact of the scene.
                key_physic_object: "ball."
                category: Solid Mechanics
                """,
            },
        ],
    },
    

    {
        "role": "user",
        "content": [
            {
                "type": "text", 
                "text": """Pour water into a clear glass.""",
            },
        ],
    },
    {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": """
                refine_video_prompt: The video shows a close-up of a clear glass being filled with water. The water is being poured from above, and we can see the stream of water hitting the bottom of the glass and causing ripples and splashes. The background is a plain white surface, which contrasts with the transparency of the glass and the clarity of the water. The glass is cylindrical in shape and appears to be of a standard size for a drinking glass. The water is clear and appears to be at room temperature. There is no visible branding or logos on the glass, and no other objects or people are present in the frame. The focus is solely on the action of the water being poured and the resulting movement in the glass.
                key_physic_object: "water. glass."
                category: Fluid Dynamics
                """,
            },
        ],
    },

    {
        "role": "user",
        "content": [
            {
                "type": "text", 
                "text": """Flame burning.""",
            },
        ],
    },
    {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": """
                refine_video_prompt: Create a cinematic video of a cozy, dimly lit room with a large floor-to-ceiling window. Outside, the night is dark, with faint moonlight casting soft shadows. Inside, a pile of wooden logs is burning brightly in a fireplace or fire pit near the window. The flames are strong and lively, flickering and dancing, casting warm, golden light across the room. The glow of the fire reflects off the glass of the window, creating a mesmerizing contrast between the warmth inside and the cool darkness outside. The atmosphere is serene and intimate, with subtle smoke rising from the burning wood. Capturing the details of the crackling fire, the texture of the wood, and the interplay of light and shadow.
                key_physic_object: "flame. smoke."
                category: Thermodynamics
                """,
            },
        ],
    },
    {
        "role": "user",
        "content": [
            {
                "type": "image",
                "image": "",  # first frame
            },
            {
                "type": "text", 
                "text": """""",
            },
        ],
    },
]
