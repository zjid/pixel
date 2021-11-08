import cv2

def skala(nama, tinggilebar = [], geser = []):
  '''Define tinggilebar [h,w] or leave it for fullscreen 1920x1080.'''
  cv2.namedWindow(nama, cv2.WINDOW_NORMAL)
  tinggilebar = list(tinggilebar)
  geser = list(geser)
  if tinggilebar:
    cv2.resizeWindow(nama, tinggilebar[1], tinggilebar[0])
  else:
    cv2.resizeWindow(nama, 1920, 1080)
    cv2.setWindowProperty(nama, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
  if geser:
    cv2.moveWindow(nama, geser[1], geser[0])

