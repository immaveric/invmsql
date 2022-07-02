
from kivy.properties import NumericProperty, StringProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget

import GlobalVariable


class KondoMpm(Screen, Widget):
    total_amount = NumericProperty("0")
    passenger_count = NumericProperty("0")
    amount = 0
    min_charge = 8
    second_stage_charge = 2
    third_stage_charge = 3
    first_stage_km = 2.5
    second_stage_km = 5
    third_stage_km = 7.5
    previous_screen = StringProperty(None)

    def trip_calculation(self):
        self.total_amount = 0
        for stop in GlobalVariable.return_stops:
            if str(self.ids[stop].ids.no_of_person.text) != '':
                if float(self.ids[stop].ids.no_of_person.text) != 0:
                    if float(self.ids[stop].ids.km.text) <= self.first_stage_km:
                        print(self.ids[stop].ids.no_of_person.text)
                        self.amount = str((self.min_charge * float(self.ids[stop].ids.no_of_person.text)))
                    elif self.second_stage_km >= float(self.ids[stop].ids.km.text) >= self.first_stage_km:
                        self.amount = str(
                            ((self.min_charge + self.second_stage_charge) * int(self.ids[stop].ids.no_of_person.text)))
                    elif self.third_stage_km >= float(self.ids[stop].ids.km.text) > self.second_stage_km:
                        self.amount = str(
                            ((self.min_charge + self.second_stage_charge + self.third_stage_charge) * float(
                                self.ids[stop].ids.no_of_person.text)))
                    if float(self.ids[stop].ids.km.text) > self.third_stage_km:
                        cascading_km = float(self.ids[stop].ids.km.text) - self.third_stage_km
                        if cascading_km % self.first_stage_km != 0:
                            self.amount = int(((self.min_charge + self.second_stage_charge + self.third_stage_charge +
                                                (int(
                                                    cascading_km / self.first_stage_km) + 1) * self.second_stage_charge) *
                                               float(self.ids[stop].ids.no_of_person.text)))
                        else:
                            self.amount = str(((self.min_charge + self.second_stage_charge + self.third_stage_charge +
                                                int(
                                                    cascading_km / self.first_stage_km - 1) * self.second_stage_charge + self.third_stage_charge) *
                                               float(self.ids[stop].ids.no_of_person.text)))
                    self.total_amount += float(self.amount)
                    self.manager.current = 'Invoice'


    def instant_passengers_count(self, value):
        self.passenger_count = 0
        bus_stop = value
        i = 0
        for stop in GlobalVariable.return_stops:
            if bus_stop.upper() == self.ids[stop].ids.name.text and i == 0:
                i += 1
            if bus_stop.upper() == 'KONDOTTY' and i == 0:
                    i += 1
            if i >= 1 and bus_stop.upper() != self.ids[stop].ids.name.text:
                if str(self.ids[stop].ids.no_of_person.text) != '':
                    self.passenger_count += int(self.ids[stop].ids.no_of_person.text)
