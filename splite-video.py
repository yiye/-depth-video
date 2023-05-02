from modules.video import VideoProcessor
import os
import gradio as gr

output_dir = os.path.join(os.getcwd(), "output")
max_images = 12


def splite_video(video, interval, druation):
    print(f"video path: {video}")
    print(f"blink: interval {interval}， druation {druation}")
    video_processor = VideoProcessor(video_path=video, output_dir=output_dir)
    frames = video_processor.getFrames(interval=interval, druation=druation)
    video_processor.release()
    images = [frame["image"] for frame in frames]

    return images


with gr.Blocks() as app:
    image_inputs = []
    with gr.Row():
        with gr.Column():
            with gr.Row().style(height=400):
                video_input = gr.Video(label="Select a Video")
            with gr.Row():
                interval_input = gr.Slider(value=5, minimum=1, maximum=10, step=1, label="Blink Interval(s)")
                duration_input = gr.Slider(value=0.2, minimum=0.1, maximum=0.6,  step=0.1, label="duration_input(s)")
            with gr.Row():
                splite_button = gr.Button(value="Splite Video")
                replace_button = gr.Button(value="Replace Frames")
        
        with gr.Column():
            with gr.Row():
                caped_images_output = gr.Gallery(label="caped_images").style(columns=4, height="auto", object_fit="contain")
            with gr.Box():
                with gr.Row():
                    gr.Markdown("Select the blink images")
                with gr.Row():
                    for i in range(max_images):
                        image_input = gr.Image(label=f"{i}")
                        image_inputs.append(image_input)


    ips = [video_input, interval_input, duration_input]
    ops = caped_images_output 
    splite_button.click(splite_video,ips, ops)

app.launch(inline=False, debug=True)