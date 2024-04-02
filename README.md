# LivePy
LivePy reloads your html/css/js files, that are related to your html file 
you're working on.  

It uses [Live.js](https://livejs.com/) under the hood for the main work.  
LivePy injects the `live.js` file below your `<head>` tag and removes it, 
after you shutted down the programm via `Ctrl-c`.  

## Usage
You'll need the `live.py` and `live.js` in the same folder as your html file.  
This is a current 'limitation' by the `live.js` file and I don't want to hack 
it. In the future(TM) I'll create a more dynamic approach, that isn't dependend 
on the `live.js` file.  

```console
usage: live.py [-h] [-p PORT] html

positional arguments:
  html                  The file name of your html. You can omit the file extension ".html" if you want.

options:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Custom port. [Optional] (Default: 9005)
```

## Dependencies / License
You'll need:
- Python 3.9+
- Optional: current [Live.js](https://livejs.com/)

Inside this project, there's a live.js already included. But if you wish the 
latest version, fetch it from their homepage.  

`Live.js` comes with it's own license. Please see `LICENSE` for more information.

