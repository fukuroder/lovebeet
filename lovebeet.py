import cv2
import numpy as np


def draw(scale, width, div, grad1, color1, color2, color3, lines, angle, pad, grad2, color4, color5):
    assert scale > 0 and scale % 2 == 1
    assert 0 < width
    assert 0 < div
    assert 0 <= grad1 <= 100
    assert 0 <= color1[0] <= 255 and 0 <= color1[1] <= 255 and 0 <= color1[2] <= 255
    assert 0 <= color2[0] <= 255 and 0 <= color2[1] <= 255 and 0 <= color2[2] <= 255
    assert 0 <= color3[0] <= 255 and 0 <= color3[1] <= 255 and 0 <= color3[2] <= 255
    assert 0 < lines
    assert 0 <= angle < 360
    assert 0 <= pad
    assert 0 <= grad2 <= 100
    assert 0 <= color4[0] <= 255 and 0 <= color4[1] <= 255 and 0 <= color4[2] <= 255
    assert 0 <= color5[0] <= 255 and 0 <= color5[1] <= 255 and 0 <= color5[2] <= 255

    x = __draw1(scale, width, div, grad1, color1, color2, color3)
    x = __draw2(x, lines)
    x = __draw3(x, angle)
    x = __draw4(x, scale, pad, grad2, color4, color5)

    return np.clip(x, 0, 255).astype(np.uint8)


def __draw1(scale, width, div, grad1, color1, color2, color3):
    width = width*scale
    grad1 = (grad1*width) // 100

    x0 = np.zeros((1, width, 3), dtype=np.uint8)
    x0[:] = color1

    x1 = np.zeros((1, width, 3), dtype=np.uint8)
    x1[:] = color2

    one = np.ones((grad1,), dtype=np.float32)
    one_to_zero = np.linspace(
        1, 0, width-grad1, endpoint=False, dtype=np.float32)
    one_to_zero = one_to_zero*one_to_zero * \
        (3-2*one_to_zero)  # 3rd order interpolation
    gradation = np.r_[one, one_to_zero]
    gradation = gradation[None, :, None]

    x = x0 * gradation + x1 * (1-gradation)

    pos = np.arange(width)
    mask_width = pos // div

    mask_width[mask_width < scale] = scale
    mask_width[(mask_width > mask_width[-1]-scale) &
               (mask_width < mask_width[-1])] = mask_width[-1] - scale

    pos_in_segment = ((pos * div) % width) // div
    mask = (pos_in_segment <= mask_width)
    x[:, mask, :] = color3

    return x


def __draw2(x, lines):
    width = x.shape[1]

    pos = np.arange(width)
    mask = ((pos*lines) // width) % 2 == 0

    xx = np.zeros((width, width, 3), dtype=np.float32)
    xx[mask] = x
    xx[~mask] = x[:, ::-1]
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
        trans[1, 2] = width*np.sin(angle/180*np.pi)
        x = cv2.warpAffine(x, trans, (int(adjust*width)+1,
                           int(adjust*width)+1), flags=cv2.INTER_NEAREST)
    return x


def __draw4(x, scale, pad, grad2, color3, color4):
    x_width = x.shape[1]
    pad = pad*scale
    width = x_width+pad*2

    grad2 = (grad2*width) // 100

    bk1 = np.zeros((width, width, 3), dtype=np.float32)
    bk1[:] = color3

    bk2 = np.zeros((width, width, 3), dtype=np.float32)
    bk2[:] = color4

    one = np.ones((grad2,), dtype=np.float32)
    one_to_zero = np.linspace(
        1, 0, width-grad2, endpoint=False, dtype=np.float32)
    one_to_zero = one_to_zero*one_to_zero * \
        (3-2*one_to_zero)  # 3rd order interpolation
    gradation = np.r_[one, one_to_zero]

    gradation = gradation[None, :, None]
    bk = bk1 * gradation + bk2 * (1-gradation)

    bk[pad:pad+x_width, pad:pad+x_width] = x[:, :, :3] * x[:, :, 3:4] + \
        bk[pad:pad+x_width, pad:pad+x_width]*(1-x[:, :, 3:4])

    if scale > 1:
        bk = cv2.resize(
            bk, (bk.shape[1]//scale, bk.shape[0]//scale), interpolation=cv2.INTER_AREA)

    return bk
