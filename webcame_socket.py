# import cv2
# import socket
# import pickle
# import struct

# # Khởi tạo kết nối socket
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host = 'localhost'  # Địa chỉ IP của máy chủ
# port = 12345  # Cổng kết nối socket

# server_socket.bind((host, port))
# server_socket.listen(5)

# print("Đang lắng nghe kết nối...")

# # Chấp nhận kết nối từ client
# client_socket, addr = server_socket.accept()
# print("Đã kết nối từ:", addr)

# # Khởi tạo webcam
# cap = cv2.VideoCapture(0)

# while True:
#     # Đọc khung hình từ webcam
#     ret, frame = cap.read()

#     # Chuyển đổi khung hình thành chuỗi bytes
#     data = pickle.dumps(frame)

#     # Tính toán kích thước dữ liệu và gửi qua kết nối socket
#     size = struct.pack("L", len(data))
#     client_socket.sendall(size + data)

#     # Gửi dữ liệu qua kết nối socket
#     # client_socket.sendall(struct.pack("L", len(data)) + data)

#     # Nhận dữ liệu từ client (nếu cần)
#     # received_data = client_socket.recv(1024)

#     # Hiển thị khung hình
#     cv2.imshow('Webcam', frame)

#     # Nhấn 'q' để thoát
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Đóng kết nối và giải phóng tài nguyên
# cap.release()
# cv2.destroyAllWindows()
# server_socket.close()


import cv2
from flask import Flask, render_template, Response

app = Flask(__name__)

# Khởi tạo webcam
cap = cv2.VideoCapture(0)

def generate_frames():
    while True:
        # Đọc khung hình từ webcam
        success, frame = cap.read()
        if not success:
            break
        else:
            # Chuyển đổi khung hình thành dạng chuỗi bytes
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

        # Trả về khung hình dưới dạng response
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    # Trả về response chứa khung hình từ webcam
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)