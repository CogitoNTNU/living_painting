import subprocess
import os

deep_face_lab_folder = './DeepFaceLab'
target_folder = '/workspace/data_dst'
source_folder = '/workspace/data_src'

if os.path.isdir(deep_face_lab_folder):
    if not os.listdir(deep_face_lab_folder+target_folder):
        print('Add target video')
        exit()
    if not os.listdir(deep_face_lab_folder+source_folder):
        print('Add source video')
        exit()
    
    subprocess.run(["name", "-n"]])
    subprocess.run(Step3)
    subprocess.run(Step4)
    subprocess.run(Step5)
    subprocess.run(Step6)
    subprocess.run(Step7)
    subprocess.run(Step8)




else:
    print("Install https://github.com/iperov/DeepFaceLab and add to ./DeepFaceLab")
