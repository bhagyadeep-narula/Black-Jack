
import random

suits = ("Hearts", "Diamonds", "Spades", "Clubs")
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
          'Queen':10, 'King':10, 'Ace':11}

playing = True
total_chips = 100

class Card:

    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:

    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))

    def __str__(self):
        deck_comp = ""
        for card in self.deck:
            deck_comp += "\n " + card.__str__()
        return "This Deck Has: {}".format(deck_comp)

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card


class Hand:

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]

        if card.rank == "Ace":
            self.aces += 1

    def adjust_ace(self):
        if self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1


class Chips:

    def __init__(self,total):
        self.total = total
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):

    while True:
        try:
            chips.bet = int(input("How many chips would you like to bet? "))
        except TypeError:
            print("Sorry, a bet must be an integer! ")
        else:
            if chips.bet > chips.total:
                print("Sorry, your bet can't exceed {}".format(chips.total))
            else:
                break


def hit(deck,hand):

    hand.add_card(deck.deal())
    hand.adjust_ace()


def hit_or_stand(deck,hand):

    global playing

    while True:
        decision = input("Would You Like To Hit Or Stand ? Enter 'h' or 's': ")

        if decision[0].lower() == "h":
            hit(deck,hand)
        elif decision[0].lower() == "s":
            print("Player Stands ! Dealer Is Playing")
            playing = False
        else:
            print("Sorry! I did not understand that, please enter either 'h' or 's'")
            continue
        break


def show_some(player,dealer):

    print("\nDealer's Hand:")
    print(" <Card Hidden>")
    print("",dealer.cards[1])
    print("\nPlayer's Hand:")
    for card in player.cards:
        print("",card)

def show_all(player,dealer):

    print("\nDealer's Hand:\n", *dealer.cards, sep="\n")
    print("Dealer's Hand =",dealer.value)
    print("\nPlayer's Hand:\n", *player.cards, sep="\n")
    print("Player's Hand =",player.value)


def player_busts(player,dealer,chips):
    print("BUST PLAYER!")
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print("PLAYER WON!")
    chips.win_bet()

def dealer_wins(player,dealer,chips):
    print("PLAYER WON! DEALER BUSTED!")
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print("DEALER WINS!")
    chips.win_bet()

def push(player,dealer):
    print("Dealer and Player Tie! PUSH")


while True:

    print("WELCOME TO BLACKJACK!!")

    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    player_chips = Chips(total_chips)

    take_bet(player_chips)

    show_some(player_hand,dealer_hand)

    while playing:

        hit_or_stand(deck,player_hand)

        show_some(player_hand,dealer_hand)

        if player_hand.value > 21 :
            player_busts(player_hand,dealer_hand,player_chips)
            break

    if player_hand.value <= 21:

        while dealer_hand.value < 17:
            hit(deck,dealer_hand)

        show_all(player_hand,dealer_hand)

        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)
        else:
            push(player_hand,dealer_hand)


    print("\nPlayer's winnings stand at {}".format(player_chips.total))

    again = input("Would you like to play another hand? enter 'yes' or 'no': ")
    if again[0].lower() == 'y':
        total_chips = player_chips.total
        playing = True
        continue
    else:
        print("Thanks For Playing! Good Bye! TATA! Tak e Care!"
              "\n See You Again! Come Back Again! Have A Good Day!")
        break
