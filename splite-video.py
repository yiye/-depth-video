from modules.video import VideoProcessor
import os
import gradio as gr

max_images = 12
output_dir = os.path.join(os.getcwd(), "output")
video_processor = VideoProcessor(output_dir=output_dir)

def splite_video(video, interval, druation):
    print(f"video path: {video}")
    print(f"blink: interval {interval}， druation {druation}")
    
    global video_processor
    video_processor.loadVideo(video)
    video_processor.getFrames(interval=interval, druation=druation)

    images = [frame["image"] for frame in video_processor.blink_frames]

    return images

def replace_video(*image_inputs):
    # if video_processor or blink_frames is None, print error
    if video_processor.blink_frames is None:
        print("please splite video first")
        return  
    
    # replace blink frame with selected images  
    new_video_path = video_processor.replaceFrames(image_inputs)
    # video_processor.release()

    return new_video_path

with gr.Blocks() as app:
    image_inputs = []
    state = gr.State({"video_processor": None, "blink_frames": None})    
    with gr.Row():
        with gr.Column():
            with gr.Box():
                video_input = gr.Video(label="Select a Video")
            with gr.Row():
                interval_input = gr.Slider(value=5, minimum=1, maximum=10, step=1, label="Blink Interval(s)")
                duration_input = gr.Slider(value=0.2, minimum=0.1, maximum=0.6,  step=0.1, label="duration_input(s)")
            with gr.Row():
                splite_button = gr.Button(value="Splite Video")
                replace_button = gr.Button(value="Replace Frames")
            with gr.Box():  
                relaced_video_output = gr.Video(label="Replaced Video")

        with gr.Column():
            with gr.Box():
                caped_images_output = gr.Gallery(label="caped_images").style(columns=4, height="auto", object_fit="contain")
            with gr.Box():
                with gr.Row():
                    gr.Markdown("Select the blink images")
                with gr.Row():
                    for i in range(max_images):
                        image_input = gr.Image(label=f"{i}")
                        image_inputs.append(image_input)
            

    # extract blink frame from video
    ips = [video_input, interval_input, duration_input]
    ops = caped_images_output 
    splite_button.click(splite_video,ips, ops)
    # replace blink frame with selected images
    ips = image_inputs
    ops = relaced_video_output
    replace_button.click(replace_video, ips, ops)

app.launch(inline=False, debug=True)