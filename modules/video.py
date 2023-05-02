import cv2
import os
import shutil

class VideoProcessor:
    def __init__(self,video_path, output_dir) -> None:

        self.video_path = video_path
        self.output_dir = output_dir
        self.temp_dir = os.path.join(output_dir, "temp")
        
        if not os.path.exists(self.video_path):
            raise Exception("Video path does not exist") 
           
        self.clearOoutputDir()
        
        self.cap = cv2.VideoCapture(self.video_path)
    
    def clearOoutputDir(self):   
        shutil.rmtree(self.output_dir,ignore_errors=True)
        os.makedirs(self.output_dir)
        os.makedirs(self.temp_dir)  

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def getFrames(self, interval=8, druation=0.3):
        extracted_frames = []

        fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT)) 

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
    
        return extracted_frames


