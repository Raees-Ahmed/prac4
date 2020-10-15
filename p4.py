# Import libraries
import RPi.GPIO as GPIO
import random
import ES2EEPROMUtils
import os
from time import sleep
import time
import sys
from array import *
# some global variables that need to change as we run the program
end_of_game = None  # set if the user wins or ends the game
LED_NUMBER = 0
guess_number = 0
number_of_guesses = 0
VALUE = 0
# DEFINE THE PINS USED HERE
LED_value = [11, 13, 15]
LED_accuracy = 32
btn_submit = 16
btn_increase = 18
buzzer = 33
eeprom = ES2EEPROMUtils.ES2EEPROM()


# Print the game banner
def welcome():
    os.system('clear')
    print("  _   _                 _                  _____ _            __  __ _")
    print("| \ | |               | |                / ____| |          / _|/ _| |")
    print("|  \| |_   _ _ __ ___ | |__   ___ _ __  | (___ | |__  _   _| |_| |_| | ___ ")
    print("| . ` | | | | '_ ` _ \| '_ \ / _ \ '__|  \___ \| '_ \| | | |  _|  _| |/ _ \\")
    print("| |\  | |_| | | | | | | |_) |  __/ |     ____) | | | | |_| | | | | | |  __/")
    print("|_| \_|\__,_|_| |_| |_|_.__/ \___|_|    |_____/|_| |_|\__,_|_| |_| |_|\___|")
    print("")
    print("Guess the number and immortalise your name in the High Score Hall of Fame!")


# Print the game menu
def menu():
    global value
    global end_of_game
    option = input("Select an option:   H - View High Scores     P - Play Game       Q - Quit\n")
    option = option.upper()
    if option == "H":
        os.system('clear')
        print("HIGH SCORES!!")
        s_count, ss = fetch_scores()
        display_scores(s_count, ss)
    elif option == "P":
        end_of_game = False
        os.system('clear')
        print("Starting a new round!")
        print("Use the buttons on the Pi to make and submit your guess!")
        print("Press and hold the guess button to cancel your game")
        value = generate_number()
        while not end_of_game:
            pass
    elif option == "Q":
        print("Come back soon!")
        exit()
    else:
        print("Invalid option. Please select a valid one!")


def display_scores(count, raw_data):
    # print the scores to the screen in the expected format
	print ("There are {} scores. Here are the top 3!".format(count))
    # print out the scores in the required format
	print (raw_data)
pass


# Setup Pins
def setup():
	global LED_PULSE
	global BUZZER_PULSE
	GPIO.setwarnings(False) #sometimes when using the pins we're trying to use are already in function, we can get errors. this tells the program to 
	# ignore the warnings and procede with the code
	GPIO.setmode(GPIO.BOARD) # setting to boar numbering system
	GPIO.setup(11,GPIO.OUT) 
	GPIO.setup(13,GPIO.OUT)
	GPIO.setup(15,GPIO.OUT)

	GPIO.setup(32,GPIO.OUT)
	GPIO.output(32,GPIO.HIGH)
	sleep(0.1)
	GPIO.output(32,GPIO.LOW)

	LED_PULSE = GPIO.PWM(32,100)
	LED_PULSE.start(0)

	GPIO.setup(33,GPIO.OUT)
	BUZZER_PULSE=GPIO.PWM(33,100)
	BUZZER_PULSE.start(0)

	GPIO.setup(16,GPIO.IN,pull_up_down=GPIO.PUD_UP)
	GPIO.setup(18,GPIO.IN,pull_up_down=GPIO.PUD_UP)

	GPIO.add_event_detect(btn_submit,GPIO.FALLING,callback=btn_guess_pressed,bouncetime=1000)

	GPIO.add_event_detect(btn_increase,GPIO.FALLING,callback=btn_increase_pressed, bouncetime = 1000)
    # Setup board mode
    # Setup regular GPIO
    # Setup PWM channels
    # Setup debouncing and callbacks
pass


# Load high scores
def fetch_scores():
    # get however many scores there are
	
	scorenum = eeprom.read_byte(0)
	scorecount = scorenum
	if scorenum>3:
		scorecount=3
	score_count = ''
	for x in range(1,scorecount+1):
		name =eeprom.read_block(x,4)
		score_count += "Name: " + chr(name[0])+chr(name[1])+chr(name[2])+ " took " + str(name[3]) + " guesses. \n"
    # convert the codes back to ascii
    
    # return back the results
	return score_count, score_count


# Save high scores
def save_scores(data):
    # fetch scores
    # include new score
    # sort
    # update total amount of scores
    # write new scores
	scorenum =  eeprom.read_byte(0)
	scores = [[0]*4]*scorenum
	for p in range(1,scorenum+1):
		name = eeprom.read_block(p,4)
		scores[p-1] = name
	scores.append(data)
	scores.sort(key = lambda x: x[3])
	eeprom.write_byte(0,scorenum+1)

	i=1
	for x in scores:
		eeprom.write_block(i,x)
		i+=1
pass

# Generate guess number
def generate_number():
    return random.randint(1, pow(2, 3)-1)


# Increase button pressed
def btn_increase_pressed(channel):

# Increase the value shown on the LEDs
    # You can choose to have a global variable store the user's current guess, 
    # or just pull the value off the LEDs when a user makes a guess
	global LED_NUMBER
	LED_NUMBER +=1
	if LED_NUMBER>7:
		print ("End of sequence")
		LED_NUMBER = 0
	if LED_NUMBER==1:
		GPIO.output(11,GPIO.LOW)
		GPIO.output(13,GPIO.LOW)
		GPIO.output(15,GPIO.HIGH)
	elif LED_NUMBER==2:
		GPIO.output(11,GPIO.LOW)
		GPIO.output(13,GPIO.HIGH)
		GPIO.output(15,GPIO.LOW)
	elif LED_NUMBER==3:
		GPIO.output(11,GPIO.LOW)
		GPIO.output(13,GPIO.HIGH)
		GPIO.output(15,GPIO.HIGH)
	elif LED_NUMBER == 4:
		GPIO.output(11,GPIO.HIGH)
		GPIO.output(13,GPIO.LOW)
		GPIO.output(15,GPIO.LOW)
	elif LED_NUMBER ==5:
		GPIO.output(11,GPIO.HIGH)
		GPIO.output(13,GPIO.LOW)
		GPIO.output(15,GPIO.HIGH)
	elif LED_NUMBER==6:
		GPIO.output(11,GPIO.HIGH)
		GPIO.output(13,GPIO.HIGH)
		GPIO.output(15,GPIO.LOW)
	elif LED_NUMBER == 7:
		GPIO.output(11,GPIO.HIGH)
		GPIO.output(13,GPIO.HIGH)
		GPIO.output(15,GPIO.HIGH)
	else:
		GPIO.output(11,GPIO.LOW)
		GPIO.output(13,GPIO.LOW)
		GPIO.output(15,GPIO.LOW)

pass


def restart_game():
	global LED_NUMBER
	global BUZZER_PULSE
	global LED_PULSE
	global number_of_guesses

	LED_NUMBER=0
	GPIO.output(11,GPIO.LOW)
	GPIO.output(13,GPIO.LOW)
	GPIO.output(15,GPIO.LOW)

	LED_PULSE.start(0)
	BUZZER_PULSE.start(0)
	number_of_guesses = 0
pass


# Guess button
def btn_guess_pressed(channel):
    # If they've pressed and held the button, clear up the GPIO and take them back to the menu screen
    # Compare the actual value with the user value displayed on the LEDs
    # Change the PWM LED
    # if it's close enough, adjust the buzzer
    # if it's an exact guess:
    # - Disable LEDs and Buzzer
    # - tell the user and prompt them for a name
    # - fetch all the scores
    # - add the new score
    # - sort the scores
    # - Store the scores back to the EEPROM, being sure to update the score count
	global LED_NUMBER
	global end_of_game
	global number_of_guesses
	global value

	start_time = time.time()
	while GPIO.input(btn_submit)==0:
		sleep(0.1)
	buttonTime = time.time()-start_time
	if buttonTime>=3:
		print ("####Game will restart####")
		restart_game()
		end_of_game = True
	if (end_of_game == False):
		if (LED_NUMBER != value):
			print ("try again")
			trigger_buzzer()
			accuracy_leds()
		elif LED_NUMBER == value:
			print ("you win")
			turn_off_LED()
			turn_off_buzzer()

			name_length = 0
			while name_length !=3:
				name = input("Enter a name(3 characters)\n")
				name_length = len(name)
				if name_length !=3:
					print ("PLease try again")

			letter1 = ord(name[0])
			letter2 = ord(name[1])
			letter3 = ord(name[2])
			player_info = [letter1,letter2,letter3,number_of_guesses]
			save_scores(player_info)
			restart_game()
			end_of_game = True

pass


def turn_off_buzzer():
	BUZZER_PULSE.stop()
pass

def turn_off_LED():
	LED_PULSE.stop()



# LED Brightness
def accuracy_leds():
    # Set the brightness of the LED based on how close the guess is to the answer
    # - The % brightness should be directly proportional to the % "closeness"
    # - For example if the answer is 6 and a user guesses 4, the brightness should be at 4/6*100 = 66%
    # - If they guessed 7, the brightness would be at ((8-7)/(8-6)*100 = 50%
	global value
	global LED_NUMBER
	global LED_PULSE
	#print (LED_PULSE)
	print (LED_NUMBER)
	print (value)
	if (value<LED_NUMBER):
		intensity = (value/LED_NUMBER)*100
		#print (intensity)
		LED_PULSE.ChangeDutyCycle(intensity)
	elif(value>LED_NUMBER):
		intensity = ((8-value)/(8-LED_NUMBER))*100
		#print (intensity)
		LED_PULSE.ChangeDutyCycle(intensity)
	

pass

# Sound Buzzer
def trigger_buzzer():
    # The buzzer operates differently from the LED
    # While we want the brightness of the LED to change(duty cycle), we want the frequency of the buzzer to change
    # The buzzer duty cycle should be left at 50%
    # If the user is off by an absolute value of 3, the buzzer should sound once every second
    # If the user is off by an absolute value of 2, the buzzer should sound twice every second
    # If the user is off by an absolute value of 1, the buzzer should sound 4 times a second
	global value
	global LED_NUMBER
	global BUZZER_PULSE
	off_by = abs(value-LED_NUMBER)
	BUZZER_PULSE.ChangeDutyCycle(50)
	if off_by == 1:
		BUZZER_PULSE.ChangeFrequency(4)
#		print (off_by)

	elif off_by ==2:
		BUZZER_PULSE.ChangeFrequency(2)
#		print (off_by)
	elif off_by ==3:
		BUZZER_PULSE.ChangeFrequency(1)
#		print (off_by)

	pass
	


if __name__ == "__main__":
    try:
        # Call setup function
        setup()
        welcome()
        while True:
            menu()
            pass
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()
