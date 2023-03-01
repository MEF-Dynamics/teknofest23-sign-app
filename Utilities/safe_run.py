from Constants import (
    PROGRAM_STRUCTURE_CHECK_LIST, 
    PROGRAM_PRE_EXITS_CHECK_LIST, 
    PROGRAM_POST_CLEANUP_CHECK_LIST, 
    PROGRAM_POST_CACHE_CHECK_LIST
)
import shutil
import os

def safe_start() -> None:
    """
    Method to check program structure and create folders if not exists.
    @Params:
        None
    @Returns:
        None
    """

    # Check these folders in PROGRAM_STRUCTURE_CHECK_LIST. Raise error if not exists.
    for path in PROGRAM_STRUCTURE_CHECK_LIST :
        if not os.path.exists(path) :
            raise FileNotFoundError("Program structure does not match, please reinstall the program. Missing: " + path)

    # Check these folders in PROGRAM_PRE_EXITS_CHECK_LIST. Clear if exists create otherwise.
    for path in PROGRAM_PRE_EXITS_CHECK_LIST :
        if not os.path.exists(path) :
            os.mkdir(path)

def safe_stop() -> None:
    """
    Method to check program structure and delete folders if exists.
    @Params:
        None
    @Returns:
        None
    """
    
    # Check these folders in PROGRAM_POST_CLEANUP_CHECK_LIST. Delete if exists.
    for path in PROGRAM_POST_CLEANUP_CHECK_LIST :
        if os.path.exists(path) :
            shutil.rmtree(path)

    # Check python cache folders in PROGRAM_POST_CACHE_CHECK_LIST. Delete if exists.
    for path in PROGRAM_POST_CACHE_CHECK_LIST :
        if os.path.exists(os.path.join(path, "__pycache__")) :
            shutil.rmtree(os.path.join(path, "__pycache__"))