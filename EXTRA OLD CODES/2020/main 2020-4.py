import time, os
from datetime import datetime

import pyautogui, pygame, win32gui, win32con

import screen_monitoring.find_game_position.find_game_position as find_game_position
import screen_monitoring.pixel_matching.pixel_matching as pm
import decision_making.decide
import decision_making.rules_and_info.starting_hands as hand_ranking
from readability.read_cards import read_and_save_my_cards,\
read_and_save_flop_cards, read_and_save_turn_card,\
read_and_save_river_card
from readability.ocr import ocr_my_bank
from readability.click import fold, check, call, all_in,\
raising, check_fold
from readability.fix_game_disruption import fix_game_disruption,\
set_just_do_check_fold_to_true, reset_just_do_check_fold_to_false,\
screenshot_error
#importing same level directory modules
import config
from iprint import shout
from set_variables import set_all_variables_to_none,\
determine_small_big_dealer_seats,\
read_and_save_banks_and_names,reset_table_information, red_chips,\
read_and_save_bets

"""
Note 1: global new_hand = hand_is_ended() inside waiting functions.
Note 2: If I've resume the game, set 
        config.bot_status = 'WAITING_FOR_FIRST_HAND' inside resume function.
"""
def wait_celebration_ends(waiting_seconds = 10):
    global new_hand

    t1 = time.time()
    while True:
        new_hand = hand_is_ended()
        if not new_hand:
            break
        if time.time() - t1 > waiting_seconds:
            fix_game_disruption('game is stuck at celebration')
            break
    # sleep time so buttons and cards are dealt properly
    time.sleep(1)

def wait_for_my_new_hand(waiting_minutes = 10):
    global new_hand

    shout("Looking for my cards in 'I_AM_PLAYING' Section..."
          , color = 'light_magenta')
    t1 = time.time()
    while True:
        if pm.player_cards_pixel(config.game_position, config.my_seat_number):
            shout("My cards are founded", color = 'light_magenta')
            config.preflop_stage = True
            break
        new_hand = hand_is_ended()
        if not new_hand:
            break
        if time.time() - t1 > 60*waiting_minutes:
            fix_game_disruption('buttons are not founded')
            break

def wait_for_my_first_hand(waiting_minutes = 5):
    """Don't break this waiting function if new_hand is True, because I'm 
    waiting for first hand and maybe several hands are played without me.
    """
    shout("Looking for cards in 'WAITING_FOR_FIRST_HAND' Section..."
          , color = 'light_magenta')
    t1 = time.time()
    fixing_retry = 1
    while True:

        if pm.player_cards_pixel(config.game_position, config.my_seat_number):
            shout("My cards are founded", color = 'light_magenta')
            config.bot_status = 'I_AM_PLAYING'
            # If I've resume the game, set 
            # config.bot_status = 'WAITING_FOR_FIRST_HAND' inside resume function.
            # Even at preflop (betting_round = 0) I can resume the game without 
            # doing set_just_do_check_fold_to_true().
            if (not pm.pre_flop_pixel(config.game_position)  
                or (pm.pre_flop_pixel(config.game_position) 
                    and is_there_any_raiser() )) :
                set_just_do_check_fold_to_true("program is started again "\
                                               "from middle of the game")
            break
        if (time.time()-t1) > ((60*waiting_minutes)/3) and fixing_retry <= 1:
            fixing_retry += 1
            fix_game_disruption()
        if time.time() - t1 > 60 * waiting_minutes :
            config.bot_status = 'ON_MAIN_MENU'
            shout("No one join the table, call operator to go to main menu")
            break

def wait_for_sb_b_d_buttons(waiting_seconds = 5):
    """5 seconds waiting does not need new_hand to break it"""
    t1 = time.time()
    while True:
        if sb_b_d_buttons_are_founded():
            break
        if time.time() - t1 > waiting_seconds:
            fix_game_disruption('buttons are not founded')
            if not sb_b_d_buttons_are_founded():
                set_just_do_check_fold_to_true('buttons are not founded')
            break

def sb_b_d_buttons_are_founded():
    """For cheet there is no small or big blind buttons"""
    small_blind_button_founded = False
    big_blind_button_founded = False 
    dealer_button_founded = False
    for seat in [1,2,3,4,5]:
        if pm.small_blind_pixel(config.game_position, seat) == True:
            small_blind_button_founded = True
            break
    for seat in [1,2,3,4,5]:
        if pm.big_blind_pixel(config.game_position, seat) == True:
            big_blind_button_founded = True
            break
    for seat in [1,2,3,4,5]:
        if pm.dealer_pixel(config.game_position, seat) == True:
            dealer_button_founded = True
            break
    return small_blind_button_founded and big_blind_button_founded and dealer_button_founded

def is_there_any_raiser():
    """ Except me """
    for seat in range(1,6):
        if seat == config.my_seat_number :
            continue
        elif red_chips(seat) :
            return True
    return False

def shifted_to_next_stage():
    if (not config.flop_stage and pm.flop_pixel() 
        and not pm.turn_pixel() and not pm.river_pixel()):
        config.flop_stage = True
        shout("Waiting for my turn at flop_stage...", 'light_magenta') 
        return True
    if not config.turn_stage and pm.turn_pixel() and not pm.river_pixel():
        config.turn_stage = True
        shout("Waiting for my turn at turn_stage...", 'light_magenta') 
        return True
    if not config.river_stage and pm.river_pixel():
        config.river_stage = True
        shout("Waiting for my turn at river_stage...", 'light_magenta')
        return True
    return False

def read_board_cards():
    if config.flop_stage and not config.turn_stage and not config.river_stage:
        read_and_save_flop_cards()
    if config.turn_stage and not config.river_stage:
        read_and_save_turn_card()
    if config.river_stage:
        read_and_save_river_card()
 
def stages_are_sequenced():
    if pm.flop_pixel() and config.preflop_stage == False:
        return False
    if pm.turn_pixel() and False in (config.preflop_stage, config.flop_stage):
        return False
    if (pm.river_pixel() and
        False in (config.preflop_stage, config.flop_stage, config.turn_stage)):
        return False
    return True

def update_betting_rounds():
    if config.preflop_stage and not config.flop_stage:
        config.preflop_betting_round += 1
        shout('TESTING. preflop_betting_round is:%s'
              %config.preflop_betting_round, color = 'on_light_red')
    if config.flop_stage and not config.turn_stage:
        config.flop_betting_round += 1
        shout('TESTING. flop_betting_round is:%s'
              %config.flop_betting_round, color = 'on_light_red')
    if config.turn_stage and not config.river_stage:
        config.turn_betting_round += 1
        shout('TESTING. turn_betting_round is:%s'
              %config.turn_betting_round, color = 'on_light_red')
    if config.river_stage:
        config.river_betting_round += 1
        shout('TESTING. river_betting_round is:%s'
              %config.river_betting_round, color = 'on_light_red')

def hand_is_ended():
    """
    This is an important function, because it determines
    when new hand will start.
    For cheet: 
    1.Yellow around winning cards 
    2.If everyone fold the somebodies raise, only one player have cards.
    """
    for seat in [1,2,3,4,5]:
        if pm.my_seat_won_pixel(config.game_position, seat):
            return True
        if pm.other_seat_won_pixel(config.game_position, seat):
            return True
    return False

def declare_the_winners():
    """May differs for Cheet"""
    for seat in [1,2,3,4,5]:
        if pm.my_seat_won_pixel(config.game_position, seat) == True:
            shout("I won the game!", color = 'on_light_magenta')
        if pm.other_seat_won_pixel(config.game_position, seat) == True :
            shout("Seat %s won the game!" %seat)

def rebuy_if_bank_is_low(min_blinds = 15):
    my_bank = ocr_my_bank()
    if my_bank == None :
        shout("My bank can't be read")
    elif my_bank != None :
        shout(paint.light_green.bold("My bank is:%s" %my_bank))
        if 0 < my_bank <= min_blinds * config.BLIND_VALUE:
            shout("Rebuying...")
            pass # Later i'll build

def its_my_turn():
    if pm.active_player_pixel(config.game_position, config.my_seat_number):
        shout("It is my turn now", color = 'light_magenta')
        return True
    return False

def play_sound_for_good_starting_hands() :

    def sound(string_name) :
        try :
            pygame.mixer.init()
            pygame.mixer.music.load( os.path.join('Sounds' ,
                                                  "%s.wav" %string_name ) )
            return pygame.mixer.music.play()
        except :
            pass
            
    if config.preflop_stage == True and config.flop_stage == False :
        if hand_ranking.hand1() :
            sound("Michel")
            shout("Playing Music: 'Michel'", color = 'light_cyan')
        elif hand_ranking.hand2() :
            sound("Alan Walker")
            shout("Playing Music: 'Alan Walker'", color = 'light_cyan')
        elif hand_ranking.hand3() :
            sound("Alan Walker")
            shout("Playing Music: 'Alan Walker'", color = 'light_cyan')
        elif hand_ranking.hand4() :
            sound("Pocket low pairs")
            shout("Playing Music: 'Pocket low pairs'", color = 'light_cyan')
        elif hand_ranking.hand5() :
            sound("Bob Marley")
            shout("Playing Music: 'Bob Marley'", color = 'light_cyan')

def click_decision():

    decision = decision_making.decide.decide()
    if decision[0] == "check" :
        check()
    elif decision[0] == "call" :
        call()
    elif decision[0] == "fold" :
        fold()
    elif decision[0] == "raise" :
        raising(decision[1] * BLIND_VALUE)
    elif decision[0] == "all_in" :
        all_in()
    elif decision[0] == "check_fold" :
        check_fold()
    elif decision[0] == "not defined" :
        screenshot_error("decide function deficiency")
        check_fold()
    elif decision == None:
        screenshot_error("A play function returned None")
        check_fold()
    else :
        screenshot_error("returned string is not in standard format")
        check_fold()
    time.sleep(1)

def create_report_folder():
    config.DATED_REPORT_FOLDER = datetime.now().strftime("%Y.%m.%d %A %H.%M.%S")
    config.REPORTS_DIRECTORY = "Reports/%s" %config.DATED_REPORT_FOLDER
    if not os.path.exists( config.REPORTS_DIRECTORY ):
        os.makedirs( config.REPORTS_DIRECTORY )


if __name__ == '__main__':
    hwnd = win32gui.GetForegroundWindow()
    win32gui.SetWindowPos(hwnd,win32con.HWND_TOPMOST,1153,222,440,593,0)

    # Cleaning variables off the last run by set them all to None.
    set_all_variables_to_none()
    create_report_folder()

    # Initial values:
    config.MY_PROFILE_NAME = "XXX"
    if input("Is my name: %s ?(Enter:yes/any keyword:no)"%config.MY_PROFILE_NAME) != "" :
        config.MY_PROFILE_NAME = input("Enter profile name: ")
    config.my_seat_number = int( input("My seat number? ") )
    config.bot_status = 'WAITING_FOR_FIRST_HAND'
    config.BLIND_VALUE = 100000000
    config.game_position = find_game_position.find_game_reference_point()




while True:

    reset_table_information() 

    if config.bot_status == 'ON_MAIN_MENU':
        shout("* bot_status == 'ON_MAIN_MENU' *", color = 'on_green')
        raise Exception("5.This can not happen IN FUTURE because main "\
                        "menu automation is built " \
                        "( fix_game_disruption --> Sit_In --> "\
                        "table is full --> exit --> "\
                        "config.bot_status = 'ON_MAIN_MENU' --> main menu "\
                        "--> config.bot_status = 'WAITING_FOR_FIRST_HAND' )")

    # Why do we need to have 'WAITING_FOR_FIRST_HAND' status?
    # Answer: Because we may need to wait for several hands before we start  
    # our first hand and wait_for_my_first_hand() will not break by new hands. 
    elif config.bot_status == 'WAITING_FOR_FIRST_HAND':
        shout("* bot_status == 'WAITING_FOR_FIRST_HAND' *",color = 'on_green')
        rebuy_if_bank_is_low(min_blinds = 15)
        read_and_save_banks_and_names()
        wait_for_my_first_hand(waiting_minutes = 5)

    elif config.bot_status == 'I_AM_PLAYING':
        new_hand = hand_is_ended()
        if new_hand: 
            declare_the_winners()
            wait_celebration_ends(waiting_seconds = 10)
        shout("* bot_status == 'I_AM_PLAYING' *")
        wait_for_my_new_hand(waiting_minutes = 10)
        # use this statement after functions which use fix_game_disruption()
        if config.bot_status != 'I_AM_PLAYING': 
            continue
        # use this statement after waiting functions 
        # which uses new_hand = hand_is_ended()
        if new_hand: 
            continue
        shout ("-------- New Hand Started --------", color = 'on_green')
        wait_for_sb_b_d_buttons(waiting_seconds = 5) 
        if config.bot_status != 'I_AM_PLAYING': 
            continue
        determine_small_big_dealer_seats()
        read_and_save_my_cards()
        rebuy_if_bank_is_low(min_blinds = 15)
        read_and_save_banks_and_names()
        if config.bot_status != 'I_AM_PLAYING': 
            continue
        play_sound_for_good_starting_hands()

        shout("Waiting for my turn at preflop_stage...", 'light_magenta') 
        t1 = time.time()
        # Playing a whole hand in this loop
        while True:
            if shifted_to_next_stage(): 
                read_board_cards()
                if not stages_are_sequenced():
                    set_just_do_check_fold_to_true('stages are not sequenced')
                    screenshot_error('stages are not sequenced')
            if its_my_turn():
                update_betting_rounds()
                read_and_save_bets()
                if config.bot_status == 'I_AM_PLAYING':
                    click_decision()
            if t1 - time.time() > 5 * 60:
                fix_game_disruption('This hand last more than 5 minutes')
            new_hand = hand_is_ended()
            if new_hand:
                shout ("-------- Hand ended --------", color = 'on_green')
                break
            if config.bot_status != 'I_AM_PLAYING':
                break

    else:
        # Develop 'OBSERVING' status for bot_status later.
        # 'OBSERVING' status can be used to test screen monitoring or to
        # get opponents playing styles or to gather statistical data.
        raise Exception("bot_status is can be only 'ON_MAIN_MENU' or "\
                        "'WAITING_FOR_FIRST_HAND' or 'I_AM_PLAYING'")

