
def s(Card) :
    if Card in ('A c','2 c','3 c','4 c','5 c','6 c','7 c','8 c','9 c','10 c','J c','Q c','K c') :
        return "c"
    if Card in ('A d','2 d','3 d','4 d','5 d','6 d','7 d','8 d','9 d','10 d','J d','Q d','K d') :
        return "d"
    if Card in ('A h','2 h','3 h','4 h','5 h','6 h','7 h','8 h','9 h','10 h','J h','Q h','K h') :
        return "h"
    if Card in ('A s','2 s','3 s','4 s','5 s','6 s','7 s','8 s','9 s','10 s','J s','Q s','K s') :
        return "s"

def n(Card) :
    if Card in ('2 c','2 d','2 h','2 s',2):
        return 2
    if Card in ('3 c','3 d','3 h','3 s',3):
        return 3
    if Card in ('4 c','4 d','4 h','4 s',4):
        return 4
    if Card in ('5 c','5 d','5 h','5 s',5):
        return 5
    if Card in ('6 c','6 d','6 h','6 s',6):
        return 6
    if Card in ('7 c','7 d','7 h','7 s',7):
        return 7
    if Card in ('8 c','8 d','8 h','8 s',8):
        return 8
    if Card in ('9 c','9 d','9 h','9 s',9):
        return 9
    if Card in ('10 c','10 d','10 h','10 s',10):
        return 10
    if Card in ('J c','J d','J h','J s',11):
        return 11
    if Card in ('Q c','Q d','Q h','Q s',12):
        return 12
    if Card in ('K c','K d','K h','K s',13):
        return 13
    if Card in ('A c','A d','A h','A s',14):
        return 14
#----

def hand1( My_1th_Card , My_2th_Card ) :
    """ AA,KK """
    if  n( My_1th_Card ) == n( My_2th_Card )  and 13 <= n( My_1th_Card ) <= 14 :
        shout("hand1 is True")
        return True
    else :
        return None

def hand2( My_1th_Card , My_2th_Card ) :
    """ QQ,JJ """
    if  n( My_1th_Card ) == n( My_2th_Card )  and 11 <= n( My_1th_Card ) <= 12 :
        shout("hand2 is True")
        return True
    else :
        return None

def hand3( My_1th_Card , My_2th_Card ) :
    """ 1010,99 """
    if  n( My_1th_Card ) == n( My_2th_Card )  and 9 <= n( My_1th_Card ) <= 10 :
        shout("hand3 is True")
        return True
    else :
        return None

def hand4( My_1th_Card , My_2th_Card ) :
    """ 88,77,...,22 """
    if  n( My_1th_Card ) == n( My_2th_Card )  and 2 <= n( My_1th_Card ) <= 8 :
        shout("hand4 is True")
        return True
    else :
        return None

def hand5( My_1th_Card , My_2th_Card ) :
    """ A10,...,KQ  3 Blind raise """
    if  n( My_1th_Card ) != n( My_2th_Card ) :
        if ( 12 <= n( My_1th_Card ) <= 13 and 12 <= n( My_2th_Card ) <= 13 ) \
        or ( 14 in [ n( My_1th_Card ) , n( My_2th_Card ) ] and n( My_1th_Card ) >= 10 and n( My_2th_Card ) >= 10 ) :
            shout("hand5 is True")
            return True
    else :
        return None

def hand6( My_1th_Card , My_2th_Card ) :
    """ KJ,QJ,,...,A2,...,(108,98 rang),109  1 Blind call """
    if  n( My_1th_Card ) != n( My_2th_Card ) :
        if hand5( My_1th_Card , My_2th_Card ) != True :
            if 14 in [ n( My_1th_Card ) , n( My_2th_Card ) ] \
            or ( n( My_1th_Card ) >= 8 and n( My_2th_Card ) >= 8 and s( My_1th_Card ) == s( My_2th_Card ) ) \
            or ( n( My_1th_Card ) >= 9 and n( My_2th_Card ) >= 9 ) :
                shout("hand6 is True")
                return True
    else :
        return None


def hand7( My_1th_Card , My_2th_Card ) :
    """ 72,73,...,96,107 (gheir rang)  Fold small blind position (otherwise Small always call Blind) """
    if not( hand1( My_1th_Card , My_2th_Card ) or hand2( My_1th_Card , My_2th_Card ) or hand3( My_1th_Card , My_2th_Card ) or \
            hand4( My_1th_Card , My_2th_Card ) or hand5( My_1th_Card , My_2th_Card ) or hand6( My_1th_Card , My_2th_Card ) \
            or s( My_1th_Card ) == s( My_2th_Card ) ) :
        for i in range(2,8) :
            if i in ( n( My_1th_Card ) , n( My_2th_Card ) )  and abs( n( My_2th_Card ) - n( My_1th_Card ) ) >= 3 \
            and n( My_1th_Card ) <= 10 and n( My_2th_Card ) <= 10 :
                shout("hand7 is True")
                return True
    else :
        return None


#--------------------------------------------


def hand8( My_1th_Card , My_2th_Card ) :
    """ AK,...,1010,...22,...,(65 rang) Blind position call 2 blind raise, otherwise fold that """
    if not( hand1( My_1th_Card , My_2th_Card ) or hand2( My_1th_Card , My_2th_Card ) ) :
        if hand3( My_1th_Card , My_2th_Card ) or hand4( My_1th_Card , My_2th_Card ) \
        or hand5( My_1th_Card , My_2th_Card ) or hand6( My_1th_Card , My_2th_Card ) \
        or ( n( My_1th_Card ) >= 5 and n( My_2th_Card ) >= 5 and \
             s( My_1th_Card ) == s( My_2th_Card ) and abs( n( My_2th_Card ) - n( My_1th_Card ) ) == 1 ) :
            shout("hand8 is True")
            return True
    else :
        return None

def hand9( My_1th_Card , My_2th_Card ) :
    """ AK,...,1010,...,(98 rang) Small position call 2 blind raise, otherwise fold that """
    if not( hand1( My_1th_Card , My_2th_Card ) or hand2( My_1th_Card , My_2th_Card ) ) :
        if hand3( My_1th_Card , My_2th_Card ) or hand4( My_1th_Card , My_2th_Card ) \
        or hand5( My_1th_Card , My_2th_Card ) or hand6( My_1th_Card , My_2th_Card ) :
            shout("hand9 is True")
            return True
    else :
        return None    


