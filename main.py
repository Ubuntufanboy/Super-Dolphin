import ffmpeg

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
            fontsize=24, fontcolor='white', shadowcolor='black', shadowx=2, shadowy=2
        )
    
    stream = ffmpeg.output(stream, input_audio, output_file, vcodec='libx264', acodec='aac', strict='experimental', pix_fmt='yuv420p')
    ffmpeg.run(stream)

# Example usage
background_video = 'ba.mp4'
image_elements = [
    {'file': 'weird.jpg', 'x': 50, 'y': 50, 'start_time': 0, 'end_time': 5},
    {'file': 'unfunny.gif', 'x': 100, 'y': 100, 'start_time': 5, 'end_time': 30, 'width': 200, 'height': 200}
]
audio_file = 'badapple.mp3'
text_elements = [
    {'text': 'Hello, World!', 'x': 200, 'y': 150, 'start_time': 2, 'end_time': 8}
]
output_file = 'output.mp4'

generate_video(background_video, image_elements, audio_file, output_file, text_elements)

