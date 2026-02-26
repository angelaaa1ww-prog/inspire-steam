# Name Angela Amani
# Date : 26/02/2026
# Program to make an alarm system


from machine import Pin
import utime

# ---------------- LCD Setup ----------------
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
    lcd_cmd(0x32)   # 4-bit mode
    lcd_cmd(0x28)   # 2 lines, 5x8 font
    lcd_cmd(0x0C)   # Display ON, cursor OFF
    lcd_cmd(0x06)   # Increment cursor
    lcd_cmd(0x01)   # Clear display
    utime.sleep_ms(2)

def lcd_clear():
    lcd_cmd(0x01)
    utime.sleep_ms(2)

def lcd_print(text):
    for char in text:
        lcd_data(ord(char))

def lcd_set_cursor(col, row):
    row_offsets = [0x00, 0x40]
    lcd_cmd(0x80 | (col + row_offsets[row]))

# ---------------- Keypad Setup ----------------
rows = [Pin(6, Pin.OUT), Pin(7, Pin.OUT), Pin(8, Pin.OUT), Pin(9, Pin.OUT)]
cols = [Pin(10, Pin.IN, Pin.PULL_DOWN), Pin(11, Pin.IN, Pin.PULL_DOWN),
        Pin(12, Pin.IN, Pin.PULL_DOWN), Pin(13, Pin.IN, Pin.PULL_DOWN)]

keys = [
    ["1","2","3","A"],
    ["4","5","6","B"],
    ["7","8","9","C"],
    ["*","0","#","D"]
]

def get_key():
    for i, row in enumerate(rows):
        row.high()
        for j, col in enumerate(cols):
            if col.value() == 1:
                utime.sleep(0.2)  # debounce
                row.low()
                return keys[i][j]
        row.low()
    return None

# ---------------- Buzzer ----------------
buzzer = Pin(15, Pin.OUT)
def beep(duration=3):  # 3 seconds beep
    buzzer.high()
    utime.sleep(duration)
    buzzer.low()

# ---------------- Password ----------------
stored_password = "123456"  # default 6-character password

# ---------------- Main Program ----------------
lcd_init()

while True:
    entered = ""
    lcd_clear()
    lcd_print("Enter Password:")
    lcd_set_cursor(0, 1)

    while len(entered) < 6:
        key = get_key()
        if key:
            entered += key
            lcd_data(ord("*"))

    utime.sleep(0.2)

    if entered == stored_password:
        lcd_clear()
        lcd_print("ACCESS GRANTED")
        utime.sleep(2)
    else:
        lcd_clear()
        lcd_print("WRONG PASSWORD")
        beep()  # <-- Audible beep for 3 seconds
        utime.sleep(2)