import sys
from modelscope.pipelines import pipeline
from modelscope.outputs import OutputKeys

pipe = pipeline(task='image-to-video', model='damo/Image-to-Video', model_revision='v1.1.0')

def main():
    img_path = sys.argv[1]
    # convert IMG_PATH to proper VIDEO_PATH with _output.mp4 appended
    img_path_without_extension = img_path.split('.')[0]
    output_video_path = pipe(img_path, output_video=img_path_without_extension + '.mp4')[OutputKeys.OUTPUT_VIDEO]
    print("Generated:", output_video_path)

if __name__ == '__main__':
    main()
