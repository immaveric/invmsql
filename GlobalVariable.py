from kivy.properties import StringProperty, NumericProperty
from datetime import date, datetime

trip1 = StringProperty('0')
start = 0
today = date.today()
now = datetime.now().strftime('%d-%m-%Y %M%S')
count = 0
count_enable = False
total_amount = NumericProperty()
stops = ['stop1', 'stop2', 'stop3', 'stop4', 'stop5', 'stop6', 'stop7', 'stop8', 'stop9', 'stop10', 'stop11',
         'stop12', 'stop13', 'stop14', 'stop15', 'stop16', 'stop17', 'stop18', 'stop19', 'stop20', 'stop21',
         'stop22', 'stop23', 'stop24', 'stop25', 'stop26', 'stop27', 'stop28', 'stop29', 'stop30', 'stop31',
         'stop32', 'stop33', 'stop34', 'stop35', 'stop36', 'stop37', 'stop38', 'stop39', 'stop40', 'stop41',
         'stop42', 'stop43', 'stop44', 'stop45']
return_stops = ['stop101', 'stop102', 'stop103', 'stop104', 'stop105', 'stop106', 'stop107', 'stop108', 'stop109', 'stop110', 'stop111',
         'stop112', 'stop113', 'stop114', 'stop115', 'stop116', 'stop117', 'stop118', 'stop119', 'stop120', 'stop121',
         'stop122', 'stop123', 'stop124', 'stop125', 'stop126', 'stop127', 'stop128', 'stop129', 'stop130', 'stop131',
         'stop132', 'stop133', 'stop134', 'stop135', 'stop136', 'stop137', 'stop138', 'stop139', 'stop140', 'stop141',
         'stop142', 'stop143', 'stop144', 'stop145']
