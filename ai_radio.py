import os
import openai

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions

import time

RADIO_PROMPT = "You are a ai DJ bot that picks the best musics for a radio station. The current song's name, artist will be given AFTER this prompt. You will be asked for the next track which will be played. You should pick it to be harmonious and compatible with previous tracks. Change the genre slowly, IF YOU WILL. Try not to play a song couple times. Only answer with the next song's name and its artist, NEVER ADD ANY COMMENTS! LIKE THIS EXAMPLE: 'Eye of the tiger - Survivor' Note that the current song will be given after this. Don't try to choose the next song right now."

SPOTIFY_BASE_URL = "https://open.spotify.com/"
SPOTIFY_LOGIN_URL = "https://accounts.spotify.com/en/login"









## PRIVATE VARIABLES

openai.api_key = "API_KEY_HERE"
SPOTIFY_USERNAME = "USERNAME_HERE"
SPOTIFY_PASSWORD = "PASSWORD_HERE"

current_song = input("First song: ")

messages=[
    {"role": "system", "content": RADIO_PROMPT},
]

def update_chat(messages, role, content):
  messages.append({"role": role, "content": content})
  return messages

def get_chatgpt_response(messages):
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature=0.2,
    messages=messages
  )
  return response.choices[0].message.content

class Spotify:
  def __init__(self, username, password):
    driver_path = "DRIVER_PATH_HERE"
    self.browser = webdriver.Chrome(executable_path=driver_path)

    self.browser.get(SPOTIFY_LOGIN_URL)

    usernameBox = self.browser.find_element(By.XPATH, '//*[@id="login-username"]')
    usernameBox.send_keys(username)

    passwordBox = self.browser.find_element(By.XPATH, '//*[@id="login-password"]')
    passwordBox.send_keys(password)
    passwordBox.send_keys(Keys.ENTER)

    time.sleep(1)

    self.browser.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div/button[2]').click()

    time.sleep(1)

  def get_second(self, time_str):
    mm, ss = time_str.split(':')
    return int(mm) * 60 + int(ss)

  def open_song(self, song_data):
    self.browser.get(f"{SPOTIFY_BASE_URL}search/{song_data}")

    time.sleep(3)
    
    self.browser.find_element(By.XPATH, '//*[@id="searchPage"]/div/div/section[2]/div[2]/div/div/div/div[2]/div[1]/div/div[1]/div[1]/img').click()

    time.sleep(3)

    while True:
      current_time = self.get_second(self.browser.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/footer/div[1]/div[2]/div/div[2]/div[1]').text)
      total_time = self.get_second(self.browser.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[2]/footer/div[1]/div[2]/div/div[2]/div[3]').text)
 
      if current_time >= total_time - 5 :
        break
      time.sleep(0.5)

spotify = Spotify(SPOTIFY_USERNAME, SPOTIFY_PASSWORD)

while True:
  print("Current song: " + current_song)

  spotify.open_song(current_song)

  messages = update_chat(messages, "user", current_song)
  model_response = get_chatgpt_response(messages)
  print("AI choosed: " + model_response)

  current_song = model_response
  messages = update_chat(messages, "assistant", model_response)
