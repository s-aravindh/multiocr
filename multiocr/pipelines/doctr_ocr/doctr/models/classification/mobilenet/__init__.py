from doctr.file_utils import is_tf_available, is_torch_available

if is_tf_available():
    from .tensorflow import *
elif is_torch_available():
    from .pytorch import *
