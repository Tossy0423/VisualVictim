# ==========Import Modules==========#
# OpenCV
import cv2
# print("OpenCV ver : ") + (cv2.__version__)

# Subprocess
import subprocess

# Time
import time

#numpy
import numpy as np

# Serial Communication
import serial

# Struct
import struct



print("----------Import Modules Clear----------")

# ==========Define GlobalValue==========#
## Debug Switch
FLAG_DEBUG = 'ON'
# FLAG_DEBUG = 'OFF' #Competition Mode

# Debug Monitor
FLAG_DEBUG_MONITOR = 'ON'
# FLAG_DEBUG_MONITOR = 'OFF'

## SerialCom
# FLAG_SERIAL = 'ON'
FLAG_SERIAL = 'OFF'


## Detect Area Range
# 0: Min
# 1: Max
AREA_RANGE = [2000, 17000]

## Set Bilateral Filter Prameta
# 0: Operator Size
# 1: Standard Deviation on Color Space
# 2: Standard Deviation on Distance Space
Pram_BF = [7, 18, 31]

## Set Threshold Parameta
# 0: Min
# 1: Max
Pram_Threshold = [0, 54]

## Dsiplay Text
String_Victim = ' '

## Original Data (VisualVictim)
Victim_Num = 3
#After warp covert Param
pts2 = np.float32([[0, 0], [240 * 0.75, 0], [0, 240], [240 * 0.75, 240]]) #Result Img

## Setting Victim "S"
# 0: img_src(gray),
# 1: inverted img_src,
# 2: set img_src point,
# 3: Convert img_src point to pts2
# 4: warp perspective img_src
Original_victim_S = [ 0 for i in range(0, 5) ] # Initialize Array
Original_victim_S[0] = cv2.imread("Original/S.png", 0) # Import img "S"
Original_victim_S[1] = cv2.bitwise_not(Original_victim_S[0]) # img inverted
#set point
Original_victim_S[2] = np.float32([[0, 0], #Left Up
                           [Original_victim_S[1].shape[1], 0], #Right Up
                           [0, Original_victim_S[1].shape[0]],#Left Down
                           [Original_victim_S[1].shape[1], Original_victim_S[1].shape[0]]])#Right Down
# Warp Perspective
Original_victim_S[3] = cv2.getPerspectiveTransform(Original_victim_S[2], pts2)
Original_victim_S[4] = cv2.warpPerspective(Original_victim_S[1], Original_victim_S[3], (int(240 * 0.76), 240))

## Setting Victim "H"
# 0: img_src(gray),
# 1: inverted img_src,
# 2: set img_src point,
# 3: Convert img_src point to pts2
# 4: warp perspective img_src
Original_victim_H = [ 0 for i in range(0, 5) ] # Initialize Array
Original_victim_H[0] = cv2.imread("Original/H.png", 0) # Import img "S"
Original_victim_H[1] = cv2.bitwise_not(Original_victim_H[0]) # img inverted
#set point
Original_victim_H[2] = np.float32([[0, 0], #Left Up
                           [Original_victim_H[1].shape[1], 0], #Right Up
                           [0, Original_victim_H[1].shape[0]],#Left Down
                           [Original_victim_H[1].shape[1], Original_victim_H[1].shape[0]]])#Right Down
# Warp Perspective
Original_victim_H[3] = cv2.getPerspectiveTransform(Original_victim_H[2], pts2)
Original_victim_H[4] = cv2.warpPerspective(Original_victim_H[1], Original_victim_H[3], (int(240 * 0.76), 240))

## Setting Victim "U"
# 0: img_src(gray),
# 1: inverted img_src,
# 2: set img_src point,
# 3: Convert img_src point to pts2
# 4: warp perspective img_src
Original_victim_U = [ 0 for i in range(0, 5) ] # Initialize Array
Original_victim_U[0] = cv2.imread("Original/U.png", 0) # Import img "S"
Original_victim_U[1] = cv2.bitwise_not(Original_victim_U[0]) # img inverted
#set point
Original_victim_U[2] = np.float32([[0, 0], #Left Up
                           [Original_victim_U[1].shape[1], 0], #Right Up
                           [0, Original_victim_U[1].shape[0]],#Left Down
                           [Original_victim_U[1].shape[1], Original_victim_U[1].shape[0]]])#Right Down
# Warp Perspective
Original_victim_U[3] = cv2.getPerspectiveTransform(Original_victim_U[2], pts2)
Original_victim_U[4] = cv2.warpPerspective(Original_victim_U[1], Original_victim_U[3], (int(240 * 0.76), 240))

## Capture Victim && Original Victim Result
#[0, x]: Victim "S", x=0: Area Size, 1: Perimeter, 2: Roundness
#[1, x]: Victim "H", x=0: Area Size, 1: Perimeter, 2: Roundness
#[2, x]: Victim "U", x=0: Area Size, 1: Perimeter, 2: Roundness
Result_victim_S = [ 0 for i in range(0, 3) ]
Result_victim_H = [ 0 for i in range(0, 3) ]
Result_victim_U = [ 0 for i in range(0, 3) ]

print("----------Define GlobalValue Clear----------")


# ==========Define Function==========#

# TrackBar
if (FLAG_DEBUG == 'ON') & (FLAG_DEBUG_MONITOR == 'ON'):
    TrackBarArray = [0 for i in range(0, 7)]
    def TrackbarEvent(Value):
        global TrackBarArray

        TrackBarArray[0] = cv2.getTrackbarPos('G_Lower', 'img_ColorCircle')
        TrackBarArray[1] = cv2.getTrackbarPos('G_Upper', 'img_ColorCircle')
        TrackBarArray[2] = 2 * cv2.getTrackbarPos('OpeSize', 'img_ColorCircle') + 1
        TrackBarArray[3] = cv2.getTrackbarPos('C_deviation', 'img_ColorCircle')
        TrackBarArray[4] = cv2.getTrackbarPos('D_deviation', 'img_ColorCircle')

        #print('[DebugTrackbar] 0=%d, 1=%d, 2=%d, 3=%d, 4=%d, 5=%d' %
        #       (TrackBarArray[0] ,TrackBarArray[1] ,TrackBarArray[2] ,TrackBarArray[3] ,TrackBarArray[4] ,TrackBarArray[5]))

    # トラックバーを表示させるための色相環をインポート
    img_ColorCircle = cv2.imread('ColorCircle.jpg', 1)
    cv2.namedWindow('img_ColorCircle', cv2.WINDOW_NORMAL)

    cv2.createTrackbar('G_Lower', 'img_ColorCircle', 0, 255, TrackbarEvent)
    cv2.createTrackbar('G_Upper', 'img_ColorCircle', 0, 255, TrackbarEvent)
    cv2.createTrackbar('OpeSize', 'img_ColorCircle', 0, 20, TrackbarEvent)
    cv2.createTrackbar('C_deviation', 'img_ColorCircle', 0, 255, TrackbarEvent)
    cv2.createTrackbar('D_deviation', 'img_ColorCircle', 0, 255, TrackbarEvent)


#LaberingProcess
#1:ImportImg, 2:Upper Object Num, 3:Objet Area Max, 4:Object Area Min
def LabelingProcess(ImportImg, LabelNumUpper, AreaMax, AreaMin):

    Data = [0 for i in range(0, 9)]

    #connectedComponents:ラベリング結果(二値画像)のみを返す
    #connectedComponentsWithStats:詳細なデータ(重心,面積,バウンディングボックス(x,y,with,height))
    labelnum, labeling, contours, GoCs = cv2.connectedComponentsWithStats(ImportImg)

    #ラベリング個数が一定個数のみ処理を実行(時短のため)
    if (1 <= labelnum & labelnum <= LabelNumUpper):

        for label in range(1, labelnum):

            center_x, center_y = GoCs[label]  #重心座標取得
            square_x, square_y, w, h, size = contours[label]  #オブジェクトの左上の座標(x,y),横幅,縦幅,面積取得

            #デバッグ効率を上げるため検知したオブジェクトを四角形で囲む
            #img_src = cv2.rectangle(img_src, (square_x, square_y),(square_x + w, square_y + h),(255, 255, 0), 1)

            #こっちは重心を赤い点で表す
            #img_src = cv2.circle(img_src, (int(center_x), int(center_y)), 1,(0, 0, 255), -1)

            #面積サイズが一定以内ならば、重心を取得
            if ((AreaMin <= size) & (size <= AreaMax)):

                Data[0] = label  #割り当てられたラベルナンバー(あんまり使わない？)
                Data[1] = size  #ラベルナンバーの面積
                Data[2] = center_x  #重心(x座標)
                Data[3] = center_y  #重心(y座標)
                Data[4] = square_x  #認識したオブジェクトの左上のx座標
                Data[5] = square_y  #認識したオブジェクトの左上のy座標
                Data[6] = w  #横幅
                Data[7] = h  #縦幅
                #Data[8] = 0#算出結果(二値画像)

            #print('label=%d x=%d y=%d w=%d h=%d size=%d ' % (Data[0], Data[2], Data[3], Data[6], Data[7], Data[1]))
    return Data

# Import Camera & Setting Device
# Import Camera
cap = cv2.VideoCapture(1)

# Setting Device
# Prameta
CAMERA_SETTING_WIDTH = 320
CAMERA_SETTING_HEIGHT = 240
CAMERA_SETTING_FPS = 30
cap.set(3, CAMERA_SETTING_WIDTH)  # Width
cap.set(4, CAMERA_SETTING_HEIGHT)  # Height
cap.set(5, CAMERA_SETTING_FPS)  # FPS
print("[CamSetRst]Width=%d Height=%d FPS=%d" % (cap.get(3), cap.get(4), cap.get(5)))
print("Import Camera Clear")


# Logical AND Img
# 1:ImportImg , 2:Upper(int, max255) , 3:Lower(intm min0)
def LogicalANDRange(InportImg, UpperRange, LowerRange):
    # Upeer
    _, img_upper = cv2.threshold(
        InportImg,  # ImportImage
        UpperRange,  # Parameta
        255,  # Pixe,lMax(255)
        cv2.THRESH_BINARY_INV)  # Options

    # Lower
    _, img_lower = cv2.threshold(
        InportImg,  # ImportImage
        LowerRange,  # Parameta
        255,  # Pixe,lMax(255)
        cv2.THRESH_BINARY)  # Options

    # LogicalAnd
    img_logicaland = cv2.bitwise_and(img_upper, img_lower)

    return img_logicaland


## Object Extraction
def ObjectExtraction(ImportImg):

    # Contour
    contours = cv2.findContours(ImportImg,  # Import Img
                                cv2.RETR_EXTERNAL,  # [輪郭抽出モード]最も外側の輪郭のみ抽出
                                cv2.CHAIN_APPROX_SIMPLE  # [輪郭近似手法]すべての輪郭点を完全に格納
                                )[1]

    # Area size
    Area_Size = cv2.contourArea(contours[0])

    # Exception
    if Area_Size <= 0:
        Area_Size = 1

    # Perimeter
    Perimeter = cv2.arcLength(np.array(contours[0]), True)

    # Exception
    if Perimeter <= 0:
        Perimeter = 1

    # Roundness
    Roundness = 4.0 * np.pi * Area_Size / Perimeter / Perimeter

    return Area_Size, Perimeter, Roundness


print("----------Define Function Clear----------")

# ====================Program Start====================#

while True:

    ## Record Start Time
    START_TIME = time.time()

    ## image capture
    ret, img_src = cap.read()
    if ret != True:
        print("[ERROR]Faild Camera")
        break

    ## Img Convert RGB to Gray
    img_gray = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)

    ## Bilateral Filter
    if (FLAG_DEBUG == 'ON') & (FLAG_DEBUG_MONITOR == 'ON'):

        img_gray_BF = cv2.bilateralFilter(img_gray, TrackBarArray[2], TrackBarArray[3], TrackBarArray[4])

        cv2.namedWindow("[DEBUG]img_gray_BF", cv2.WINDOW_NORMAL)
        cv2.imshow("[DEBUG]img_gray_BF", img_gray_BF)
    else:
        img_gray_BF = cv2.bilateralFilter(img_gray, Pram_BF[0], Pram_BF[1], Pram_BF[2])


    ## Threshold Process
    if (FLAG_DEBUG == 'ON') & (FLAG_DEBUG_MONITOR == 'ON'):

        img_result_gray = LogicalANDRange(img_gray_BF, TrackBarArray[1], TrackBarArray[0])

        cv2.namedWindow("[DEBUG]img_result_gray", cv2.WINDOW_NORMAL)
        cv2.imshow("[DEBUG]img_result_gray", img_result_gray)
    else:
        img_result_gray = LogicalANDRange(img_gray_BF, Pram_Threshold[1], Pram_Threshold[0])

    # My Labering Process
    LabelingResult = [0 for i in range(0, 9)]
    LabelingResult = LabelingProcess(img_result_gray,  # Img Import (Binary img)
                                        5,  # Detect Objectq
                                        AREA_RANGE[1],  # Area Max Range
                                        AREA_RANGE[0])  # Area Min Range
    if FLAG_DEBUG == 'ON':

        # オブジェクトを四角形で囲む
        img_result_Labering = cv2.rectangle(img_src, #Write Image
                                    (LabelingResult[4], LabelingResult[5]),
                                    (LabelingResult[4] + LabelingResult[6], LabelingResult[5] + LabelingResult[7]),
                                    (0, 0, 255),
                                    2)

        # こっちは重心を赤い点で表す
        img_result_Labering = cv2.circle(img_result_Labering, (int(LabelingResult[2]), int(LabelingResult[3])), 3, (0, 0, 255), -1)

        # Display Text
        cv2.putText(
            img_result_Labering,  # DrawImge
            String_Victim,  # String
            (LabelingResult[4], LabelingResult[5] - 10),  # Position
            cv2.FONT_HERSHEY_COMPLEX,  # Font
            0.5,  # StringSize
            (0, 0, 255))  # Color

        #Result
        cv2.namedWindow("[DEBUG]img_result_Labering", cv2.WINDOW_NORMAL)
        cv2.imshow("[DEBUG]img_result_Labering", img_result_Labering)


    # Warp Perspective
    # Capture
    pts1 = np.float32([[LabelingResult[4], LabelingResult[5]],  # Left Up
                       [LabelingResult[4] + LabelingResult[6], LabelingResult[5]],  # Right Up
                       [LabelingResult[4], LabelingResult[5] + LabelingResult[7]],  # Left Down
                       [LabelingResult[4] + LabelingResult[6], LabelingResult[5] + LabelingResult[7]]])  # Right Down


    if LabelingResult[0] != 0:

        #Original Img
        # Moment img_src
        M = cv2.getPerspectiveTransform(pts1, pts2)
        img_result_victim = cv2.warpPerspective(img_result_gray, M, (int(240 * 0.76), 240))

        # Original Victim && Capture Victim
        img_result_S = cv2.bitwise_and(img_result_victim, Original_victim_S[4])
        img_result_H = cv2.bitwise_and(img_result_victim, Original_victim_H[4])
        img_result_U = cv2.bitwise_and(img_result_victim, Original_victim_U[4])

        # Import Object Data
        Result_victim_S = ObjectExtraction(img_result_S)
        Result_victim_H = ObjectExtraction(img_result_H)
        Result_victim_U = ObjectExtraction(img_result_U)

        ## Detect Area Renge
        if Result_victim_S[0] >= 13000:

            print("Detect S")

            if (FLAG_DEBUG == 'ON') & (FLAG_DEBUG_MONITOR == 'ON'):
                ## Set String
                String_Victim = 'Victim: S, Area: %d' % (Result_victim_S[0])

        elif Result_victim_H[0] >= 13000:

            print("Detect H")


            if (FLAG_DEBUG == 'ON') & (FLAG_DEBUG_MONITOR == 'ON'):

                ## Set String
                String_Victim = 'Victim: H, Area: %d' % (Result_victim_H[0])

        elif Result_victim_U[0] >= 13000:

            print("Detect U")

            if (FLAG_DEBUG == 'ON') & (FLAG_DEBUG_MONITOR == 'ON'):

                ## Set String
                String_Victim = 'Victim: U, Area: %d' % (Result_victim_U[0])

        else:

            print("No Detect")



            if (FLAG_DEBUG == 'ON') & (FLAG_DEBUG_MONITOR == 'ON'):
                ## Set String
                String_Victim = 'Victim: ?, Area: ?'

        if FLAG_DEBUG == 'ON':

            if FLAG_DEBUG_MONITOR == 'ON':

                #concat img
                img_result_add = cv2.hconcat([img_result_S, img_result_H, img_result_U, img_result_victim])

                # Result
                cv2.namedWindow("img_result_add[S, H, U, victim(Th)]", cv2.WINDOW_NORMAL)
                cv2.imshow("img_result_add[S, H, U, victim(Th)]", img_result_add)

            # print("[DEBUG_S]Area=%d, Perimeter=%d, Roundness=%0.2f" % (Result_victim_S[0], Result_victim_S[1], Result_victim_S[2]))
            # print("[DEBUG_H]Area=%d, Perimeter=%d, Roundness=%0.2f" % (Result_victim_H[0], Result_victim_H[1], Result_victim_H[2]))
            # print("[DEBUG_U]Area=%d, Perimeter=%d, Roundness=%0.2f" % (Result_victim_U[0], Result_victim_U[1], Result_victim_U[2]))


    # Recode End Time
    END_TIME = time.time()
    passegetime = END_TIME - START_TIME
    frequancy = 1 / passegetime
    #print("Time=%0.2f frequancy=%0.2f[Hz]" % (passegetime, frequancy))

    # Finish Program
    key = cv2.waitKey(1)
    if key == ord('q'):

        print("[UserSet BilateralFilter Prameta]\n"
              "OperatorSize: %d \n"
              "Standard Deviation on Color Space: %d \n"
              "Standard Deviation on Distance Space: %d \n"
              "=*=*=*=*=*=*Prease Write 'Set Bilateral Filter Prameta'=*=*=*=*=*=*"
              % (TrackBarArray[2], TrackBarArray[3], TrackBarArray[4]))

        print("[UserSet Threshold Prameta]\n"
              "Upper: %d \n"
              "Lower: %d \n"
              "=*=*=*=*=*=*Prease Write 'Set Threshold Parameta'=*=*=*=*=*=*"
              % (TrackBarArray[1], TrackBarArray[0]))



        break

cv2.destroyAllWindows()
# ====================Program End====================#
print("----------Finish Program----------")

