#!/usr/bin/python3

from random import shuffle
from tkinter import *

card_dir = "./cards/"

class Deck:
	def __init__(self):
		values = list(map(str,list(range(2,10))))+['T','J','Q','K','A']
		suits = ['H','D','S','C']
		deck = [v+s for s in suits for v in values]
		shuffle(deck)
		self.deck = deck

	def draw_card(self):
		return self.deck.pop()

	def draw_n_cards(self,n):
		return [self.draw_card() for i in range(n)]

class Hand:
	def __init__(self, deck):
		self.cards = deck.draw_n_cards(5)
		self.images = [PhotoImage(file=card_dir+self.cards[i]+'.gif') for i in range(5)]

	def discard(self, deck, positions):
		for p in positions:
			self.cards[p] = deck.draw_card()
			self.images[p] = PhotoImage(file=card_dir+self.cards[p]+'.gif')

	def evaluation(self):
		def value(card):
			if card[0]=='A':
				return 14
			elif card[0]=='K':
				return 13
			elif card[0]=='Q':
				return 12
			elif card[0]=='J':
				return 11
			elif card[0]=='T':
				return 10
			else:
				return int(card[0])
		
		def valhand(hand):
			vhand=[]
			for i in range(5):
				vhand.append(value(hand[i]))
			vhand.sort()
			vhand.reverse()
			return vhand
		
		def suithand(hand):
			suithand=[]
			for i in range(5):
				suithand.append(hand[i][1])
			return suithand
	
		def onepair(hand):
			vhand=valhand(hand)
			pairvalue=[]
			for i in vhand:
				if vhand.count(i)==2:
					pairvalue.append(i)
			if len(pairvalue)!=2:
				return False
			for i in pairvalue:
				vhand.remove(i)
			pairvalue=list(set(pairvalue))
			pairvalue.sort()
			return pairvalue+vhand
	
		def twopair(hand):
			vhand=valhand(hand)
			pairvalue=[]
			for i in vhand:
				if vhand.count(i)==2:
					pairvalue.append(i)
			if len(pairvalue)!=4:
				return False
			for i in pairvalue:
				vhand.remove(i)
			pairvalue=list(set(pairvalue))
			pairvalue.sort()
			return pairvalue+vhand
	
		def threekind(hand):
			vhand=valhand(hand)
			pairvalue=[]
			for i in vhand:
				if vhand.count(i)==3:
					pairvalue.append(i)
			if len(pairvalue)!=3:
				return False
			for i in pairvalue:
				vhand.remove(i)
			pairvalue=list(set(pairvalue))
			return pairvalue+vhand
		
		def straight(hand):
			vhand=valhand(hand)
			vhand.reverse()
			if vhand==range(vhand[0],vhand[0]+5):
				return [vhand[0]+5]
			else:
				return False
		
		def flush(hand):
			vhand=valhand(hand)
			shand=suithand(hand)
			if shand.count(shand[0])==5:
				return vhand
			else:
				return False
		
		def fullhouse(hand):
			if threekind(hand) and onepair(hand):
				return [threekind(hand)[0],onepair(hand)[0]]
			else:
				return False
		
		def fourkind(hand):
			vhand=valhand(hand)
			pairvalue=[]
			for i in vhand:
				if vhand.count(i)==4:
					pairvalue.append(i)
			if len(pairvalue)!=4:
				return False
			for i in pairvalue:
				vhand.remove(i)
			pairvalue=list(set(pairvalue))
			return pairvalue+vhand
		
		def straightflush(hand):
			if straight(hand) and flush(hand):
				return straight(hand)
			else:
				return False
		
		def royal(hand):
			if straightflush(hand) and valhand(hand)[0]==10:
				return True
	
		if royal(self.cards):
			return (10,10)
		elif straightflush(self.cards):
			return (9,straightflush(self.cards))
		elif fourkind(self.cards):
			return (8,fourkind(self.cards))
		elif fullhouse(self.cards):
			return (7,fullhouse(self.cards))
		elif flush(self.cards):
			return (6,flush(self.cards))
		elif straight(self.cards):
			return (5,straight(self.cards))
		elif threekind(self.cards):
			return (4,threekind(self.cards))
		elif twopair(self.cards):
			return (3,twopair(self.cards))
		elif onepair(self.cards):
			return (2,onepair(self.cards))
		else:
			return (1,valhand(self.cards))


def summary(score_human, score_AI):
	hand_names = {1:'high card', 2:'one pair', 3:'two pair', 4:'three of a kind', 5:'a straight', 6:'a flush', 7:'a full house', 8:'four of a kind', 9:'a straight flush', 10:'a royal flush'}
	result = "The AI has " + hand_names[score_AI[0]] + ", whereas the human has " + hand_names[score_human[0]] + ".\n"
	if score_human[0] > score_AI[0]:
		result += "Thus, the human wins."
	elif score_human[0] < score_AI[0]:
		result += "Thus, the AI wins."
	else:
		tiebreaker_human = score_human[1]
		tiebreaker_AI = score_AI[1]
		while tiebreaker_human:
			if tiebreaker_human[0] > tiebreaker_AI[0]:
				result += "However, the human ultimately has a stronger hand and therefore wins."
				break
			elif tiebreaker_human[0] < tiebreaker_AI[0]:
				result += "However, the AI ultimately has a stronger hand and therefore wins."
				break
			else:
				tiebreaker_human.pop(0)
				tiebreaker_AI.pop(0)
	return result


def play(hand_human, hand_AI, deck, cardlabels_human, cardlabels_AI, states, announcer, play_button):
	states = [state.get() for state in states]
	positions = [i for i in range(len(states)) if not states[i]]
	hand_human.discard(deck, positions)
	for p in positions:
		cardlabels_human[p].config(image=hand_human.images[p])
	for i in range(5):
		cardlabels_AI[i].config(image=hand_AI.images[i])
	score_human = hand_human.evaluation()
	score_AI = hand_AI.evaluation()
	result = summary(score_human, score_AI)
	announcer.config(text=result)
	disable(play_button)

def disable(button):
	button.config(state=DISABLED)

def main():
	master = Tk()
	master.title('Simple Five-Card Draw')
	deck = Deck()
	hand_AI = Hand(deck)
	hand_human = Hand(deck)

	announcer = Label(master, text="Select the cards you would like to retain")
	announcer.grid(row=1, column=0, columnspan=5)

	cardlabels_human = [Label(master) for i in range(5)]
	cardlabels_AI = [Label(master) for i in range(5)]
	discard_states = []
	back = PhotoImage(file=card_dir+'back.gif')
	
	for i in range(5):
		cardlabels_AI[i].grid(row=0, column=i)
		cardlabels_AI[i].config(image=back)
		cardlabels_human[i].grid(row=2, column=i)
		cardlabels_human[i].config(image=hand_human.images[i])
		discard_card = IntVar()
		chk = Checkbutton(master, variable=discard_card)
		chk.grid(row=3,column=i)
		discard_states.append(discard_card)
	
	play_button = Button(master, text='DRAW', command=lambda: play(hand_human, hand_AI, deck, cardlabels_human, cardlabels_AI, discard_states, announcer, play_button))
	play_button.grid(row=4, column=2)

	master.mainloop()


main()

#if __name__ == '__main__':
#	main()

