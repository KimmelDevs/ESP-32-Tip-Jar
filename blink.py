from machine import I2C, Pin
from i2c_lcd import I2cLcd
import time
import network
import ujson
from umqtt.simple import MQTTClient

# ── Wi-Fi config ───────────────────────────────────────────
WIFI_SSID     = "GFiber_39E55"
WIFI_PASSWORD = "28673359"

# ── MQTT config ───────────────────────────────────────────────
MQTT_BROKER   = "broker.hivemq.com"   # free public broker (no auth)
MQTT_PORT     = 1883
MQTT_CLIENT   = "my_esp32"
MQTT_TOPIC    = b"bubble/tip"           # Android publishes here

# ── LCD setup (your original code, unchanged) ─────────────────
i2c = I2C(0, sda=Pin(22), scl=Pin(21), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)
lcd.backlight_on()
lcd.clear()
lcd.move_to(0, 0)
lcd.putstr("Welcome to our Humble Place!")
lcd.move_to(0, 1)
lcd.putstr("Please Leave a tip!")

# ── Helpers ───────────────────────────────────────────────────
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr("Connecting WiFi")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        timeout = 15
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
    if wlan.isconnected():
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr("WiFi OK!")
        time.sleep(1)
    else:
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr("WiFi FAILED")
        time.sleep(2)

def show_thank_you(amount):
    """Show animated thank-you message for `amount` pesos."""
    messages = [
        ("Salamat!", f"Tip: P{amount}"),
        ("Thank You!", "Maraming Salamat"),
        ("WELCOME TO JOLLIBEE!", "hehehehe!"),   # back to default
    ]
    for top, bot in messages:
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr(top[:16])
        lcd.move_to(0, 1)
        lcd.putstr(bot[:16])
        time.sleep(2)

def on_message(topic, msg):
    """Called whenever a message arrives on MQTT_TOPIC."""
    try:
        payload = ujson.loads(msg)
        amount  = payload.get("amount", 0)
        print(f"[MQTT] Tip received: P{amount}")
        show_thank_you(amount)
    except Exception as e:
        print("[MQTT] Bad payload:", e)

# ── Main ──────────────────────────────────────────────────────
connect_wifi()

client = MQTTClient(MQTT_CLIENT, MQTT_BROKER, port=MQTT_PORT)
client.set_callback(on_message)
client.connect()
client.subscribe(MQTT_TOPIC)

lcd.clear()
lcd.move_to(0, 0)
lcd.putstr("Hi WELCOME TO ")
lcd.move_to(0, 1)
lcd.putstr("JOLLIBEE!")

print("[MQTT] Subscribed, waiting for tips…")

while True:
    client.check_msg()   # non-blocking check
    time.sleep_ms(200)