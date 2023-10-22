import subprocess
import os
import re
import argparse

def process_text(input_file_path, output_dir_path):
    # Ensure the output directory exists
    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)

    # Read the lines from the input file
    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    total_lines = len(lines)
    for index, line in enumerate(lines, start=1):
        # Remove any non-alphanumeric characters and replace spaces with underscores
        sanitized_line = re.sub(r'[^a-zA-Z0-9 ]', '', line).replace(' ', '_').strip()

        # Formulate the output path
        output_path_wav = os.path.join(output_dir_path, f'{sanitized_line}.wav')
        output_path_mp3 = os.path.join(output_dir_path, f'{sanitized_line}.mp3')

        # Check if files with the same name already exist and delete them
        for path in [output_path_wav, output_path_mp3]:
            if os.path.exists(path):
                os.remove(path)

        # Display progress
        print(f'Processing line {index} of {total_lines}: {line.strip()}')

        if not line.strip().endswith(('.', '?', '!')):
            line = line.strip() + '.'

        # Run the TTS command
        subprocess.run([
            'tts',
            '--text', line.strip(),
            '--model_name', 'tts_models/en/ljspeech/tacotron2-DDC_ph', # tts_models/en/ljspeech/tacotron2-DDC_ph
            '--vocoder_name', 'vocoder_models/en/ljspeech/multiband-melgan',
            '--out_path', output_path_wav
        ])

        # Convert the WAV file to MP3
        subprocess.run([
            'ffmpeg',
            '-i', output_path_wav,
            output_path_mp3
        ])

        # Delete the WAV file
        os.remove(output_path_wav)

def main():
    parser = argparse.ArgumentParser(description='Process text to speech.')
    parser.add_argument('input_file', help='Path to the input text file.')
    parser.add_argument('output_dir', help='Path to the output directory.')
    args = parser.parse_args()

    process_text(args.input_file, args.output_dir)

if __name__ == '__main__':
    main()
