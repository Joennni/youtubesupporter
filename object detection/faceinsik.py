
#python detect_min.py --weights yolov5s.pt --conf 0.3 --source 0
# YOLOv5 🚀 by Ultralytics, GPL-3.0 license

# 인터페이스 설명
"""
Run inference on images, videos, directories, streams, etc.

Usage - sources:
    $ python path/to/detect.py --weights yolov5s.pt --source 0              # webcam
                                                             img.jpg        # image
                                                             vid.mp4        # video
                                                             path/          # directory
                                                             path/*.jpg     # glob
                                                             'https://youtu.be/Zgi9g1ksQHc'  # YouTube
                                                             'rtsp://example.com/media.mp4'  # RTSP, RTMP, HTTP stream

Usage - formats:
    $ python path/to/detect.py --weights yolov5s.pt                 # PyTorch
                                         yolov5s.torchscript        # TorchScript
                                         yolov5s.onnx               # ONNX Runtime or OpenCV DNN with --dnn
                                         yolov5s.xml                # OpenVINO
                                         yolov5s.engine             # TensorRT
                                         yolov5s.mlmodel            # CoreML (macOS-only)
                                         yolov5s_saved_model        # TensorFlow SavedModel
                                         yolov5s.pb                 # TensorFlow GraphDef
                                         yolov5s.tflite             # TensorFlow Lite
                                         yolov5s_edgetpu.tflite     # TensorFlow Edge TPU
"""
from pathlib import Path
from PIL import Image
from PIL import ImageFilter
from datetime import datetime
from bs4 import BeautifulSoup
from models.common import DetectMultiBackend
from utils.dataloaders import IMG_FORMATS, VID_FORMATS, LoadImages, LoadStreams
from utils.general import (LOGGER, check_file, check_img_size, check_imshow, check_requirements, colorstr, cv2,
                           increment_path, non_max_suppression, print_args, scale_coords, strip_optimizer, xyxy2xywh)
from utils.plots import Annotator, colors, save_one_box
from utils.torch_utils import select_device, time_sync
import sqlite3
import argparse
import os
import sys
import pyautogui
import torch
import torch.backends.cudnn as cudnn
import pandas as pd
import time
import glob
import shutil
import warnings 
warnings.filterwarnings('ignore')
import re
import keyboard


FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative
fw = pyautogui.getActiveWindow()


class faceinsik:   
    
    print('faceinsik') 
    
    def __init__(self):
        parser2 = argparse.ArgumentParser()
        parser2.add_argument('--weights', nargs='+', type=str, default=ROOT / './runs/train/test/weights/best.pt', help='model path(s)')
        parser2.add_argument('--source', type=str, default=ROOT / '1', help='file/dir/URL/glob, 0 for webcam')
        parser2.add_argument('--data', type=str, default=ROOT / 'data/coco128.yaml', help='(optional) dataset.yaml path')
        parser2.add_argument('--imgsz', '--img', '--img-size', nargs='+', type=int, default=[640], help='inference size h,w')
        parser2.add_argument('--conf-thres', type=float, default=0.25, help='confidence threshold')
        parser2.add_argument('--iou-thres', type=float, default=0.45, help='NMS IoU threshold')
        parser2.add_argument('--max-det', type=int, default=1000, help='maximum detections per image')
        parser2.add_argument('--device', default='', help='cuda device, i.e. 0 or 0,1,2,3 or cpu')
        parser2.add_argument('--view-img', action='store_true', help='show results')
        parser2.add_argument('--save-txt', action='store_true', help='save results to *.txt')
        parser2.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels')
        parser2.add_argument('--save-crop', action='store_true', help='save cropped prediction boxes')
        parser2.add_argument('--nosave', action='store_true', help='do not save images/videos')
        parser2.add_argument('--classes', nargs='+', type=int, help='filter by class: --classes 0, or --classes 0 2 3')
        parser2.add_argument('--agnostic-nms', action='store_true', help='class-agnostic NMS')
        parser2.add_argument('--augment', action='store_true', help='augmented inference')
        parser2.add_argument('--visualize', action='store_true', help='visualize features')
        parser2.add_argument('--update', action='store_true', help='update all models')
        parser2.add_argument('--project', default=ROOT / 'runs/detect', help='save results to project/name')
        parser2.add_argument('--name', default='exp', help='save results to project/name')
        parser2.add_argument('--exist-ok', action='store_true', help='existing project/name ok, do not increment')
        parser2.add_argument('--line-thickness', default=3, type=int, help='bounding box thickness (pixels)')
        parser2.add_argument('--hide-labels', default=False, action='store_true', help='hide labels')
        parser2.add_argument('--hide-conf', default=False, action='store_true', help='hide confidences')
        parser2.add_argument('--half', action='store_true', help='use FP16 half-precision inference')
        parser2.add_argument('--dnn', action='store_true', help='use OpenCV DNN for ONNX inference')
        self.opt = parser2.parse_args()
        self.opt.imgsz *= 2 if len(self.opt.imgsz) == 1 else 1  # expand
        print_args(vars(self.opt))
        check_requirements(exclude=('tensorboard', 'thop'))
        self.run(**vars(self.opt))

    @torch.no_grad()
    def run(self,weights=ROOT / './runs/train/test/weights/best.pt' ,  # model.pt path(s)
        source= ROOT / '1',  # file/dir/URL/glob, 0 for webcam
        data=ROOT / 'data/coco128.yaml',  # dataset.yaml path
        imgsz=(640, 640),  # inference size (height, width)
        conf_thres=0.25,  # confidence threshold
        iou_thres=0.45,  # NMS IOU threshold
        max_det=1000,  # maximum detections per image
        device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
        view_img=False,  # show results
        save_txt=False,  # save results to *.txt
        save_conf=False,  # save confidences in --save-txt labels
        save_crop=False,  # save cropped prediction boxes
        nosave=False,  # do not save images/videos
        classes=None,  # filter by class: --class 0, or --class 0 2 3
        agnostic_nms=False,  # class-agnostic NMS
        augment=False,  # augmented inference
        visualize=False,  # visualize features
        update=False,  # update all models
        project=ROOT / 'runs/detect',  # save results to project/name
        name='exp',  # save results to project/name
        exist_ok=False,  # existing project/name ok, do not increment
        line_thickness=3,  # bounding box thickness (pixels)
        hide_labels=False,  # hide labels
        hide_conf=False,  # hide confidences
        half=False,  # use FP16 half-precision inference
        dnn=False,  # use OpenCV DNN for ONNX inference
        ):

        source = str(source)
        save_img = not nosave and not source.endswith('.txt')  # save inference images
        is_file = Path(source).suffix[1:] in (IMG_FORMATS + VID_FORMATS)
        is_url = source.lower().startswith(('rtsp://', 'rtmp://', 'http://', 'https://'))
        webcam = source.isnumeric() or source.endswith('.txt') or (is_url and not is_file)
        if is_url and is_file:
            source = check_file(source)  # download

        # Directories
        save_dir = increment_path(Path(project) / name, exist_ok=exist_ok)  # increment run
        (save_dir / 'labels' if save_txt else save_dir).mkdir(parents=True, exist_ok=True)  # make dir

        # Load model
        device = select_device(device)
        model = DetectMultiBackend(weights, device=device, dnn=dnn, data=data, fp16=half)
        stride, names, pt = model.stride, model.names, model.pt
        imgsz = check_img_size(imgsz, s=stride)  # check image size
        print('화면이 켜지면 shift + z를 눌러 유저를 활성화 시키십시오.')  
        print('유저가 바뀌면 다시 shift + z를 눌러 유저를 활성화 시키십시오.')
        print('  ')
        print('손동작 인식 가이드')
        print('손동작 인식을 실행시키면 유튜브 창이 자동으로 켜지며 손동작을 인식합니다.')
        print('손동작을 인식하는 카메라는 유저의 손이 화면에 인식될때만 동작합니다. 만약 윈도우 창의 위치를 이동하고 싶다면 손바닥을 카메라에 보여주고 조작하십시오.')
        print('shift + a를 누르면서 검지와 엄지사이의 거리를 조절하면 볼륨조절을 할 수 있습니다.')
        print('손등을 카메라쪽으로 보여주며 브이를 하면 Yeah~! 라는 문구가 뜨며 이때 shift + x를 누르면 해시태그가 수집됩니다.')
        print('손등을 카메라쪽으로 보여주며 검지하나만 올리면 no! 라는 문구가 뜨며 이때 shift + x를 누르면 유튜브창이 스크롤되며 댓글이 수집됩니다.')
        print('손등을 카메라쪽으로 보여주며 엄지만 펴면 Thumbs up! 라는 문구가 뜨며 이때 shift + x를 누르면 활성화창의 화면이 스크랩됩니다')
        print('손등을 카메라쪽으로 보여주며 엄지와 검지를 펴면 two 라는 문구가 뜨며 이때 shift + x를 누르면 자막이 수집됩니다. 이때 자막이 없는 동영상에서 실행시에는 오류가 발생할 수 있습니다.')
        print('    ')
        print('http://gmrain.synology.me:8080/ 에서 접속하여 수집된 데이터를 확인할 수 있습니다.')
        
        
        
        # Dataloader
        if webcam:
            view_img = check_imshow()
            cudnn.benchmark = True  # set True to speed up constant image size inference
            dataset = LoadStreams(source, img_size=imgsz, stride=stride, auto=pt)
            bs = len(dataset)  # batch_size
        else:
            dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt)
            bs = 1  # batch_size
        vid_path, vid_writer = [None] * bs, [None] * bs

        # Run inference
        model.warmup(imgsz=(1 if pt else bs, 3, *imgsz))  # warmup
        seen, windows, dt = 0, [], [0.0, 0.0, 0.0]
        print('화면이 켜지면 shift + z를 눌러 유저를 활성화 시키십시오.')  
        for path, im, im0s, vid_cap, s in dataset:
            t1 = time_sync()
            im = torch.from_numpy(im).to(device)
            im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
            im /= 255  # 0 - 255 to 0.0 - 1.0
            if len(im.shape) == 3:
                im = im[None]  # expand for batch dim
            t2 = time_sync()
            dt[0] += t2 - t1

            # Inference
            visualize = increment_path(save_dir / Path(path).stem, mkdir=True) if visualize else False
            pred = model(im, augment=augment, visualize=visualize)
            t3 = time_sync()
            dt[1] += t3 - t2

            # NMS
            pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)
            dt[2] += time_sync() - t3

            # Second-stage classifier (optional)
            # pred = utils.general.apply_classifier(pred, classifier_model, im, im0s)
            
            # Process predictions
            for i, det in enumerate(pred):  # per image
                seen += 1
                if webcam:  # batch_size >= 1
                    p, im0, frame = path[i], im0s[i].copy(), dataset.count
                    s += f'{i}: '
                else:
                    p, im0, frame = path, im0s.copy(), getattr(dataset, 'frame', 0)

                p = Path(p)  # to Path
                save_path = str(save_dir / p.name)  # im.jpg
                txt_path = str(save_dir / 'labels' / p.stem) + ('' if dataset.mode == 'image' else f'_{frame}')  # im.txt
                s += '%gx%g ' % im.shape[2:]  # print string
                gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
                imc = im0.copy() if save_crop else im0  # for save_crop
                annotator = Annotator(im0, line_width=line_thickness, example=str(names))
                if len(det):
                    # Rescale boxes from img_size to im0 size
                    det[:, :4] = scale_coords(im.shape[2:], det[:, :4], im0.shape).round()

                    # Print results
                    for c in det[:, -1].unique():
                        n = (det[:, -1] == c).sum()  # detections per class
                        s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to string

                    # Write results
                    for *xyxy, conf, cls in reversed(det):
                        if save_txt:  # Write to file
                            xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh
                            line = (cls, *xywh, conf) if save_conf else (cls, *xywh)  # label format
                            with open(f'{txt_path}.txt', 'a') as f:
                                f.write(('%g ' * len(line)).rstrip() % line + '\n')

                        if save_img or save_crop or view_img:  # Add bbox to image
                            c = int(cls)  # integer class
                            label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}')
                            annotator.box_label(xyxy, label, color=colors(c, True))
                        if save_crop:
                            save_one_box(xyxy, imc, file=save_dir / 'crops' / names[c] / f'{p.stem}.jpg', BGR=True)

                # Stream results
                im0 = annotator.result()

                # 시간대 설정
                now = datetime.now()
                today = now.date()
                current_time = now.strftime("%H:%M:%S")

                # 사진 담을 폴더 만들기
                dest_folder = 'Z:/homes/gmrain/djangoproject/Youtube_Supporter/static/screenshot/{}'.format(today)
                if not os.path.exists(dest_folder):
                    os.makedirs(dest_folder)
                

                if view_img:
                    if p not in windows:
                        windows.append(p)
                        cv2.namedWindow(str(p), cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # allow window resize (Linux)
                        cv2.resizeWindow(str(p), im0.shape[1], im0.shape[0])

                    if keyboard.is_pressed('shift'):
                        if keyboard.is_pressed('z'):
                            if str(names[c])== "SoHyun" :
                                                #sqlite3 DB 연결
                                connect = sqlite3.connect("Z:/homes/gmrain/djangoproject/Youtube_Supporter/db.sqlite3")
                                Cursor = connect.cursor()
                                Cursor.execute("SELECT * FROM board_Member_list ORDER BY ROWID DESC LIMIT 1")
                                if Cursor.fetchone() == ('SoHyun','SoHyun',):
                                    print('SoHyun 유저가 이미 활성화 되어있습니다')
                                    time.sleep(2)
                                    Cursor.close()
                                    connect.close()
                                    continue
                                Cursor.execute("INSERT INTO board_Member_list VALUES (?,?)", ('SoHyun',"SoHyun",))
                                Cursor.execute("INSERT INTO board_Member_time VALUES (?,?,?,?,?)", ('SoHyun',"SoHyun","{} {}".format(today,current_time),today,current_time))
                                connect.commit()
                                print('SoHyun 유저가 활성화 되었습니다')
                                Cursor.close()
                                connect.close()
                                time.sleep(2)
                            if str(names[c])== "SangA" :
                                connect = sqlite3.connect("Z:/homes/gmrain/djangoproject/Youtube_Supporter/db.sqlite3")
                                Cursor = connect.cursor()
                                Cursor.execute("SELECT * FROM board_Member_list ORDER BY ROWID DESC LIMIT 1")
                                if Cursor.fetchone() == ('SangA','SangA',):
                                    print('SangA 유저가 이미 활성화 되어있습니다')
                                    time.sleep(2)
                                    continue
                                Cursor.execute("INSERT INTO board_Member_list VALUES (?,?)", ('SangA',"SangA",))
                                Cursor.execute("INSERT INTO board_Member_time VALUES (?,?,?,?,?)", ('SangA',"SangA","{} {}".format(today,current_time),today,current_time))
                                connect.commit()
                                print('SangA 유저가 활성화 되었습니다')
                                Cursor.close()
                                connect.close()
                                time.sleep(2)
                            if str(names[c])== "MinHee" :
                                connect = sqlite3.connect("Z:/homes/gmrain/djangoproject/Youtube_Supporter/db.sqlite3")
                                Cursor = connect.cursor()
                                Cursor.execute("SELECT * FROM board_Member_list ORDER BY ROWID DESC LIMIT 1")
                                if Cursor.fetchone() == ('MinHee','MinHee',):
                                    print('MinHee 유저가 이미 활성화 되어있습니다')
                                    time.sleep(2)
                                    continue
                                Cursor.execute("INSERT INTO board_Member_list VALUES (?,?)", ('MinHee',"MinHee",))
                                Cursor.execute("INSERT INTO board_Member_time VALUES (?,?,?,?,?)", ('MinHee',"MinHee","{} {}".format(today,current_time),today,current_time))
                                connect.commit()
                                print('MinHee 유저가 활성화 되었습니다')
                                Cursor.close()
                                connect.close()
                                time.sleep(2)
                            if str(names[c])== "JiHyun" :
                                connect = sqlite3.connect("Z:/homes/gmrain/djangoproject/Youtube_Supporter/db.sqlite3")
                                Cursor = connect.cursor()
                                Cursor.execute("SELECT * FROM board_Member_list ORDER BY ROWID DESC LIMIT 1")
                                if Cursor.fetchone() == ('JiHyun','JiHyun',):
                                    print('JiHyun 유저가 이미 활성화 되어있습니다')
                                    Cursor.close()
                                    connect.close()
                                    time.sleep(2)
                                    continue
                                Cursor.execute("INSERT INTO board_Member_list VALUES (?,?)", ('JiHyun',"JiHyun",))
                                Cursor.execute("INSERT INTO board_Member_time VALUES (?,?,?,?,?)", ('JiHyun',"JiHyun","{} {}".format(today,current_time),today,current_time))
                                connect.commit()
                            
                                print('JiHyun 유저가 활성화 되었습니다')
                                Cursor.close()
                                connect.close()
                                time.sleep(2)

    

                    cv2.imshow3(str(p), im0)
                    cv2.waitKey(1)  # 1 millisecond

                                        
                # Save results (image with detections)
                if save_img:
                    if dataset.mode == 'image':
                        cv2.imwrite(save_path, im0)
                    else:  # 'video' or 'stream'
                        if vid_path[i] != save_path:  # new video
                            vid_path[i] = save_path
                            if isinstance(vid_writer[i], cv2.VideoWriter):
                                vid_writer[i].release()  # release previous video writer
                            if vid_cap:  # video
                                fps = vid_cap.get(cv2.CAP_PROP_FPS)
                                w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                                h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                            else:  # stream
                                fps, w, h = 30, im0.shape[1], im0.shape[0]
                            save_path = str(Path(save_path).with_suffix('.mp4'))  # force *.mp4 suffix on results videos
                            vid_writer[i] = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
                        vid_writer[i].write(im0)

            # Print time (inference-only)
            LOGGER.info(f'{s}Done. ({t3 - t2:.3f}s)')

        # Print results
        t = tuple(x / seen * 1E3 for x in dt)  # speeds per image
        LOGGER.info(f'Speed: %.1fms pre-process, %.1fms inference, %.1fms NMS per image at shape {(1, 3, *imgsz)}' % t)
        if save_txt or save_img:
            s = f"\n{len(list(save_dir.glob('labels/*.txt')))} labels saved to {save_dir / 'labels'}" if save_txt else ''
            LOGGER.info(f"Results saved to {colorstr('bold', save_dir)}{s}")
        if update:
            strip_optimizer(weights)  # update model (to fix SourceChangeWarning)










