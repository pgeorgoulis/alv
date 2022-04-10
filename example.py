'''
Got this today during an interview. Came up with an O(N*logN) solution.
Wondering whether there is an O(N) solution available...

Overview: Join individual schedules into one list intervals --> Sort it by intervals' starting time --> M
'''

import unittest

# O(N * logN) + O(2 * N) time
# O(3 * N) space

def find_available_times(schedules):
    ret = []

    intervals = [list(x) for personal in schedules for x in personal]

    intervals.sort(key=lambda x: x[0], reverse=True)  # O(N * logN)

    tmp = []

    while intervals:
        pair = intervals.pop()

        if tmp and tmp[-1][1] >= pair[0]:
            tmp[-1][1] = max(pair[1], tmp[-1][1])

        else:
            tmp.append(pair)

    for i in range(len(tmp) - 1):
        ret.append([tmp[i][1], tmp[i + 1][0]])

    return ret


class CalendarTests(unittest.TestCase):

    def test_find_available_times(self):
        p1_meetings = [
            ( 845,  900),
            (1230, 1300),
            (1300, 1500),
        ]

        p2_meetings = [
            ( 0,    844),
            ( 845, 1200),
            (1515, 1546),
            (1600, 2400),
        ]

        p3_meetings = [
            ( 845, 915),
            (1235, 1245),
            (1515, 1545),
        ]

        schedules = [p1_meetings, p2_meetings, p3_meetings]

        availability = [[844, 845], [1200, 1230], [1500, 1515], [1546, 1600]]

        print(find_available_times(schedules))
        self.assertEqual(
            find_available_times(schedules),
            availability
            )


'''
##################################################################################
#################################################################################
##############################################################################

This solution only works for whole hour intervals and you cannot enter for example 14:30
'''

'''
A starting point, still to optimize a bit, might be the following (code is in Python).
You have the following data (the allPeople list will be clearly created dynamically):

person_1 = ["4-16","18-24"]
person_2 = ["2-14","17-24"]
person_3 = ["6-8","12-20"]
person_4 = ["10-22"]
allPeople = [person_1, person_2, person_3, person_4]

What you might do is to create a list containing all the time slots of the day
(i.e. ["0-1", "1-2", "2-3", etc.] as follows:
'''
allTimeSlots = []
for j in range(0,24):
    allTimeSlots.append(str(j) + "-" + str(j+1))
'''
and then create a list called commonFreeSlots, which is made of all the time
slots that are inside each person's free time slot collection:
'''
commonFreeSlots = []
for j in range(0,len(allTimeSlots)):
    timeSlotOk = True
    for k in range(0,len(allPeople)):
        person_free_slots = parseSlot(allPeople[k])
        if allTimeSlots[j] not in person_free_slots:
            timeSlotOk = False
            break
    if timeSlotOk:
        commonFreeSlots.append(allTimeSlots[j])
'''
Please note that the function parseSlot is just taking a list of strings
(like "2-14","15-16") and returning a list of hourly time slots (like ["2-3","3-4","4-5" etc.]
in order to make it comparable with the hourly time slot list allTimeSlots created above:
'''

def parseSlot(list_of_slots):
    result = []
    for j in range(0,len(list_of_slots)):
        start_time = int(list_of_slots[j].split("-")[0])
        end_time = int(list_of_slots[j].split("-")[1])
        k = 0
        while (start_time + k) < end_time:
            result.append(str(start_time+k) + "-" + str(start_time+k+1))
            k += 1
    return result

'''
If I run the above script, I get the following result:

['12-13', '13-14', '18-19', '19-20']

Of course you will have to still work a bit the output in order to aggregate the
hours (and having ['12-14','18-20'] instead of the hourly version), but this should
be easier I think.

The above solution should work always, however I'm not sure it's optimal,
it probably exists a better one. But since you didn't share any attempt yet,
I guess you'd just like some tips to get started so I hope this one helps a bit.
'''
