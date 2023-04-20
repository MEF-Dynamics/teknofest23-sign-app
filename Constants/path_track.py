from os import path, listdir

def connect_pathes(*pathes): return path.join(*pathes)

PROJECT_DIRECTORY = path.dirname(path.dirname(path.abspath(__file__)))

RUN_ASSETS_FOLDER_PATH = connect_pathes(PROJECT_DIRECTORY, "Assets")
RUN_TEMP_FOLDER_PATH = connect_pathes(PROJECT_DIRECTORY, "Temp")
RUN_UTILITIES_FOLDER_PATH = connect_pathes(PROJECT_DIRECTORY, "Utilities")
RUN_SOURCES_FOLDER_PATH = connect_pathes(PROJECT_DIRECTORY, "Sources")
RUN_CONSTANTS_FOLDER_PATH = connect_pathes(PROJECT_DIRECTORY, "Constants")
RUN_GUI_FOLDER_PATH = connect_pathes(PROJECT_DIRECTORY, "GUI")

AI_MODEL_PATH = connect_pathes(RUN_SOURCES_FOLDER_PATH, "Model", "model.h5")

GUI_FOLDER_PATH = connect_pathes(RUN_ASSETS_FOLDER_PATH, "GUI")
GUI_CAMERA_B_PNG = connect_pathes(GUI_FOLDER_PATH, "GUI_Cam_B.png")
GUI_CAMERA_R_PNG = connect_pathes(GUI_FOLDER_PATH, "GUI_Cam_R.png")
GUI_MICROPHONE_R_PNG = connect_pathes(GUI_FOLDER_PATH, "GUI_Mic_R.png")
GUI_MICROPHONE_B_PNG = connect_pathes(GUI_FOLDER_PATH, "GUI_Mic_B.png")
GUI_NOTFOUND_PNG = connect_pathes(GUI_FOLDER_PATH, "GUI_Not_Found.png")
GUI_PHONE_PNG = connect_pathes(GUI_FOLDER_PATH, "GUI_Phone.png")

OTHER_FOLDER_PATH = connect_pathes(RUN_ASSETS_FOLDER_PATH, "Other")
OTHER_CLUB_ICO_ICO = connect_pathes(OTHER_FOLDER_PATH, "Club_Ico.ico")
OTHER_CLUB_LOGO_PNG = connect_pathes(OTHER_FOLDER_PATH, "Club_Logo.png")
OTHER_TEKNOFEST_LOGO_PNG = connect_pathes(OTHER_FOLDER_PATH, "Teknofest_Logo.png")

ANIM_FOLDER_PATH = connect_pathes(RUN_ASSETS_FOLDER_PATH, "Animations")
ANIM_ANIMATIONS = {file.split("\\")[-1].split(".")[0][len("ANIM_"):]: file for file in [connect_pathes(ANIM_FOLDER_PATH, file) for file in listdir(ANIM_FOLDER_PATH)]}
ANIM_DEFAULT = connect_pathes(ANIM_FOLDER_PATH, "ANIM_Default.gif")
ANIM_DEFAULT_LISTENING = connect_pathes(ANIM_FOLDER_PATH, "ANIM_Default_Listening.gif")
ANIM_teknofest = connect_pathes(ANIM_FOLDER_PATH, "ANIM_teknofest.gif")

PROGRAM_STRUCTURE_CHECK_LIST = [
    RUN_ASSETS_FOLDER_PATH,
    RUN_UTILITIES_FOLDER_PATH,
    RUN_SOURCES_FOLDER_PATH,
    GUI_FOLDER_PATH,
    OTHER_FOLDER_PATH,
    ANIM_FOLDER_PATH,
    AI_MODEL_PATH,
    RUN_GUI_FOLDER_PATH
]

PROGRAM_PRE_EXITS_CHECK_LIST = [
    RUN_TEMP_FOLDER_PATH,
]

PROGRAM_POST_CLEANUP_CHECK_LIST = [
    RUN_TEMP_FOLDER_PATH,
]

PROGRAM_POST_CACHE_CHECK_LIST = [
    RUN_CONSTANTS_FOLDER_PATH,
    RUN_UTILITIES_FOLDER_PATH,
    RUN_GUI_FOLDER_PATH
]