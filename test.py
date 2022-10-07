from operator import truediv
from Driver import ChromeDriver, PageSource, precheck, ChromeDriverOption
import Driver
from room import Room, Roomate, Agency, Lease, Uptown

opt = ChromeDriverOption()
browser = ChromeDriver(opt=opt)
browser.open('https://www.ziroom.com/z/r0/?p=g2&qwd=%E5%B7%A5%E4%BD%93&cp=2000TO5000&isOpen=1')
tab = browser.find_tab_by_name('default')

def has_next_page():
    return len(tab.find_elements('//a[@class="next"]',wait=5))>0
def click_to_next_page():
    if has_next_page():
        tab.find_elements('//a[@class="next"]')[0].click()
def deal_with_room_link(link):
    try:
        room_tab = browser.openNewTab(link)
        room =  Room()
        room.link=link
        
    finally:
        room_tab.close()



room_links=[]
last_page=False
page_ind = 0
while True:
    page_room_links = tab.source().sp().select('div.item > div.pic-box > a')
    
    for room in page_room_links:
        room_links.append(room)
    
    if not has_next_page():
       break
    else:
        click_to_next_page()
        page_ind+=1
        
for room in room_links:
    deal_with_room_link(room.attrs['href'])

pass