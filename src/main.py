"""
WARNING! THIS CODE DOES *NOT* WORK. THIS IS A COMMIT SO THAT OTHERS CAN WORK ON THIS AT THE SAME TIME
WARNING! THIS CODE DOES *NOT* WORK. THIS IS A COMMIT SO THAT OTHERS CAN WORK ON THIS AT THE SAME TIME
WARNING! THIS CODE DOES *NOT* WORK. THIS IS A COMMIT SO THAT OTHERS CAN WORK ON THIS AT THE SAME TIME
WARNING! THIS CODE DOES *NOT* WORK. THIS IS A COMMIT SO THAT OTHERS CAN WORK ON THIS AT THE SAME TIME
WARNING! THIS CODE DOES *NOT* WORK. THIS IS A COMMIT SO THAT OTHERS CAN WORK ON THIS AT THE SAME TIME
WARNING! THIS CODE DOES *NOT* WORK. THIS IS A COMMIT SO THAT OTHERS CAN WORK ON THIS AT THE SAME TIME
WARNING! THIS CODE DOES *NOT* WORK. THIS IS A COMMIT SO THAT OTHERS CAN WORK ON THIS AT THE SAME TIME
WARNING! THIS CODE DOES *NOT* WORK. THIS IS A COMMIT SO THAT OTHERS CAN WORK ON THIS AT THE SAME TIME
WARNING! THIS CODE DOES *NOT* WORK. THIS IS A COMMIT SO THAT OTHERS CAN WORK ON THIS AT THE SAME TIME
WARNING! THIS CODE DOES *NOT* WORK. THIS IS A COMMIT SO THAT OTHERS CAN WORK ON THIS AT THE SAME TIME
WARNING! THIS CODE DOES *NOT* WORK. THIS IS A COMMIT SO THAT OTHERS CAN WORK ON THIS AT THE SAME TIME
WARNING! THIS CODE DOES *NOT* WORK. THIS IS A COMMIT SO THAT OTHERS CAN WORK ON THIS AT THE SAME TIME
WARNING! THIS CODE DOES *NOT* WORK. THIS IS A COMMIT SO THAT OTHERS CAN WORK ON THIS AT THE SAME TIME
WARNING! THIS CODE DOES *NOT* WORK. THIS IS A COMMIT SO THAT OTHERS CAN WORK ON THIS AT THE SAME TIME
WARNING! THIS CODE DOES *NOT* WORK. THIS IS A COMMIT SO THAT OTHERS CAN WORK ON THIS AT THE SAME TIME
WARNING! THIS CODE DOES *NOT* WORK. THIS IS A COMMIT SO THAT OTHERS CAN WORK ON THIS AT THE SAME TIME
WARNING! THIS CODE DOES *NOT* WORK. THIS IS A COMMIT SO THAT OTHERS CAN WORK ON THIS AT THE SAME TIME
WARNING! THIS CODE DOES *NOT* WORK. THIS IS A COMMIT SO THAT OTHERS CAN WORK ON THIS AT THE SAME TIME
WARNING! THIS CODE DOES *NOT* WORK. THIS IS A COMMIT SO THAT OTHERS CAN WORK ON THIS AT THE SAME TIME
WARNING! THIS CODE DOES *NOT* WORK. THIS IS A COMMIT SO THAT OTHERS CAN WORK ON THIS AT THE SAME TIME
WARNING! THIS CODE DOES *NOT* WORK. THIS IS A COMMIT SO THAT OTHERS CAN WORK ON THIS AT THE SAME TIME
WARNING! THIS CODE DOES *NOT* WORK. THIS IS A COMMIT SO THAT OTHERS CAN WORK ON THIS AT THE SAME TIME
WARNING! THIS CODE DOES *NOT* WORK. THIS IS A COMMIT SO THAT OTHERS CAN WORK ON THIS AT THE SAME TIME
WARNING! THIS CODE DOES *NOT* WORK. THIS IS A COMMIT SO THAT OTHERS CAN WORK ON THIS AT THE SAME TIME
WARNING! THIS CODE DOES *NOT* WORK. THIS IS A COMMIT SO THAT OTHERS CAN WORK ON THIS AT THE SAME TIME
WARNING! THIS CODE DOES *NOT* WORK. THIS IS A COMMIT SO THAT OTHERS CAN WORK ON THIS AT THE SAME TIME
WARNING! THIS CODE DOES *NOT* WORK. THIS IS A COMMIT SO THAT OTHERS CAN WORK ON THIS AT THE SAME TIME
WARNING! THIS CODE DOES *NOT* WORK. THIS IS A COMMIT SO THAT OTHERS CAN WORK ON THIS AT THE SAME TIME
WARNING! THIS CODE DOES *NOT* WORK. THIS IS A COMMIT SO THAT OTHERS CAN WORK ON THIS AT THE SAME TIME
WARNING! THIS CODE DOES *NOT* WORK. THIS IS A COMMIT SO THAT OTHERS CAN WORK ON THIS AT THE SAME TIME
"""
print("WARNING THIS DOES NOT WORK RIGHT NOW!")
import ffmpeg
import json

def approximate_font_size(desired_width, num_chars):
    """
    This function approximates the font size required to fit a given number of characters within a desired width.

    Args:
        desired_width: The desired width of the text in pixels.
        num_chars: The number of characters in the text.

    Returns:
    An integer representing the approximate font size in pixels (rounded down).
    """

    average_char_width = 7  # pixels per character. NOTE: This is an approximate
    char_spacing_factor = 0.2  # Account for space between characters (adjust as needed)

    min_font_size = 6  # adjust as needed

    special_char_penalty = (num_chars > 0) * 1  # Add 1 pixel for non-empty strings

    required_space = desired_width - special_char_penalty

    estimated_font_size = int(required_space / (num_chars * (average_char_width + char_spacing_factor)))

    # Ensure the font size isn't too small (round down for safety)
    return estimated_font_size - 1
def generate_video(background_video, image_elements, audio_file, output_file, text_elements=[]):
    """
    Generate a video with a background video, image elements, audio, and text.

    :param background_video: Path to the background video file.
    :param image_elements: List of dictionaries with keys 'file', 'x', 'y', 'start_time', 'end_time'.
    :param audio_file: Path to the audio file.
    :param output_file: Path to the output video file.
    :param text_elements: List of dictionaries with keys 'text', 'x', 'y', 'start_time', 'end_time'.
    """
    input_video = ffmpeg.input(background_video)
    input_audio = ffmpeg.input(audio_file)
    
    stream = input_video

    for image in image_elements:
        if image['file'].endswith('.gif'):
            image_input = ffmpeg.input(image['file'], ignore_loop=0)
            image_stream = image_input['v'].filter('scale', image.get('width', -1), image.get('height', -1))
            stream = ffmpeg.overlay(
                stream, image_stream, x=image['x'], y=image['y'], 
                enable=f'between(t,{image["start_time"]},{image["end_time"]})',
                shortest=1
            )
        else:
            image_input = ffmpeg.input(image['file'])
            stream = ffmpeg.overlay(
                stream, image_input, x=image['x'], y=image['y'], 
                enable=f'between(t,{image["start_time"]},{image["end_time"]})'
            )
    
    for text in text_elements:
        stream = ffmpeg.drawtext(
            stream, text=text['text'], x=text['x'], y=text['y'],
            enable=f'between(t,{text["start_time"]},{text["end_time"]})',
            fontsize=12, fontcolor='white', shadowcolor='black', shadowx=2, shadowy=2
        )
    
    stream = ffmpeg.output(stream, input_audio, output_file, vcodec='libx264', acodec='aac', strict='experimental', pix_fmt='yuv420p')
    ffmpeg.run(stream)

"""
# Example usage
background_video = 'ba.mp4'
image_elements = [
    {'file': 'weird.jpg', 'x': 50, 'y': 50, 'start_time': 0, 'end_time': 5},
    {'file': 'unfunny.gif', 'x': 100, 'y': 100, 'start_time': 5, 'end_time': 30, 'width': 200, 'height': 200}
]
audio_file = 'badapple.mp3'

text_elements = [
    {'text': 'Hello, World!', 'x': 10, 'y': 10, 'start_time': 2, 'end_time': 8}
]
"""

def read_layout_from_json(file_path):
    text_elements = []
    image_elements = []
    video_elements = []

    try:
        with open(file_path, 'r') as json_file:
            layout_data = json.load(json_file)
            elements = layout_data.get('elements', [])
            for element in elements:
                if element["type"] == "text":
                    text_elements.append({
                        "text": element['text'],
                        "x": element['x'],
                        "y": element['y']
                    })
                elif element["type"] == "image":
                    image_elements.append({
                        "path": element['path'],
                        "x": element['x'],
                        "y": element['y']
                    })
                elif element["type"] == "video":
                    video_elements.append({
                        "path": element['path'],
                        "x": element['x'],
                        "y": element['y']
                    })
                else:
                    print(f"Unknown Element: {element}")

        return text_elements, image_elements, video_elements

    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
        return text_elements, image_elements, video_elements
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file {file_path}.")
        return text_elements, image_elements, video_elements
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return text_elements, image_elements, video_elements

if __name__ == "__main__":
    file_path = 'layout.json'  # TODO: Change path of main.py in the design directory to save layout.json to src/
    text_elements, image_elements, video_elements = read_layout_from_json(file_path)
    
    background_video = input("Please enter the file path to the background video. If you don't want a video background please type \"n\"")
    if background_video.lower() == "n":
        file = "nobackground.mp4"
    else:
        file = background_video

    images_ffmpeg = []
    for img in image_elements:
        images_ffmpeg.append({'file': img['path'], 'x': img['x'], 'y': img['y'], 'start_time': 0, 'end_time': 30})

    video_ffmpeg = []
    for vid in video_elements:
        video_ffmpeg.append({'file': vid['path'], 'x': vid['x'], 'y': vid['y'], 'start_time': 0, 'end_time': 30})

    generate_video(background_video, image_elements, audio_file=None, )
