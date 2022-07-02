from datetime import datetime
from kivy.app import App
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.widget import Widget
import GlobalVariable
from kondoMpm import KondoMpm
import mysql.connector
import mysql

Window.softinput_mode = "below_target"
Window.keyboard_anim_args = {'d': .2, 't': 'in_out_expo'}

mydb = mysql.connector.connect(
    host="139.59.20.11",
    user="inv-user",
    passwd="Need4$peed",
    database="trip_db",
    auth_plugin='mysql_native_password',
)

c = mydb.cursor()

# create an actual database
# c.execute("CREATE DATABASE  IF NOT EXISTS trip_dp")

# create a table

mydb.commit()

mydb.close()


class KondoMpm(ScreenManager, KondoMpm):
    pass


class WindowManager(ScreenManager):
    pass


class LoginScreen(Screen):

    def credential_check(self):
        mydb = mysql.connector.connect(
            host="139.59.20.11",
            user="inv-user",
            passwd="Need4$peed",
            database="trip_db",
            auth_plugin='mysql_native_password',

        )
        c = mydb.cursor()

        c.execute("SELECT username, psword FROM credentials")
        datas = c.fetchall()
        if self.login_uname.text == '' or self.login_pword.text == '':
            user_error()
        else:
            for data in datas:
                if data[0] == self.login_uname.text.lower() and data[1] == self.login_pword.text:
                    self.manager.current = 'HomePage'
                    self.manager.transition.direction = "left"
                    break
            else:
                login_error()


class LoginErrorPopup(Popup):
    log_error_label = ObjectProperty(None)


class SignInScreen(Screen):
    def add_credentials(self):
        mydb = mysql.connector.connect(
            host="139.59.20.11",
            user="inv-user",
            passwd="Need4$peed",
            database="trip_db",
            auth_plugin='mysql_native_password',
        )
        c = mydb.cursor()
        c.execute("SELECT username FROM credentials")
        datas = c.fetchall()
        if self.uname_field.text.lower() == '' or self.pw_field.text.lower() == '':
            user_error()
        else:
            for data in datas:
                if data[0] == self.uname_field.text.lower():
                    user_error()
                    break
            else:
                sql_command = "INSERT INTO credentials (username, psword) VALUES (%s, %s) "
                values = (self.uname_field.text.lower(), self.pw_field.text)
                c.execute(sql_command, values)
                mydb.commit()
                mydb.close()
                user_added()


class ExitingUserPopup(Popup):
    pass


class AccountInfo(Screen):
    pass


class ChangePasswordScreen(Screen):
    def change_password(self):
        mydb = mysql.connector.connect(
            host="139.59.20.11",
            user="inv-user",
            passwd="Need4$peed",
            database="trip_db",
            auth_plugin='mysql_native_password',
        )
        c = mydb.cursor()
        c.execute("SELECT username FROM credentials")
        datas = c.fetchall()
        for data in datas:
            if data[0] == self.uname_change.text.lower() and self.pw_change.text != "":
                sql_command = "UPDATE credentials SET psword = %s WHERE username = %s "
                values = (self.pw_change.text, self.uname_change.text.lower())
                c.execute(sql_command, values)
                mydb.commit()
                mydb.close()
                self.manager.current = "LoginPage"
                self.manager.transition.direction = "right"
                break
        else:
            login_error()

    def back_previous_screen(self):
        InvScreen.previous_screen(self)


class TripInfo(Screen):
    trip_data = ObjectProperty(None)
    bus_number = StringProperty(None)

    btn = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(TripInfo, self).__init__(**kwargs)

    def on_trip_data(self):
        user_copy = self.manager.get_screen('LoginPage').ids.login_uname.text
        i = 1
        mydb = mysql.connector.connect(
            host="139.59.20.11",
            user="inv-user",
            passwd="Need4$peed",
            database="trip_db",
            auth_plugin='mysql_native_password',
        )

        c = mydb.cursor()
        entries = "SELECT DATE_FORMAT(tripdate, '%d/%m/%Y'), amount, route, drivername, conductorname, trip_number FROM invoice WHERE tripdate = %s AND userid = %s"
        values = (self.ids.from_date.text, self.manager.get_screen('LoginPage').ids.login_uname.text)
        c.execute(entries, values)
        records = c.fetchall()

        for record in records:
            btn = Button(text=str(
                f" Date : {record[0]} \n Trip_id: {record[5]} \n Amount : {record[1]} \n Route : {record[2]} \n Driver : {record[3]} \n Conductor : {record[4]}"),
                         size_hint=(.5, .3), pos=(i * 0, i * 10))
            self.ids['reset'] = btn
            self.ids.database.add_widget(btn)

        mydb.commit()

        mydb.close()

    def remove(self):
        children = self.ids.database.children
        for child in reversed(children):
            self.ids.database.remove_widget(child)
        self.ids.from_date.text = ''


class TripFormScreen(Screen):
    trip1 = StringProperty("0")
    bus_number = ObjectProperty("0")
    from_location = ObjectProperty("0")
    driver = ObjectProperty("0")
    conductor = ObjectProperty("0")
    date = ObjectProperty("0")

    def __init__(self, **kwargs):
        super(TripFormScreen, self).__init__(**kwargs)

    def trip_auto_number(self):
        self.trip1 = str(datetime.now().strftime('%d-%m-%Y %M%S'))
        self.ids.date.text = str(GlobalVariable.today)

    def route_selector(self, value):
        if self.bus_number.text == "":
            self.ids.bus_number.hint_text = "**Required***"
            self.ids.select_trip.text = "Select Route"
        if self.driver.text == "":
            self.ids.driver.hint_text = "**Required***"
            self.ids.select_trip.text = "Select Route"
        if self.conductor.text == "":
            self.ids.conductor.hint_text = "**Required***"
            self.ids.select_trip.text = "Select Route"
        elif value == 'MALAPPURAM - KONDOTTY':
            self.manager.current = 'CalPage'
            self.manager.transition.direction = "left"
            self.manager.get_screen('CalPage').ids.passenger_count.text = '0'
            for stop in GlobalVariable.stops:
                self.manager.get_screen('CalPage').ids[stop].ids.no_of_person.text = ''
        elif value == 'KONDOTTY - MALAPPURAM':
            self.manager.current = 'CalPageKondoMpm'
            self.manager.transition.direction = "left"
            self.manager.get_screen('CalPageKondoMpm').ids.passenger_count.text = '0'
            for stop in GlobalVariable.return_stops:
                self.manager.get_screen('CalPageKondoMpm').ids[stop].ids.no_of_person.text = ''


class UserAddedPopup(Popup):
    pass


class KondoMpm(Screen, Widget):
    pass


class MpmKondo(Screen, Widget):
    total_amount = NumericProperty("0")
    passenger_count = NumericProperty("0")
    min_charge = 8
    second_stage_charge = 2
    third_stage_charge = 3
    first_stage_km = 2.5
    second_stage_km = 5
    third_stage_km = 7.5

    def trip_calculation(self):
        self.total_amount = 0
        for stop in GlobalVariable.stops:
            if str(self.ids[stop].ids.no_of_person.text) != '':
                if float(self.ids[stop].ids.no_of_person.text) != 0:
                    if float(self.ids[stop].ids.km.text) <= self.first_stage_km:
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
        for stop in GlobalVariable.stops:
            if bus_stop.upper() == self.ids[stop].ids.name.text and i == 0:
                i += 1
            if bus_stop.upper() == 'MPM' and i == 0:
                i += 1
            if i >= 1 and bus_stop.upper() != self.ids[stop].ids.name.text:
                if str(self.ids[stop].ids.no_of_person.text) != '':
                    self.passenger_count += int(self.ids[stop].ids.no_of_person.text)


class CounterForIn(BoxLayout):
    pass


class MenuScreen(Screen):
    pass


class InvScreen(Screen):
    total_amount_copy = NumericProperty(0)
    i = 0

    def store_trip_info(self):
        bus_number_copy = self.manager.get_screen('Trip').ids.bus_number.text
        driver_copy = self.manager.get_screen('Trip').ids.driver.text
        conductor_copy = self.manager.get_screen('Trip').ids.conductor.text
        cleaner_copy = self.manager.get_screen('Trip').ids.cleaner.text
        checker_copy = self.manager.get_screen('Trip').ids.checker.text
        date_copy = self.manager.get_screen('Trip').ids.date.text
        from_to_copy = self.manager.get_screen('Trip').ids.select_trip.text
        user_copy = self.manager.get_screen('LoginPage').ids.login_uname.text
        self.i += 1
        mydb = mysql.connector.connect(
            host="139.59.20.11",
            user="inv-user",
            passwd="Need4$peed",
            database="trip_db",
            auth_plugin='mysql_native_password'
        )

        c = mydb.cursor()

        sql_command = "INSERT INTO invoice (userid, tripdate, amount, route, drivername, conductorname, trip_number) VALUES (%s,%s, %s, %s, %s, %s, %s) "
        values = (user_copy.lower(), date_copy, self.total_amount_copy, from_to_copy.upper(), driver_copy.upper(),
                  conductor_copy.upper(),  self.trip_number_copy.text)
        c.execute(sql_command, values)

        mydb.commit()

        mydb.close()

    def previous_screen(self):
        if self.manager.previous_screen == "CalPageKondoMpm":
            self.manager.current = 'CalPageKondoMpm'
            self.manager.transition.direction = "right"
        elif self.manager.previous_screen == "CalPage":
            self.manager.current = 'CalPage'
            self.manager.transition.direction = "right"
        elif self.manager.previous_screen == "LoginPage":
            self.manager.current = 'LoginPage'
            self.manager.transition.direction = "right"
        elif self.manager.previous_screen == "Account":
            self.manager.current = 'Account'
            self.manager.transition.direction = "right"

    def total_amount(self):
        if self.manager.get_screen('Trip').ids.select_trip.text == "KONDOTTY - MALAPPURAM":
            self.total_amount_copy = self.manager.get_screen('CalPageKondoMpm').total_amount
        elif self.manager.get_screen('Trip').ids.select_trip.text == "MALAPPURAM - KONDOTTY":
            self.total_amount_copy = self.manager.get_screen('CalPage').total_amount


class UserProfile(Screen):
    pass


class MyKmLabel(BoxLayout):
    pass


class BusApp(App):

    def build(self):
        self.icon = "icon.png"
        Window.clearcolor = (0, 40 / 255, 77 / 255, 1)
        return WindowManager()


def login_error():
    show1 = LoginErrorPopup()
    show1.open()


def user_error():
    show = ExitingUserPopup()
    show.open()


def user_added():
    show2 = UserAddedPopup()
    show2.open()


BusApp().run()
