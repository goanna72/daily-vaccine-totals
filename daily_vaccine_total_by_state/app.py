import boto3
#ddb = boto3.client("dynamodb")
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name


state_fullname = {
    "VIC" : "Victoria",
    "WA" : "Western Australia",
    "SA" : "South Australia",
    "TAS" : "Tasmania",
    "NSW" : "New South Wales",
    "NT" : "Northern Territory",
    "ACT" : "Australian Capital Territory"
}

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        handler_input.response_builder \
            .speak("Welcome to vaccine totals for Australia") \
            .set_should_end_session(False)
        return handler_input.response_builder.response

class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        print(exception)
        handler_input.response_builder.speak("Sorry, there was some problem. Please try again")
        return handler_input.response_builder.response

class VaccineIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("VaccineIntent")(handler_input)

    def handle(self, handler_input):
        state = handler_input.request_envelope.request.intent.slots['states'] \
            .resolutions.resolutions_per_authority[0].values[0].value.id

        dyndb = boto3.resource('dynamodb', region_name='ap-southeast-2')
        table = dyndb.Table('Vaccines')
        state_upper = state.upper()
        pop = table.get_item(Key={'MeasureName': f"{state_upper} - Population 16 and over"})
        result2 = pop['Item']
        statepop = result2['Total']
        vaccinepop = table.get_item(Key={'MeasureName': f"{state_upper} - Residence state - Number of people 16 and over fully vaccinated"})
        result3 = vaccinepop['Item']
        statefullpop = result3['Total']
        percentage2 = statefullpop / statepop
        percentage = format(percentage2 * 100, '.2f')
        data = table.get_item(Key={'MeasureName': f"{state_upper} - Administration state - Daily increase doses recorded"})
        result = data['Item']
        statename = state_fullname[state_upper]

        speech_text = "The daily vaccine totals for " + statename + " is " + str(result['Total']) + ". " + str(percentage) + "% of the eligible " + state + " population are fully vaccinated"
        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response

sb = SkillBuilder()
sb.add_request_handler(LaunchRequestHandler())
sb.add_exception_handler(CatchAllExceptionHandler())
sb.add_request_handler(VaccineIntentHandler())

def lambda_handler(event, context):
    return sb.lambda_handler()(event, context)
