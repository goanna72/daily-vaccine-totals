import json

import pytest

from daily_vaccine_total_by_state import app


@pytest.fixture()
def alexa_event():
    """ Generates Alexa Event"""

    return {
      "version": "1.0",
      "session": {
        "new": False,
        "sessionId": "amzn1.echo-api.session.xxxx",
        "application": {
          "applicationId": "amzn1.ask.skill.xxxx"
        },
        "attributes": {},
        "user": {
          "userId": "amzn1.ask.account.xxxx"
        }
      },
      "context": {
        "Viewports": [
          {
            "type": "APL",
            "id": "main",
            "shape": "RECTANGLE",
            "dpi": 213,
            "presentationType": "STANDARD",
            "canRotate": False,
            "configuration": {
              "current": {
                "mode": "HUB",
                "video": {
                  "codecs": [
                    "H_264_42",
                    "H_264_41"
                  ]
                },
                "size": {
                  "type": "DISCRETE",
                  "pixelWidth": 1280,
                  "pixelHeight": 800
                }
              }
            }
          }
        ],
        "Viewport": {
          "experiences": [
            {
              "arcMinuteWidth": 346,
              "arcMinuteHeight": 216,
              "canRotate": False,
              "canResize": False
            }
          ],
          "mode": "HUB",
          "shape": "RECTANGLE",
          "pixelWidth": 1280,
          "pixelHeight": 800,
          "dpi": 213,
          "currentPixelWidth": 1280,
          "currentPixelHeight": 800,
          "touch": [
            "SINGLE"
          ],
          "video": {
            "codecs": [
              "H_264_42",
              "H_264_41"
            ]
          }
        },
        "Extensions": {
          "available": {
            "aplext:backstack:10": {}
          }
        },
        "System": {
          "application": {
            "applicationId": "amzn1.ask.skill.xxx"
          },
          "user": {
            "userId": "amzn1.ask.account.xxxx"
          },
          "device": {
            "deviceId": "amzn1.ask.device.xxxx",
            "supportedInterfaces": {}
          },
          "apiEndpoint": "https://api.fe.amazonalexa.com",
          "apiAccessToken": ""
        }
      },
      "request": {
        "type": "IntentRequest",
        "requestId": "amzn1.echo-api.request.5b8f8478-b1e8-4ea1-96b2-52f404a262db",
        "locale": "en-US",
        "timestamp": "2021-10-19T04:57:36Z",
        "intent": {
          "name": "VaccineIntent",
          "confirmationStatus": "NONE",
          "slots": {
            "states": {
              "name": "states",
              "value": "Tasmania",
              "resolutions": {
                "resolutionsPerAuthority": [
                  {
                    "authority": "amzn1.er-authority.echo-sdk.amzn1.ask.skill.xxxx.states",
                    "status": {
                      "code": "ER_SUCCESS_MATCH"
                    },
                    "values": [
                      {
                        "value": {
                          "name": "tasmania",
                          "id": "TAS"
                        }
                      }
                    ]
                  }
                ]
              },
              "confirmationStatus": "NONE",
              "source": "USER"
            }
          }
        },
        "dialogState": "COMPLETED"
      }
    }


def test_lambda_handler(alexa_event, mocker):
    # we should really mock the call to dynamodb
    ret = app.lambda_handler(alexa_event, "")
    assert "The daily vaccine total for Tasmania" in ret['response']['outputSpeech']['ssml']
    
