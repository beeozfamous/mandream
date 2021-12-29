def super_process(mask_name, im_name):
    print(im_name)
    img = cv2.cvtColor(image_resize(cv.imread(im_name), im_size, im_size), cv2.COLOR_BGR2RGB)

    imgcopy = np.copy(image_resize(cv.imread(im_name, -1), im_size, im_size))

    alpha = image_resize(cv.imread(mask_name, 0), im_size, im_size)
    alphacopy = np.copy(alpha)

    no_matting = save_img_nomatting(img, alpha)
    h, w = img.shape[:2]

    masku2net_new = np.copy(alpha)  # np.copy(exposure.equalize_adapthist(alpha, clip_limit=0.03))
    masku2net_new[masku2net_new > 240] = 255
    masku2net_new[masku2net_new < 10] = 0
    masku2net_new[(masku2net_new <= 240) & (masku2net_new >= 10)] = 128

    trimap = masku2net_new

    for x11 in [0]:
        for y11 in [0]:
            pwh = [0, 0, 0, 0]
            pwh = [ph1, ph2, pw1, pw2]
            imgbp = cv2.copyMakeBorder(imgzys, pwh[0], pwh[1], pwh[2], pwh[3], cv2.BORDER_REPLICATE)
            tri = trimap
            trizys = tri.copy()
            tribp = cv2.copyMakeBorder(tri, pwh[0], pwh[1], pwh[2], pwh[3], cv2.BORDER_CONSTANT)
            imgbpp = cv2.copyMakeBorder(imgbp, wsss2, wsss2, wsss2, wsss2, cv2.BORDER_REPLICATE)
            tribpp = cv2.copyMakeBorder(tribp, wsss2, wsss2, wsss2, wsss2, cv2.BORDER_CONSTANT)
            alls = []
            for px in range(hx):
                for py in range(wx):
                    nnns = 0
                    for zzz in range(16):
                        if np.sum(tp[px * qsss:px * qsss + wsss, py * qsss:py * qsss + wsss, zzz]) == 0:
                            nnns = zzz
                            break
                    wp[px * qsss: px * qsss + wsss, py * qsss:py * qsss + wsss, nnns] = wsm
                    tp[px * qsss:px * qsss + wsss, py * qsss:py * qsss + wsss, nnns] = 1
                    alls = []
                    for fl1, fl2 in zip([0], [0]):
                        if fl1 >= 0:
                            imgf = imgbp[px * qsss:px * qsss + wsss, py * qsss:py * qsss + wsss].copy()
                            trif = tribp[px * qsss:px * qsss + wsss, py * qsss:py * qsss + wsss].copy()
                            imgrr = cv2.flip(imgf, fl1)
                            trirr = cv2.flip(trif, fl1)
                            imgss2 = cv2.flip(imgzys.copy(), fl1)
                            triss2 = cv2.flip(trizys.copy(), fl1)
                            img4x2 = imgbpp[px * qsss:(px) * qsss + wsss + wsss,
                                     py * qsss:(py) * qsss + wsss + wsss].copy()
                            tri4x2 = tribpp[px * qsss:(px) * qsss + wsss + wsss,
                                     py * qsss:(py) * qsss + wsss + wsss].copy()
                            img4x2 = cv2.flip(img4x2, fl1)
                            tri4x2 = cv2.flip(tri4x2, fl1)
                        else:
                            imgf = imgbp[px * qsss:px * qsss + wsss, py * qsss:py * qsss + wsss].copy()
                            trif = tribp[px * qsss:px * qsss + wsss, py * qsss:py * qsss + wsss].copy()
                            imgrr = imgf.copy()
                            trirr = trif.copy()
                            imgss2 = imgzys.copy()
                            triss2 = trizys.copy()
                            img4x2 = imgbpp[px * qsss:(px) * qsss + wsss + wsss,
                                     py * qsss:(py) * qsss + wsss + wsss].copy()
                            tri4x2 = tribpp[px * qsss:(px) * qsss + wsss + wsss,
                                     py * qsss:(py) * qsss + wsss + wsss].copy()
                        for fr1, fr2 in zip([0], [2]):
                            if fr1 >= 0:
                                imgrr3 = cv2.rotate(imgrr.copy(), fr1)
                                trirr3 = cv2.rotate(trirr.copy(), fr1)
                                imgss3 = cv2.rotate(imgss2.copy(), fr1)
                                triss3 = cv2.rotate(triss2.copy(), fr1)
                                img4x3 = cv2.rotate(img4x2.copy(), fr1)
                                tri4x3 = cv2.rotate(tri4x2.copy(), fr1)
                            else:
                                imgrr3 = imgrr.copy()
                                trirr3 = trirr.copy()
                                imgss3 = imgss2.copy()
                                triss3 = triss2.copy()
                                img4x3 = img4x2.copy()
                                tri4x3 = tri4x2.copy()
                            img = imgrr3
                            tri = trirr3
                            imgss = imgss3
                            triss = triss3
                            img4x = img4x3
                            tri4x = tri4x3
                            tritemp = np.zeros([*tri.shape, 2], np.float32)
                            tritemp[:, :, 0] = (tri == 0)
                            tritemp[:, :, 1] = (tri == 255)
                            sixc = trimap_transform(tritemp)
                            sixc = np.transpose(sixc, [2, 0, 1])
                            tritemp = np.zeros([*tri4x.shape, 2], np.float32)
                            tritemp[:, :, 0] = (tri4x == 0)
                            tritemp[:, :, 1] = (tri4x == 255)
                            sixc4x = trimap_transform(tritemp)
                            sixc4x = np.transpose(sixc4x, [2, 0, 1])
                            h_, w_ = tri.shape
                            tri2 = np.array(tri, np.float32) / 255.
                            tri2 = tri2[np.newaxis, np.newaxis, :, :]
                            tri24x = np.array(tri4x, np.float32) / 255.
                            tri24x = tri2[np.newaxis, np.newaxis, :, :]
                            mattinginput = ((img[:, :, ::-1] / 255.) - IMG_MEAN) / IMG_STD
                            mattinginput4x = ((img4x[:, :, ::-1] / 255.) - IMG_MEAN) / IMG_STD
                            raw = img[:, :, ::-1] / 255.
                            raw = np.transpose(raw, [2, 0, 1])[None, :, :, :]
                            h_, w_ = tri.shape
                            trixs = np.zeros((1, 3, h_, w_), np.float32)
                            trixs[0, 0] = (tri == 0)
                            trixs[0, 1] = (tri == 128)
                            trixs[0, 2] = (tri == 255)
                            ntrixs = trixs
                            trixs = torch.from_numpy(trixs)
                            h_, w_ = tri4x.shape
                            tris4x = np.zeros((1, 3, h_, w_), np.float32)
                            tris4x[0, 0] = (tri4x == 0)
                            tris4x[0, 1] = (tri4x == 128)
                            tris4x[0, 2] = (tri4x == 255)
                            tris4x = torch.from_numpy(tris4x)
                            mattinginput = np.transpose(mattinginput, (2, 0, 1)).astype(np.float32)
                            mattinginput = np.array(mattinginput)[np.newaxis, :, :, :]
                            mattinginput4x = np.transpose(mattinginput4x, (2, 0, 1)).astype(np.float32)
                            mattinginput4x = np.array(mattinginput4x)[np.newaxis, :, :, :]
                            i1 = torch.from_numpy(mattinginput)
                            i2 = torch.from_numpy(mattinginput4x)
                            sixc = sixc[None, :, :, :]
                            sixc4x = sixc4x[None, :, :, :]
                            sixc2 = torch.from_numpy(sixc)
                            sixc24x = torch.from_numpy(sixc4x)
                            i2i = torch.cat([i2, tris4x, sixc24x], 1).float().cuda()
                            i1i = torch.cat([i1, trixs, sixc2], 1).float().cuda()
                            rawi = torch.from_numpy(raw).float().cuda()
                            with torch.no_grad():
                                preda = segmodel(i1i, i2i, rawi)
                            preda = preda.detach().cpu()
                            ap = preda[0, 0].numpy() * ntrixs[0, 1] + ntrixs[0, 2]
                            a1 = ap
                            if fr2 >= 0:
                                a1 = cv2.rotate(a1, fr2)
                            if fl2 >= 0:
                                a1 = cv2.flip(a1, fl2)
                            alls.append(a1)
                    a1 = np.array(sum(alls) * 255. / len(alls))
                    alls = []
                    apPP[px * qsss:px * qsss + wsss, py * qsss:py * qsss + wsss, nnns] = a1
    palpha = np.sum(apPP * wp, 2) / np.sum(wp, 2)
    palpha = np.clip(palpha, 0, 255)
    palpha = np.array(palpha, np.uint8)
    wholealpha = palpha[ph1:ph1 + raw_h, pw1:pw1 + raw_w]
    wholealpha[trizys == 0] = 0
    wholealpha[trizys == 255] = 255

    img = cv2.cvtColor(image_resize(cv.imread(im_name), im_size, im_size), cv2.COLOR_BGR2RGB)
    im = composite4_nobg(img, wholealpha / 255)

    tmp = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    alpha = wholealpha
    b, g, r = cv2.split(im)
    rgba = [b, g, r, alpha]
    masked_tr = cv2.merge(rgba, 4)

    last = cv2.cvtColor(masked_tr, cv2.COLOR_BGRA2RGBA)

    return imgcopy, no_matting, alphacopy, trimap, wholealpha, last