import os
import sys
import json
import subprocess
import glob
import shutil
from pathlib import Path

def main():
    print("Starting Spark-TTS inference...")
    
    # Create outputs directory if it doesn't exist
    os.makedirs("/outputs", exist_ok=True)

    # Get input from environment variables
    input_text = os.environ.get("INPUT", "Hello, this is a test of the text to speech system.")
    
    # Set default values for voice cloning
    prompt_speech_path = os.environ.get("PROMPT_SPEECH_PATH", "/app/audio/voice.wav")
    prompt_text = os.environ.get("PROMPT_TEXT", "You can generate a customized voice by adjusting parameters such as pitch and speed")
    
    # Determine if we're using voice cloning (now always true unless file doesn't exist)
    use_voice_cloning = os.path.exists(prompt_speech_path)
    
    try:
        # Change to the Spark-TTS directory
        os.chdir("/app/Spark-TTS")
        
        # Create save directory
        save_dir = "/outputs"
        
        # Set the model directory
        model_dir = "pretrained_models/Spark-TTS-0.5B"
        
        # Check if the model exists
        if not os.path.exists(model_dir):
            raise FileNotFoundError(f"Model directory not found: {model_dir}")
        
        # Check if GPU is available
        try:
            import torch
            device = 0 if torch.cuda.is_available() else -1
            if device == 0:
                print("✅ GPU detected - using GPU for inference")
            else:
                print("ℹ️ No GPU detected - falling back to CPU")
        except ImportError:
            print("ℹ️ Torch not available - falling back to CPU")
            device = -1
        
        # Build the command
        cmd = [
            "python", "-m", "cli.inference",
            "--text", input_text,
            "--device", str(device),
            "--save_dir", save_dir,
            "--model_dir", model_dir
        ]
        
        if use_voice_cloning:
            print(f"Using voice cloning with reference audio: {prompt_speech_path}")
            print(f"Reference audio transcript: {prompt_text}")
            cmd.extend(["--prompt_speech_path", prompt_speech_path, "--prompt_text", prompt_text])
        else:
            print(f"Warning: Reference audio file not found at {prompt_speech_path}")
            print("Falling back to default voice (zero-shot mode)")
        
        print(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Print the output
        print("STDOUT:", result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
            
        if result.returncode != 0:
            raise Exception(f"Inference failed with return code {result.returncode}")
        
        # Find the generated audio file - Spark-TTS names files with timestamps
        generated_files = glob.glob(f"{save_dir}/*.wav")
        if not generated_files:
            raise FileNotFoundError(f"No audio files were generated in {save_dir}")
        
        # Get the most recently created file
        latest_file = max(generated_files, key=os.path.getctime)
        print(f"✅ Successfully generated audio at {latest_file}")
            
        # Create metadata for output
        output_data = {
            "input_text": input_text,
            "audio_path": latest_file,
            "mode": "voice_cloning" if use_voice_cloning else "default_voice",
            "status": "success"
        }
        
        if use_voice_cloning:
            output_data["prompt_text"] = prompt_text
            output_data["prompt_speech_path"] = prompt_speech_path
        
        # Save metadata to JSON
        metadata_path = "/outputs/result.json"
        with open(metadata_path, "w") as f:
            json.dump(output_data, f, indent=2)
        
        print(f"✅ Metadata saved to {metadata_path}")
        
    except Exception as error:
        print(f"❌ Error during processing: {error}", flush=True)
        import traceback
        traceback.print_exc()
        
        # Create error output
        output_data = {
            "input_text": input_text,
            "status": "error",
            "error": str(error)
        }
        
        # Save error metadata
        metadata_path = "/outputs/result.json"
        with open(metadata_path, "w") as f:
            json.dump(output_data, f, indent=2)

if __name__ == "__main__":
    main()