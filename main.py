from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json
import requests

class Profile:
    name=""
    room_number=""
    email=""
    branch=""
    phone=""

class MainScrean(Screen):
    def login(self):
        email = self.ids.email_input.text
        password = self.ids.password_input.text

        # Replace 'your-firebase-url' with your actual Firebase Realtime Database URL
        firebase_url = 'https://maintenance-f1a82-default-rtdb.firebaseio.com/'

        # Fetch user data from Firebase
        response = requests.get(f'{firebase_url}.json')
        users_data = response.json()

        # Check if email and password match any user in the database
        for user_id, user_info in users_data.items():
            if email=="Admin" and password=="admin":
                self.manager.current = 'ComplainData'
                self.ids.email_input.text=""
                self.ids.password_input.text=""
                return
            elif user_info.get('email') == email and user_info.get('password') == password:
                #p=Profile(user_info.get('name'),user_info.get('rollnumber'),user_info.get('email'),user_info.get('branch'),user_info.get('phone'))
                Profile.name=user_info.get('name')
                Profile.room_number=user_info.get('rollnumber')
                Profile.email=user_info.get('email')
                Profile.branch=user_info.get('branch')
                Profile.phone=user_info.get('phone')
                self.manager.current = 'Complaint'# Switch to the ComplaintScreen
                self.ids.email_input.text=""
                self.ids.password_input.text=""
                return

        # If no matching user found, show a popup
        success_popup = Popup(title='Login failed',
                              content=Label(text='Invalid email or password.'),
                              size_hint=(None, None), size=(400, 200))
        success_popup.open()
        self.ids.email_input.text=""
        self.ids.password_input.text=""

class ComplainData(Screen):
    def on_enter(self):
        self.fetch_data()

    def fetch_data(self):
        # Replace this with your Firebase Realtime Database URL
        url = "https://maintenance2-b0923-default-rtdb.firebaseio.com/.json"

        response = requests.get(url)
        data = response.json() if response.ok else {}

        # Display keys as table headers
        header_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        header_layout.add_widget(Label(text=f'Complains', size_hint_x=0.1, halign='center', text_size=(None, None)))
        header_layout.add_widget(Label(text=f'Complains Details', size_hint_x=0.3, halign='center', text_size=(None, None)))
        header_layout.add_widget(Label(text=f'Branch', size_hint_x=0.1, halign='center', text_size=(None, None)))
        header_layout.add_widget(Label(text=f'Email', size_hint_x=0.1, halign='center', text_size=(None, None)))
        header_layout.add_widget(Label(text=f'Name', size_hint_x=0.1, halign='center', text_size=(None, None)))
        header_layout.add_widget(Label(text=f'Phone', size_hint_x=0.1, halign='center', text_size=(None, None)))
        header_layout.add_widget(Label(text=f'Room Number', size_hint_x=0.1, halign='center', text_size=(None, None)))
        header_layout.add_widget(Label(text=f'Button', size_hint_x=0.1, halign='center', text_size=(None, None)))
        self.ids.head_layout.add_widget(header_layout)
        for key, value in data.items():
            row_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            row_layout.add_widget(Label(text=f'{value.get('Complains')}', size_hint_x=0.1, halign='center', text_size=(None, None)))
            row_layout.add_widget(Label(text=f'{value.get('Complains_Details')}', size_hint_x=0.3, halign='center', text_size=(None, None)))
            row_layout.add_widget(Label(text=f'{value.get('branch')}', size_hint_x=0.1, halign='center', text_size=(None, None)))
            row_layout.add_widget(Label(text=f'{value.get('email')}', size_hint_x=0.1, halign='center', text_size=(None, None)))
            row_layout.add_widget(Label(text=f'{value.get('name')}', size_hint_x=0.1, halign='center', text_size=(None, None)))
            row_layout.add_widget(Label(text=f'{value.get('phone')}', size_hint_x=0.1, halign='center', text_size=(None, None)))
            row_layout.add_widget(Label(text=f'{value.get('room_number')}', size_hint_x=0.1, halign='center', text_size=(None, None)))
            delete_button = Button(text='Delete', size_hint_x=0.1)
            delete_button.bind(on_press=lambda instance, row_key=key: self.delete_data(row_key))
            row_layout.add_widget(delete_button)
            self.ids.data_layout.add_widget(row_layout)

    def delete_data(self, row_key):
        # Implement Firebase data deletion logic here
        # Replace this with your Firebase Realtime Database URL
        url = f"https://maintenance2-b0923-default-rtdb.firebaseio.com/{row_key}.json"

        # Make a DELETE request to remove the data with the specified key
        response = requests.delete(url)

        if response.ok:
            # If the deletion was successful, remove the corresponding UI element
            for child in self.ids.data_layout.children:
                if isinstance(child, BoxLayout) and child.children[0].text.startswith(row_key):
                    self.ids.data_layout.remove_widget(child)
                    break

class ComplaintScreen(Screen):
    def handle_press(self):
        com=[]
        # Get selected values from each dropdown
        electrical_value = self.ids.electrical_spinner.text
        plumbing_value = self.ids.plumbing_spinner.text
        carpentry_value = self.ids.carpentry_spinner.text
        water_cooler_value = self.ids.water_cooler_spinner.text
        washing_machine_value = self.ids.washing_machine_spinner.text
        dryer_value = self.ids.dryer_spinner.text
        furniture_value = self.ids.furniture_spinner.text
        air_conditioner_value = self.ids.air_conditioner_spinner.text
        it_value = self.ids.it_spinner.text
        civil_value = self.ids.civil_spinner.text
        fire_safety_value = self.ids.fire_safety_spinner.text
        telephone_value = self.ids.telephone_spinner.text
        housekeeping_value = self.ids.housekeeping_spinner.text
        other_value = self.ids.other_spinner.text
        
        
        # Get complaint details from TextInput
        complaint_details = self.ids.complaint_input.text
        if electrical_value == "ELECTRICAL":
            electrical_value =""
        else:
            com.append(electrical_value)

        if plumbing_value == "PLUMBING":
            plumbing_value =""
        else:
            com.append(plumbing_value)

        if carpentry_value == "CARPENTRY":
            carpentry_value =""
        else:
            com.append(carpentry_value)

        if water_cooler_value == "WATER COOLER":
            water_cooler_value =""
        else:
            com.append(water_cooler_value)

        if washing_machine_value == "WASHING MACHINE":
            washing_machine_value =""
        else:
            com.append(washing_machine_value)

        if dryer_value == "DRYER":
            dryer_value =""
        else:
            com.append(dryer_value)

        if furniture_value == "FURNITURE":
            furniture_value =""
        else:
            com.append(furniture_value)

        if air_conditioner_value == "AIR CONDITIONER":
            air_conditioner_value =""
        else:
            com.append(air_conditioner_value)

        if it_value == "IT":
            it_value =""
        else:
            com.append(it_value)

        if civil_value == "CIVIL":
            civil_value =""
        else:
            com.append(civil_value)

        if fire_safety_value == "FIRE & SAFETY":
            fire_safety_value =""
        else:
            com.append(fire_safety_value)

        if telephone_value == "TELEPHONE":
            telephone_value =""
        else:
            com.append(telephone_value)

        if housekeeping_value == "HOUSEKEEPING":
            housekeeping_value =""
        else:
            com.append(housekeeping_value)
        
        if other_value == "OTHER":
            other_value =""
        else:
            com.append(other_value)
        # Perform further processing or submit the values as needed
        
        url="https://maintenance2-b0923-default-rtdb.firebaseio.com/.json"
        for item in com:
            input_data = {"name": Profile.name, "room_number": Profile.room_number, "phone": Profile.phone, "branch": Profile.branch,"email": Profile.email, "Complains": item,"Complains_Details": complaint_details}
            json_input = json.dumps(input_data, indent=2)
            to_database = json.loads(json_input)
            response=requests.post(url=url, json=to_database)
          
        success_popup = Popup(title='Complains Submitted Successful',
                              content=Label(text='Your complaint has been submitted successfully.'),
                              size_hint=(None, None), size=(400, 200))
        success_popup.open()
        self.ids.complaint_input.text=""
class RegistrationScreen(Screen):
    def handle_registration(self):
        # Retrieve input values
        name = self.ids.name_input.text
        rollnumber = self.ids.rollnumber_input.text
        hostel_number = self.ids.hostel_input.text
        room_number = self.ids.room_input.text
        phone = self.ids.phone_input.text
        branch = self.ids.branch_input.text
        email = self.ids.email_input.text
        password = self.ids.password_input.text
        url="https://maintenance-f1a82-default-rtdb.firebaseio.com/.json"
        if (
            name is not None and
            rollnumber is not None and
            hostel_number is not None and
            room_number is not None and
            phone is not None and
            branch is not None and
            email is not None and '@gim.ac.in' in email and
            password is not None and
            hostel_number.isdigit() and len(hostel_number) == 1 and  # Specify the length for hostel_number
            room_number.isdigit() and len(room_number) == 4 and  # Specify the length for room_number
            phone.isdigit() and len(phone) == 10  # Specify the length for phone
        ):
            # All conditions are met, proceed with further actions
            print("All values are valid.")
            input_data = {rollnumber:{"name": name, "rollnumber": rollnumber, "hostel_number": hostel_number, "room_number": room_number, "phone": phone, "branch": branch,"email": email, "password": password}}
            json_input = json.dumps(input_data, indent=2)
            to_database = json.loads(json_input)
            response=requests.patch(url=url, json=to_database)
           
            success_popup = Popup(title='Congratulations!',
                              content=Label(text='Your registration was successful.'),
                              size_hint=(None, None), size=(400, 200))
            success_popup.open()
        else:
            # At least one condition is not met, handle accordingly
            success_popup = Popup(title='Error',
                              content=Label(text='Fill the form correctly'),
                              size_hint=(None, None), size=(400, 200))
            success_popup.open()
            
        self.ids.name_input.text=""
        self.ids.rollnumber_input.text=""
        self.ids.hostel_input.text=""
        self.ids.room_input.text=""
        self.ids.phone_input.text=""
        self.ids.branch_input.text=""
        self.ids.email_input.text=""
        self.ids.password_input.text=""
        # For demonstration purposes, show a popup with a success message
        
    
class WindowManager(ScreenManager):
    pass        
kv = Builder.load_file("my.kv")
class MyApp(App):
    def build(self):
        return kv

if __name__ == '__main__':
    MyApp().run()
