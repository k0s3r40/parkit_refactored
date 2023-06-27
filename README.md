# yolo7-stream-count
# Create vitrualenv & install requirements
    virtualenv -p python3 .
    . bin/activate
    pip install -r requirements.txt


# Download weights
    wget https://github.com/WongKinYiu/yolov7/releases/download/v0.1/yolov7x.pt

# Run the test 
    ./test.sh