from typing import Text, List, Any, Dict
import re
import json

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, FollowupAction

# from form_responses import get_response_result_and_keys, get_file_info

class ValidateSignupForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_signup_form"

    def validate_email(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate email value."""
        if slot_value == tracker.get_slot("password"):
            dispatcher.utter_message(text="Email should not be the same as the password.")
            return {"email": None}
        return {"email": slot_value}

    def validate_password(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate password value."""
        if len(slot_value) < 8:
            dispatcher.utter_message(text="Password should be at least 8 characters long.")
            return {"password": None}

        if not re.search(r"\d", slot_value) or not re.search(r"[a-zA-Z]", slot_value) or not re.search(r"\W", slot_value):
            dispatcher.utter_message(text="Password should contain letters, numbers and special symbols.")
            return {"password": None}

        return {"password": slot_value}

class ActionSubmitForm(Action):
    def name(self) -> Text:
        return "action_submit_form"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        email = tracker.get_slot("email")
        password = tracker.get_slot("password")

        if email and password:  # check if both slots are filled
            return [SlotSet("logged_in", True)]
        else:
            return [SlotSet("logged_in", False)]

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'pptx'}

class ValidatePaymentfacilitatorForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_payment_facilitator_form"

    def validate_cac_documents(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate cac documents value."""

        fileInfo = json.loads(slot_value)
        filename, filetype, filesize = fileInfo['name'], fileInfo['type'], fileInfo['size']
        ext = filetype.split("/")[1]

        if (ext in ALLOWED_EXTENSIONS) and (filesize > 10):
            dispatcher.utter_message(text=f"Success. Document Received")
            return {"cac_documents":filename}
        else:
            dispatcher.utter_message(text="Failure, Document not Received")
            return {"cac_documents": None}
        
    def validate_cbn_license(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate CBN License value."""

        fileInfo = json.loads(slot_value)
        filename, filetype, filesize = fileInfo['name'], fileInfo['type'], fileInfo['size']
        ext = filetype.split("/")[1]

        if (ext in ALLOWED_EXTENSIONS) and (filesize > 10):
            if filename == tracker.get_slot("cac_documents"):
                dispatcher.utter_message(text="CAC DOCUMENTS AND CBN_LICENSE SHOULD NOT BE THE SAME!!")
                return {"cbn_license": None}
            else:
                dispatcher.utter_message(text=f"Success, Document Received")
                return {"cbn_license": filename}   
        else:
            dispatcher.utter_message(text="Failure, Document not Received")
            return {"cbn_license": None}
        
    def validate_pci_dss_certificate(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate PCIDSS Certificate value."""
        
        fileInfo = json.loads(slot_value)
        filename, filetype, filesize = fileInfo['name'], fileInfo['type'], fileInfo['size']
        ext = filetype.split("/")[1]

        if (ext in ALLOWED_EXTENSIONS) and (filesize > 10):
            if filename == tracker.get_slot("cbn_license"):
                dispatcher.utter_message(text="CBN_LICENSE AND PCIDSS_CERTIFICATE SHOULD NOT BE THE SAME!!")
                return {"pci_dss_certificate": None}
            else:
                dispatcher.utter_message(text=f"Success, Document Received")
                return {"pci_dss_certificate": filename}   
        else:
            dispatcher.utter_message(text="Failure, Document not Received")
            return {"pci_dss_certificate": None}
        
    def validate_line_of_business(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate Line of Business value."""
        
        if len(slot_value) > 5:
            dispatcher.utter_message(text=f"Success")
            return {"line_of_business": slot_value}
        else:
            dispatcher.utter_message(text="Failure")
            return {"line_of_business": slot_value}
        
    def validate_business_projection(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        
        """Validate Business Projection value."""

        fileInfo = json.loads(slot_value)
        filename, filetype, filesize = fileInfo['name'], fileInfo['type'], fileInfo['size']
        ext = filetype.split("/")[1]

        if (ext in ALLOWED_EXTENSIONS) and (filesize > 10):
            if filename == tracker.get_slot("pci_dss_certificate"):
                dispatcher.utter_message(text="PCIDSS_CERTIFICATE AND BUSINESS_PROJECTION SHOULD NOT BE THE SAME!!")
                return {"business_projection": None}
            else:
                dispatcher.utter_message(text=f"Success, Document Received")
                return {"business_projection": filename}   
        else:
            dispatcher.utter_message(text="Failure, Document not Received")
            return {"business_projection": None}
        
    def validate_aml_policy(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate AML Policy value."""
        
        fileInfo = json.loads(slot_value)
        filename, filetype, filesize = fileInfo['name'], fileInfo['type'], fileInfo['size']
        ext = filetype.split("/")[1]

        if (ext in ALLOWED_EXTENSIONS) and (filesize > 10):
            if filename == tracker.get_slot("business_projection"):
                dispatcher.utter_message(text="BUSINESS_PROJECTION AND AML POLICY SHOULD NOT BE THE SAME!!")
                return {"aml_policy": None}
            else:
                dispatcher.utter_message(text=f"Success, Document Received")
                return {"aml_policy": filename}   
        else:
            dispatcher.utter_message(text="Failure, Document not Received")
            return {"aml_policy": None}
        
    def validate_wema_amf_policy(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate WEMA AMF Policy value."""
        
        fileInfo = json.loads(slot_value)
        filename, filetype, filesize = fileInfo['name'], fileInfo['type'], fileInfo['size']
        ext = filetype.split("/")[1]

        if (ext in ALLOWED_EXTENSIONS) and (filesize > 10):
            if filename == tracker.get_slot("aml_policy"):
                dispatcher.utter_message(text="AML POLICY AND WEMA AMF POLICY SHOULD NOT BE THE SAME!!")
                return {"wema_amf_policy": None}
            else:
                dispatcher.utter_message(text=f"Success, Document Received")
                return {"wema_amf_policy": filename}   
        else:
            dispatcher.utter_message(text="Failure, Document not Received")
            return {"wema_amf_policy": None}

class ValidateIsomForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_iso_m_form"

    def validate_cac_documents(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate cac documents value."""

        fileInfo = json.loads(slot_value)
        filename, filetype, filesize = fileInfo['name'], fileInfo['type'], fileInfo['size']
        ext = filetype.split("/")[1]

        if (ext in ALLOWED_EXTENSIONS) and (filesize > 10):
            dispatcher.utter_message(text=f"Success. Document Received")
            return {"cac_documents":filename}
        else:
            dispatcher.utter_message(text="Failure, Document not Received")
            return {"cac_documents": None}
        
    
    def validate_line_of_business(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate Line of Business value."""
        
        if len(slot_value) > 5:
            dispatcher.utter_message(text=f"Success")
            return {"line_of_business": slot_value}
        else:
            dispatcher.utter_message(text="Failure")
            return {"line_of_business": slot_value}
        
    def validate_business_projection(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        
        """Validate Business Projection value."""

        fileInfo = json.loads(slot_value)
        filename, filetype, filesize = fileInfo['name'], fileInfo['type'], fileInfo['size']
        ext = filetype.split("/")[1]

        if (ext in ALLOWED_EXTENSIONS) and (filesize > 10):
            if filename == tracker.get_slot("pci_dss_certificate"):
                dispatcher.utter_message(text="PCIDSS_CERTIFICATE AND BUSINESS_PROJECTION SHOULD NOT BE THE SAME!!")
                return {"business_projection": None}
            else:
                dispatcher.utter_message(text=f"Success, Document Received")
                return {"business_projection": filename}   
        else:
            dispatcher.utter_message(text="Failure, Document not Received")
            return {"business_projection": None}
        
    def validate_aml_policy(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate AML Policy value."""
        
        fileInfo = json.loads(slot_value)
        filename, filetype, filesize = fileInfo['name'], fileInfo['type'], fileInfo['size']
        ext = filetype.split("/")[1]

        if (ext in ALLOWED_EXTENSIONS) and (filesize > 10):
            if filename == tracker.get_slot("business_projection"):
                dispatcher.utter_message(text="BUSINESS_PROJECTION AND AML POLICY SHOULD NOT BE THE SAME!!")
                return {"aml_policy": None}
            else:
                dispatcher.utter_message(text=f"Success, Document Received")
                return {"aml_policy": filename}   
        else:
            dispatcher.utter_message(text="Failure, Document not Received")
            return {"aml_policy": None}
     
class ValidateDirectmerchantForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_direct_merchant_form"

    def validate_cac_documents(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate cac documents value."""

        fileInfo = json.loads(slot_value)
        filename, filetype, filesize = fileInfo['name'], fileInfo['type'], fileInfo['size']
        ext = filetype.split("/")[1]

        if (ext in ALLOWED_EXTENSIONS) and (filesize > 10):
            dispatcher.utter_message(text=f"Success. Document Received")
            return {"cac_documents":filename}
        else:
            dispatcher.utter_message(text="Failure, Document not Received")
            return {"cac_documents": None}
        
    def validate_line_of_business(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate Line of Business value."""
        
        if len(slot_value) > 5:
            dispatcher.utter_message(text=f"Success")
            return {"line_of_business": slot_value}
        else:
            dispatcher.utter_message(text="Failure")
            return {"line_of_business": slot_value}
        
    def validate_business_projection(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        
        """Validate Business Projection value."""

        fileInfo = json.loads(slot_value)
        filename, filetype, filesize = fileInfo['name'], fileInfo['type'], fileInfo['size']
        ext = filetype.split("/")[1]

        if (ext in ALLOWED_EXTENSIONS) and (filesize > 10):
            if filename == tracker.get_slot("pci_dss_certificate"):
                dispatcher.utter_message(text="PCIDSS_CERTIFICATE AND BUSINESS_PROJECTION SHOULD NOT BE THE SAME!!")
                return {"business_projection": None}
            else:
                dispatcher.utter_message(text=f"Success, Document Received")
                return {"business_projection": filename}   
        else:
            dispatcher.utter_message(text="Failure, Document not Received")
            return {"business_projection": None}
        

class ValidateShareholderDetailsForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_shareholder_details_form"

    def validate_bvn(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate bvn value."""

        # If the bvn is a number and it is 10 digits
        if slot_value is None:
            return {}
        elif (slot_value.isdigit()) and (len(slot_value) == 10):
            return {"bvn": slot_value}
        else:
            # If the bvn is not valid, set its value to None so that the form will ask for it again
            dispatcher.utter_message(text="This BVN is Invalid.")
            return {"bvn": None}
           
    def validate_phone_no(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate phone_no value."""
        
        if slot_value is None:
            return {}
        # If the phone_no is a number, it is 11 digits, and it begins with a 0
        elif (slot_value.isdigit()) and (len(slot_value) == 11) and (slot_value.startswith('0')):
            return {"phone_no": slot_value}
        else:
            dispatcher.utter_message(text="This Phone Number is invalid.")
            # If the phone_no is not valid, set its value to None so that the form will ask for it again
            return {"phone_no": None}
        
    def validate_valid_id(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate valid_id value."""
        
        fileInfo = json.loads(slot_value)
        filename, filetype, filesize = fileInfo['name'], fileInfo['type'], fileInfo['size']
        ext = filetype.split("/")[1]

        if (ext in ALLOWED_EXTENSIONS) and (filesize > 10):
            dispatcher.utter_message(text=f"Success. Document Received")
            return {"valid_id":filename}
        else:
            dispatcher.utter_message(text="Failure, Document not Received")
            return {"valid_id": None}

class ActionPartnershipForm(Action):
    def name(self) -> Text:
        return "action_partnership_form"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        partnership_type = tracker.get_slot("partnership_type")
        
        if partnership_type == "payment_facilitator":
            return [FollowupAction("payment_facilitator_form")]
        elif partnership_type == "iso_m":
            return [FollowupAction("iso_m_form")]
        else:
            return [FollowupAction("direct_merchant_form")]
        
class ActionNumShareholdersForm(Action):
    def name(self) -> Text:
        return "action_num_shareholders_form"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        bvn = tracker.get_slot("bvn")
        valid_id = tracker.get_slot("valid_id")
        num_shareholders = tracker.get_slot("num_shareholders") or 0

        if bvn and valid_id:
            # If the required slots of the shareholder_details form are filled
            # Increment the num_shareholders slot by 1
            num_shareholders += 1
            # Reset the shareholder_details form
            return [SlotSet("num_shareholders", num_shareholders), SlotSet("name", None), SlotSet("address", None), SlotSet("bvn", None), SlotSet("phone_no", None), SlotSet("valid_id", None), FollowupAction("shareholder_details_form")]
        elif num_shareholders >= 1:
            # If the num_shareholders slot is filled
            # Reset the shareholder_details form
            return [SlotSet("name", None), SlotSet("address", None), SlotSet("bvn", None), SlotSet("phone_no", None), SlotSet("valid_id", None), FollowupAction("shareholder_details_form")]
        else:
            return []
        
# class ActionAskAddShareholder(Action):
#     def name(self) -> Text:
#         return "action_ask_add_shareholder"
#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         dispatcher.utter_message(text="Do you want to add another shareholder?")
#         return []

class ValidateNumShareholders(Action):
    def name(self) -> Text:
        return "action_validate_num_shareholders"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        num_shareholders = tracker.get_slot('num_shareholders')
        if num_shareholders >= 1:
            return [SlotSet("is_valid_num_shareholders", True)]
        else:
            return [SlotSet("is_valid_num_shareholders", False)]
