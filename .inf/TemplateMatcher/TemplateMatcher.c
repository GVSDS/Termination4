#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>
#include <wchar.h>

#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image_write.h"

#ifdef __cplusplus
#define DLL_EXPORT extern "C" __declspec(dllexport)
#else
#define DLL_EXPORT __declspec(dllexport)
#endif

typedef struct {
    int width;
    int height;
    unsigned char* data;
} GrayImage;

typedef struct {
    int x;
    int y;
    int error;
    double confidence;
} MatchResult;

// 辅助：UTF8 → WCHAR
static wchar_t* utf8_to_wchar(const char* utf8) {
    int len = MultiByteToWideChar(CP_UTF8, 0, utf8, -1, NULL, 0);
    wchar_t* buf = (wchar_t*)malloc(sizeof(wchar_t) * len);
    MultiByteToWideChar(CP_UTF8, 0, utf8, -1, buf, len);
    return buf;
}

// 修复1：支持中文/UTF8路径
DLL_EXPORT GrayImage* LoadImageGray(const char* filename, int* errorCode) {
    *errorCode = 0;
    if (!filename) { *errorCode = 100; return NULL; }

    wchar_t* wpath = utf8_to_wchar(filename);
    FILE* f = _wfopen(wpath, L"rb");
    free(wpath);

    if (!f) { *errorCode = 100; return NULL; }

    int w, h, ch;
    unsigned char* data = stbi_load_from_file(f, &w, &h, &ch, 1);
    fclose(f);

    if (!data) { *errorCode = 100; return NULL; }

    GrayImage* im = (GrayImage*)malloc(sizeof(GrayImage));
    if (!im) { stbi_image_free(data); *errorCode = 101; return NULL; }

    im->width = w;
    im->height = h;
    im->data = data;
    return im;
}

// 修复2：多显示器虚拟屏幕截图
DLL_EXPORT GrayImage* CaptureScreenGray(int* errorCode) {
    *errorCode = 0;
    int w = GetSystemMetrics(SM_CXVIRTUALSCREEN);
    int h = GetSystemMetrics(SM_CYVIRTUALSCREEN);
    int x0 = GetSystemMetrics(SM_XVIRTUALSCREEN);
    int y0 = GetSystemMetrics(SM_YVIRTUALSCREEN);

    HDC hdc = GetDC(NULL);
    HDC mem = CreateCompatibleDC(hdc);
    HBITMAP bmp = CreateCompatibleBitmap(hdc, w, h);
    SelectObject(mem, bmp);

    if (!BitBlt(mem, 0, 0, w, h, hdc, x0, y0, SRCCOPY)) { *errorCode = 4; goto cleanup; }

    BITMAPINFOHEADER bi = {0};
    bi.biSize = sizeof(BITMAPINFOHEADER);
    bi.biWidth = w;
    bi.biHeight = -h;
    bi.biPlanes = 1;
    bi.biBitCount = 24;
    bi.biCompression = BI_RGB;

    unsigned char* rgb = (unsigned char*)malloc(w * h * 3);
    if (!GetDIBits(hdc, bmp, 0, h, rgb, (BITMAPINFO*)&bi, DIB_RGB_COLORS)) { *errorCode = 6; free(rgb); goto cleanup; }

    GrayImage* out = (GrayImage*)malloc(sizeof(GrayImage));
    out->width = w;
    out->height = h;
    out->data = (unsigned char*)malloc(w * h);

    #pragma omp parallel for
    for (int y = 0; y < h; y++) {
        for (int x = 0; x < w; x++) {
            int off = y * w * 3 + x * 3;
            int r = rgb[off+2], g = rgb[off+1], b = rgb[off];
            out->data[y*w + x] = (unsigned char)(0.299*r + 0.587*g + 0.114*b);
        }
    }

    free(rgb);
cleanup:
    DeleteObject(bmp);
    DeleteDC(mem);
    ReleaseDC(NULL, hdc);
    return *errorCode ? NULL : out;
}

// 修复3：加入 SearchArea(x1,y1,x2,y2)
DLL_EXPORT MatchResult FindTemplateOptimized(
    GrayImage* screen,
    GrayImage* target,
    double threshold,
    int searchX1, int searchY1, int searchX2, int searchY2
) {
    MatchResult res = {-1, -1, 0, 0.0};
    double bestDiff = 1e18;

    if (!screen || !target || !screen->data || !target->data) { res.error = 200; return res; }
    int tw = target->width, th = target->height;
    int sw = screen->width, sh = screen->height;
    if (tw > sw || th > sh) { res.error = 201; return res; }

    // 区域裁剪
    int x1 = (searchX1 >= 0) ? searchX1 : 0;
    int y1 = (searchY1 >= 0) ? searchY1 : 0;
    int x2 = (searchX2 > 0) ? searchX2 : sw;
    int y2 = (searchY2 > 0) ? searchY2 : sh;
    if (x2 - x1 < tw || y2 - y1 < th) { res.error = 201; return res; }

    long maxDiff = 255LL * 255LL * tw * th;

    #pragma omp parallel
    {
        double locBest = 1e18;
        int lx = -1, ly = -1;

        #pragma omp for schedule(dynamic, 4) nowait
        for (int y = y1; y <= y2 - th; y++) {
            for (int x = x1; x <= x2 - tw; x++) {
                long sum = 0;
                for (int dy = 0; dy < th; dy++) {
                    for (int dx = 0; dx < tw; dx++) {
                        int s = screen->data[(y+dy)*sw + (x+dx)];
                        int t = target->data[dy*tw + dx];
                        int d = s - t;
                        sum += d * d;
                    }
                }
                if (sum < locBest) {
                    locBest = sum;
                    lx = x + tw/2;
                    ly = y + th/2;
                }
            }
        }

        #pragma omp critical
        if (locBest < bestDiff) {
            bestDiff = locBest;
            res.x = lx;
            res.y = ly;
        }
    }

    res.confidence = 1.0 - (double)bestDiff / maxDiff;
    if (res.confidence < threshold) {
        res.x = res.y = -1;
        res.error = 202;
    }
    return res;
}

// 修复4：绝对坐标鼠标点击
DLL_EXPORT int ClickAt(int x, int y) {
    if (!SetCursorPos(x, y)) return 300;

    INPUT in[2] = {0};
    in[0].type = INPUT_MOUSE;
    in[0].mi.dwFlags = MOUSEEVENTF_LEFTDOWN | MOUSEEVENTF_ABSOLUTE;
    in[1].type = INPUT_MOUSE;
    in[1].mi.dwFlags = MOUSEEVENTF_LEFTUP | MOUSEEVENTF_ABSOLUTE;

    float fx = (float)x / GetSystemMetrics(SM_CXVIRTUALSCREEN) * 65535.0f;
    float fy = (float)y / GetSystemMetrics(SM_CYVIRTUALSCREEN) * 65535.0f;
    in[0].mi.dx = (LONG)fx;
    in[0].mi.dy = (LONG)fy;
    in[1].mi.dx = (LONG)fx;
    in[1].mi.dy = (LONG)fy;

    if (SendInput(2, in, sizeof(INPUT)) != 2) return 301;
    return 0;
}

DLL_EXPORT void FreeGrayImage(GrayImage* im) {
    if (im) { free(im->data); free(im); }
}

DLL_EXPORT int Initialize() {
    omp_set_num_threads(omp_get_num_procs());
    return 0;
}