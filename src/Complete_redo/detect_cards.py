#          .x+=:.                     ..    .         s                   .                        
#     z`    ^%              x .d88"    @88>      :8                  @88>                          
#        .   <k        u.    5888R     %8P      .88                  %8P      .u    .              
#      .@8Ned8"  ...ue888b   '888R      .      :888ooo       u        .     .d88B :@8c       .u    
#    .@^%8888"   888R Y888r   888R    .@88u  -*8888888    us888u.   .@88u  ="8888f8888r   ud8888.  
#   x88:  `)8b.  888R I888>   888R   ''888E`   8888    .@88 "8888" ''888E`   4888>'88"  :888'8888. 
#   8888N=*8888  888R I888>   888R     888E    8888    9888  9888    888E    4888> '    d888 '88%" 
#    %8"    R88  888R I888>   888R     888E    8888    9888  9888    888E    4888>      8888.+"    
#     @8Wou 9%  u8888cJ888    888R     888E   .8888Lu= 9888  9888    888E   .d888L .+   8888L      
#   .888888P`    "*888*P"    .888B .   888&   ^%888*   9888  9888    888&   ^"8888*"    '8888c. .+ 
#   `   ^"F        'Y"       ^*888%    R888"    'Y"    "888*""888"   R888"     "Y"       "88888%   
#                              "%       ""              ^Y"   ^Y'     ""                   "YP'    
#    
#   62410 CDIO-Projekt F20 - Solitaire solver
#   https://github.com/MaxTheScrub/CDIO_Project 
#
#   Group 7:                                    
#   Henrik Peter Warncke s184801                
#   Max Feng Chen Bjørnsen s184811              
#   Jeppe Møller Bak s164871                    
#   Adam Aron Edelsten s173057                  
#   Tobias Lauge Borgstrøm s184810              
#   Tobias Ladefoged Jensen s184815             
#   Markus Repnak Jacobsen s184808              
#   Ajs Ritsmer Stormholt s174517               
#
#   Naming convention: https://www.python.org/dev/peps/pep-0008/                       
#   Class names: PascalCase                         
#   Function names: snake_case                       
#   Variables: camelCase
#   Objects: camelCase                        
#   Constants: SCREAMING_SNAKE_CASE 

# This code is based on "object_detection.py" from the opencv github.
# This code uses several files from the dnn examples folder.
# https://github.com/opencv/opencv/tree/master/samples/dnn 

import cv2
import argparse
import numpy as np
import sys
import time
from classes import *
from testing import *
from prediction import *
from threading import Thread
if sys.version_info[0] == 2:
    import Queue as queue
else:
    import queue
import os

# Import needed OpenCV example python documents to run the code
from common import *
from tf_text_graph_common import readTextMessage
from tf_text_graph_ssd import createSSDGraph
from tf_text_graph_faster_rcnn import createFasterRCNNGraph

# Define the possible backends and targets. Is used with the parser 

backends = (cv2.dnn.DNN_BACKEND_DEFAULT, cv2.dnn.DNN_BACKEND_HALIDE, cv2.dnn.DNN_BACKEND_INFERENCE_ENGINE, cv2.dnn.DNN_BACKEND_OPENCV)
targets = (cv2.dnn.DNN_TARGET_CPU, cv2.dnn.DNN_TARGET_OPENCL, cv2.dnn.DNN_TARGET_OPENCL_FP16, cv2.dnn.DNN_TARGET_MYRIAD)

# Add the parser arguments
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('--zoo', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models.yml'),
                    help='An optional path to file with preprocessing parameters.')
parser.add_argument('--input', help='Path to input image or video file. Skip this argument to capture frames from a camera.')
parser.add_argument('--out_tf_graph', default='graph.pbtxt',
                    help='For models from TensorFlow Object Detection API, you may '
                         'pass a .config file which was used for training through --config '
                         'argument. This way an additional .pbtxt file with TensorFlow graph will be created.')
parser.add_argument('--framework', choices=['caffe', 'tensorflow', 'torch', 'darknet', 'dldt'],
                    help='Optional name of an origin framework of the model. '
                         'Detect it automatically if it does not set.')
parser.add_argument('--thr', type=float, default=0.5, help='Confidence threshold')
parser.add_argument('--nms', type=float, default=0.4, help='Non-maximum suppression threshold')
parser.add_argument('--backend', choices=backends, default=cv2.dnn.DNN_BACKEND_DEFAULT, type=int,
                    help="Choose one of computation backends: "
                         "%d: automatically (by default), "
                         "%d: Halide language (http://halide-lang.org/), "
                         "%d: Intel's Deep Learning Inference Engine (https://software.intel.com/openvino-toolkit), "
                         "%d: OpenCV implementation" % backends)
parser.add_argument('--target', choices=targets, default=cv2.dnn.DNN_TARGET_CPU, type=int,
                    help='Choose one of target computation devices: '
                         '%d: CPU target (by default), '
                         '%d: OpenCL, '
                         '%d: OpenCL fp16 (half-float precision), '
                         '%d: VPU' % targets)
parser.add_argument('--async', type=int, default=0,
                    dest='asyncN',
                    help='Number of asynchronous forwards at the same time. '
                         'Choose 0 for synchronous mode')
args, _ = parser.parse_known_args()
add_preproc_args(args.zoo, parser, 'object_detection')
parser = argparse.ArgumentParser(parents=[parser],
                                 description='Use this script to run object detection deep learning networks using OpenCV.',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
args = parser.parse_args()

# Set the model (yolocards_90000.weights), config file (yolocards_test.cfg) and class file (cards.names)

args.model = findFile(args.model)
args.config = findFile(args.config)
args.classes = findFile(args.classes)

# List used for all detected card objects
detectedCards = []

# Function used to setup the games piles and initialising the Game object properly
def setup_game_computer_vision(game):
    # Make the lists
    game.playingCards = []
    game.tableauPiles = []
    game.foundationPiles = []
    
    # Make the tableaupiles and append them to the list 
    for pileNumber in range(1, 8):
        currentPile = TableauPile(pileNumber)
        game.tableauPiles.append(currentPile)

    # Make the foundationPiles and append them to the list
    for suit in Suit:
        newFoundationPile = FoundationPile(suit)
        newFoundationPile.nextCard = Value.ACE
        game.foundationPiles.append(newFoundationPile)
    # Initializes the "lowest needed card" for each foundationPile, which is set to 1 in this case.
    newLowestNeededCard(game)

# The game object is initialized
game = Game()
setup_game_computer_vision(game) 

# If config specified, try to load it as TensorFlow Object Detection API's pipeline.
config = readTextMessage(args.config)
if 'model' in config:
    print('TensorFlow Object Detection API config detected')
    if 'ssd' in config['model'][0]:
        print('Preparing text graph representation for SSD model: ' + args.out_tf_graph)
        createSSDGraph(args.model, args.config, args.out_tf_graph)
        args.config = args.out_tf_graph
    elif 'faster_rcnn' in config['model'][0]:
        print('Preparing text graph representation for Faster-RCNN model: ' + args.out_tf_graph)
        createFasterRCNNGraph(args.model, args.config, args.out_tf_graph)
        args.config = args.out_tf_graph

# Load names of classes
classes = None
if args.classes:
    with open(args.classes, 'rt') as f:
        classes = f.read().rstrip('\n').split('\n')

# Load a network
net = cv2.dnn.readNet(cv2.samples.findFile(args.model), cv2.samples.findFile(args.config), args.framework)
net.setPreferableBackend(args.backend)
net.setPreferableTarget(args.target)
outNames = net.getUnconnectedOutLayersNames()

confThreshold = args.thr
nmsThreshold = args.nms

def ID_to_card(subject, leftPos, topPos):
    # Convert a cardID to a card object
    # Attributes for a new card is initialized.
    suit = None
    color = None
    pile = 0
    value = None
    visible = Visible.TRUE
    left = leftPos
    top = topPos
    # Determine suit and color based on offset defined in cards.names.
    if subject < 13:
        suit = Suit.H
        color = Color.RED   
        value = (subject - 13)*(-1)
    elif subject > 12 and subject < 26:
        suit = Suit.D
        color = Color.RED
        value = (subject - 26)*(-1)
    elif subject > 25 and subject < 39:
        suit = Suit.C
        color = Color.BLACK
        value = (subject - 39)*(-1)
    elif subject > 38:
        suit = Suit.S
        color = Color.BLACK
        value = (subject - 52)*(-1)
    card = create_card(value, suit, pile, color, left, top)
    return card

# Generate the cards 
def generate_cards(cardIDs, confidences, boxes):
    count = 0
    # If the detectedCards list already contains cards, clear the list and the stock.
    if len(detectedCards) > 0:
        detectedCards.clear()
        game.stock.cards.clear()
        game.stock.frontCard = None
    
    # Clear all the tableau piles
    for tableauPile in game.tableauPiles:
        tableauPile.cards.clear()
    # CardsIDS contains the "raw" number corresponding to the cards.names file of all the detected cards.
    # If the confidence level is high enough, create a card and append to detectedCards.
    for cardID in cardIDs:
        if confidences[count] > CONFIDENCE_THRESHOLD:
            card = ID_to_card(cardID, boxes[count][0], boxes[count][1])
            detectedCards.append(card)
        count+=1
    # Since some cards have two visible symbols and are therefore added twice to the detectedCards list, they are removed.
    remove_duplicate(detectedCards)
    #remove_duplicate(detectedCards) # Was needed at one point
    breakFlag = False
    for card in game.stock.cards:
        # Check if a card was moved from the stock to tableau. Remove card from stock if true.
        for tableauPile in game.tableauPiles:
            if len(tableauPile.cards) > 0:
                if card.ID == tableauPile.frontCard.ID:
                    game.stock.cards.remove(card)
                    breakFlag = True
                    break
        # Check if a card was moved from the stock to foundation. Remove card from stock if true.
        for foundationPile in game.foundationPiles:
            if len(foundationPile.cards) > 0:
                if card.ID == foundationPile.frontCard.ID:
                    game.stock.cards.remove(card)
                    breakFlag = True
                    break
        if breakFlag:
            break

# Remove duplicate card from list
def remove_duplicate(cards):
    for card in cards:
        n = 0
        for element in cards:
            if card.ID == element.ID:
                n+=1
            if n == 2:
                cards.remove(element)
                n = 0

# If the card is in the stock (wastepile) position, add to stock as frontCard
def add_initial_stock(card):
    if card.left < CARD_WIDTH*2 and card.left > CARD_WIDTH*1:
        game.stock.frontCard = card
        game.stock.cards.append(card)


def add_foundation_piles(card):
    foundationNumber = 0
    placementNumber = 3
    for foundationPile in game.foundationPiles:
        # if the card is one of the foundationPile positions:
        if card.left > CARD_WIDTH*placementNumber and card.left < CARD_WIDTH*(placementNumber+1):
            # Add the card to the foundationPile using the start_add_to_goal() function
            start_add_to_goal(card, foundationPile, game)
        
        # Make the card added last the frontCard 
        if len(foundationPile.cards) > 0:
            foundationPile.frontCard = foundationPile.cards[LAST_INDEX]
        # Increment
        foundationNumber += 1
        placementNumber += 1

def add_tableau_piles(card):
    tableauNumber = 0
    for tableauPile in game.tableauPiles:
        if card.left > CARD_WIDTH*tableauNumber and card.left < CARD_WIDTH*(tableauNumber+1):
            tableauPile.cards.append(card)
        if len(tableauPile.cards) > 0:
            tableauPile.frontCard = tableauPile.cards[LAST_INDEX]
        tableauNumber += 1

def add_piles(cards, game):
    for card in cards:
        if card.top > CARD_HEIGHT: # The top cards
            add_tableau_piles(card)
        elif card.top < CARD_HEIGHT: # The top cards
            add_foundation_piles(card)
            add_initial_stock(card)
 
def sort_tableau_piles():
    i = 0
    for tableauPile in game.tableauPiles:
        tableauPile.cards.sort(key=lambda x: x.top)
        if len(tableauPile.cards )> 0:  
            tableauPile.frontCard = tableauPile.cards[LAST_INDEX]
        i+=1

def piles_legal():
    for tableau in game.tableauPiles:
        if len(tableau.cards) > 1:
            if  not (tableau.frontCard.value.value - tableau.cards[len(tableau.cards)-2].value.value == -1 and tableau.frontCard.color != tableau.cards[len(tableau.cards)-2].color):
                print("Cards do not match!!!")
                print("Move " + tableau.frontCard.to_string() + " away from " + tableau.cards[len(tableau.cards)-2].to_string())

def drawPred(frame, classId, conf, left, top, right, bottom):
    # Draw a bounding box.
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0))
    label = '%.2f' % conf

    # Print a label of class.
    if classes:
        assert(classId < len(classes))
        label = '%s: %s' % (classes[classId], label)

    labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_DUPLEX, 0.5, 1)
    top = max(top, labelSize[1])
    cv2.rectangle(frame, (left, top - labelSize[1]), (left + labelSize[0], top + baseLine), (255, 255, 255), cv2.FILLED)
    cv2.putText(frame, label, (left, top), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 0))

def postprocess(frame, outs, game):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]

    layerNames = net.getLayerNames()
    lastLayerId = net.getLayerId(layerNames[-1])
    lastLayer = net.getLayer(lastLayerId)
    classIds = []
    confidences = []
    boxes = []
    if lastLayer.type == 'DetectionOutput':
        # Network produces output blob with a shape 1x1xNx7 where N is a number of
        # detections and an every detection is a vector of values
        # [batchId, classId, confidence, left, top, right, bottom]
        for out in outs:
            for detection in out[0, 0]:
                confidence = detection[2]
                if confidence > confThreshold:
                    left = int(detection[3])
                    top = int(detection[4])
                    right = int(detection[5])
                    bottom = int(detection[6])
                    width = right - left + 1
                    height = bottom - top + 1
                    if width <= 2 or height <= 2:
                        left = int(detection[3] * frameWidth)
                        top = int(detection[4] * frameHeight)
                        right = int(detection[5] * frameWidth)
                        bottom = int(detection[6] * frameHeight)
                        width = right - left + 1
                        height = bottom - top + 1
                    classIds.append(int(detection[1]) - 1)  # Skip background label
                    confidences.append(float(confidence))
                    boxes.append([left, top, width, height])

    elif lastLayer.type == 'Region':
        # Network produces output blob with a shape NxC where N is a number of
        # detected objects and C is a number of classes + 4 where the first 4
        # numbers are [center_x, center_y, width, height]
        for out in outs:
            for detection in out:
                scores = detection[5:]
                classId = np.argmax(scores)
                confidence = scores[classId]
                if confidence > confThreshold:
                    center_x = int(detection[0] * frameWidth)
                    center_y = int(detection[1] * frameHeight)
                    width = int(detection[2] * frameWidth)
                    height = int(detection[3] * frameHeight)
                    left = int(center_x - width / 2)
                    top = int(center_y - height / 2)
                    classIds.append(classId)
                    confidences.append(float(confidence))
                    boxes.append([left, top, width, height])
                
    else:
        print('Unknown output layer type: ' + lastLayer.type)
        exit()

    # NMS is used inside Region layer only on DNN_BACKEND_OPENCV for another backends we need NMS in sample
    # or NMS is required if number of outputs > 1
    if len(outNames) > 1 or lastLayer.type == 'Region' and args.backend != cv2.dnn.DNN_BACKEND_OPENCV:
        indices = []
        classIds = np.array(classIds)
        boxes = np.array(boxes)
        confidences = np.array(confidences)
        unique_classes = set(classIds)
        for cl in unique_classes:
            class_indices = np.where(classIds == cl)[0]
            conf = confidences[class_indices]
            box  = boxes[class_indices].tolist()
            nms_indices = cv2.dnn.NMSBoxes(box, conf, confThreshold, nmsThreshold)
            nms_indices = nms_indices[:, 0] if len(nms_indices) else []
            indices.extend(class_indices[nms_indices])
    else:
        indices = np.arange(0, len(classIds))
    
    #print("Detected cards reset")
    for i in indices:
        box = boxes[i]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        drawPred(frame, classIds[i], confidences[i], left, top, left + width, top + height)
    
    generate_cards(classIds, confidences, boxes)
    add_piles(detectedCards, game)
    sort_tableau_piles()
    piles_legal()
    print_table(game)


# Process inputs
winName = 'CV Solitaire solver - Gruppe 7'
cv2.namedWindow(winName, cv2.WINDOW_NORMAL)

cap = cv2.VideoCapture(cv2.samples.findFileOrKeep(args.input) if args.input else 0)

class QueueFPS(queue.Queue):
    def __init__(self):
        queue.Queue.__init__(self)
        self.startTime = 0
        self.counter = 0

    def put(self, v):
        queue.Queue.put(self, v)
        self.counter += 1
        if self.counter == 1:
            self.startTime = time.time()

    def getFPS(self):
        return self.counter / (time.time() - self.startTime)

process = True

#
# Frames capturing thread
#
framesQueue = QueueFPS()
def framesThreadBody():
    global framesQueue, process

    while process:
        hasFrame, frame = cap.read()
        if not hasFrame:
            break
        framesQueue.put(frame)

#
# Frames processing thread
#
processedFramesQueue = queue.Queue()
predictionsQueue = QueueFPS()
def processingThreadBody():
    global processedFramesQueue, predictionsQueue, args, process

    futureOutputs = []
    while process:
        # Get a next frame
        frame = None
        try:
            frame = framesQueue.get_nowait()

            if args.asyncN:
                if len(futureOutputs) == args.asyncN:
                    frame = None  # Skip the frame
            else:
                framesQueue.queue.clear()  # Skip the rest of frames
        except queue.Empty:
            pass

        if not frame is None:
            frameHeight = frame.shape[0]
            frameWidth = frame.shape[1]

            # Create a 4D blob from a frame.
            inpWidth = args.width if args.width else frameWidth
            inpHeight = args.height if args.height else frameHeight
            blob = cv2.dnn.blobFromImage(frame, size=(inpWidth, inpHeight), swapRB=args.rgb, ddepth=cv2.CV_8U)
            processedFramesQueue.put(frame)

            # Run a model
            net.setInput(blob, scalefactor=args.scale, mean=args.mean)
            if net.getLayer(0).outputNameToIndex('im_info') != -1:  # Faster-RCNN or R-FCN
                frame = cv2.resize(frame, (inpWidth, inpHeight))
                net.setInput(np.array([[inpHeight, inpWidth, 1.6]], dtype=np.float32), 'im_info')

            if args.asyncN:
                futureOutputs.append(net.forwardAsync())
            else:
                outs = net.forward(outNames)
                predictionsQueue.put(np.copy(outs))

        while futureOutputs and futureOutputs[0].wait_for(0):
            out = futureOutputs[0].get()
            predictionsQueue.put(np.copy([out]))

            del futureOutputs[0]


framesThread = Thread(target=framesThreadBody)
framesThread.start()

processingThread = Thread(target=processingThreadBody)
processingThread.start()

#
# Postprocessing and rendering loop
#
while cv2.waitKey(1) < 0:
    try:
        # Request prediction first because they put after frames
        outs = predictionsQueue.get_nowait()
        frame = processedFramesQueue.get_nowait()

        give_advice(game, stockpile_is_empty(frame, game), frame)
        win_check(game)

        postprocess(frame, outs, game)

        # Put efficiency information.
        if predictionsQueue.counter > 1:
            label = '%.2f FPS' % (predictionsQueue.getFPS())
            cv2.putText(frame, label, (5, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0))

        cv2.imshow(winName, frame)

    except queue.Empty:
        pass

process = False
framesThread.join()
processingThread.join()
