from pygrabber.dshow_graph import FilterGraph
from PIL import Image
import pyaudio

def get_available_michrophones() -> dict:
    """
    Method, that returns the microphones that are available on the computer.
    @Params
        None
    @Returns
        available_microphones : dict - Available microphones.
    """

    available_microphones = {}
    pyduo = pyaudio.PyAudio()
    devices_info = pyduo.get_host_api_info_by_index(0)
    number_of_devices = devices_info.get('deviceCount')
    for device_index in range(0, number_of_devices):
        if (pyduo.get_device_info_by_host_api_device_index(0, device_index).get('maxInputChannels')) > 0:
            available_microphones[device_index] = pyduo.get_device_info_by_host_api_device_index(0, device_index).get('name')

    return available_microphones

def get_available_cameras() -> dict:
    """
    Method, that returns the cameras that are available on the computer.
    @Params
        None
    @Returns
        available_cameras : dict - Available cameras.
    """

    devices = FilterGraph().get_input_devices()

    available_cameras = {}

    for device_index, device_name in enumerate(devices):
        available_cameras[device_index] = device_name

    return available_cameras

def get_gif_frame_count(gif_file_path:str) -> int:
    """
    Method, that returns the number of frames in a gif file.
    @Params
        gif_file_path : str - (Required) The path to the gif file.
    @Returns
        number_of_frames : int - The number of frames in the gif file.
    """

    with Image.open(gif_file_path) as gif_file:
        number_of_frames = 0
        while True:
            try:
                gif_file.seek(number_of_frames)
                number_of_frames += 1
            except EOFError:
                break

    return number_of_frames