import pickle, os
from pathlib import PurePath
from decision_making.rules_and_info.suit_and_value import s, n
#from suit_and_value import s, n

"""
Functions with True or False return,are in 2 kind of categoreis: 1.Me_Flush_ Me_Flush_draw 2.Table_Flush Table_Flush_draw
If one of them is True the rest will be False. All functions can be False at the same time.

Ranking Functions are :1.Me_flush_Ranking 2.Me_flush_draw_Ranking .
Ranking Functions return 1.a Number or 2.None value if their True or False Functions have not been True already.
Table functions has no rankings in Flush and Pair files. in Str file there are Table_.._Number functions. 
"""

def load_variables():
    """ variables order is important while loading """
    global game_position , DATED_REPORT_FOLDER , REPORTS_DIRECTORY,\
    preflop_stage , flop_stage , turn_stage , river_stage ,\
    preflop_betting_round , flop_betting_round ,\
    turn_betting_round , river_betting_round ,\
    board_card_1th , board_card_2th , board_card_3th ,\
    board_card_4th, board_card_5th , my_1th_card , my_2th_card ,\
    my_seat_number , MY_PROFILE_NAME ,\
    just_do_check_fold , waiting_for_first_hand ,\
    player_cards_cache , white_chips_cache , red_chips_cache , bets_cache ,\
    last_white_chips_cache , last_red_chips_cache ,\
    last_player_cards_cache , last_bets_cache,\
    did_i_raised_at  , my_last_raise_at , players_name , players_bank ,\
    BLIND_VALUE , small_blind_seat , big_blind_seat , dealer_seat

    current_path = os.path.abspath(os.path.dirname(__file__)) 
    pickle_path = PurePath(current_path).parent.parent / 'pickled variables.p'

    game_position , DATED_REPORT_FOLDER , REPORTS_DIRECTORY,\
    preflop_stage , flop_stage , turn_stage , river_stage ,\
    preflop_betting_round , flop_betting_round ,\
    turn_betting_round , river_betting_round ,\
    board_card_1th , board_card_2th , board_card_3th ,\
    board_card_4th, board_card_5th , my_1th_card , my_2th_card ,\
    my_seat_number , MY_PROFILE_NAME ,\
    just_do_check_fold , waiting_for_first_hand ,\
    player_cards_cache , white_chips_cache , red_chips_cache , bets_cache ,\
    last_white_chips_cache , last_red_chips_cache ,\
    last_player_cards_cache , last_bets_cache,\
    did_i_raised_at  , my_last_raise_at , players_name , players_bank ,\
    BLIND_VALUE , small_blind_seat , big_blind_seat , dealer_seat = \
    pickle.load( open( str(pickle_path), "rb" ) )


def Me_Flush_by_3_table_cards( List = None ) :
    """ ( ['6 c','8 c','10 c','K c','A d'] , '2 c' , '3 c' ) return False """
    global flop_stage , turn_stage , river_stage ,\
    board_card_1th , board_card_2th , board_card_3th , board_card_4th , board_card_5th , my_1th_card , my_2th_card
    load_variables()
    
    if List == None :
        if flop_stage == True and turn_stage == False :
            List = [ board_card_1th , board_card_2th , board_card_3th ]
        elif turn_stage == True and river_stage == False :
            List = [ board_card_1th , board_card_2th , board_card_3th , board_card_4th ]
        elif river_stage == True :
            List = [ board_card_1th , board_card_2th , board_card_3th , board_card_4th , board_card_5th ]

    if s(my_1th_card) == s(my_2th_card) :
        sign = 0
        for i in List :
            if s(my_1th_card) == s(i) :
                sign += 1
        if sign == 3 :
            return True
    return False

def Me_Flush_by_4_table_cards( List = None ) :
    """ ( ['6 c','8 c','10 c','K c','A c'] , 'Q c' , '3 c' ) return False """
    global flop_stage , turn_stage , river_stage ,\
    board_card_1th , board_card_2th , board_card_3th , board_card_4th , board_card_5th , my_1th_card , my_2th_card
    load_variables()
    
    if List == None :
        if flop_stage == True and turn_stage == False :
            List = [ board_card_1th , board_card_2th , board_card_3th ]
        elif turn_stage == True and river_stage == False :
            List = [ board_card_1th , board_card_2th , board_card_3th , board_card_4th ]
        elif river_stage == True :
            List = [ board_card_1th , board_card_2th , board_card_3th , board_card_4th , board_card_5th ]

    sign1 = 0
    sign2 = 0
    for i in List :
        if s(my_1th_card) == s(i) :
            sign1 += 1
        if s(my_2th_card) == s(i) :
            sign2 += 1
    if sign1 == 4 or sign2 == 4 :
        return True
    return False

def Me_Flush_by_5_table_cards( List = None ) :
    """
    ( ['6 c','8 c','10 c','K c','A c'] , '2 c' , '3 c' ) return False
    ( ['6 c','8 c','10 c','K c','A c'] , 'Q c' , '7 c' ) return True
    """
    global flop_stage , turn_stage , river_stage ,\
    board_card_1th , board_card_2th , board_card_3th , board_card_4th , board_card_5th , my_1th_card , my_2th_card
    load_variables()
    
    if List == None :
        if flop_stage == True and turn_stage == False :
            List = [ board_card_1th , board_card_2th , board_card_3th ]
        elif turn_stage == True and river_stage == False :
            List = [ board_card_1th , board_card_2th , board_card_3th , board_card_4th ]
        elif river_stage == True :
            List = [ board_card_1th , board_card_2th , board_card_3th , board_card_4th , board_card_5th ]

    sign1 = 0
    sign2 = 0
    for i in List :
        if s(my_1th_card) == s(i) :
            sign1 += 1
        if s(my_2th_card) == s(i) :
            sign2 += 1

    if sign1 == 5 and sign2 == 5:
        My_highest = max(n(my_1th_card),n(my_2th_card))
    elif sign1 == 5 :
        My_highest = n(my_1th_card)
    elif sign2 == 5 :
        My_highest = n(my_2th_card)
    sign_List = []
    for i in List :
        sign_List.append(n(i))
    if (sign1 == 5 or sign2 == 5) and My_highest > min(sign_List) :
        return True
    return False

def Me_Flush( List = None ) :
    """ if Me_Flush_by_3_table_cards or Me_Flush_by_4_table_cards or Me_Flush_by_5_table_cards """
    global flop_stage , turn_stage , river_stage ,\
    board_card_1th , board_card_2th , board_card_3th , board_card_4th , board_card_5th , my_1th_card , my_2th_card
    load_variables()
    
    if List == None :
        if flop_stage == True and turn_stage == False :
            List = [ board_card_1th , board_card_2th , board_card_3th ]
        elif turn_stage == True and river_stage == False :
            List = [ board_card_1th , board_card_2th , board_card_3th , board_card_4th ]
        elif river_stage == True :
            List = [ board_card_1th , board_card_2th , board_card_3th , board_card_4th , board_card_5th ]

    
    if Me_Flush_by_3_table_cards( List ) or Me_Flush_by_4_table_cards( List ) or Me_Flush_by_5_table_cards( List ) :
        return True
    else:
        return False

def Me_Flush_Ranking( List = None ) :
    """
    Rank 1,...,9
    Example: Rank 3: ( ['6 c','K c','5 c'] , 'J c' , '3 c' )
    return None if Me_Flush_ == False
    """    
    global flop_stage , turn_stage , river_stage ,\
    board_card_1th , board_card_2th , board_card_3th , board_card_4th , board_card_5th , my_1th_card , my_2th_card
    load_variables()
    
    if List == None :
        if flop_stage == True and turn_stage == False :
            List = [ board_card_1th , board_card_2th , board_card_3th ]
        elif turn_stage == True and river_stage == False :
            List = [ board_card_1th , board_card_2th , board_card_3th , board_card_4th ]
        elif river_stage == True :
            List = [ board_card_1th , board_card_2th , board_card_3th , board_card_4th , board_card_5th ]

    if Me_Flush( List ) == False :
        return None
    c = 0; d = 0; h = 0; sp = 0
    for i in List :
        if s(i) == "c" : c = c + 1
        if s(i) == "d" : d = d + 1
        if s(i) == "h" : h = h + 1
        if s(i) == "s" : sp = sp + 1
    sign_List = []
    
    if c >= 3 :
        if s(my_1th_card) == s(my_2th_card) :
            My_highest = max(n(my_1th_card),n(my_2th_card))
        elif s(my_1th_card) == "c" :
            My_highest = n(my_1th_card)
        elif s(my_2th_card) == "c" :
            My_highest = n(my_2th_card)
        for i in List :
            if s(i) == "c" : sign_List.append(n(i))

    elif d >= 3 :
        if s(my_1th_card) == s(my_2th_card) :
            My_highest = max(n(my_1th_card),n(my_2th_card))
        elif s(my_1th_card) == "d" :
            My_highest = n(my_1th_card)
        elif s(my_2th_card) == "d" :
            My_highest = n(my_2th_card)
        for i in List :
            if s(i) == "d" : sign_List.append(n(i))
            
    elif h >= 3 :
        if s(my_1th_card) == s(my_2th_card) :
            My_highest = max(n(my_1th_card),n(my_2th_card))
        elif s(my_1th_card) == "h" :
            My_highest = n(my_1th_card)
        elif s(my_2th_card) == "h" :
            My_highest = n(my_2th_card)
        for i in List :
            if s(i) == "h" : sign_List.append(n(i))

    elif sp >= 3 :
        if s(my_1th_card) == s(my_2th_card) :
            My_highest = max(n(my_1th_card),n(my_2th_card))
        elif s(my_1th_card) == "s" :
            My_highest = n(my_1th_card)
        elif s(my_2th_card) == "s" :
            My_highest = n(my_2th_card)
        for i in List :
            if s(i) == "s" : sign_List.append(n(i))

    sign_List.sort(reverse=True)
    rank = 1
    for i in range(14,1,-1):
        if i == My_highest :
            break
        elif i in sign_List :
            continue
        rank += 1

    return rank



def Me_Flush_draw_by_2_table_cards( List = None ) :
    global flop_stage , turn_stage , river_stage ,\
    board_card_1th , board_card_2th , board_card_3th , board_card_4th , board_card_5th , my_1th_card , my_2th_card
    load_variables()
    
    if List == None :
        if flop_stage == True and turn_stage == False :
            List = [ board_card_1th , board_card_2th , board_card_3th ]
        elif turn_stage == True and river_stage == False :
            List = [ board_card_1th , board_card_2th , board_card_3th , board_card_4th ]
        elif river_stage == True :
            List = [ board_card_1th , board_card_2th , board_card_3th , board_card_4th , board_card_5th ]

    if s(my_1th_card) == s(my_2th_card) and len(List) <= 4 :
        sign = 0
        for i in List :
            if s(my_1th_card) == s(i) :
                sign += 1
        if sign == 2 :
            return True
    return False

def Me_Flush_draw_by_3_table_cards( List = None ) :
    global flop_stage , turn_stage , river_stage ,\
    board_card_1th , board_card_2th , board_card_3th , board_card_4th , board_card_5th , my_1th_card , my_2th_card
    load_variables()
    
    if List == None :
        if flop_stage == True and turn_stage == False :
            List = [ board_card_1th , board_card_2th , board_card_3th ]
        elif turn_stage == True and river_stage == False :
            List = [ board_card_1th , board_card_2th , board_card_3th , board_card_4th ]
        elif river_stage == True :
            List = [ board_card_1th , board_card_2th , board_card_3th , board_card_4th , board_card_5th ]

    sign1 = 0
    sign2 = 0
    if s(my_1th_card) != s(my_2th_card) and len(List) <= 4 : 
        for i in List :
            if s(my_1th_card) == s(i) :
                sign1 += 1
            if s(my_2th_card) == s(i) :
                sign2 += 1
        if sign1 == 3 or sign2 == 3 :
            return True
    return False    

def Me_Flush_draw_Ranking( List = None ) :
    """
    Rank 1,...,10
    Example: Rank 2: ( ['6 c','K c','5 h'] , 'Q c' , '3 c' )
    return None if Me_Flush == True or on River or not Me_Flush_draw
    """
    global flop_stage , turn_stage , river_stage ,\
    board_card_1th , board_card_2th , board_card_3th , board_card_4th , board_card_5th , my_1th_card , my_2th_card
    load_variables()
    
    if List == None :
        if flop_stage == True and turn_stage == False :
            List = [ board_card_1th , board_card_2th , board_card_3th ]
        elif turn_stage == True and river_stage == False :
            List = [ board_card_1th , board_card_2th , board_card_3th , board_card_4th ]
        elif river_stage == True :
            List = [ board_card_1th , board_card_2th , board_card_3th , board_card_4th , board_card_5th ]

    if Me_Flush( List ) == True or len(List) == 5 \
       or( Me_Flush_draw_by_2_table_cards( List ) == False and Me_Flush_draw_by_3_table_cards( List ) == False ) :
        return None
    c = 0; d = 0; h = 0; sp = 0
    for i in List :
        if s(i) == "c" : c = c + 1
        if s(i) == "d" : d = d + 1
        if s(i) == "h" : h = h + 1
        if s(i) == "s" : sp = sp + 1
    sign_List = []
    
    if c >= 2 :
        if s(my_1th_card) == s(my_2th_card) and s(my_1th_card) == "c" and c == 2:
            My_highest = max(n(my_1th_card),n(my_2th_card))
        elif s(my_1th_card) == "c" and c == 3 :
            My_highest = n(my_1th_card)
        elif s(my_2th_card) == "c" and c == 3 :
            My_highest = n(my_2th_card)
        for i in List :
            if s(i) == "c" : sign_List.append(n(i))

    elif d >= 2 :
        if s(my_1th_card) == s(my_2th_card) and s(my_1th_card) == "d" and d == 2:
            My_highest = max(n(my_1th_card),n(my_2th_card))
        elif s(my_1th_card) == "d" and d == 3 :
            My_highest = n(my_1th_card)
        elif s(my_2th_card) == "d" and d == 3 :
            My_highest = n(my_2th_card)
        for i in List :
            if s(i) == "d" : sign_List.append(n(i))

            
    elif h >= 2 :
        if s(my_1th_card) == s(my_2th_card) and s(my_1th_card) == "h" and h == 2:
            My_highest = max(n(my_1th_card),n(my_2th_card))
        elif s(my_1th_card) == "h" and h == 3 :
            My_highest = n(my_1th_card)
        elif s(my_2th_card) == "h" and h == 3 :
            My_highest = n(my_2th_card)
        for i in List :
            if s(i) == "h" : sign_List.append(n(i))

    elif sp >= 2 :
        if s(my_1th_card) == s(my_2th_card) and s(my_1th_card) == "s" and sp == 2:
            My_highest = max(n(my_1th_card),n(my_2th_card))
        elif s(my_1th_card) == "s" and sp == 3 :
            My_highest = n(my_1th_card)
        elif s(my_2th_card) == "s" and sp == 3 :
            My_highest = n(my_2th_card)
        for i in List :
            if s(i) == "s" : sign_List.append(n(i))


    sign_List.sort(reverse=True)
    rank = 1
    for i in range(14,1,-1):
        if i == My_highest :
            break
        elif i in sign_List :
            continue
        rank += 1

    return rank


def Table_Flush_3_cards( List = None ) :
    global flop_stage , turn_stage , river_stage ,\
    board_card_1th , board_card_2th , board_card_3th , board_card_4th , board_card_5th 
    load_variables()
    
    if List == None :
        if flop_stage == True and turn_stage == False :
            List = [ board_card_1th , board_card_2th , board_card_3th ]
        elif turn_stage == True and river_stage == False :
            List = [ board_card_1th , board_card_2th , board_card_3th , board_card_4th ]
        elif river_stage == True :
            List = [ board_card_1th , board_card_2th , board_card_3th , board_card_4th , board_card_5th ]

    c = 0; d = 0; h = 0; sp = 0
    for i in List :
        if s(i) == "c" : c = c + 1
        if s(i) == "d" : d = d + 1
        if s(i) == "h" : h = h + 1
        if s(i) == "s" : sp = sp + 1

    if 3 in (c,d,h,sp) :
        return True
    return False

def Table_Flush_4_cards( List = None ) :
    global flop_stage , turn_stage , river_stage ,\
    board_card_1th , board_card_2th , board_card_3th , board_card_4th , board_card_5th 
    load_variables()
    
    if List == None :
        if flop_stage == True and turn_stage == False :
            List = [ board_card_1th , board_card_2th , board_card_3th ]
        elif turn_stage == True and river_stage == False :
            List = [ board_card_1th , board_card_2th , board_card_3th , board_card_4th ]
        elif river_stage == True :
            List = [ board_card_1th , board_card_2th , board_card_3th , board_card_4th , board_card_5th ]
    
    c = 0; d = 0; h = 0; sp = 0
    for i in List :
        if s(i) == "c" : c = c + 1
        if s(i) == "d" : d = d + 1
        if s(i) == "h" : h = h + 1
        if s(i) == "s" : sp = sp + 1

    if 4 in (c,d,h,sp) :
        return True
    return False

def Table_Flush_5_cards( List = None ) :
    global flop_stage , turn_stage , river_stage ,\
    board_card_1th , board_card_2th , board_card_3th , board_card_4th , board_card_5th 
    load_variables()
    
    if List == None :
        if flop_stage == True and turn_stage == False :
            List = [ board_card_1th , board_card_2th , board_card_3th ]
        elif turn_stage == True and river_stage == False :
            List = [ board_card_1th , board_card_2th , board_card_3th , board_card_4th ]
        elif river_stage == True :
            List = [ board_card_1th , board_card_2th , board_card_3th , board_card_4th , board_card_5th ]
    
    c = 0; d = 0; h = 0; sp = 0
    for i in List :
        if s(i) == "c" : c = c + 1
        if s(i) == "d" : d = d + 1
        if s(i) == "h" : h = h + 1
        if s(i) == "s" : sp = sp + 1

    if 5 in (c,d,h,sp) :
        return True
    return False

def Table_Flush_draw( List = None ) :
    """
    True if 2 same sign card availabe on the table(not more or less than 2)
    returns False on River
    """
    global flop_stage , turn_stage , river_stage ,\
    board_card_1th , board_card_2th , board_card_3th , board_card_4th , board_card_5th 
    load_variables()
    
    if List == None :
        if flop_stage == True and turn_stage == False :
            List = [ board_card_1th , board_card_2th , board_card_3th ]
        elif turn_stage == True and river_stage == False :
            List = [ board_card_1th , board_card_2th , board_card_3th , board_card_4th ]
        elif river_stage == True :
            List = [ board_card_1th , board_card_2th , board_card_3th , board_card_4th , board_card_5th ]

    if len(List) > 4 :
        return False
    
    c = 0; d = 0; h = 0; sp = 0
    for i in List :
        if s(i) == "c" : c = c + 1
        if s(i) == "d" : d = d + 1
        if s(i) == "h" : h = h + 1
        if s(i) == "s" : sp = sp + 1

    if 2 in (c,d,h,sp) :
        return True
    return False

def Table_Flush( List = None ) :
    """ if Table_Flush_3_cards( List ) or Table_Flush_4_cards( List ) or Table_Flush_5_cards( List ) """
    global flop_stage , turn_stage , river_stage ,\
    board_card_1th , board_card_2th , board_card_3th , board_card_4th , board_card_5th 
    load_variables()
    
    if List == None :
        if flop_stage == True and turn_stage == False :
            List = [ board_card_1th , board_card_2th , board_card_3th ]
        elif turn_stage == True and river_stage == False :
            List = [ board_card_1th , board_card_2th , board_card_3th , board_card_4th ]
        elif river_stage == True :
            List = [ board_card_1th , board_card_2th , board_card_3th , board_card_4th , board_card_5th ]

    if Table_Flush_3_cards( List ) or Table_Flush_4_cards( List ) or Table_Flush_5_cards( List ) :
        return True
    return False

