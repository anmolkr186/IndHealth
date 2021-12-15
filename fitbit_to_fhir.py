# -*- coding: utf-8 -*-
"""fitbit to fhir.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pjjLQerH5H0WnHdBNrBjzfar9hSlJZgr
"""

#Fitbit
Heartrate = {
  "activities-heart": [
    {
      "dateTime": "2019-05-08",
      "value": {
        "customHeartRateZones": [
          {
            "caloriesOut": 1164.09312,
            "max": 90,
            "min": 30,
            "minutes": 718,
            "name": "Below"
          },
          {
            "caloriesOut": 203.65344,
            "max": 110,
            "min": 90,
            "minutes": 74,
            "name": "Custom Zone"
          },
          {
            "caloriesOut": 330.76224,
            "max": 220,
            "min": 110,
            "minutes": 42,
            "name": "Above"
          }
        ],
        "heartRateZones": [
          {
            "caloriesOut": 979.43616,
            "max": 86,
            "min": 30,
            "minutes": 626,
            "name": "Out of Range"
          },
          {
            "caloriesOut": 514.16208,
            "max": 121,
            "min": 86,
            "minutes": 185,
            "name": "Fat Burn"
          },
          {
            "caloriesOut": 197.92656,
            "max": 147,
            "min": 121,
            "minutes": 18,
            "name": "Cardio"
          },
          {
            "caloriesOut": 6.984,
            "max": 220,
            "min": 147,
            "minutes": 5,
            "name": "Peak"
          }
        ],
        "restingHeartRate": 76
      }
    }
  ]
}

Heartrate['activities-heart'][0]['value']['restingHeartRate']

#fitbit functions
def heartrate_tofhir(val ):
  ret = {
  "resourceType": "Observation",
  "id": "heart-rate",
  "meta": {
    "profile": [
      "http://hl7.org/fhir/StructureDefinition/vitalsigns"
    ]
  },
  "status": "final",
  "category": [
    {
      "coding": [
        {
          "system": "http://terminology.hl7.org/CodeSystem/observation-category",
          "code": "vital-signs",
          "display": "Vital Signs"
        }
      ],
      "text": "Vital Signs"
    }
  ],
  "code": {
    "coding": [
      {
        "system": "http://loinc.org",
        "code": "8867-4",
        "display": "Heart rate"
      }
    ],
    "text": "Heart rate"
  },
  "subject": {
    "reference": "Patient/example"
  },
  "effectiveDateTime": "",
  "valueQuantity": {
    "value": 0,
    "unit": "beats/minute",
    "system": "http://unitsofmeasure.org",
    "code": "/min"
  }
  } 
  ret['valueQuantity']['value'] = val['activities-heart'][0]['value']['restingHeartRate']
  ret['effectiveDateTime'] = val['activities-heart'][0]['dateTime']
  return ret

print(heartrate_tofhir(Heartrate))

def fat_tofhir(val):
  ret = {
  "resourceType" : "Observation",
  "id" : "example-16",
  "meta" : {
    "profile" : [
      "https://nrces.in/ndhm/fhir/r4/StructureDefinition/ObservationGeneralAssessment"
    ]
  },
  "text" : {
    "status" : "generated",
    "div" : "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p><b>Narrative with Details</b></p><p><b>id</b>: example-16</p><p><b>status</b>: final</p><p><b>code</b>: Body fat [Mass] Calculated <span>(Details : LOINC code '73708-0' = 'Body fat [Mass] Calculated', given as 'Body fat [Mass] Calculated')</span></p><p><b>subject</b>: ABC</p><p><b>performer</b>: Dr. DEF, MD</p><p><b>value</b>: 6 kg<span> (Details: UCUM code kg = 'kg')</span></p></div>"
  },
  "status" : "final",
  "code" : {
    "coding" : [
      {
        "system" : "http://loinc.org",
        "code" : "73708-0",
        "display" : "Body fat [Mass] Calculated"
      }
    ],
    "text" : "Body fat [Mass] Calculated"
  },
  "subject" : {
    "reference" : "Patient/1"
  },
  "performer" : [
    {
      "reference" : "Practi/1"
    }
  ],
  "valueQuantity" : {
    "value" : 6,
    "unit" : "kg",
    "system" : "http://unitsofmeasure.org",
    "code" : "kg"
  }
  }

  ret['valueQuantity']['value'] = val['fat'][0]['fat']
  return ret

print(fat_tofhir(fat))

fat = {
  "fat": [
    {
      "date": "2019-03-20",
      "fat": 15,
      "logId": 1553067000000,
      "source": "Aria",
      "time": "07:38:14"
    }
  ]
}

def pedo_tofhir(val):
  ret  = {
  "resourceType" : "Observation",
  "id" : "stepcount-example",
  "text" : {
    "status" : "generated",
    "div" : "<div xmlns=\"http://www.w3.org/1999/xhtml\"><p><b>Generated Narrative</b></p><p><b>id</b>: stepcount-example</p><p><b>contained</b>: </p><p><b>identifier</b>: 12341567</p><p><b>status</b>: unknown</p><p><b>category</b>: <span title=\"Codes: {http://snomed.info/sct 68130003}\">Physical activity (observable entity)</span></p><p><b>code</b>: <span title=\"Codes: {http://loinc.org 55423-8}\">Step count</span></p><p><b>subject</b>: <a href=\"#p\">unknown resource contained</a></p><p><b>effective</b>: Apr 16, 2018, 5:00:00 PM --&gt; Apr 23, 2018, 5:00:00 PM</p><p><b>issued</b>: Apr 24, 2018, 10:13:50 AM</p><p><b>device</b>: <span>Jawbone UP API, modality =sensed, sourceCreationDateTime = 2018-04-17T17:13:50Z</span></p><h3>Components</h3><table class=\"grid\"><tr><td>-</td><td><b>Code</b></td><td><b>Value[x]</b></td></tr><tr><td>*</td><td><span title=\"Codes: {http://hl7.org/fhir/observation-statistics maximum}\">Maximum</span></td><td>7939 steps/day</td></tr></table></div>"
  },
  "contained" : [
    {
      "resourceType" : "Patient",
      "id" : "p",
      "identifier" : [
        {
          "system" : "https://omh.org/shimmer/patient_ids",
          "value" : "some-user"
        }
      ]
    }
  ],
  "identifier" : [
    {
      "system" : "https://omh.org/shimmer/ids",
      "value" : "12341567"
    }
  ],
  "status" : "unknown",
  "category" : [
    {
      "coding" : [
        {
          "system" : "http://snomed.info/sct",
          "code" : "68130003",
          "display" : "Physical activity (observable entity)"
        }
      ]
    }
  ],
  "code" : {
    "coding" : [
      {
        "system" : "http://loinc.org",
        "code" : "55423-8",
        "display" : "Number of steps in unspecified time Pedometer"
      }
    ],
    "text" : "Step count"
  },
  "subject" : {
    "reference" : "#p"
  },
  "effectivePeriod" : {
    "start" : "2018-04-17T00:00:00Z",
    "end" : "2018-04-24T00:00:00Z"
  },
  "issued" : "2018-04-24T17:13:50Z",
  "device" : {
    "display" : "Jawbone UP API, modality =sensed, sourceCreationDateTime = 2018-04-17T17:13:50Z"
  },
  "component" : [
    {
      "code" : {
        "coding" : [
          {
            "system" : "http://hl7.org/fhir/observation-statistics",
            "code" : "maximum",
            "display" : "Maximum"
          }
        ],
        "text" : "Maximum"
      },
      "valueQuantity" : {
        "value" : 7939,
        "unit" : "steps/day",
        "system" : "http://unitsofmeasure.org",
        "code" : "{steps}/d"
      }
    }
  ]
  }
  # print(val[])
  ret["component"][0]['valueQuantity']['value'] = val['activities'][0]["steps"]
  return ret



pedo = {
  "activities": [
    {
      "activeDuration": 1536000,
      "activityLevel": [
        {
          "minutes": 3,
          "name": "sedentary"
        },
        {
          "minutes": 9,
          "name": "lightly"
        },
        {
          "minutes": 2,
          "name": "fairly"
        },
        {
          "minutes": 11,
          "name": "very"
        }
      ],
      "activityName": "Walk",
      "activityTypeId": 90013,
      "calories": 204,
      "caloriesLink": "https://api.fitbit.com/1/user/-/activities/calories/date/2019-01-03/2019-01-03/1min/time/12:08/12:34.json",
      "duration": 1536000,
      "elevationGain": 0,
      "lastModified": "2019-01-04T19:31:15.000Z",
      "logId": 19018673358,
      "logType": "auto_detected",
      "manualValuesSpecified": {
        "calories": False,
        "distance": False,
        "steps": False
      },
      "originalDuration": 1536000,
      "originalStartTime": "2019-01-03T12:08:29.000-08:00",
      "startTime": "2019-01-03T12:08:29.000-08:00",
      "steps": 1799,
      "tcxLink": "https://api.fitbit.com/1/user/-/activities/19018673358.tcx"
    }
  ],
  "pagination": {
    "afterDate": "2019-01-01",
    "limit": 1,
    "next": "https://api.fitbit.com/1/user/-/activities/list.json?offset=0&limit=1&sort=asc&afterDate=2019-01-01",
    "offset": 0,
    "previous": "",
    "sort": "asc"
  }
  }

