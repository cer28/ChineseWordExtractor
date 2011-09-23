from distutils.core import setup
import py2exe

# setup(console=['main.py'])



# Notes on icons as resources:
#  - The settings I have that seem to work well are a combination of 64x64, 48x48, 32x32, and 16x16. Using 256 colors
#       seems to be adequate.
#  - The sizes in the icon set need to be sorted from largest size to smallest.

setup(
    windows = [
        {
            "script": "main.py",
            "icon_resources": [(1, "application-icon.ico")]
        }
    ],
)