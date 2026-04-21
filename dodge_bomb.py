import os
import sys
import pygame as pg
import random
import time


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


def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー画面を表示するための関数です。
    gm_imgは黒い背景
    fontoは「Game Over」という言葉
    gmkk_imgはこうかとんです。
    """

    gm_img = pg.Surface((WIDTH, HEIGHT))    #Game Over用背景画像作成
    pg.draw.rect(gm_img, (0, 0, 0), pg.Rect(0, 0,  WIDTH, HEIGHT))
    gm_img.set_alpha(100)
    gm_rct = gm_img.get_rect()
    # gm_rct.center = WIDTH, HEIGHT
    fonto = pg.font.Font(None, 80)      #Game Overの文字と背景作成
    txt = fonto.render("Game Over", 
                       True, (255, 255, 255))
    txt.set_alpha(255)                  #透明度個別調整
    gmkk_img = pg.image.load("fig/0.png")   #左のこうかとん
    gmkk_img.set_alpha(255)     #透明度個別調整
    gmkk_rct = gmkk_img.get_rect()
    gmkk_rct.center = 350, 320
    gmkk2_img = pg.image.load("fig/0.png")   #右のこうかとん
    gmkk2_img.set_alpha(255)        #透明度個別調整
    gmkk2_rct = gmkk2_img.get_rect()
    gmkk2_rct.center = 750, 320

    screen.blit(gm_img, gm_rct)

    screen.blit(txt, [400, 300])
    screen.blit(gmkk_img, gmkk_rct)     #左こうかとんblit
    screen.blit(gmkk2_img, gmkk2_rct)   #右こうかとんblit

    pg.display.update()     #6.の操作
    time.sleep(5)


# def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
#     for r in range(1, 11):
#         bb_img = pg.Surface((20*r, 20*r))
#         pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
#         bb_imgs.append(bb_img)
    
    bb_accs = [a for a in range(1, 11)]
    


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

    # init_bb_imgs(vx, vy)
    # avx = vx*bb_accs[min(tmr//500, 9)]
    # bb_img = bb_imgs[min(tmr//500, 9)]
    # bb_rct.width = bb_img.get_rect().width

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bb_rct):      #こうかとんと爆弾がぶつかったときの処理
            gameover(screen)
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
