import cv2
import numpy as np

def draw(scale, width, div, grad1, color1, color2, color3, lines, angle, pad, grad2, color4, color5):
    x1_ = __draw1(
        scale, 
        width, 
        div,
        grad1,
        color1,
        color2,
        color3)
    x2_ = __draw2(
        x1_, 
        lines)
    x3_ = __draw3(
        x2_, 
        angle)
    x4_ = __draw4(
        x3_, 
        scale,
        pad,
        grad2,
        color4,
        color5)
    return x4_

def __draw1(scale, width, div, grad_s, color1, color2, color3):
    assert div >= 1

    width = width*scale

    grad_s = (grad_s*width) // 100

    green_back = np.zeros((1, width, 3), dtype=np.uint8)
    green_back[:] = color1

    white_back = np.zeros((1, width, 3), dtype=np.uint8)
    white_back[:] = color2

    ones = np.ones((grad_s,), dtype=np.float32)
    grad = np.linspace(1, 0, width-grad_s, endpoint=False, dtype=np.float32)
    grad = grad*grad*(3-2*grad) # 3rd order interpolation
    grad = np.r_[ones, grad]
    grad = grad[None, :, None]
    x = green_back * (grad) + white_back * (1-grad)
    
    pos = np.arange(width)
    mask2 = (pos // div)
    mask1 = ((pos*div)%width)//div

    mask2[mask2<scale]=scale
    mask2[(mask2>mask2[-1]-scale) & (mask2 < mask2[-1]) ]= mask2[-1]-scale

    mask = (mask1 <= mask2) 
    
    x[:, mask, :] = color3
    return x

def __draw2(x, lines):
    assert lines >= 1

    width = x.shape[1]

    pos = np.arange(width)
    mask = ((pos*lines) // width) % 2 ==0 

    # slow
    # mask = mask[:, None, None]
    # x=np.where(mask, x, x[:,::-1])
    # return x

    # fast
    xx = np.zeros((width, width, 3), dtype=np.float32)
    xx[mask] = x
    xx[~mask] = x[:,::-1]
    return xx

def __draw3(x, angle):
    # add alpha channel    
    x = cv2.cvtColor(x, cv2.COLOR_BGR2BGRA)

    # rotate coarsely
    if angle < 90:
        pass
    elif angle < 180:
        angle -= 90
        x = cv2.rotate(x, cv2.ROTATE_90_COUNTERCLOCKWISE)
    elif angle < 270:
        angle -= 180
        x = cv2.rotate(x, cv2.ROTATE_180)
    elif angle < 360:
        angle -= 270
        x = cv2.rotate(x, cv2.ROTATE_90_CLOCKWISE)
    
    # rotate finely
    if angle > 0:
        adjust = np.sqrt(2) * np.sin(angle/180*np.pi + np.pi/4)
        trans = cv2.getRotationMatrix2D((0, 0), angle, 1)
        width = x.shape[1]
        trans[1,2] = width*np.sin(angle/180*np.pi)
        x = cv2.warpAffine(x, trans, (int(adjust*width)+1, int(adjust*width)+1), flags=cv2.INTER_NEAREST)
    return x

def __draw4(x, scale, pad, grad_s, color3, color4):
    x_width = x.shape[1]
    pad = pad*scale
    width = x_width+pad*2

    grad_s = (grad_s*width) // 100

    bk1 = np.zeros((width, width, 3), dtype=np.float32)
    bk1[:] = color3

    bk2 = np.zeros((width, width, 3), dtype=np.float32)
    bk2[:] = color4

    ones = np.ones((grad_s,), dtype=np.float32)
    grad = np.linspace(1, 0, width-grad_s, endpoint=False, dtype=np.float32)
    grad = grad*grad*(3-2*grad) # 3rd order interpolation
    grad = np.r_[ones, grad]

    grad = grad[None, :, None]
    bk = bk1 * (grad) + bk2 * (1-grad)

    bk[pad:pad+x_width, pad:pad+x_width] = x[:,:,:3] * x[:,:,3:4] + bk[pad:pad+x_width, pad:pad+x_width]*(1-x[:,:,3:4])

    if scale > 1:
        #bk = cv2.GaussianBlur(bk, (scale,scale), 0, borderType=cv2.BORDER_REPLICATE)
        #bk = bk[(scale-1)//2::scale, (scale-1)//2::scale]
        bk = cv2.resize(bk, (bk.shape[1]//scale, bk.shape[0]//scale), interpolation=cv2.INTER_AREA)
    
    return np.clip(bk, 0, 255).astype(np.uint8)
