from Bot import Bot
from time import sleep
from numpy.random import randint

import Creds as C

def likeOrNot(probability=0.5):
    #return a bool according to the provided probability
    return randint(100) <= 100*probability

if __name__ == "__main__":
    bot = Bot()
    bot.login(C.f_username, C.f_password)
    totalLikes = 0
    totalReloads = 0
    while True:
        print("total reload: ",totalReloads)
        print("total Likes: ", totalLikes)
        sleep(2)
        bot.reload()
        totalReloads += 1
        passedButtons = []
        for _ in range(5):

            #list all the like buttons
            # except the buttons that are already processed
            btns = [
                x for x in bot.driver.find_elements_by_link_text('Like')
                if x.get_attribute('style') != 'color: rgb(32, 120, 244);'
                and x not in passedButtons]
            print("posts found: ",len(btns))

            for btn in btns:
                sleep(2)
                #Selenium can't click a button if it's not in view
                bot.driver.execute_script('arguments[0].scrollIntoView();',
                                           btn)
                sleep(2)
                if likeOrNot(0.7):
                    btn.click()
                    totalLikes += 1
                    print("liked")
                else:
                    print("skipped")
                passedButtons.append(btn)

    bot.quit()
