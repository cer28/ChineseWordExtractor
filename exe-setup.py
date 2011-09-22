from distutils.core import setup
import py2exe

# setup(console=['main.py'])


setup(
    windows = [
        {
            "script": "main.py",
            "icon_resources": [(1, "application-icon.ico")]
        }
    ],
)