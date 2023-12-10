import cv2


# 투명한 영역이 있는 이미지 영상에 오버레이하는 함수
# reference : bard, gpt
def overlay(image, x, y, w, h, overlay_image): # 대상 이미지 (3채널), x, y 좌표, width, height, 덮어씌울 이미지 (4채널)
    alpha = overlay_image[:, :, 3] # BGRA
    mask_image = alpha / 255 # 0 ~ 255 -> 255 로 나누면 0 ~ 1 사이의 값 (1: 불투명, 0: 완전)
    # (255, 255)  ->  (1, 1)
    # (255, 0)        (1, 0)
    
    # 1 - mask_image ?
    # (0, 0)
    # (0, 1)
    
    for c in range(0, 3): # channel BGR
        image[y-h:y+h, x-w:x+w, c] = (overlay_image[:, :, c] * mask_image) + (image[y-h:y+h, x-w:x+w, c] * (1 - mask_image))
        
        
def ImageBlending(img1, img2):

    img = cv2.addWeighted(img1, 0.5, img2 , 0.5, 0)

    return img
