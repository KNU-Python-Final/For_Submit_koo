angel_str = 'angel'

angel_1_path = './assets/3round_images/angel/1.png'
angel_2_path = './assets/3round_images/angel/2.png'
angel_3_path = './assets/3round_images/angel/3.png'
angel_4_path = './assets/3round_images/angel/4.png'
angels_path = [
    angel_1_path, 
    angel_2_path, 
    angel_3_path, 
    angel_4_path, 
]

heart_angel_str = 'heart_angel'

heart_angel_1_path = './assets/3round_images/heart_angel/1.png'
heart_angel_2_path = './assets/3round_images/heart_angel/2.png'
heart_angel_3_path = './assets/3round_images/heart_angel/3.png'
heart_angel_4_path = './assets/3round_images/heart_angel/4.png'
heart_angels_path = [
    heart_angel_1_path, 
    heart_angel_2_path, 
    heart_angel_3_path, 
    heart_angel_4_path, 
]


king_str = 'king'

king_1_path = './assets/3round_images/king/1.png'
king_2_path = './assets/3round_images/king/2.png'
king_3_path = './assets/3round_images/king/3.png'
king_4_path = './assets/3round_images/king/4.png'
kings_path = [
    king_1_path, 
    king_2_path, 
    king_3_path, 
    king_4_path, 
]


heart_king_str = 'heart_king'

heart_king_1_path = './assets/3round_images/heart_king/1.png'
heart_king_2_path = './assets/3round_images/heart_king/2.png'
heart_king_3_path = './assets/3round_images/heart_king/3.png'
heart_king_4_path = './assets/3round_images/heart_king/4.png'
heart_kings_path = [
    heart_king_1_path, 
    heart_king_2_path, 
    heart_king_3_path, 
    heart_king_4_path, 
]


leaf_str = 'leaf'

leaf_1_path = './assets/3round_images/leaf/1.png'
leaf_2_path = './assets/3round_images/leaf/2.png'
leaf_3_path = './assets/3round_images/leaf/3.png'
leaf_4_path = './assets/3round_images/leaf/4.png'
leafs_path = [
    leaf_1_path, 
    leaf_2_path, 
    leaf_3_path, 
    leaf_4_path, 
]


heart_leaf_str = 'heart_leaf'

heart_leaf_1_path = './assets/3round_images/heart_leaf/1.png'
heart_leaf_2_path = './assets/3round_images/heart_leaf/2.png'
heart_leaf_3_path = './assets/3round_images/heart_leaf/3.png'
heart_leaf_4_path = './assets/3round_images/heart_leaf/4.png'
heart_leafs_path = [
    heart_leaf_1_path, 
    heart_leaf_2_path, 
    heart_leaf_3_path, 
    heart_leaf_4_path, 
]


santa_str = 'santa'

santa_1_path = './assets/3round_images/santa/1.png'
santa_2_path = './assets/3round_images/santa/2.png'
santa_3_path = './assets/3round_images/santa/3.png'
santa_4_path = './assets/3round_images/santa/4.png'
santas_path = [
    santa_1_path,
    santa_2_path,
    santa_3_path,
    santa_4_path,
]


heart_santa_str = 'heart_santa'

heart_santa_1_path = './assets/3round_images/heart_santa/1.png'
heart_santa_2_path = './assets/3round_images/heart_santa/2.png'
heart_santa_3_path = './assets/3round_images/heart_santa/3.png'
heart_santa_4_path = './assets/3round_images/heart_santa/4.png'
heart_santas_path = [
    heart_santa_1_path,
    heart_santa_2_path,
    heart_santa_3_path,
    heart_santa_4_path,
]

default_str = 'default'

default_1_path = './assets/3round_images/default/1.png'
default_2_path = './assets/3round_images/default/2.png'
default_3_path = './assets/3round_images/default/3.png'
default_4_path = './assets/3round_images/default/4.png'
defaults_path = [
    default_1_path, 
    default_2_path, 
    default_3_path, 
    default_4_path, 
]

angel_sign_path = './assets/3round_images/etc/angel_sign.png'
angel_sign_str = 'angel_sign'

bg_path = './assets/3round_images/etc/bg.png'
bg_sign_str = 'bg_sign'

buy_sign_path = './assets/3round_images/etc/buy_sign.png'
buy_sign_str = 'buy_sign'

heart_convert_path = './assets/3round_images/etc/heart_convert.png'
heart_convert_str = 'heart_convert'

exit_path = './assets/3round_images/etc/exit.png'
exit_str = 'exit_path'

king_sign_path = './assets/3round_images/etc/king_sign.png'
king_sign_str = 'king_sign'

leaf_sign_path = './assets/3round_images/etc/leaf_sign.png'
leaf_sign_str = 'leaf_sign'

santa_sign_path = './assets/3round_images/etc/santa_sign.png'
santa_sign_str = 'santa_sign'

shop_sign_path = './assets/3round_images/etc/shop_sign.png'
shop_sign_str = 'shop_sign'

return_sign_path = './assets/3round_images/etc/return.png'
return_sign_str = 'return_sign'



def get_image_path(name: str) -> str:
    if name == default_str:
        return default_1_path
    elif name == king_str:
        return king_1_path
    elif name == heart_king_str:
        return heart_king_1_path
    elif name == leaf_str:
        return leaf_1_path
    elif name == heart_leaf_str:
        return heart_leaf_1_path
    elif name == angel_str:
        return angel_1_path
    elif name == heart_angel_str:
        return heart_angel_1_path
    elif name == santa_str:
        return santa_1_path
    elif name == heart_santa_str:
        return heart_santa_1_path
    
    elif name == angel_sign_str:
        return angel_sign_path
    elif name == bg_sign_str:
        return bg_path
    elif name == buy_sign_str:
        return buy_sign_path
    elif name == heart_convert_str:
        return heart_convert_path
    elif name == exit_str:
        return exit_path
    elif name == king_sign_str:
        return king_sign_path
    elif name == leaf_sign_str:
        return leaf_sign_path
    elif name == santa_sign_str:
        return santa_sign_path
    elif name == shop_sign_str:
        return shop_sign_path
    elif name == return_sign_str:
        return return_sign_path
    else:
        return '' # error

def get_images_path(name: str) -> list[str]:
    if name == default_str:
        return defaults_path
    elif name == king_str:
        return kings_path
    elif name == heart_king_str:
        return heart_kings_path
    elif name == leaf_str:
        return leafs_path
    elif name == heart_leaf_str:
        return heart_leafs_path
    elif name == angel_str:
        return angels_path
    elif name == heart_angel_str:
        return heart_angels_path
    elif name == santa_str:
        return santas_path
    elif name == heart_santa_str:
        return heart_santas_path
    else:
        return [] # error