# Name Angela Amani
# Date : 26/02/2026
# Program to make an alarm system


from machine import Pin, PWM
import utime

# -----------------------
# BUZZER
# -----------------------
buzzer = PWM(Pin(15))
buzzer.duty_u16(0)

def play_wrong_tone():
    buzzer.freq(2000)
    buzzer.duty_u16(40000)
    utime.sleep(3)
    buzzer.duty_u16(0)

# -----------------------
# LCD
# -----------------------
RS = Pin(0, Pin.OUT)
E  = Pin(1, Pin.OUT)
D4 = Pin(2, Pin.OUT)
D5 = Pin(3, Pin.OUT)
D6 = Pin(4, Pin.OUT)
D7 = Pin(5, Pin.OUT)

def pulse_enable():
    E.low()
    utime.sleep_us(1)
    E.high()
    utime.sleep_us(1)
    E.low()
    utime.sleep_us(100)

def send_nibble(n):
    D4.value((n >> 0) & 1)
    D5.value((n >> 1) & 1)
    D6.value((n >> 2) & 1)
    D7.value((n >> 3) & 1)
    pulse_enable()

def send_byte(b, is_data):
    RS.value(is_data)
    send_nibble(b >> 4)
    send_nibble(b & 0x0F)
    utime.sleep_us(50)

def lcd_cmd(c):
    send_byte(c, False)

def lcd_data(d):
    send_byte(d, True)

def lcd_init():
    utime.sleep_ms(20)
    lcd_cmd(0x33)
    lcd_cmd(0x32)
    lcd_cmd(0x28)
    lcd_cmd(0x0C)
    lcd_cmd(0x06)
    lcd_clear()

def lcd_clear():
    lcd_cmd(0x01)
    utime.sleep_ms(2)

def lcd_set_cursor(col, row):
    row_offsets = [0x00, 0x40]
    lcd_cmd(0x80 | (col + row_offsets[row]))

def lcd_print(text):
    for char in text:
        lcd_data(ord(char))

# -----------------------
# KEYPAD (4x4)
# -----------------------
ROWS = [Pin(6, Pin.OUT), Pin(7, Pin.OUT), Pin(8, Pin.OUT), Pin(9, Pin.OUT)]
COLS = [Pin(10, Pin.IN, Pin.PULL_DOWN), Pin(11, Pin.IN, Pin.PULL_DOWN),
        Pin(12, Pin.IN, Pin.PULL_DOWN), Pin(13, Pin.IN, Pin.PULL_DOWN)]

KEY_MAP = [['1','2','3','A'],
           ['4','5','6','B'],
           ['7','8','9','C'],
           ['*','0','#','D']]

def scan_keypad():
    for i, row in enumerate(ROWS):
        row.high()
        for j, col in enumerate(COLS):
            if col.value() == 1:
                while col.value() == 1:  # wait for release
                    utime.sleep_ms(10)
                row.low()
                return KEY_MAP[i][j]
        row.low()
    return None

# -----------------------
# PASSWORD
# -----------------------
correct_password = "123456"
entered_password = ""

# -----------------------
# MAIN LOOP
# -----------------------
lcd_init()
lcd_print("Enter Password:")

while True:
    key = scan_keypad()

    if key:
        # Only accept up to 6 digits
        if len(entered_password) < 6:
            entered_password += key
            lcd_set_cursor(len(entered_password)-1, 1)
            lcd_data(ord("*"))  # hide key
            utime.sleep(0.2)  # debounce

        # Automatically check after 6 keys
        if len(entered_password) == 6:
            if entered_password == correct_password:
                lcd_clear()
                lcd_print("ACCESS GRANTED")
            else:
                lcd_clear()
                lcd_print("WRONG PASSWORD")
                play_wrong_tone()

            utime.sleep(2)
            entered_password = ""
            lcd_clear()
            lcd_print("Enter Password:")