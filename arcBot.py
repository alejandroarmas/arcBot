from collections import namedtuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located


AvailableSlot = namedtuple("AvailableSlot", ["workoutInterval", "actionJavascript"])


class ArcBot():
   
    def __init__(self, username, password):

        self.arc_booking_url = "https://rec.ucdavis.edu/booking/c5a89e9a-e24b-4634-8516-6317ffd2fdd4"
        self.driver = webdriver.Firefox()
        self.wait = WebDriverWait(self.driver, 10)

        self.__kerebos_username = username
        self.__kerebos_password = password
        self.available_reservation_dates = {} 
        self.reserved_slots = {}
    

    def login_kerebos(self):


        self.driver.maximize_window()
        self.driver.get(self.arc_booking_url)
        print(f"Accessing: {self.driver.title}")

        # Gives us the login link form and access it.
        # Wait until atleast 10 seconds for element to be clickable
        login_route = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-lg.btn-block.btn-social.btn-linkedin")))
        login_route.click()

        username_input = self.driver.find_element_by_css_selector("input[name='username']")
        password_input = self.driver.find_element_by_css_selector("input[name='password']")
        username_input.send_keys(self.__kerebos_username)
        password_input.send_keys(self.__kerebos_password)
        login_button = self.driver.find_element_by_id("submit")
        login_button.click()
        print(f"Logged in successfully as: {self.__kerebos_username}")


    def obtain_available_arc_sessions(self):
        """
        Scrapes booking webpage for all the available time slots inserts them into 
            self.available_reservation_dates
        """

        self.driver.get(self.arc_booking_url)
        self.driver.implicitly_wait(5) # seconds
        gym_reservation_days = self.driver.find_elements_by_css_selector(".single-date-select-button.single-date-select-one-click")
        self.driver.implicitly_wait(1)

        for date in gym_reservation_days:
            date.click()
            day = date.get_attribute("data-day")
            month = date.get_attribute("data-month")
            year = date.get_attribute("data-year")

            slots_to_book_eachday = self.driver.find_elements_by_class_name("booking-slot-item")
            
            for slot in slots_to_book_eachday:
                slot_interval = slot.find_element_by_tag_name("strong").text
                number_of_open_spaces = int(slot.find_element_by_xpath('//*[@id="divBookingSlots"]/div/div/span').text.split(" ")[0])
                book_now_button = slot.find_element(By.TAG_NAME, "button")
                javascriptFunction = book_now_button.get_attribute("onclick")
                can_book = book_now_button.text == "BOOK NOW" and number_of_open_spaces > 0
                already_booked = book_now_button.text == "  Booked"

                message = f"Checking {month}-{day}-{year} at {slot_interval}.\n"

                if can_book:
                    self.available_reservation_dates.setdefault(f"{month}-{day}-{year}", []).append(AvailableSlot(workoutInterval=slot_interval, actionJavascript=javascriptFunction))
                    message += "It is available."
                elif already_booked:
                    self.reserved_slots.setdefault(f"{month}-{day}-{year}", []).append(slot_interval)
                    message += "You already booked it."
                else:
                    message += "It is not available."
                print(message)


    def book_times(self):
        """
        Looks into available_reservation_dates and reserves the earliest time slot.
        """
        KEY = 0
        VALUE = 1
        self.driver.get(self.arc_booking_url)
        self.driver.implicitly_wait(5) # seconds
        gym_reservation_days = self.driver.find_elements_by_css_selector(".single-date-select-button.single-date-select-one-click")

        for reservation_day in self.available_reservation_dates.items():
            date = reservation_day[KEY]
            available_slots = reservation_day[VALUE]

            earliest_slot = available_slots[0]
            workout_interval = earliest_slot.workoutInterval
            jsScript = earliest_slot.actionJavascript
            
            self.driver.execute_script(jsScript)
            self.reserved_slots[date] = workout_interval
            print(f"Successfully reserved a slot for {workout_interval} on {date}")

    
    def __del__(self):
        self.driver.close()

        


