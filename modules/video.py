import cv2
import os
import datetime
import shutil

class VideoProcessor:
    def __init__(self, output_dir) -> None:

        self.video_path = None
        self.output_dir = output_dir
        self.temp_dir = os.path.join(output_dir, "temp")
        
        self.clearOoutputDir()
        
        self.cap = None
        self.blink_frames = None
    
    def clearOoutputDir(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir,ignore_errors=True)
        os.makedirs(self.temp_dir)  

    def release(self):
        self.cap.release()
        self.video_path = None
        self.cap = None
        self.blink_frames = None
        cv2.destroyAllWindows()

    def loadVideo(self, video_path):
        if not os.path.exists(video_path):
            raise Exception("Video path does not exist") 
        self.video_path = video_path
        self.cap = cv2.VideoCapture(self.video_path)

    def getFrames(self, interval=8, druation=0.3):
        extracted_frames = []

        fps = int(self.cap.get(cv2.CAP_PROP_FPS))

        # calculate number of frames to extract every interval  
        num_frames = int(fps * druation)
        # calculate number of frames every interval
        num_interval_frames = int(fps * interval)

        frame_index = 0
        success = True
        times = 0
        while success:
            times += 1
            frame_index += num_interval_frames
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
            
            for i in range(num_frames):
                success, frame = self.cap.read()
                if not success:
                    break
                
                print(f"extracted:  {times} : {i}")

                # save frame to temp dir
                frame_path = os.path.join(self.temp_dir, f"orgin_{frame_index+i}.jpg")
                cv2.imwrite(frame_path, frame)

                # convert frame to image
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
                
                extracted_frames.append({
                    "index": frame_index+i,
                    "name": f"orgin_{frame_index+i}",
                    "frame": frame,
                    "image": image,
                    "frame_path": frame_path
                })

        self.blink_frames = extracted_frames
        return extracted_frames

    def replaceFrames(self, images):
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))   
        fps = int(self.cap.get(cv2.CAP_PROP_FPS))

        # set video encoder
        fourcc_code = int(self.cap.get(cv2.CAP_PROP_FOURCC))
        # fourcc_str = "".join([chr((fourcc_code >> 8 * i) & 0xFF) for i in range(4)])

        now = datetime.datetime.now()   
        format_now = now.strftime("%Y-%m-%d_%H-%M-%S")
        output_video_name = f"video_{format_now}.mp4"
        output_video_path = os.path.join(self.output_dir, output_video_name)

        output_video = cv2.VideoWriter(output_video_path, fourcc_code, fps, (width, height))

        # cosntruct a dict of frame index and image
        replacement_frames = {}
        for index, image in enumerate(images):
            if image is None:
                break

            frame = self.blink_frames[index]
            if frame is None:
                break
            resized_image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)   
            replacement_frames[frame["index"]] = resized_image  
            
        # write self.cap frames to output video, if frame index is in images, replace it with image
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        while True:
            success, frame = self.cap.read()
            if not success:
                break
            frame_index = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
            if frame_index in replacement_frames:
                frame = replacement_frames[frame_index]   
                
            output_video.write(frame)   
        
        output_video.release()
        
        return output_video_path   

