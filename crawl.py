from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.common.exceptions import ElementNotInteractableException, StaleElementReferenceException
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions() 

options.add_argument('--user-data-dir=C:/Users/PM-COMPUTER/AppData/Local/Google/Chrome/User Data')
# options.add_argument('--profile-directory=Profile 1')

driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)

question_class_name = "q-box qu-display--block qu-cursor--pointer qu-hover--textDecoration--underline Link___StyledBox-t2xg9c-0 roKEj"
div_answer_amount = "q-text qu-dynamicFontSize--regular qu-medium qu-color--gray_dark qu-passColorToLinks"
div_answer_box = "CssComponent-sc-1oskqb9-0 cXjXFI"
div_answer_text = "q-text"
div_answer_nodelist_index = 7 #Where answer text (qtext) is at in the answer box
button_comment = "q-click-wrapper ClickWrapper___StyledClickWrapperBox-zoqi4f-0 bIwtPb base___StyledClickWrapper-lx6eke-1 laIUvT   qu-active--bg--darken qu-active--textDecoration--none qu-borderRadius--pill qu-alignItems--center qu-justifyContent--center qu-whiteSpace--nowrap qu-userSelect--none qu-display--inline-flex qu-tapHighlight--white qu-textAlign--center qu-cursor--pointer qu-hover--bg--darken qu-hover--textDecoration--none"
div_sub_comment_button = "q-relative qu-pb--small"

xpath_comment_section = "//*[@id=\"mainContent\"]/div[2]/div[5]/div/div/div/div/div/div/div/div[2]/div/div/div[2]"

## RECURSE 3 lEVELS TO ACCESS 
    #Start from "CssComponent-sc-1oskqb9-0 cXjXFI"
    #Go through 3 nested div we'll see
        #Parent main comment
        #div of all sub comment which is wrapper of q-relative qu-pl--medium qu-pt--small qu-pb--small class =>
        #Click above divs will got "CssComponent-sc-1oskqb9-0 cXjXFI"
        #goto step 1 again (recurse)

# Data structure

# top level
# [
# div 1
#     cXjXFI
#         q-box
#             q-box
#                 q-box qu-borderTop qu-px--medium qu-pt--medium qu-bg--gray_ultralight 
#                     q-relative qu-pb--small (Parent text comment)
#                     q-relative qu-pl--medium qu-pt--small qu-pb--small (Sub cmd tree)
#                     [
#                         div 1
#                             (RECURSE) cXjXFI
#                         div 2
#                             (RECURSE) cXjXFI
#                     ]
# div 2
#     cXjXFI
#     . . .
# ]


div_subcomment_class = "CssComponent-sc-1oskqb9-0 cXjXFI"


def define_js_function():
    driver.execute_script(open("./js/util.js").read())

def click_comment_btn():
    driver.execute_script(open("./js/click_comment_btn.js").read())
    driver.execute_script("window.click_comment_btn()")

def click_more_text(max_iter=1):
    more_text = "q-text qu-cursor--pointer qt_read_more qu-color--blue_dark qu-fontFamily--sans qu-hover--textDecoration--underline"
    mores = driver.execute_script("return document.getElementsByClassName(\"" + more_text +"\")")
    for i in range(max_iter):
        for k,more in enumerate(mores):
                # try: more.click()
                # except (ElementNotInteractableException, StaleElementReferenceException, Exception): continue
            driver.execute_script("arguments[0].click();", more)

def click_more_comment(max_iter=None):
    more_comment = "q-click-wrapper qu-active--textDecoration--none qu-focus--textDecoration--none ClickWrapper___StyledClickWrapperBox-zoqi4f-0 bIwtPb base___StyledClickWrapper-lx6eke-1 fURggN   qu-borderRadius--pill qu-alignItems--center qu-justifyContent--center qu-whiteSpace--nowrap qu-userSelect--none qu-display--flex qu-bg--gray_ultralight qu-tapHighlight--white qu-textAlign--center qu-cursor--pointer qu-hover--textDecoration--none"
    load_more = "q-text qu-dynamicFontSize--small qu-borderAll qu-px--small qu-py--tiny qu-mb--tiny qu-borderRadius--small qu-color--gray qu-bg--darken qu-cursor--pointer qu-hover--borderColor--gray_dark qu-truncateLines--1"
    max_patient = 2
    count_stable = 0
    old_length = None
    count = 0
    while (True):
        load_more_divs = driver.execute_script("return document.getElementsByClassName(\"" + load_more +"\")")
        more_comment_divs = driver.execute_script("return document.getElementsByClassName(\"" + more_comment +"\")")
        if old_length is not None:
            if old_length == len(load_more_divs): count_stable += 1
        if count_stable == max_patient or count == max_iter: break
        old_length = len(load_more_divs)
        for divs in load_more_divs:
            try: divs.click()
            except (ElementNotInteractableException, StaleElementReferenceException, Exception): continue
        time.sleep(3)
        for divs in more_comment_divs:
            try: divs.click()
            except (ElementNotInteractableException, StaleElementReferenceException, Exception): continue
        count += 1 
        print("more : iter :",count_stable)

def extract_answer_div():
    define_js_function()
    driver.execute_script(open("./js/extract_question.js").read())
    return driver.execute_script("return get_all_answer_div()")


def scroll(max_iter = None):
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    count = 0
    while(match==False):
        lastCount = lenOfPage
        time.sleep(3)
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage:
            match=True
        if max_iter is not None:
            if max_iter == count: break
        count += 1
    return

def question_scrapper(keyword,max_iter = None):
    driver.get("https://www.quora.com/search?q="+keyword)
    scroll(max_iter)
    element = driver.execute_script("return document.getElementsByClassName(\"" + question_class_name + "\"" + ")")
    result = []
    for e in element:
        result.append({"question":e.text, "url":e.get_attribute('href')})
    return result

def getChildByClass(webEl, className):
    return driver.execute_script("return ")
def toggle_main_comment():
    driver.execute_script("document.getElementsByClassName(\"q-click-wrapper ClickWrapper___StyledClickWrapperBox-zoqi4f-0 bIwtPb base___StyledClickWrapper-lx6eke-1 laIUvT   qu-active--bg--darken qu-active--textDecoration--none qu-borderRadius--pill qu-alignItems--center qu-justifyContent--center qu-whiteSpace--nowrap qu-userSelect--none qu-display--inline-flex qu-tapHighlight--white qu-textAlign--center qu-cursor--pointer qu-hover--bg--darken qu-hover--textDecoration--none\")[5].click()")

define_js_function()

result = question_scrapper("covid",1)

class Node():
    def __init__(self, text):
        self.text = text
        self.sub_comment = []
    def append_child(self,node):
        self.sub_comment.append(node)

#Extract from q-text

def build_tree(element):
    element
    node = Node()

#arg : the list div element of each section of comment
# Class CssComponent-sc-1oskqb9-0 cXjXFI
def get_qbox(main_el): #extract only current text {no child text}
    lev_3 = main_el.find_element_by_xpath("./*")
    print(lev_3.get_attribute("class"))
    lev_3 = lev_3.find_element_by_xpath("./*")
    print(lev_3.get_attribute("class"))
    lev_3 = lev_3.find_element_by_xpath("./*")
    print(lev_3.get_attribute("class"))
    lev_3 = lev_3.find_element_by_xpath("./*")
    print(lev_3.get_attribute("class"))
    lev_3 = lev_3.find_element_by_xpath("./*")
    print(lev_3.get_attribute("class"))
    lev_3 = lev_3.find_element_by_xpath("./*")
    print(lev_3.get_attribute("class"))
    lev_3 = lev_3.find_element_by_xpath("./*")
    print(lev_3.get_attribute("class"))
    lev_3 = lev_3.find_element_by_xpath("./*")
    print(lev_3.get_attribute("class"))
    lev_3 = lev_3.find_elements_by_class_name("qu-flex--auto")[0]
    lev_3 = lev_3.find_elements_by_class_name("q-box")[9].text

    return lev_3

    



for question in result:
    driver.get(question["url"])
    scroll(1)
    time.sleep(3)
    click_comment_btn()
    time.sleep(3)
    click_more_comment(max_iter=1)
    # click_comment_btn()
    click_more_text(1)
    toggle_main_comment()
    answer_elements = extract_answer_div()
    for answer_e,idx in answer_elements:
        # print(answer_e,idx)
        
        main_xpath = "//*[@id=\"mainContent\"]/div[2]/div["+str(idx+1)+"]/div/div/div/div/div/div/div"
        main_answer_el = driver.find_element_by_xpath(main_xpath)
        answer_xpath = "//*[@id=\"mainContent\"]/div[2]/div["+str(idx+1)+"]/div/div/div/div/div/div/div/div[1]"
        comment_section_xpath = "//*[@id=\"mainContent\"]/div[2]/div["+str(idx+1)+"]/div/div/div/div/div/div/div/div[2]/div/div/div[2]"
        answer_el = driver.find_element_by_xpath(answer_xpath)
        comment_section_el = driver.find_element_by_xpath(comment_section_xpath)

        comment_list = comment_section_el.find_elements_by_xpath("./*")
        for c in comment_list:
            if c.text == "View more comments": continue
            print(get_qbox(c))


        # //*[@id="mainContent"]/div[2]/div[9]
    break

    

print(result)