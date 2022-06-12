import time
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(executable_path="./chromedriver.exe")

try:
    def login(username="standard_user", password="secret_sauce"):
        driver.get("https://www.saucedemo.com/")

        login_username_input = driver.find_element(By.ID, "user-name")
        login_username_input.click()
        login_username_input.send_keys(username)

        login_password_input = driver.find_element(By.ID, "password")
        login_password_input.click()
        login_password_input.send_keys(password)

        login_button = driver.find_element(By.ID, "login-button")
        login_button.click()
        return driver

    def test_correct_login_and_password():
        driver = login("standard_user", "secret_sauce")
        next_url = driver.current_url

        assert next_url == "https://www.saucedemo.com/inventory.html", "URL is incorrect"
        time.sleep(5)

    def test_incorrect_password():
        driver = login(password="incorrect")

        error_message = driver.find_element(By.XPATH, "//h3[text()='Epic sadface: Username and password do not match any user in this service']")
        assert error_message.text == "Epic sadface: Username and password do not match any user in this service", "Incprrect error text"
        time.sleep(5)


    def test_incorrect_login():
        driver = login("incorrect", "secret_sauce")

        error_message = driver.find_element(By.XPATH, "//h3[text()='Epic sadface: Username and password do not match any user in this service']")
        assert error_message.text == "Epic sadface: Username and password do not match any user in this service", "Incprrect error text"
        time.sleep(5)

    def test_items_quantity():
        driver = login()

        items = driver.find_elements(By.CLASS_NAME, "inventory_item")
        assert len(items) == 6, "6 items should be displayed"
        time.sleep(5)

    def test_add_to_cart():
        driver = login()
        item_add_to_cart_button = driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")
        item_add_to_cart_button.click()

        #Test that remove button shows up
        remove_button = driver.find_element(By.ID, "remove-sauce-labs-backpack")
        assert remove_button.text == "REMOVE", "Remove button is not shows up"

        #Test that cart counter is incrementing
        cart_counter = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
        assert cart_counter.text == "1", "Incorrect value for cart counter"

        return driver


    def test_cart_items():
        driver = test_add_to_cart()
        cart_link = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        cart_link.click()

        next_url = driver.current_url

        #Test that user redirects to cart page
        assert next_url == "https://www.saucedemo.com/cart.html", "URL is incorrect"

        #Test that one element added to cart
        cart_list = driver.find_elements(By.CLASS_NAME, "cart_item")
        assert len(cart_list) == 1, "More that 1 item in cart"
        time.sleep(5)


    test_correct_login_and_password()
    test_incorrect_password()
    test_incorrect_login()
    test_items_quantity()
    test_add_to_cart()
    test_cart_items()
    test_cart_items()






except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()