import cv2

def skala(nama, tinggilebar = []):
  '''Define tinggilebar [h,w] or leave it for fullscreen.'''
  cv2.namedWindow(nama, cv2.WINDOW_NORMAL)
  if tinggilebar:
    cv2.resizeWindow(nama, tinggilebar[1], tinggilebar[0])
  else:
    cv2.resizeWindow(nama, 1920, 1080)
    cv2.setWindowProperty(nama, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

