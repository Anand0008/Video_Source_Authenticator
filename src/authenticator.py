from tkinter import *
from tkinter import messagebox
from Crypto.Cipher import AES
from tinyec import registry
import moviepy.editor as mp
from tkinter import filedialog
from moviepy.editor import *
import cv2
from stegano import lsb
import os
import binascii
import hashlib
import secrets
import shutil
def encrypt_AES_GCM(msg, secretKey):
    aesCipher = AES.new(secretKey, AES.MODE_GCM)
    ciphertext, authTag = aesCipher.encrypt_and_digest(msg)
    return (ciphertext, aesCipher.nonce, authTag)

def ecc_point_to_256_bit_key(point):
    sha = hashlib.sha256(int.to_bytes(point.x, 32, 'big'))
    sha.update(int.to_bytes(point.y, 32, 'big'))
    return sha.digest()

curve = registry.get_curve('brainpoolP256r1')

def encrypt_ECC(msg, pubKey):
    ciphertextPrivKey = secrets.randbelow(curve.field.n)
    sharedECCKey = ciphertextPrivKey * pubKey
    secretKey = ecc_point_to_256_bit_key(sharedECCKey)
    ciphertext, nonce, authTag = encrypt_AES_GCM(msg, secretKey)
    ciphertextPubKey = ciphertextPrivKey * curve.g
    return (ciphertext, nonce, authTag, ciphertextPubKey)

def takeinput():
 msg = message.get()
 b = msg.encode('utf-8')
 privKey = secrets.randbelow(curve.field.n)
 pubKey = privKey * curve.g

 encryptedMsg = encrypt_ECC(b, pubKey)
 encryptedMsgObj = {
    'ciphertext': binascii.hexlify(encryptedMsg[0]),
    'nonce': binascii.hexlify(encryptedMsg[1]),
    'authTag': binascii.hexlify(encryptedMsg[2]),
    'ciphertextPubKey': hex(encryptedMsg[3].x) + hex(encryptedMsg[3].y % 2)[2:]
}
 def printci():
  print("encrypted msg:", binascii.hexlify(encryptedMsg[0]))
  messagebox.showinfo("encrypted text", binascii.hexlify(encryptedMsg[0]))
 Button(screen, text=" Show ciphertext ", font=myfont, bg="blue", fg="white", command= printci).grid(row=5, column=1)
 def printnonce():
  print("Nonce:", binascii.hexlify(encryptedMsg[1]))
  messagebox.showinfo("Nonce", binascii.hexlify(encryptedMsg[1]))
 Button(screen, text=" Show Nonce", bg="blue", fg="white", command= printnonce).grid(row=6, column=1)
 def printauthtag():
  print("Auth Tag:", binascii.hexlify(encryptedMsg[2]))
  messagebox.showinfo("Auth Tag", binascii.hexlify(encryptedMsg[2]))
 Button(screen, text=" Show Auth Tag", bg="blue", fg="white", command= printauthtag).grid(row=7, column=1)
 def Pubkey():
  print("Public Key:", hex(encryptedMsg[3].x) + hex(encryptedMsg[3].y % 2)[2:])
  messagebox.showinfo("Public Key", hex(encryptedMsg[3].x) + hex(encryptedMsg[3].y % 2)[2:])
 Button(screen, text=" Show Public Key", bg="blue", fg="white", command= Pubkey).grid(row=8, column=1)
 global s
 s=binascii.hexlify(encryptedMsg[0])

def open():
    screen.filename = filedialog.askopenfilename(initialdir="/", title="Select Video File",filetypes=(("mp4 files", ".mp4"), ("all files", ".*")))
    global m
    m=screen.filename
def extractandembeed():

    # set video file path of input video with name and extension
    vid = cv2.VideoCapture(m)

    if not os.path.exists('images'):
        os.makedirs('images')

    if not os.path.exists('Encode'):
        os.makedirs('Encode')

    cap = cv2.VideoCapture(m)
    property_id = int(cv2.CAP_PROP_FRAME_COUNT)
    length = int(cv2.VideoCapture.get(cap, property_id))

    # for frame identity
    index = 1
    while (index <= length):
        # Extract images
        ret, frame = vid.read()
        # end of frames
        if not ret:
            break
        # Saves images
        name = './images/frame' + str(index) + '.jpg'
        print('Creating...' + name)
        cv2.imwrite(name, frame)
        # next frame
        # for loop for selecting frames
        secret = lsb.hide(name,s)  # hiding text in selected frames
        name1 = './Encode/encode_image' + str(index) + '.png'
        secret.save(name1)  # saving encoded image
        # replacing the frames
        size = (1280, 720)
        index += 1
def extractaudio():
    # Insert Local Video File Path
    clip = mp.VideoFileClip(m)
    # Insert Local Audio File Path
    clip.audio.write_audiofile(r"audio.mp3")
    # Create an object by passing the location as a string
def combineVideo():
    # Finding time of a video
    video = mp.VideoFileClip(m)
    # Contains the duration of the video in terms of seconds
    T = int(video.duration)
    # Finding total number of frames in video
    cap = cv2.VideoCapture(m)
    property_id = int(cv2.CAP_PROP_FRAME_COUNT)
    f = int(cv2.VideoCapture.get(cap, property_id))
    # making video out of frames
    s = "ffmpeg -framerate "
    l = int(f / T)
    print(l)
    g = str(l)
    p = " -i Encode/encode_image%01d.png -vcodec mpeg4 -y -vb 40M video.mp4"
    x = s + g + p
    os.system(x)
'''
#merging audio back into video to form stegano video
    clip = VideoFileClip("video.mp4")
    clip = clip.subclip(0, T)
    audioclip = AudioFileClip("audio.mp3").subclip(0, T)
    videoclip = clip.set_audio(audioclip)
'''
#delete all file as we don't need them now
def delete():
    shutil.rmtree(r'images')
    shutil.rmtree(r'Encode')
    os.remove("video.mp4")
    os.remove("audio.mp3")
#create a window(screen)
screen = Tk()
screen.title("VIDEO AUTHENTICATOR")
screen.geometry("1500x1400")
myfont = "Times 14 bold"
# Create a label to show the sub heading

label1 = Label(screen, text="||!!   Encryptor  !!||",font=myfont).grid(row=0, column=1)
# Create a label and put it on the grid
label10=Label(screen,text=" ").grid(row=1,column=0)
Label(screen, text="Enter Message:", font=myfont).grid(row=2, column=0)
message = StringVar()
Entry(screen, width=100, font=myfont, textvariable=message).grid(row=2, column=1)
label2=Label(screen,text=" ").grid(row=3,column=0)
# Create a button
Button(screen, text=" Encrypt ", font=myfont, bg="red", fg="white", command=takeinput,padx=80).grid(row=4, column=1)
label3=Label(screen,text=" ").grid(row=9,column=0)
mybutton= Button(screen, text=" Insert video file", font=myfont, bg="blue", fg="white", command=open,padx=35).grid(row=10, column=1)
label4=Label(screen,text=" ").grid(row=11,column=0)
mybutton1= Button(screen, text=" Extract frames and embeed", font=myfont, bg="blue", fg="white", command=extractandembeed).grid(row=12, column=0)
mybutton2= Button(screen, text=" Extract audio", font=myfont, bg="blue", fg="white", command=extractaudio).grid(row=12, column=2)
label5=Label(screen,text=" ").grid(row=13,column=0)
label6=Label(screen,text=" ").grid(row=14,column=0)
mybutton3= Button(screen, text=" Combine Video", font=myfont, bg="blue", fg="white", command=combineVideo,padx=20).grid(row=14, column=1)
label7=Label(screen,text=" ").grid(row=15,column=0)
mybutton4= Button(screen, text=" DELETE", font=myfont, bg="red", fg="white", padx="80",command=delete).grid(row=16, column=1)
label9=Label(screen,text=" ").grid(row=17,column=0)
label11=Label(screen,text="==================================================================================").grid(row=18,column=1)
label13 = Label(screen, text="||!!   Decryptor   !!||", font=myfont).grid(row=19, column=1)
label14=Label(screen,text=" ").grid(row=20,column=0)
Label(screen, text="Enter Video Id:", font=myfont).grid(row=21, column=0)
message1 = StringVar()
Entry(screen, width=100, font=myfont, textvariable=message1).grid(row=21, column=1)
label15=Label(screen,text=" ").grid(row=22,column=0)
Label(screen, text="Enter Public Key:", font=myfont).grid(row=23, column=0)
message2 = StringVar()
Entry(screen, width=100, font=myfont, textvariable=message2).grid(row=23, column=1)
label16=Label(screen,text=" ").grid(row=24,column=0)
Label(screen, text="Enter Video Length:", font=myfont).grid(row=25, column=0)
message3 = StringVar()
Entry(screen, width=100, font=myfont, textvariable=message3).grid(row=25, column=1)

screen.mainloop()