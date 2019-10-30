


def click_couse(course_name,*args):
    for i in course_name:
        if i.text in args:
            i.click()
