import os
import torch
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
import imageio
from slugify import slugify
import shutil


class MyModel:
    def __init__(self):
        print("Loading model...")
        """Load the model into memory to make running multiple predictions efficient"""
        self.pipe = DiffusionPipeline.from_pretrained(
            "damo-vilab/text-to-video-ms-1.7b",
            torch_dtype=torch.float16,
            variant="fp16",
        ).to("cuda")

        self.pipe.scheduler = DPMSolverMultistepScheduler.from_config(
            self.pipe.scheduler.config
        )
        self.pipe.enable_model_cpu_offload()
        self.pipe.enable_vae_slicing()

    def predict(
        self,
        prompt="An astronaut riding a horse",
        num_frames=32,
        num_inference_steps=50,  # >= 1, <= 500 -- denoising steps
        fps=8,
        seed=None,  # leave none to randomize
    ):
        print("Running inference...")
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

        out = f"_out/{slugify(prompt)}.mp4"
        writer = imageio.get_writer(out, format="FFMPEG", fps=fps)
        for frame in frames:
            writer.append_data(frame)
        writer.close()


if __name__ == "__main__":
    """
Give me a bunch of funny meme-worthy topics. These topics are used to feed an AI video generator.

Example topics:
- Neo eating a sandwich
- Will Smith eating spaghetti
    """
    model = MyModel()
    prompts = """Albert Einstein riding a skateboard
Elon Musk running a lemonade stand
Squirrels organizing a heist for acorns
Shrek doing yoga
The Queen of England playing video games
The statue of Liberty taking a selfie
Penguins having a snowball fight
Mona Lisa ordering a pizza
The Rock preparing a Vegan meal
A T-Rex trying to play the piano
Darth Vader in a baking show
Abraham Lincoln DJing at a club
Sherlock Holmes lost in Ikea
The Eiffel Tower doing the Macarena
Bruce Lee in a ballet class
A UFO stuck in traffic
Spiderman knitting a sweater
Napoleon Bonaparte in a rap battle
Aliens learning to use chopsticks
Godzilla on a surfing holiday
Bill Gates trying to fix a printer
A mermaid at a sushi bar
Zombies participating in a marathon
Captain America on a pottery wheel
The Loch Ness Monster at a pool party.
A cactus going for a walk.
Bigfoot doing a TikTok dance.
A robot struggling with a Rubik's cube.
A unicorn running a coffee shop.
The Sphinx getting a nose job.""".split('\n')
    print("My prompts:", prompts)
    for prompt in prompts:
        model.predict(prompt)
