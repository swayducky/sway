import os
import torch
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
import imageio
import shutil


class MyModel:
    def __init__(self):
        MODEL_CACHE = "model-cache"
        # if os.path.exists(MODEL_CACHE):
        #   shutil.rmtree(MODEL_CACHE)
        os.makedirs(MODEL_CACHE, exist_ok=True)
        """Load the model into memory to make running multiple predictions efficient"""
        self.pipe = DiffusionPipeline.from_pretrained(
            "damo-vilab/text-to-video-ms-1.7b",
            torch_dtype=torch.float16,
            variant="fp16",
            cache_dir=MODEL_CACHE,
            local_files_only=True,
        ).to("cuda")

        self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
            self.pipe.scheduler.config
        )
        self.pipe.enable_model_cpu_offload()
        self.pipe.enable_vae_slicing()

    def predict(
        self,
        prompt="An astronaut riding a horse",
        num_frames=16,
        num_inference_steps=50,  # >= 1, <= 500 -- denoising steps
        fps=8,
        seed=None,  # leave none to randomize
    ):
        if seed is None:
            seed = int.from_bytes(os.urandom(2), "big")
        print(f"Using seed: {seed}")

        generator = torch.Generator("cuda").manual_seed(seed)
        frames = self.pipe(
            prompt,
            num_inference_steps=num_inference_steps,
            num_frames=num_frames,
            generator=generator,
        ).frames

        out = "out.mp4"
        writer = imageio.get_writer(out, format="FFMPEG", fps=fps)
        for frame in frames:
            writer.append_data(frame)
        writer.close()


if __name__ == "__main__":
    model = MyModel()
