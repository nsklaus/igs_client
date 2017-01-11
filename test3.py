import tkinter as tk

image_data = '''
    R0lGODlhEAAQAMQZAMPDw+zs7L+/v8HBwcDAwLW1teLi4t7e3uDg4MLCwuHh4e7u7t/f38TExLa2
    tre3t7i4uL6+vu/v77q6uu3t7b29vby8vLm5ubu7u+3t7QAAAAAAAAAAAAAAAAAAAAAAACH5BAEA
    ABkALAAAAAAQABAAAAWNYCaOZFlWV6pWZlZhTQwAyYSdcGRZGGYNE8vo1RgYCD2BIkK43DKXRsQg
    oUQiFAkCI3iILgCLIEvJBiyQiOML6GElVcsFUllD25N3FQN51L81b2ULARN+dhcDFggSAT0BEgcQ
    FgUicgQVDHwQEwc+DxMjcgITfQ8Pk6AlfBEVrjuqJhMOtA4FBRctuiUhADs=
'''

root = tk.Tk()

image = tk.PhotoImage(data=image_data)
back = tk.PhotoImage(file="images/goban2.png")
stone  = tk.PhotoImage(file="images/black.png")

dimensions = "image size: %dx%d" % (image.width(), image.height())
bgnd = tk.Label(root, compound="top", image=back)
bgnd.pack()

icon = tk.Label(root, compound="top", image=stone) #image, text=dimensions)
icon.place(x=100, y=200)
root.mainloop()