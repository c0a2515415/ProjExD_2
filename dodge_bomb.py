import os
import sys
import pygame as pg
import random


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数で与えられたRectが画面内か画面外か判定する関数
    引数：こうかとんRectかばくだんRect
    戻り値：タプル（横方向、縦方向）
    画面内ならTrue、画面外ならFalse
    """


    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:    #横方向判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = pg.Surface((20, 20))       #爆弾用の空のSurfaceを作る
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)   #爆弾円を描く
    bb_img.set_colorkey((0, 0, 0))      #余計な黒い部分を見えない様にする
    bb_rct = bb_img.get_rect()      #爆弾Rectを取得する
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)    #爆弾の場所を乱数で設定する

    clock = pg.time.Clock()
    tmr = 0

    vx = 5
    vy = 5
    DELTA = {pg.K_UP:(0, -5), pg.K_DOWN:(0, 5), pg.K_LEFT:(-5, 0), pg.K_RIGHT:(5, 0)}   #押下キー用の辞書です
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for i in DELTA:         #ifを4つ削除し、forで押下キーを回しています。
            if key_lst[i]:      #方向確認し、
                sum_mv =  DELTA[i]      #確認された方向の数値を代入

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])      #画面外なら、逆向きに動かすことで動きを止める
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)        #横5, 縦5の速度で動くように設定
        yoko, tate = check_bound(bb_rct)
        if not yoko:    #横方向の判定（Falseになっていたら
            vx *= -1
        if not tate:    #縦判定
            vy *= -1
        screen.blit(bb_img, bb_rct)     #爆弾をblit

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
