from tkinter import *
import subprocess
# TODO script needs to be a file where the console output comes from
# https://stackoverflow.com/questions/665566/redirect-command-line-results-to-a-tkinter-gui
# https: // stackoverflow.com/questions/2449250/any-way-to-assign-terminal-output-to-variable-with-python
p = subprocess.Popen('echo "to stdout"', shell=True, stdout=subprocess.PIPE, )
output, errors = p.communicate()

root = Tk()
text = Text(root)
text.pack()
text.insert(END, output)
root.mainloop()
