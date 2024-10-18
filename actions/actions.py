from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import random

import sys
import os

from Inventory.InventoryCheck_4 import check_stock_bts, check_tire_size, check_tire_type,  check_vehicle_type, get_tire_size
from typing import List
from rasa_sdk import Action
from rasa_sdk.events import SessionStarted, ActionExecuted, EventType

from rasa_sdk.events import SlotSet



class ActionHello(Action):
    def name(self):
        return "action_hello"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        dispatcher.utter_message(text="Hello! and welcome to your tyre WheelWizard. I am here to help you choose tires for your vehicle. For this purpose, please choose what kind of vehicle it is *example: (car, jeep/pickup, van, or truck)")
        return []
    
class Greet(Action):
    def name(self):
        return "action_utter_greet"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):


        messages = [
            'Hello and welcome to your WheelWizard. I am here to help you choose tires for your vehicle. For this purpose, please choose what kind of vehicle it is *example: (car, jeep/pickup, van, or truck)',
            'Hello 👋 and welcome to your WheelWizard. I am here to help you choose tires for your vehicle. In order to be able to do that, I will need information on what kind of vehicle do you need tires for? *example: (car, jeep/pickup, van, or truck)'
        ]
        
        message = random.choice(messages)
        dispatcher.utter_message(text=message)
        
        return []

class V_Type(Action):
    def name(self):
        return "action_utter_confirm_v_type"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):

        vehicle_type = tracker.get_slot('vehicle_type')
        if vehicle_type != None:
            response = check_vehicle_type(vehicle_type)
        else:
            dispatcher.utter_message(text="Please try again using the following example: (car, jeep/pickup, van, or truck)")

        messages = [
            f"Ok great! So that I can find you tires for {response}, I will need you to tell me what season you need them for? *Example (summer, winter, or for all seasons)",
            f"Excellent! Now that I know that you need tires for {response}, please tell me for exactly what season you need the tires to be? *Example (summer, winter, or for all seasons)",
            f"Ok, so I can see what we have in stock for your {response} please let me know what season the tires should be? *Example (summer, winter, or for all seasons)"
        ]
        if response:
            message = random.choice(messages)
            dispatcher.utter_message(text=message)
        
            return []
        else:
            dispatcher.utter_message(text="Please try again using the following example: (car, jeep/pickup, van, or truck)")

class Type(Action):
    def name(self):
        return "action_utter_confirm_type"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        tire_type = tracker.get_slot('type')
        
        vehicle_type = tracker.get_slot('vehicle_type')
        if tire_type and vehicle_type:

            response_V = check_vehicle_type(vehicle_type)
            response = check_tire_type(tire_type)
        else:
            dispatcher.utter_message(text="Please try again using the following Example (summer, winter, or all seasons)")
            return []
        messages = [
        f"Now that I know that you need {response} tires, I just need you to tell me the dimensions for the tires width/profile/diameter with numbers *example (225/40/R15)",
        f"Ok, please just tell me {response} tires for {response_V} in what dimensions should they be (width/profile/diameter)?*example (225/45/18)",
        f"So {response} tires, {response_V} can you still tell me the dimensions (width/profile/diameter)? *example (225/45/18)"
        ]
        
        if response_V != None and response != None:
            message = random.choice(messages)
            dispatcher.utter_message(text=message)
        else:
            dispatcher.utter_message(text="Please try again using the following Example (summer, winter, or all seasons)")
        
        return []

class Size(Action):
    def name(self):
        return "action_utter_confirm_size"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict):
        size = tracker.get_slot("size")
        response = check_tire_size(size)
        response = str(response)
        width = response[:3]
        aspect_ratio = response[3:5]
        diameter = response[5:]
        messages = [
            f"I will immediately check what we have in stock with width {width}, profile {aspect_ratio} and diameter {diameter}. What quantity do you need? example: (1, 4, 5)",
            f"I will check right away what we have in stock with width {width}, profile {aspect_ratio} and diameter {diameter}. What quantity do you need? example: (1, 4, 5)",
            "One more thing I need you to tell me is how many tires you need."
        ]
        if response != None:
            message = random.choice(messages)
            dispatcher.utter_message(text=message)
        else:
            dispatcher.utter_message(text="Please try again using the following example: (225/45/18)")
        return []






class Check_Stock(Action):
    def name(self):
        return "action_testing"

    def run(self, dispatcher, tracker, domain):
        size = tracker.get_slot('size')
        tire_type = tracker.get_slot('type')
        vehicle_type = tracker.get_slot('vehicle_type')
        stock = tracker.get_slot('stock')

        if vehicle_type and size and tire_type  and stock:
            pdf_file_path = check_stock_bts(vehicle_type, tire_type, size, stock)
            try:

                pdf_list = pdf_file_path.apply(lambda row: f"Company: {row['company']}, Tire model: {row['Tire Model']}, Season: {row['Season']}, Vehicle type: {row['vehicle type']}, Size: {row['Size_Apear']}", axis=1).tolist()
                pdf_message = "\n".join(pdf_list)
                dispatcher.utter_message(text="Here is your PDF offer:")
                dispatcher.utter_message(text=pdf_message)
            except AttributeError:
                dispatcher.utter_message(text=pdf_file_path)
        return []
    



#_____________________________________________________________________- new

class Missing_st(Action):
    def name(self):
        return "action_incomplete_st"

    def run(self, dispatcher, tracker, domain):
        size = tracker.get_slot('size')
        tire_type = tracker.get_slot('type')
        response_t = check_tire_type(tire_type)
        response_s = check_tire_size(size)

        response_s = str(response_s)
        width = response_s[:3]
        aspect_ratio = response_s[3:5]
        diameter = response_s[5:]
        messages = [
            f"Now that I know you need {response_t} tires with width {width}, profile {aspect_ratio} and diameter {diameter}. Please specify what type of vehicle you need them for. *Example (Passenger vehicle, Cargo vehicle, Jeep).",
            f"Ok please just tell me {response_t} tires with width {width}, profile {aspect_ratio} and diameter {diameter} for what type of vehicle you need. *Example (Passenger vehicle, Cargo vehicle, Jeep).",
            f"So {response_t} tires, width {width}, profile {aspect_ratio} and diameter {diameter} still tell me the type of vehicle. *Example (Passenger vehicle, Cargo vehicle, Jeep)."
        ]
        if response_t and response_s:
            message = random.choice(messages)
            dispatcher.utter_message(text=message)
        else:
            dispatcher.utter_message(text="Please try again using the following example: ( Winter tires 225/45/18 )")
        
        return []

class Missing_sv(Action):
    def name(self):
        return "action_incomplete_sv"

    def run(self, dispatcher, tracker, domain):
        size = tracker.get_slot('size')
        vehicle_type = tracker.get_slot('vehicle_type')
        response_V = check_vehicle_type(vehicle_type)
        response_s = check_tire_size(size)

        response_s = str(response_s)
        width = response_s[:3]
        aspect_ratio = response_s[3:5]
        diameter = response_s[5:]
        messages = [
            f"Now that I know you need tires for {response_V} with width {width}, profile {aspect_ratio} and diameter {diameter}. Please specify what type of vehicle you need them for. *Example (Passenger vehicle, Cargo vehicle, Jeep).",
            f"Ok, please tell me {response_V} with width {width}, profile {aspect_ratio} and diameter {diameter} for what type of vehicle you need. *Example (Passenger vehicle, Cargo vehicle, Jeep).",
            f"So {response_V}, width {width}, profile {aspect_ratio} and diameter {diameter}, tell me the type of vehicle. *Example (Passenger vehicle, Cargo vehicle, Jeep)."
        ]
        if response_V and response_s:
            message = random.choice(messages)
            dispatcher.utter_message(text=message)
        else:
            dispatcher.utter_message(text="Please try again using the following example: ( Passenger vehicle 225/45/18 )")
        
        return []

class Missing_tv(Action):
    def name(self):
        return "action_incomplete_tv"

    def run(self, dispatcher, tracker, domain):
        tire_type = tracker.get_slot('type')
        vehicle_type = tracker.get_slot('vehicle_type')
        response_V = check_vehicle_type(vehicle_type)
        response = check_tire_type(tire_type)

        messages = [
            f"Now that I know that you need {response} tires, I just need you to tell me the dimensions for the tires width/profile/diameter with numbers *example (225/40/R15)",
            f"Ok, please just tell me {response} tires for {response_V} in what dimensions should they be (width/profile/diameter)?*example (225/45/18)",
            f"So {response} tires, {response_V} can you still tell me the dimensions (width/profile/diameter)? *example (225/45/18)"
        ]
        
        if response_V and response:
            message = random.choice(messages)
            dispatcher.utter_message(text=message)
        else:
            dispatcher.utter_message(text="Please try again using the following Example: ( summer tires for a passenger car, winter tires for a truck )")
        
        return []


class Neznam(Action):
    def name(self):
        return "action_neznam"

    def run(self, dispatcher, tracker, domain):
        maker = tracker.get_slot('maker')
        model = tracker.get_slot('model')
        year = tracker.get_slot('year')
        sizee = get_tire_size(model, maker, year)
        SlotSet("size", str(sizee))
        sizee = str(sizee)
        messages = [
            f"I will immediately check that we have {sizee} tires in stock. What quantity do you need? example: (1, 4, 5)",
            f"I'll check right away to see what we have in stock with dimension {sizee}. What quantity do you need? example: (1, 4, 5)",
            "One more thing I need you to tell me is how many tires you need."
        ]
        message = random.choice(messages)
        dispatcher.utter_message(text=message)
        return [SlotSet("size", str(sizee))]
