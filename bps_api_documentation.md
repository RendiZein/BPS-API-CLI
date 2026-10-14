Homepage
Domain
Subject
Subject Categories
Dynamic Data
Data
List Derived Period Data
List Derived Variable
List Period Data
List Unit Data
List Variable
List Vertical Variable
Census Data
SIMDASI
Static Table
Detail Static Table
List All Static Table
CSA Subject
Press Release
Detail Press Release
List All Press Release
Publication
Detail Publication
List All Publication
Strategic Indicator
Infographic
Glosarium
Foreign Trade Data
Sustainable Development Goals
SDDS
Statistical Classifications
Searching
News
Detail News
List All BPS News
List News Category
Badan Pusat Statistik
API Documentation
The BPS APIs provides programmatic access to read BPS data. User can read about Publication, Press Release, BPS Event, and a lot of various kinds of data presented in the static table and dynamic tables. The BPS API identifies user with key token. User can get the key token from API-Portal website. Every user can get two until three key token to access the API. Responses are available in JSON.

Domain
This service is used to displays all BPS Statistics domain website
https://webapi.bps.go.id/v1/api/domain

Parameter
FieldTypeDescriptiontypeStringType to show domain (all:for all domain ; prov:for province domain ; kab:for city/regency domain ; kabbyprov:for all city/regency in province)
Allowed values: "all", "prov", "kab", "kabbyprov"
prov optionalStringProv ID selected to show all city/regency domain. input this parameter when using "kabbyprov" type.
Size range: 4
keyStringKey app to access API
Send a Sample Request

Success 200
FieldTypeDescriptionstatusStringReturn status, OK if success and Error if any error occured.
data-availabilityStringAvailability status of list domain.
dataObject[]Response Data
  0ObjectInformation status
    pageNumberInformation page
    pagesNumberInformation total page
    per_pageNumbersum of per page
    countNumbercount on this return list
    totalNumbertotal page
  1ObjectList Domain
    domain_idStringID domain
    domain_nameStringname of domain
    domain_urlStringURL domain

Success Response
HTTP/1.1 200 OK
            {
              "status": "OK",
              "data-availability": "available",
              "data":[{
              "page":1,
              "pages":1,
              "total":3
            },
            [{
            "domain_id":"0000",
            "domain_name":"Pusat",
            "domain_url":"https://www.bps.go.id"
          },{
          "domain_id":"1100",
          "domain_name":"Aceh",
          "domain_url":"https://aceh.bps.go.id"
        },{
        "domain_id":"1200",
        "domain_name":"Sumatera Utara",
        "domain_url":"https://sumut.bps.go.id",
      }]
      ]

    }

Error 4xx
NameDescriptionUserNotFoundThe id of the User was not found.

Error Response
HTTP/1.1 404 Not Found
      {
        "error": "UserNotFound"
      }

Subject
List of All Subject
This service is used to displays all subject data on the website
https://webapi.bps.go.id/v1/api/list/

Parameter
FieldTypeDescriptionmodelStringModel to display Subject Data (subject) for subject is "subject"
lang optionalStringLanguage to display subject
Default value: ind
Allowed values: "ind", "eng"
domainNumberDomains that will be displayed subject (see master domain)
Allowed values: 4
subcat optionalNumberSubject categories selected to display subject data
Allowed values: 1, 2, 3, 4, ..., n
page optionalNumberPage to display subject
Allowed values: 1, 2, 3, 4, ..., n
keyStringKey app to access API
Send a Sample Request

Success 200
FieldTypeDescriptionstatusStringReturn status, OK if success and Error if any error occured.
data-availabilityStringAvailability status of list subject.
dataObject[]Response Data
  0ObjectInformation status
    pageNumberInformation page
    pagesNumberInformation total page
    per_pageNumbersum of per page
    countNumbercount on this return list
    totalNumbertotal page
  1ObjectList subject
    sub_idNumberID unique of subject
    titleStringTitle of subject
    subcat_idStringID unique of sub category
    subcatStringName of sub category
    ntableNumberSum of table on each subject

Success Response
HTTP/1.1 200 OK
{
  "status": "OK",
  "data-availability": "available",
  "data": [
    {
      "page": 1,
      "pages": 5,
      "per_page": 10,
      "count": 10,
      "total": 48
    },
    [
      {
        "sub_id": 40,
        "title": "Gender",
        "subcat_id": 1,
        "subcat": "Sosial dan Kependudukan",
        "ntabel": null
      }, ...
    ]

}

Error 4xx
NameDescriptionUserNotFoundThe id of the User was not found.

Error Response
HTTP/1.1 404 Not Found
  {
    "error": "UserNotFound"
  }

Subject Categories
List of All Subject Categories
This service is used to displays all subject data categories on the website
https://webapi.bps.go.id/v1/api/list/

Parameter
FieldTypeDescriptionmodelStringModel to display Subject Categories (subcat) for subcat is "subcat"
lang optionalStringLanguage to display subject category
Default value: ind
Allowed values: "ind", "eng"
domainNumberDomains that will be displayed subcat (see master domain)
Size range: 4
page optionalNumberPage to display subcat
Allowed values: 1, 2, 3, 4, ..., n
keyStringKey app to access API
Send a Sample Request

Success 200
FieldTypeDescriptionstatusStringReturn status, OK if success and Error if any error occured.
data-availabilityStringAvailability status of list subcat.
dataObject[]Response Data
  0ObjectInformation status
    pageNumberInformation page
    pagesNumberInformation total page
    per_pageNumbersum of per page
    countNumbercount on this return list
    totalNumbertotal page
  1ObjectList subcat
    subcat_idNumberID unique of subcat
    titleStringTitle of subcat

Success Response
HTTP/1.1 200 OK
{
  "status": "OK",
  "data-availability": "available",
  "data": [
    {
      "page": 1,
      "pages": 1,
      "per_page": 10,
      "count": 4,
      "total": 4
    },
    [
      ...
      {
        "subcat_id": 1,
        "title": "Sosial dan Kependudukan"
      },
      ...
    ]
  ]
}

Error 4xx
NameDescriptionUserNotFoundThe id of the User was not found.

Error Response
HTTP/1.1 404 Not Found
  {
    "error": "UserNotFound"
  }

Dynamic Data
Data
This service is used to displays data of dynamic table in the website
https://webapi.bps.go.id/v1/api/list

Parameter
FieldTypeDescriptionmodelStringModel to display Data for variable is "data"
lang optionalStringLanguage to display data
Default value: ind
Allowed values: "ind", "eng"
domainNumberDomains that will be displayed variable (see master domain)
Size range: 4
varNumberVariable ID selected to display data
Allowed values: 1, 2, 3, 4, ..., n
turvar optionalNumberDerived Variable ID selected to display data
Allowed values: 1, 2, 3, 4, ..., n
vervar optionalNumberVertical Variable ID selected to display data
Allowed values: 1, 2, 3, 4, ..., n
thNumberPeriod data ID selected to display data
Allowed values: 1, 2;3, 2:6
turth optionalNumberDerived Period Data ID selected to display data
Allowed values: 1, 2;3, 2:6
keyStringKey app to access API
Send a Sample Request

Success 200
FieldTypeDescriptionstatusStringReturn status, OK if success and Error if any error occured.
data-availabilityStringAvailability status of list subject.
varNumberVariable ID
turvarNumberDerived Variable ID
labelvervarNumberTitle of Vertical Variable
vervarNumberVertical Variable ID
tahunNumberPeriod of Data
turtahunNumberDerived period data
datacontentObjectData

Success Response
HTTP/1.1 200 OK
{
  "status": "OK",
  "data-availability": "available",
  "data": [
    {
      "val": 145,
      "label": "Persentase Rumah Tangga Menurut Provinsi dan Sumber Penerangaan",
      "unit": "Persen",
      "subj": "Lingkungan Hidup",
      "def": "",
      "decimal": "",
      "note": "- Sumber: Diolah dari Hasil Survei Sosial Ekonomi Nasional (Susenas), BPS.\n<br>- Tahun 2000 Tidak termasuk Dista Aceh dan Maluku\n<br>- Tahun 2006 Tanpa kabupaten Bantul \n<br>-Data dikutip dari Publikasi Statistik Indonesia.\n"
    }
  ],
  "turvar": [
    {
      "val": 289,
      "label": "Listrik PLN"
    },
    ...
  ],
  "labelvervar": "Provinsi",
  "vervar": [
    {
      "val": 9999,
      "label": "INDONESIA"
    },
    ...
  ],
  "tahun": [
    {
      "val": 100,
      "label": "2000"
    },
    ...
  ],
  "turtahun": [
    {
      "val": 0,
      "label": "Tahun"
    },
    ...
  ],
  "metadata": {
    "activity": null,
    ...
  },
  "datacontent": {
    "99991452891000": 83.68,
    ...
  }
}

Error 4xx
NameDescriptionUserNotFoundThe id of the User was not found.

Error Response
HTTP/1.1 404 Not Found
    {
      "error": "UserNotFound"
    }

List Derived Period Data
This service is used to displays all derived period data on dynamic table in the website
https://webapi.bps.go.id/v1/api/list

Parameter
FieldTypeDescriptionmodelStringModel to display derived period data for derived period data is "turth"
lang optionalStringLanguage to display derived period data
Default value: ind
Allowed values: "ind", "eng"
domainNumberDomains that will be displayed derived period data (see master domain)
Size range: 4
var optionalNumberVariable ID selected to display derived period data
Allowed values: 1, 2, 3, 4, ..., n
page optionalNumberPage to display derived period data
Allowed values: 1, 2, 3, 4, ..., n
keyStringKey app to access API
Send a Sample Request

Success 200
FieldTypeDescriptionstatusStringReturn status, OK if success and Error if any error occured.
data-availabilityStringAvailability status of list subject.
dataObject[]Response Data
  0ObjectInformation status
    pageNumberInformation page
    pagesNumberInformation total page
    per_pageNumbersum of per page
    countNumbercount on this return list
    totalNumbertotal page
  1ObjectList subject
    turth_idStringID unique of subject
    turthStringTitle of subject
    group_turth_idStringID unique of subject
    name_group_turthStringTitle of subject

Success Response
HTTP/1.1 200 OK
      {
        "status": "OK",
        "data-availability": "available",
        "data":[{
        "page":1,
        "pages":230,
        "per_page":10,
        "count":10,
        "total":2300
      },
      [{
      "turth_id":0,
      "turth":"Tahun",
      "group_turth_id":0,
      "name_group_turth":"Tahunan"
    },{
    "turth_id":1,
    "turth":"Bulanan",
    "group_turth_id":1,
    "name_group_turth":"January"
  },{
  "turth_id":2,
  "turth":"Bulanan",
  "group_turth_id":2,
  "name_group_turth":"February"
}]
]

}

Error 4xx
NameDescriptionUserNotFoundThe id of the User was not found.

Error Response
HTTP/1.1 404 Not Found
  {
    "error": "UserNotFound"
  }

List Derived Variable
This service is used to displays all derived variable on dynamic table in the website
https://webapi.bps.go.id/v1/api/list

Parameter
FieldTypeDescriptionmodelStringModel to display derived variable for derived variable is "turvar"
lang optionalStringLanguage to display derived variable
Default value: ind
Allowed values: "ind", "eng"
domainNumberDomains that will be displayed variable (see master domain)
Size range: 4
var optionalNumberVariable selected to display derived variable
Allowed values: 1, 2, 3, 4, ..., n
group optionalNumberGroup Vertical Variable selected to display derived variable
Allowed values: 1, 2, 3, 4, ..., n
nopage optionalBooleanparam to show with no pagination (1 if want to no pagination)
Allowed values: 0, 1
page optionalNumberPage to display derived variable
Allowed values: 1, 2, 3, 4, ..., n
keyStringKey app to access API
Send a Sample Request

Success 200
FieldTypeDescriptionstatusStringReturn status, OK if success and Error if any error occured.
data-availabilityStringAvailability status of list derived variable.
dataObject[]Response Data
  0ObjectInformation status
    pageNumberInformation page
    pagesNumberInformation total page
    per_pageNumbersum of per page
    countNumbercount on this return list
    totalNumbertotal page
  1ObjectList derived variable
    turvar_idNumberID unique of derived variable
    turvarStringTitle of derived variable
    group_turvar_idNumberID unique of item group derived variable
    name_group_turvarStringGroup Name of derived variable *

Success Response
HTTP/1.1 200 OK
{
  "status": "OK",
  "data-availability": "available",
  "data":[{
     "page":1,
     "pages":230,
     "per_page":10,
     "count":10,
     "total":2300
     },
     [{
         "turvar_id":3200,
         "turvar":"Title of vertical variable",
         "group_turvar_id":"Group Name",
         "name_group_turvar":"Wilayah Provinsi"
     },{
         "turvar_id":3200,
         "turvar":"Title of vertical variable",
         "group_turvar_id":"Group Name",
         "name_group_turvar":"Wilayah Provinsi"
     }]
  ]
    
}

Error 4xx
NameDescriptionUserNotFoundThe id of the User was not found.

Error Response
HTTP/1.1 404 Not Found
  {
    "error": "UserNotFound"
  }

List Period Data
This service is used to displays all period data on dynamic table in the website
https://webapi.bps.go.id/v1/api/list

Parameter
FieldTypeDescriptionmodelStringModel to display period data for variable is "th"
lang optionalStringLanguage to display period data
Default value: ind
Allowed values: "ind", "eng"
domainNumberDomains that will be displayed variable (see master domain)
Size range: 4
var optionalNumberVariable ID selected to display period data
Allowed values: 1, 2, 3, 4, ..., n
page optionalNumberPage to display subject
Allowed values: 1, 2, 3, 4, ..., n
keyStringKey app to access API
Send a Sample Request

Success 200
FieldTypeDescriptionstatusStringReturn status, OK if success dan Error if any error occured.
data-availabilityStringAvailability status of list subject.
dataObject[]Response Data
  0ObjectInformation status
    pageNumberInformation page
    pagesNumberInformation total page
    per_pageNumbersum of per page
    countNumbercount on this return list
    totalNumbertotal page
  1ObjectList subject
    th_idNumberID unique of period data
    thStringTitle of period data

Success Response
HTTP/1.1 200 OK
{
  "status": "OK",
  "data-availability": "available",
  "data":[{
     "page":1,
     "pages":230,
     "per_page":10,
     "count":10,
     "total":2300
     },
     [{
         "th_id":117,
         "th":2017
     },{
         "th_id":116,
         "th":2016
     },{
         "th_id":115,
         "th":2015
     }]
  ]
    
}

Error 4xx
NameDescriptionUserNotFoundThe id of the User was not found.

Error Response
HTTP/1.1 404 Not Found
  {
    "error": "UserNotFound"
  }

List Unit Data
This service is used to displays all unit data on dynamic table in the website
https://webapi.bps.go.id/v1/api/list

Parameter
FieldTypeDescriptionmodelStringModel to display unit data for unit data is "unit"
lang optionalStringLanguage to display unit data
Default value: ind
Allowed values: "ind", "eng"
domainNumberDomains that will be displayed unit data(see master domain)
Size range: 4
page optionalNumberPage to display unit data
Allowed values: 1, 2, 3, 4, ..., n
keyStringKey app to access API
Send a Sample Request

Success 200
FieldTypeDescriptionstatusStringReturn status, OK if success and Error if any error occured.
data-availabilityStringAvailability status of list unit data.
dataObject[]Response Data
  0ObjectInformation status
    pageNumberInformation page
    pagesNumberInformation total page
    per_pageNumbersum of per page
    countNumbercount on this return list
    totalNumbertotal page
  1ObjectList unit data
    unit_idNumberID unique of unit data
    unitStringTitle of unit data

Success Response
HTTP/1.1 200 OK
{
  "status": "OK",
  "data-availability": "available",
  "data":[{
     "page":1,
     "pages":230,
     "per_page":10,
     "count":10,
     "total":2300
     },
     [{
         "unit_id":45678,
         "unit":"Title of unit",
     },{
         "unit_id":45678,
         "unit":"Title of unit",
     }]
  ]
    
}

Error 4xx
NameDescriptionUserNotFoundThe id of the User was not found.

Error Response
HTTP/1.1 404 Not Found
  {
    "error": "UserNotFound"
  }

List Variable
This service is used to displays all variable on dynamic table in the website
https://webapi.bps.go.id/v1/api/list

Parameter
FieldTypeDescriptionmodelStringModel to display variable Data (subject) for variable is "var"
lang optionalStringLanguage to display variable
Default value: ind
Allowed values: "ind", "eng"
domainNumberDomains that will be displayed variable (see master domain)
Allowed values: 4
subject optionalNumberSubject ID selected to display subject data
Allowed values: 1, 2, 3, 4, ..., n
page optionalNumberPage to display subject
Allowed values: 1, 2, 3, 4, ..., n
year optionalNumberYear selected to display statictable
Allowed values: 1, 2, 3, 4, ..., n
area optionalBooleanParameter to show exist variabel on domain (1 if show exist var)
Allowed values: 0, 1
vervar optionalNumberVertical Variabel ID selected
Allowed values: 1, 2, 3, 4, ..., n
keyStringKey app to access API
Send a Sample Request

Success 200
FieldTypeDescriptionstatusStringReturn status, OK if success and Error if any error occured.
data-availabilityStringAvailability status of list variable.
dataObject[]Response Data
  0ObjectInformation status
    pageNumberInformation page
    pagesNumberInformation total page
    per_pageNumbersum of per page
    countNumbercount on this return list
    totalNumbertotal page
  1ObjectList variable
    var_idNumberID unique of variable
    titleStringTitle of variable
    sub_idNumberID unique of variable
    sub_nameStringTitle of variable
    defStringDefinition of Variable
    notesStringNotes for Variable
    verticalNumberID vertical variable
    unitStringUnit Metric
    graph_idNumberID graph
    graph_nameStringgraph name

Success Response
HTTP/1.1 200 OK
{
  "status": "OK",
  "data-availability": "available",
  "data":[{
     "page":1,
     "pages":230,
     "per_page":10,
     "count":10,
     "total":2300
     },
     [{
         "var_id":45678,
         "title":"Title of variable",
         "sub_id":45,
         "sub_name":"Subject Name",
         "def":"definition",
         "notes":"notes",
         "vertical":3,
         "unit":"Billion",
         "graph_id":3,
         "graph_name":"Line",
     },{
          "var_id":458,
         "title":"Title of variable 2",
         "sub_id":45,
         "sub_name":"Subject Name",
         "def":"definition",
         "notes":"notes",
         "vertical":3,
         "unit":"Billion",
         "graph_id":3,
         "graph_name":"Line",
     }]
  ]
    
}

Error 4xx
NameDescriptionUserNotFoundThe id of the User was not found.

Error Response
HTTP/1.1 404 Not Found
  {
    "error": "UserNotFound"
  }

List Vertical Variable
This service is used to displays all vertical variable on dynamic table in the website
https://webapi.bps.go.id/v1/api/list

Parameter
FieldTypeDescriptionmodelStringModel to display vertical variable Data for vertical variable is "vervar"
lang optionalStringLanguage to display vertical variable
Default value: ind
Allowed values: "ind", "eng"
domainNumberDomains that will be displayed variable (see master domain)
Allowed values: 4
var optionalNumberVariable selected to display vertical variable
Allowed values: 1, 2, 3, 4, ..., n
page optionalNumberPage to display vertical variable
Allowed values: 1, 2, 3, 4, ..., n
keyStringKey app to access API
Send a Sample Request

Success 200
FieldTypeDescriptionstatusStringReturn status, OK if success and Error if any error occured.
data-availabilityStringAvailability status of list vertical variable.
dataObject[]Response Data
  0ObjectInformation status
    pageNumberInformation page
    pagesNumberInformation total page
    per_pageNumbersum of per page
    countNumbercount on this return list
    totalNumbertotal page
  1ObjectList vertical variable
    vervar_idNumberID unique of vertical variable
    vervarStringTitle of vertical variable
    item_ver_idNumberID unique of item vertical variable
    group_ver_idNumberID unique of Group vertical variable
    name_group_ver_idStringGroup Name of vertical variable *

Success Response
HTTP/1.1 200 OK
{
  "status": "OK",
  "data-availability": "available",
  "data":[{
     "page":1,
     "pages":230,
     "per_page":10,
     "count":10,
     "total":2300
     },
     [{
         "vervar_id":3200,
         "vervar":"Title of vertical variable",
         "item_ver_id":45,
         "group_ver_id":"Group Name",
         "name_group_ver_id":"Wilayah Provinsi"
     },{
         "vervar_id":3200,
         "vervar":"Title of vertical variable",
         "item_ver_id":45,
         "group_ver_id":"Group Name",
         "name_group_ver_id":"Wilayah Provinsi"
     }]
  ]
    
}

Error 4xx
NameDescriptionUserNotFoundThe id of the User was not found.

Error Response
HTTP/1.1 404 Not Found
  {
    "error": "UserNotFound"
  }

Census Data (sensus.bps.go.id)
List of Census Events
This service is used to return a list of events included in the Census Web
https://webapi.bps.go.id/v1/api/interoperabilitas/datasource/sensus/id/37/

Parameter
FieldTypeDescriptionidNumberId number of the service. To display a list of events that is included in the Census, use code 37.
keyStringKey app to access API
Send a Sample Request

Success 200
FieldTypeDescriptionstatusStringReturn status, OK if success and Error if any error occured.
data-availabilityStringAvailability status of events list
dataObject[]Response Data
  0ObjectInformation status
    pageNumberInformation page
    pagesNumberInformation total page
    per_pageNumbersum of per page
    countNumbercount on this return list
    totalNumbertotal page
  1ObjectList events
    idNumberID of Event
    kegiatanStringName of Event
    tahun_kegiatanNumberYear of Event

Success Response
HTTP/1.1 200 OK
{
  "status": "OK",
  "data-availability": "available",
  "data": [
    {
      "page": 1,
      "pages": 1,
      "per_page": 1,
      "count": 1,
      "total": 1
    },
    [
      {
        "id": {{id of event}},
        "kegiatan": {{name of event}},
        "tahun_kegiatan": {{year of event}}
      },
     …
    ]
  ]
}

Error 4xx
FieldTypeDescriptionStatusStringReturn status, OK if success and Error if any error occurred.
Data-availibilityStringAvailability status of events list

Error Response

{
  "status": "Error",
  "data-availability": "not-available",
  "data": [
    {
      "page": 1,
      "pages": 0,
      "per_page": 25,
      "count": 0,
      "total": 0
    },
    []
  ]
}

Data Topics in the Census
This service is used to display the data topics available in the census that we choose.
https://webapi.bps.go.id/v1/api/interoperabilitas/datasource/sensus/id/38/

Parameter
FieldTypeDescriptionidNumberId number of the service. To display a list of data topics that is included in the Census, use code 38.
KegiatanStringID of census event that we choose to display the data topics, use service list of events to get the ID. Example: sp2020
keyStringKey app to access API
Send a Sample Request

Success 200
FieldTypeDescriptionstatusStringReturn status, OK if success and Error if any error occured.
data-availabilityStringAvailability status of Data Topics
dataObject[]Response Data
  0ObjectInformation status
    pageNumberInformation page
    pagesNumberInformation total page
    per_pageNumbersum of per page
    countNumbercount on this return list
    totalNumbertotal page
  1ObjectList Data Topics
    idNumberID of Data Topics
    topikStringName of Data Topic in Bahasa
    topicStringName of Data Topic in English
    id_kegiatanNumberID of Events
    kegiatanStringName of event in Bahasa
    eventStringName of event in English
    alias_kegiatanStringAlias of event in Bahasa
    alias_eventStringAlias of event in English

Success Response
HTTP/1.1 200 OK
{
  "status": "OK",
  "data-availability": "available",
  "data": [
    {
      "page": 1,
      "pages": 1,
      "per_page": 1,
      "count": 1,
      "total": 1
    },
    [
      {
        "id": {{id of Data Topic}},
        "topik": {{name of Data topic in bahasa}},
        "topic": {{name of Data topic in english}},
        "id_kegiatan": {{Id of event}},
        "kegiatan": {{Name of event in Bahasa}},
        "event": {{Name of event in English}},
        "alias_kegiatan": {{Alias of event in Bahasa}},
        "alias_event": {{Alias of event in English}}
      }
    ]
  ]
}

Error 4xx
FieldTypeDescriptionStatusStringReturn status, OK if success and Error if any error occurred.
Data-availibilityStringAvailability status of data topics

Error Response

{
  "status": "Error",
  "data-availability": "not-available",
  "data": [
    {
      "page": 1,
      "pages": 0,
      "per_page": 25,
      "count": 0,
      "total": 0
    },
    []
  ]
}

List of Census Event Areas
This service is used to return a list of areas in the Census Event
https://webapi.bps.go.id/v1/api/interoperabilitas/datasource/sensus/id/38/

Parameter
FieldTypeDescriptionidNumberId number of the service. To display a list of census event areas, use code 39.KegiatanStringID of census event that we choose to display the census event areas, use service list of events to get the ID. Example: sp2020
keyStringKey app to access API
Send a Sample Request

Success 200
FieldTypeDescriptionstatusStringReturn status, OK if success and Error if any error occured.
data-availabilityStringAvailability status of Census Event Area
dataObject[]Response Data
  0ObjectInformation status
    pageNumberInformation page
    pagesNumberInformation total page
    per_pageNumbersum of per page
    countNumbercount on this return list
    totalNumbertotal page
  1ObjectList of Area
    idNumberID of area
    kode_mfdStringMFD Code of area
    namaStringName of area
    slugString-

Success Response
HTTP/1.1 200 OK
{
  "status": "OK",
  "data-availability": "available",
  "data": [
    {
      "page": 1,
      "pages": 1,
      "per_page": 1,
      "count": 1,
      "total": 1
    },
    [
      {
        "id": {{ ID of Census Event Area}},
        "kode_mfd": {{ MFD CODE}},
        "nama": {{ Name of area }},
        "slug": -
      },

Error 4xx
FieldTypeDescriptionStatusStringReturn status, OK if success and Error if any error occurred.
Data-availibilityStringAvailability status of census event area

Error Response

{
  "status": "Error",
  "data-availability": "not-available",
  "data": [
    {
      "page": 1,
      "pages": 0,
      "per_page": 25,
      "count": 0,
      "total": 0
    },
    []
  ]
}

List of Available Dataset based on Event and Data Topic
This service is used to return a list of events included in the Census
https://webapi.bps.go.id/v1/api/interoperabilitas/datasource/sensus/id/40/

Parameter
FieldTypeDescriptionidNumberId number of the service. To display a list of available dataset, use code 40.KegiatanStringID of census event that we choose to display the census dataset, use service list of events to get the ID. Example: sp2020
TopikNumberID of Data topic, use service list of data topics to get the ID.
keyStringKey app to access API
Send a Sample Request

Success 200
FieldTypeDescriptionstatusStringReturn status, OK if success and Error if any error occured.
data-availabilityStringAvailability status of Dataset
dataObject[]Response Data
  0ObjectInformation status
    pageNumberInformation page
    pagesNumberInformation total page
    per_pageNumbersum of per page
    countNumbercount on this return list
    totalNumbertotal page
  1ObjectList of Dataset
    idNumberID of dataset
    id_topikNumberID of data topic
    topicStringName of data topic
    id_kegiatanNumberID of census event
    NamaStringName of dataset
    deskripsiStringDescription of dataset

Success Response
HTTP/1.1 200 OK
{
  "status": "OK",
  "data-availability": "available",
  "data": [
    {
      "page": 1,
      "pages": 1,
      "per_page": 1,
      "count": 1,
      "total": 1
    },
    [
      {
        "id": {{ Id of dataset }},
        "id_topik": {{ Id of data topic }},
        "topik": {{ Name of data topic }},
        "id_kegiatan": {{ Id of Census Event }},
        "nama": {{ Name of dataset }},
        "deskripsi": {{ Description of dataset }}
      }
 ]
}

Error 4xx
FieldTypeDescriptionStatusStringReturn status, OK if success and Error if any error occurred.
Data-availibilityStringAvailability status of dataset

Error Response

{
  "status": "Error",
  "data-availability": "not-available",
  "data": [
    {
      "page": 1,
      "pages": 0,
      "per_page": 25,
      "count": 0,
      "total": 0
    },
    []
  ]
}

Census Data
This service is used to return census data
https://webapi.bps.go.id/v1/api/interoperabilitas/datasource/sensus/id/41/

Parameter
FieldTypeDescriptionidNumberId number of the service. To display census data based on ID of Census Event, Id of Census Area, and ID of Dataset, use code 41.KegiatanStringID of census event that we choose to display the census dataset, use service list of events to get the ID. Example: sp2020
Wilayah_sensusNumberID of Census Event Area, use service list of census event area to get the ID.
DatasetNumberID of Dataset, use service list of census dataset to get the ID.
keyStringKey app to access API
Send a Sample Request

Success 200
FieldTypeDescriptionstatusStringReturn status, OK if success and Error if any error occured.
data-availabilityStringAvailability status of Data
dataObject[]Response Data
  0ObjectInformation status
    pageNumberInformation page
    pagesNumberInformation total page
    per_pageNumbersum of per page
    countNumbercount on this return list
    totalNumbertotal page
  1ObjectData Details
    timestampdateLast Sync
    statusStringStatus of availability
    data_countStringCount of the data
    dataobject[]Data content
      id_wilayahnumberID of area
      kode_wilayahnumberArea code
      nama_wilayahstringName of area
      level_wilayahnumberAdministration level of area
      id_indikatornumberID of indicator
      nama_indikatornumberName of indikator
      id_kategori_xnumberID of indicator x-th category
      name_kategori_xstringName of indicator x-th category
      id_item_kategori_xnumberID of indicator x-th category item
      kode_item_kategori_xnumberCode of indicator x-th category item
      nama_item_kategori_xstringName of indicator x-th category item
      PeriodnumberYear of indicator
      nilainumberValue of indicator

Success Response
HTTP/1.1 200 OK

  "status": "OK",
  "data-availability": "available",
  "data": [
    {
      "page": 1,
      "pages": 1,
      "per_page": 1,
      "count": 1,
      "total": 1
    },
    {
      "timestamp": "2022-07-11T10:35:03.125",
      "status": 200,
      "data_count": 315,
      "data": [
        {
          "id_wilayah": "8f42c43e-051c-482b-84cf-285bc4606075",
          "kode_wilayah": "11",
          "nama_wilayah": "ACEH",
          "level_wilayah": 1,
          "id_indikator": "4700ed90-4a9a-46a4-9ccf-54ee556e2691",
          "nama_indikator": "Jumlah Penduduk Menurut Wilayah, Kesesuaian Alamat KK/KTP dengan Tempat Tinggal, dan Jenis Kelamin",
          "id_kategori_1": "d1332a64-cca8-4cdf-84e6-c79ca1e66910",
          "nama_kategori_1": "Klasifikasi Kesesuaian Alamat KK-KTP 2020",
          "id_item_kategori_1": "982b2f23-92bc-4fdc-83ea-2ebdfd478c52",
          "kode_item_kategori_1": "1",
          "nama_item__kategori_1": "Ya",
          "id_kategori_2": "05996fef-eaba-43ba-a917-c41108eaac6c",
          "nama_kategori_2": "Klasifikasi Jenis Kelamin 2010",
          "id_item_kategori_2": "3fccb669-2819-483a-8cb4-19b6aea53fe4",
          "kode_item_kategori_2": "L",
          "nama_item__kategori_2": "Laki-laki",
          "id_kategori_3": "",
          "nama_kategori_3": "",
          "id_item_kategori_3": "",
          "kode_item_kategori_3": "",
          "nama_item__kategori_3": "",
          "id_kategori_4": "",
          "nama_kategori_4": "",
          "id_item_kategori_4": "",
          "kode_item_kategori_4": "",
          "nama_item__kategori_4": "",
          "period": "2020",
          "nilai": "2523198.0"
        },
]

Error 4xx
FieldTypeDescriptionStatusStringReturn status, OK if success and Error if any error occurred.
Data-availibilityStringAvailability status of data

Error Response

{
  "status": "Error",
  "data-availability": "not-available",
  "data": [
    {
      "page": 1,
      "pages": 0,
      "per_page": 25,
      "count": 0,
      "total": 0
    },
    []
  ]
}

SIMDASI (Sistem Informasi Manajemen Data Statistik Terintegrasi)
Indonesian Statistics (SI) and Regional In Numbers (DDA) publications are BPS-issued publications that are of interest and attention by the public. At the moment the publication is available at www.bps.go.id. BPS continues to strive to improve the quality of SI and DDA through the Integrated Statistical Data Management Information System (SIMDASI).
List of 7 Digit MFD Code of Province
This service used to view the 7 Digit MFD Code of Province that is used in wilayah parameter in other SIMDASI WebAPI Parameter
https://webapi.bps.go.id/v1/api/interoperabilitas/datasource/simdasi/id/26/

Parameter
FieldTypeDescriptionkeyStringKey app to access API
Send a Sample Request

List of 7 Digit MFD Code of Regency
This service used to view the 7 Digit MFD Code of Regency that is used in wilayah parameter in other SIMDASI WebAPI Parameter
https://webapi.bps.go.id/v1/api/interoperabilitas/datasource/simdasi/id/27/

Parameter
FieldTypeDescriptionparentString7 Digit MFD code of Province, use service List of 7 Digit MFD Code of Province to get the code
keyStringKey app to access API
Send a Sample Request

List of 7 Digit MFD Code of District
This service used to view the 7 Digit MFD Code of District that is used in wilayah parameter in other SIMDASI WebAPI Parameter
https://webapi.bps.go.id/v1/api/interoperabilitas/datasource/simdasi/id/28/

Parameter
FieldTypeDescriptionparentString7 Digit MFD code of Regency, use service List of 7 Digit MFD Code of Regency to get the code
keyStringKey app to access API
Send a Sample Request

List of SIMDASI Subject
This service used to view a list of subjects or chapters used in SIMDASI
https://webapi.bps.go.id/v1/api/interoperabilitas/datasource/simdasi/id/22/

Parameter
FieldTypeDescriptionwilayahString7 digit MFD Code of Area. Example for DKI Jakarta use 3100000
keyStringKey app to access API
Send a Sample Request

Success 200
FieldTypeDescriptionstatusStringReturn status, OK if success and Error if any error occured.
data-availabilityStringAvailability status
dataObject[]Response Data
  0ObjectInformation status
    pageNumberInformation page
    pagesNumberInformation total page
    per_pageNumbersum of per page
    countNumbercount on this return list
    totalNumbertotal page
  1ObjectObject
  dataObjectList of subject
    idStringID unique of subject
    babStringName of chapter in bahasa
    bab_enStringName of chapter in english
    subjectStringName of subject in bahasa
    subject_enStringName of subject in english
    mms_idNumberMMS ID of subject. This ID may be used in other endpoint as parameter of ID Subject. (MMS - Metadata Management system)
    mms_subjectStringCSA Subject name that is used in MMS
    tabelObjectList of ID Table in this subject

Success Response

HTTP/1.1 200 OK
{
  "status": "OK",
  "data-availability": "available",
  "data": [
    {
      "page": 1,
      "pages": 1,
      "per_page": 1,
      "count": 1,
      "total": 1
    },
    {
      "status": 200,
      "condition": "OK",
      "message": "-",
      "created": "2022-08-01 11:33:33",
      "induk": "0000000",
      "wilayah": "Indonesia",
      "data": [
        {
          "id_tabel": "UFpWMmJZOVZlZTJnc1pXaHhDV1hPQT09",
          "judul": "Luas Daerah dan Jumlah Pulau Menurut Provinsi",
          "judul_en": "Total Area and Number of Islands by Province",
          "kode_tabel": "1.1.1",
          "ketersediaan_tahun": [
            2015,
            2016,
            2017,
            2018,
            2019,
            2021
          ],
          "id_subject": "OTJzVUFuRkhLQU1iTTVJUnM5Zko3QT09",
          "bab": "Geografi dan Iklim",
          "bab_en": "Geography and Climate",
          "subject": "Keadaan Geografi",
          "subject_en": "Geography Condition",
          "mms_id": 516,
          "mms_subject": "Statistik Lingkungan Hidup Dan Multi-domain"
        },

SIMDASI Master Table
This service used to view the Master Table that is used in SIMDASI
https://webapi.bps.go.id/v1/api/interoperabilitas/datasource/simdasi/id/34/

Parameter
FieldTypeDescriptionkeyStringKey app to access API
Send a Sample Request

Detail of SIMDASI Master Table
This service used to view the Detail of Master Table that is used in SIMDASI
https://webapi.bps.go.id/v1/api/interoperabilitas/datasource/simdasi/id/36/

Parameter
FieldTypeDescriptionid_tabelStringID of the Table
keyStringKey app to access API
Send a Sample Request

List of SIMDASI Table Based on Area
This service used to view a list of SIMDASI Table based on Area
https://webapi.bps.go.id/v1/api/interoperabilitas/datasource/simdasi/id/23/

Parameter
FieldTypeDescriptionwilayahString7 digit MFD Code of Area. Example for DKI Jakarta use 3100000
keyStringKey app to access API
Send a Sample Request

Success 200
FieldTypeDescriptionstatusStringReturn status, OK if success and Error if any error occured.
data-availabilityStringAvailability status
dataObject[]Response Data
  0ObjectInformation status
    pageNumberInformation page
    pagesNumberInformation total page
    per_pageNumbersum of per page
    countNumbercount on this return list
    totalNumbertotal page
  1ObjectObject
  dataObjectList of subject
    id_tabelStringID unique of table
    judulStringTable title in bahasa
    judul_enStringTable title in english
    kode_tabelStringTable code in SIMDASI
    ketersediaan_tahunStringYear availability of table
    id_subjectStringID unique of subject
    babStringName of chapter in bahasa
    bab_enStringName of chapter in english
    subjectStringName of subject in bahasa
    subject_enStringName of subject in english
    mms_idNumberMMS ID of subject. This ID may be used in other endpoint as parameter of ID Subject. (MMS - Metadata Management system)
    mms_subjectStringCSA Subject name that is used in MMS
    tabelObjectList of ID Table in this subject

Success Response

HTTP/1.1 200 OK
{
  "status": "OK",
  "data-availability": "available",
  "data": [
    {
      "page": 1,
      "pages": 1,
      "per_page": 1,
      "count": 1,
      "total": 1
    },
    {
      "status": 200,
      "condition": "OK",
      "message": "-",
      "created": "2022-08-01 11:15:20",
      "induk": "0000000",
      "wilayah": "Indonesia",
      "data": [
        {
          "id_tabel": "UFpWMmJZOVZlZTJnc1pXaHhDV1hPQT09",
          "judul": "Luas Daerah dan Jumlah Pulau Menurut Provinsi",
          "judul_en": "Total Area and Number of Islands by Province",
          "kode_tabel": "1.1.1",
          "ketersediaan_tahun": [
            2015,
            2016,
            2017,
            2018,
            2019,
            2021
          ],
          "id_subject": "OTJzVUFuRkhLQU1iTTVJUnM5Zko3QT09",
          "bab": "Geografi dan Iklim",
          "bab_en": "Geography and Climate",
          "subject": "Keadaan Geografi",
          "subject_en": "Geography Condition",
          "mms_id": 516,
          "mms_subject": "Statistik Lingkungan Hidup Dan Multi-domain"
        },

List of SIMDASI Table Based on Area and Subject
This service used to view a list of SIMDASI Table based on Area and Subject
https://webapi.bps.go.id/v1/api/interoperabilitas/datasource/simdasi/id/24/

Parameter
FieldTypeDescriptionwilayahString7 digit MFD Code of Area. Example for DKI Jakarta use 3100000
id_subjekStringMMS_id of subject, use List of SIMDASI Subject to get the ID
keyStringKey app to access API
Send a Sample Request

Success 200
FieldTypeDescriptionstatusStringReturn status, OK if success and Error if any error occured.
data-availabilityStringAvailability status
dataObject[]Response Data
  0ObjectInformation status
    pageNumberInformation page
    pagesNumberInformation total page
    per_pageNumbersum of per page
    countNumbercount on this return list
    totalNumbertotal page
  1ObjectObject
  dataObjectList of subject
    id_tabelStringID unique of table
    judulStringTable title in bahasa
    judul_enStringTable title in english
    kode_tabelStringTable code in SIMDASI
    ketersediaan_tahunStringYear availability of table
    id_subjectStringID unique of subject
    babStringName of chapter in bahasa
    bab_enStringName of chapter in english
    subjectStringName of subject in bahasa
    subject_enStringName of subject in english
    mms_idNumberMMS ID of subject. This ID may be used in other endpoint as parameter of ID Subject. (MMS - Metadata Management system)
    mms_subjectStringCSA Subject name that is used in MMS
    tabelObjectList of ID Table in this subject

Success Response

HTTP/1.1 200 OK
{
  "status": "OK",
  "data-availability": "available",
  "data": [
    {
      "page": 1,
      "pages": 1,
      "per_page": 1,
      "count": 1,
      "total": 1
    },
    {
      "status": 200,
      "condition": "OK",
      "message": "-",
      "created": "2022-08-01 11:15:20",
      "induk": "0000000",
      "wilayah": "Indonesia",
      "data": [
        {
          "id_tabel": "UFpWMmJZOVZlZTJnc1pXaHhDV1hPQT09",
          "judul": "Luas Daerah dan Jumlah Pulau Menurut Provinsi",
          "judul_en": "Total Area and Number of Islands by Province",
          "kode_tabel": "1.1.1",
          "ketersediaan_tahun": [
            2015,
            2016,
            2017,
            2018,
            2019,
            2021
          ],
          "id_subject": "OTJzVUFuRkhLQU1iTTVJUnM5Zko3QT09",
          "bab": "Geografi dan Iklim",
          "bab_en": "Geography and Climate",
          "subject": "Keadaan Geografi",
          "subject_en": "Geography Condition",
          "mms_id": 516,
          "mms_subject": "Statistik Lingkungan Hidup Dan Multi-domain"
        },

Detail of SIMDASI Table
This service used to view the detail of SIMDASI Table
https://webapi.bps.go.id/v1/api/interoperabilitas/datasource/simdasi/id/25/

Parameter
FieldTypeDescriptionwilayahString7 digit MFD Code of Area. Example for DKI Jakarta use 3100000
TahunNumberYear of the Data
id_tabelStringid_tabel of table, use List of SIMDASI Table to get the ID
keyStringKey app to access API
Send a Sample Request

Static Table
Detail Statictable
This service is used to displays detail of a statictable are shown on the website
https://webapi.bps.go.id/v1/view

Parameter
FieldTypeDescriptiondomainNumberDomains that will be displayed statictable (see master domain)
Size range: 4
modelStringModel to display statictable (statictable) for statictable is "statictable"
langStringLanguage to display static table
Default value: ind
Allowed values: "ind", "eng"
idNumberstatictable id to display
Allowed values: 1, 2, 3, 4, ..., n
keyStringKey app to access API
Send a Sample Request

Success 200
FieldTypeDescriptionstatusStringReturn status, OK if success and Error if any error occured.
data-availabilityStringAvailability status of list statictable.
dataObjectInformation status
  table_idNumberID unique of statictable
  subj_idNumberID subject of statictable
  titleStringTitle of statictable
  tableStringTitle of statictable
  cr_dateStringCreate Date of statictable
  updt_dateStringUpdate Date of statictable
  sizeStringFile size of statictable
  excelStringPath location of statictable

Success Response
HTTP/1.1 200 OK
{
  "status": "OK",
  "data-availability": "available",
  "data":{
           "table_id": 111,
           "subj_id": 23,
           "title": "Inflasi data",
           "table": "sample html table",
           "cr_date": "2017-02-24",
           "updt_date": "2017-02-24",
           "excel": "http://jabar-dev.bps.go.id/new/website/tabelExcelIndo/Indo_23_3273895.xls",
           "size": " MB"
     }         
}

Error 4xx
NameDescriptionUserNotFoundThe id of the User was not found.

Error Response
HTTP/1.1 404 Not Found
  {
    "error": "UserNotFound"
  }

List All Static Table
This service is used to displays all static table are shown on the website
https://webapi.bps.go.id/v1/api/list/

Parameter
FieldTypeDescriptionmodelStringModel to display statictable (statictable) for statictable is "statictable"
lang optionalStringLanguage to display static table
Default value: ind
Allowed values: "ind", "eng"
domainNumberDomains that will be displayed statictable (see master domain)
Size range: 4
page optionalNumberPage to display statictable
Allowed values: 1, 2, 3, 4, ..., n
month optionalNumberMonth selected to display statictable
Allowed values: 1, 2, 3, 4, ..., n
year optionalNumberYear selected to display statictable
Allowed values: 1, 2, 3, 4, ..., n
keyword optionalStringKeyword to search
keyStringKey app to access API
Send a Sample Request

Success 200
FieldTypeDescriptionstatusStringReturn status, OK if success and Error if any error occured.
data-availabilityStringAvailability status of list statictable.
dataObject[]Response Data
  0ObjectInformation status
    pageNumberInformation page
    pagesNumberInformation total page
    per_pageNumbersum of per page
    countNumbercount on this return list
    totalNumbertotal page
  1ObjectList statictable
    table_idNumberID unique of statictable
    titleStringTitle of statictable
    subj_idNumberID subject of statictable
    subjStringSubject of statictable
    updt_dateStringUpdate Date of statictable
    sizeStringFile size of statictable
    excelStringPath location of statictable

Success Response
HTTP/1.1 200 OK
      {
        "status": "OK",
        "data-availability": "available",
        "data":[{
        "page":1,
        "pages":230,
        "per_page":10,
        "count":10,
        "total":2300
      },
      [{
      "turth_id":0,
      "turth":"Tahun",
      "group_turth_id":0,
      "name_group_turth":"Tahunan"
    },{
    "turth_id":1,
    "turth":"Bulanan",
    "group_turth_id":1,
    "name_group_turth":"January"
  },{
  "turth_id":2,
  "turth":"Bulanan",
  "group_turth_id":2,
  "name_group_turth":"February"
}]
]

}

Error 4xx
NameDescriptionUserNotFoundThe id of the User was not found.

Error Response
HTTP/1.1 404 Not Found
  {
    "error": "UserNotFound"
  }

CSA Subject (Classification of Statistical Activities)
CSA (Classification of Statistical Activities) was established in 2005, used as the basis for providing information in the international statistical activities database currently managed by the Conference of European Statistics (CES). In the future, BPS will adopt the CSA Subject in the new website user interface design.
CSA Subject Categories
This service is used to show list of CSA subject categories
https://webapi.bps.go.id/v1/api/list

Parameter
FieldTypeDescriptiondomainNumberDomains that will be displayed pressrelease (see master domain)
Size range: 4
modelStringModel to display CSA Subject Categories is "subcatcsa"
keyStringKey app to access API
Send a Sample Request

Success 200
FieldTypeDescriptionstatusStringReturn status, OK if success and Error if any error occured.
data-availabilityStringAvailability status
dataObject[]Response Data
  0ObjectInformation status
    pageNumberInformation page
    pagesNumberInformation total page
    per_pageNumbersum of per page
    countNumbercount on this return list
    totalNumbertotal page
  1ObjectData List
    subcat_idNumberID unique of CSA Subject Categories
    titleStringTitle of CSA Subject Categories

Success Response
HTTP/1.1 200 OK
{
  "status": "OK",
  "data-availability": "available",
  "data": [
    {
      "page": 1,
      "pages": 1,
      "per_page": 10,
      "count": 3,
      "total": 3
    },
    [
      {
        "subcat_id": 514,
        "title": "statistik demografi dan sosial"
      },
      {
        "subcat_id": 515,
        "title": "statistik ekonomi\n"
      },
      {
        "subcat_id": 516,
        "title": "statistik lingkungan hidup dan multi-domain"
      }
    ]
  ]
}

Error 4xx
NameDescriptionUserNotFoundThe id of the User was not found.

Error Response
HTTP/1.1 404 Not Found
  {
    "error": "UserNotFound"
  }

CSA Subject
This service is used to show list of CSA subject
https://webapi.bps.go.id/v1/api/list

Parameter
FieldTypeDescriptiondomainNumberDomains that will be displayed pressrelease (see master domain)
Size range: 4
modelStringModel to display CSA Subject is "subjectcsa"
subcat optionalStringCSA Subject Categories ID, use service "CSA Subject Categories" to get the "subcat_id"
keyStringKey app to access API
Send a Sample Request

Success 200
FieldTypeDescriptionstatusStringReturn status, OK if success and Error if any error occured.
data-availabilityStringAvailability status
dataObject[]Response Data
  0ObjectInformation status
    pageNumberInformation page
    pagesNumberInformation total page
    per_pageNumbersum of per page
    countNumbercount on this return list
    totalNumbertotal page
  1ObjectData List
    sub_idNumberID unique of CSA Subject
    titleStringTitle of CSA Subject
    subcat_idNumberID unique of CSA Subject Categories
    subcatStringTitle of CSA Subject Categories

Success Response
HTTP/1.1 200 OK
{
  "status": "OK",
  "data-availability": "available",
  "data": [
    {
      "page": 1,
      "pages": 2,
      "per_page": 10,
      "count": 10,
      "total": 11
    },
    [
      {
        "sub_id": 528,
        "title": "Aktivitas Politik dan Komunitas Lainnya",
        "subcat_id": 514,
        "subcat": "statistik demografi dan sosial"
      },
    ]
  ]
}

Error 4xx
NameDescriptionUserNotFoundThe id of the User was not found.

Error Response
HTTP/1.1 404 Not Found
  {
    "error": "UserNotFound"
  }

List of Table (Using CSA Subject)
This service is used to show list of table that adopt the CSA Subject
https://webapi.bps.go.id/v1/api/list

Parameter
FieldTypeDescriptiondomainNumberDomains that will be displayed pressrelease (see master domain)
Size range: 4
modelStringModel to display List of Table is "tablestatistic"
subject optionalNumberCSA Subject ID, use service "CSA Subject" to get the "sub_id"
page optionalNumberPage to display subject
Allowed values: 1, 2, 3, 4, ..., n
perpage optionalNumberSum of Table to display per page
Allowed values: 1, 2, 3, 4, ..., n
keyStringKey app to access API
Send a Sample Request

Success 200
FieldTypeDescriptionstatusStringReturn status, OK if success and Error if any error occured.
data-availabilityStringAvailability status
dataObject[]Response Data
  0ObjectInformation status
    pageNumberInformation page
    pagesNumberInformation total page
    per_pageNumbersum of per page
    countNumbercount on this return list
    totalNumbertotal page
  1ObjectData List
    idStringID unique of table
    titleStringTitle of Table
    id_subjectNumberID unique of CSA Subject
    subjectStringTitle of CSA Subject
    id_subcatNumberID unique of CSA Subject Categories
    subcatStringTitle of CSA Subject Categories
    tablesourceStringSource of Table
1: Static Table
2: Dynamic Table
3: SIMDASI
Detail of Table (Using CSA Subject)
This service is used to show detail of table that adopt the CSA Subject
https://webapi.bps.go.id/v1/api/view

Parameter
FieldTypeDescriptiondomainNumberDomains that will be displayed pressrelease (see master domain)
Size range: 4
modelStringModel to display List of Table is "tablestatistic"
idStringID of table, use service "List of table" above to get the "id"
year optionalintegera four-digit year value between oldest_period and latest_period
langNumberLanguage to display
Allowed values: "ind", "eng"
keyStringKey app to access API
Send a Sample Request

Press Release
Detail Press Release
This service is used to displays detail of a pressrelease are shown on the website
https://webapi.bps.go.id/v1/view

Parameter
FieldTypeDescriptiondomainNumberDomains that will be displayed pressrelease (see master domain)
Size range: 4
modelStringModel to display pressrelease (pressrelease) for pressrelease is "pressrelease"
langStringLanguage to display pressrelease
Allowed values: "ind", "eng"
idNumberpressrelease id to display
Allowed values: 1, 2, 3, 4, ..., n
keyStringKey app to access API
Send a Sample Request

Success 200
FieldTypeDescriptionstatusStringReturn status, OK if success and Error if any error occured.
data-availabilityStringAvailability status of list pressrelease.
dataObjectInformation status
  brs_idNumberID unique of pressrelease
  titleStringTitle of pressrelease
  abstractStringAbstract of pressrelease
  rl_dateStringRelease Date of pressrelease
  updt_dateStringUpdated Date of pressrelease if any updated/revised pressrelease
  pdfStringPath Location of pressrelease File
  sizeStringSize File of pressrelease

Success Response
HTTP/1.1 200 OK
{
  "status": "OK",
  "data-availability": "available",
  "data":{
         "brs_id":"brs-f12345512",
         "title": "Title of pressrelease",
         "abstract":"Abstract of Press Release",
         "rl_date": "2016-10-08",
         "updt_date": null,
         "pdf": "path",
         "size": "1.2 MB",
     }         
}

Error 4xx
NameDescriptionUserNotFoundThe id of the User was not found.

Error Response
HTTP/1.1 404 Not Found
  {
    "error": "UserNotFound"
  }

List All Press Release
This service is used to displays all press release are shown on the website
https://webapi.bps.go.id/v1/api/list

Parameter
FieldTypeDescriptionmodelStringModel to display pressrelease (pressrelease) for pressrelease is "pressrelease"
lang optionalStringLanguage to display pressrelease
Default value: ind
Allowed values: "ind", "eng"
domainNumberDomains that will be displayed pressrelease (see master domain)
Size range: 4
page optionalNumberPage to display pressrelease
Allowed values: 1, 2, 3, 4, ..., n
month optionalNumberMonth selected to display pressrelease
Allowed values: 1, 2, 3, 4, ..., n
year optionalNumberYear selected to display pressrelease
Allowed values: 1, 2, 3, 4, ..., n
keyword optionalStringKeyword to search
keyStringKey app to access API
Send a Sample Request

Success 200
FieldTypeDescriptionstatusStringReturn status, OK if success and Error if any error occured.
data-availabilityStringAvailability status of list pressrelease.
dataObject[]Response Data
  0ObjectInformation status
    pageNumberInformation page
    pagesNumberInformation total page
    per_pageNumbersum of per page
    countNumbercount on this return list
    totalNumbertotal page
  1ObjectList pressrelease
    brs_idNumberID unique of pressrelease
    titleStringTitle of pressrelease
    rl_dateStringRelease Date of pressrelease
    updt_dateStringUpdated Date of pressrelease if any updated/revised pressrelease
    pdfStringPath Location of pressrelease File
    sizeStringSize File of pressrelease

Success Response
HTTP/1.1 200 OK
{
  "status": "OK",
  "data-availability": "available",
  "data":[{
     "page":1,
     "pages":230,
     "per_page":10,
     "count":10,
     "total":2300
     },
     [{
         "brs_id":"brs-13342312",
         "title": "Title of pressrelease",
         "rl_date": "2016-07-08",
         "updt_date": null,
         "pdf": "path",
         "size": "2.1 MB",
     },{
        "brs_id":"brs-13344512",
         "title": "Title of pressrelease now",
         "rl_date": "2016-07-08",
         "updt_date": null,
         "pdf": "path",
         "size": "2 MB",
     }]
  ]
    
}

Error 4xx
NameDescriptionUserNotFoundThe id of the User was not found.

Error Response
HTTP/1.1 404 Not Found
  {
    "error": "UserNotFound"
  }

Publication
Detail Publication
This service is used to displays detail of a publication are shown on the website
https://webapi.bps.go.id/v1/view

Parameter
FieldTypeDescriptiondomainNumberDomains that will be displayed publication (see master domain)
Size range: 4
modelStringModel to display publication (publication) for publication is "publication"
langStringLanguage to display publication
Allowed values: "ind", "eng"
idStringPublication id to display
keyStringKey app to access API
Send a Sample Request

Success 200
FieldTypeDescriptionstatusStringReturn status, OK if success and Error if any error occured.
data-availabilityStringAvailability status of list publication.
dataObjectInformation status
  pub_idNumberID unique of Publication
  titleStringTitle of Publication
  kat_noStringCategory Number of Publication
  pub_noStringPublication Number of Publication
  issnStringISSN/ISBN number of Publication
  abstractStringAbstract of Publication
  sch_dateStringSchedule Date of Publication
  rl_dateStringRelease Date of Publication
  updt_dateStringUpdated Date of Publication if any updated/revised publication
  coverStringPath Location of Publication cover
  pdfStringPath Location of Publication File
  sizeStringSize File of Publication

Success Response
HTTP/1.1 200 OK
{
  "status": "OK",
  "data-availability": "available",
  "data":{
         "pub_id":"pub-13342312",
         "title": "Title of Publication",
         "kat_no": "1212 1212 314",
         "pub_no": "1221",
         "issn": "0215-2169",
         "abstract": "Abstract of Publication",
         "sch_date": "2016-07-08",
         "rl_date": "2016-07-08",
         "updt_date": null,
         "cover": "path",
         "pdf": "path",
         "size": "21 MB",
     }         
}

Error 4xx
NameDescriptionUserNotFoundThe id of the User was not found.

Error Response
HTTP/1.1 404 Not Found
  {
    "error": "UserNotFound"
  }

List All Publication
This service is used to displays all publication that are shown on the website
https://webapi.bps.go.id/v1/api/list/

Parameter
FieldTypeDescriptionmodelStringModel to display publication (publication) for publication is "publication"
lang optionalStringLanguage to display publication
Default value: ind
Allowed values: "ind", "eng"
domainNumberDomains that will be displayed publication (see master domain)
Size range: 4
page optionalNumberPage to display publication
Allowed values: 1, 2, 3, 4, ..., n
month optionalNumberMonth selected to display publication
Allowed values: 1, 2, 3, 4, ..., n
year optionalNumberYear selected to display publication
Allowed values: 1, 2, 3, 4, ..., n
keyword optionalStringKeyword to search
keyStringKey app to access API
Send a Sample Request

Success 200
FieldTypeDescriptionstatusStringReturn status, OK if success and Error if any error occured.
data-availabilityStringAvailability status of list publication.
dataObject[]Response Data
  0ObjectInformation status
    pageNumberInformation page
    pagesNumberInformation total page
    per_pageNumbersum of per page
    countNumbercount on this return list
    totalNumbertotal page
  1ObjectList publication
    pub_idNumberID unique of Publication
    titleStringTitle of Publication
    issnStringISSN/ISBN number of publication
    sch_dateStringSchedule Date of Publication
    rl_dateStringRelease Date of Publication
    updt_dateStringUpdated Date of Publication if any updated/revised publication
    coverStringPath Location of Publication cover
    pdfStringPath Location of Publication File
    sizeStringSize File of Publication

Success Response
    HTTP/1.1 200 OK
    {
    "status": "OK",
    "data-availability": "available",
    "data": [
        {
            "page": 0,
            "pages": 1,
            "per_page": 10,
            "count": 3,
            "total": 3
      },
       [
           {
               "pub_id": "2016320000032000321313",
                "title": "Indeks Pembangunan Manusia Provinsi Jawa Barat 2015",
                "issn": "999-999-999-9",
                "sch_date": "2016-11-28",
                "rl_date": "2016-11-29",
             "updt_date": null,
              "cover": "http://publikasi.bps.go.id/portalpublikasi_beta/index.php/publikasi/getcover?id=2016320000032000321313",
              "pdf": "http://publikasi.bps.go.id/portalpublikasi_beta/index.php/publikasi/getpdfwatermark?id=2016320000032000321313",
                "size": "5 MB"
            },
            {
                "pub_id": "20163200000320003211",
                "title": "Provinsi Jawa Barat Dalam Angka 2016",
                "issn": "0215-2169",
                "sch_date": "2016-11-16",
                "rl_date": "2016-11-16",
                "updt_date": "2016-11-23",
                "cover": "http://publikasi.bps.go.id/portalpublikasi_beta/index.php/publikasi/getcover?id=20163200000320003211",
                "pdf": "http://publikasi.bps.go.id/portalpublikasi_beta/index.php/publikasi/getpdfwatermark?id=20163200000320003211",
               "size": "2.8 MB"
            },
           {
              "pub_id": "2016320000032000322302",
             "title": "[Updated] Testing Publikasi NON-ARC",
            "issn": "-",
           "sch_date": null,
          "rl_date": "2016-11-15",
        "updt_date": "2017-01-27",
                "cover": "http://publikasi.bps.go.id/portalpublikasi_beta/index.php/publikasi/getcover?id=2016320000032000322302",
                "pdf": "http://www.bps.go.id",
                "size": "30 MB"
            }
        ]
    ]
}

Error 4xx
NameDescriptionUserNotFoundThe id of the User was not found.

Error Response
HTTP/1.1 404 Not Found
  {
    "error": "UserNotFound"
  }

Strategic Indicators
List Strategic Indicators
This service is used to displays all strategic indicator only for the central and province website
https://webapi.bps.go.id/v1/api/list/

Parameter
FieldTypeDescriptionmodelStringModel to display strategic indicators for strategic indicators is "indicators"
lang optionalStringLanguage to display strategic indicators
Default value: ind
Allowed values: "ind", "eng"
domainNumberDomains that will be displayed derived period data (see master domain). Domains that allowed in this model only for central and province domain.
Size range: 4
var optionalNumberVariable ID selected to display derived period data
Allowed values: 1, 2, 3, 4, ..., n
page optionalNumberPage to display derived period data
Allowed values: 1, 2, 3, 4, ..., n
keyStringKey app to access API
Send a Sample Request

Success 200
FieldTypeDescriptionstatusStringReturn status, OK if success and Error if any error occured.
data-availabilityStringAvailability status of list indicators.
dataObject[]Response Data
  0ObjectInformation status
    pageNumberInformation page
    pagesNumberInformation total page
    per_pageNumbersum of per page
    countNumbercount on this return list
    totalNumbertotal page
  1ObjectList Strategic Indicators
    titleStringTitle of Strategic Indicators
    descStringDescription of Indicators
    data_sourceStringData Source if Strategic Indicators
    valueNumberValue of Strategic Indicators
    unitStringUnit Value of Strategic Indicators

Success Response
HTTP/1.1 200 OK
      {
        "status": "OK",
        "data-availability": "available",
        "data":[{
        "page":1,
        "pages":230,
        "per_page":10,
        "count":10,
        "total":2300
      },
      [{
      "turth_id":0,
      "turth":"Tahun",
      "group_turth_id":0,
      "name_group_turth":"Tahunan"
    },{
    "turth_id":1,
    "turth":"Bulanan",
    "group_turth_id":1,
    "name_group_turth":"January"
  },{
  "turth_id":2,
  "turth":"Bulanan",
  "group_turth_id":2,
  "name_group_turth":"February"
}]
]

}

Error 4xx
NameDescriptionUserNotFoundThe id of the User was not found.

Error Response
HTTP/1.1 404 Not Found
  {
    "error": "UserNotFound"
  }

Infographic
List All Infographic
This service is used to displays all infographic in the website
https://webapi.bps.go.id/v1/api/list/

Parameter
FieldTypeDescriptionmodelStringModel to display news (news) for infographic is "infographic"
lang optionalStringLanguage to display news
Default value: ind
Allowed values: "ind", "eng"
domainNumberDomains that will be displayed news (see master domain)
Size range: 4
page optionalNumberPage to display news
Allowed values: 1, 2, 3, 4, ..., n
keyword optionalStringKeyword to search
keyStringKey app to access API
Send a Sample Request

Success 200
FieldTypeDescriptionstatusStringReturn status, OK if success and Error if any error occured.
data-availabilityStringAvailability status of list indicators.
dataObject[]Response Data
  0ObjectInformation status
    pageNumberInformation page
    pagesNumberInformation total page
    per_pageNumbersum of per page
    countNumbercount on this return list
    totalNumbertotal page
  1ObjectList Infographics
    inf_idNumberId of Infographic
    titleStringTitle of Infographic
    imgStringThumbnail of Infographic
    descStringDescription of infographic
    categoryNumberCategory id of infographic (1: Social and Population, 2: Economic and Trade, 3: Agriculture and Mining)
    dlStringDownload link of Infographic

Success Response
HTTP/1.1 200 OK
{
  "status": "OK",
  "data-availability": "available",
  "data": [
    {
      "page": 1,
      "pages": 49,
      "per_page": 10,
      "count": 10,
      "total": 481
    },
      [
        {
          "inf_id": 527,
          "title": "Transportasi Rilis Oktober 2020",
          "img": "https://www.bps.go.id/website/images/Transportasi-Rilis-Oktober-2020-ind.jpg",
          "desc": "",
          "category": 2,
          "dl": "https://www.bps.go.id/galery/download.html?asdf=NTI3&qwer=ldjfdifsdjkfahi&zxcv=MjAyMC0xMC0wNiAwNzozMzowMg%3D%3D"
        },
      ]
    ] 

}

Error 4xx
NameDescriptionUserNotFoundThe id of the User was not found.

Error Response
HTTP/1.1 404 Not Found
  {
    "error": "UserNotFound"
  }

Glosarium
List of Glosarium
This service is used to display list of glosarium
https://webapi.bps.go.id/v1/api/list

Parameter
FieldTypeDescriptionmodelStringModel to display list of glosarium is "glosarium"
prefix optionalStringThe first letter that the list will look for
page optionalNumberPage to display subject
Allowed values: 1, 2, 3, 4, ..., n
perpage optionalNumberSum of Table to display per page
Allowed values: 1, 2, 3, 4, ..., 500
keyStringKey app to access API
Send a Sample Request

Success 200
FieldTypeDescriptionstatusStringReturn status, OK if success and Error if any error occured.
data-availabilityStringAvailability status
dataObject[]Response Data
  0ObjectInformation status
    pageNumberInformation page
    pagesNumberInformation total page
    per_pageNumbersum of per page
    countNumbercount on this return list
    totalNumbertotal page
  _sourceObjectData List
    kontenStringContent: Glosarium
    jenisStringType of content: Glosarium
    idNumberUnique ID of glosarium
    idSdsNumberUnique ID of SDS
    noIndikatorNumberNumber of Indicator
    judulIndikatorStringTitle of Indicator in Bahasa
    judulIndikator_enStringTitle of Indicator in English
    konsepStringStatistical Concept in Bahasa
    konsep_enStringStatistical Concept in English
    definisiStringDefinition of a Statistical Concept in Bahasa
    definisi_enStringDefinition of a Statistical Concept in English
    namaKlasifikasiStringName of Classification in Bahasa
    namaKlasifikasi_enStringName of Classification in English
    ukuranStringSize in Bahasa
    ukuran_enStringSize in English
    satuanStringunit in Bahasa
    satuan_enStringunit in English
    flagSdsStringFlag of Sds
    sumberKontenStringSource of content in Bahasa
    sumberKonten_enStringSource of Content in English
    sumberDataStringSource of Data in Bahasa
    sumberData_enStringSource of data in English
    EndpointStringType of ENdpoint
    flagboolean

Success Response
HTTP/1.1 200 OK
{
  "status": "OK",
  "data-availability": "available",
  "data": [
    {
      "page": 1,
      "pages": 508,
      "per_page": 10,
      "count": 10,
      "total": 5078
    },
    [
      {
        "_index": "glosarium",
        "_type": "_doc",
        "_id": "glosarium_4406_web",
        "_score": null,
        "_source": {
          "konten": "glosarium",
          "jenis": "glosarium",
          "id": "4406",
          "idSds": null,
          "noIndikator": null,
          "judulIndikator": "",
          "judulIndikator_en": "",
          "konsep": "Agama",
          "konsep_en": "Religion",
          "definisi": "Agama merupakan keyakinan terhadap Tuhan Yang Maha Esa yang harus dimiliki oleh setiap manusia. Agama dibedakan menjadi Islam, Kristen, Katholik, Hindu, Budha, Khong Hu Chu, dan Agama Lainnya. Agama berguna dalam menentukan kebijakan yang berkaitan dengan kerukunan umat beragama, contoh: kebijakan Kementerian Agama dalam pembangunan tempat-tempat ibadahberagama, untuk memelihara dan menyuburkan kesadaran umat dalam menghayati danmelaksanakan ajaran-ajarannya. Termasuk dalam acara agama: Sepercik Iman Pembasuh Kalbu,Terjemahan Al-Quran, Mimbar Agama Islam, Mimbar Agama Katolik, Mimbar Agama Protestan.",
          "definisi_en": "Religion is belief in Almighty God that must be possessed by every human being. Religion can be divided into Muslim, Christian, Catholic, Hindu, Buddhist, Hu Khong Chu, and Other Religion. ",
          "namaKlasifikasi": "",
          "namaKlasifikasi_en": "",
          "klasifikasi": "",
          "klasifikasi_en": "",
          "ukuran": "",
          "ukuran_en": "",
          "satuan": "",
          "satuan_en": "",
          "flagSds": "",
          "sumberKonten": "",
          "sumberKonten_en": "",
          "sumberData": "",
          "sumberData_en": "",
          "endpoint": "web",
          "flag": "t"
        },
        "sort": [
          "agama"
        ]
      },
    ]
  ]
}

Error 4xx
NameDescriptionUserNotFoundThe id of the User was not found.

Error Response
HTTP/1.1 404 Not Found
  {
    "error": "UserNotFound"
  }

Detail of Glosarium
This service is used to display the detail of statistical concept
https://webapi.bps.go.id/v1/api/view

Parameter
FieldTypeDescriptionmodelStringModel to display list of glosarium is "glosarium"
idNumberThe ID of glosarium
langStringLanguage to display
Default value: ind
Allowed values: "ind", "eng"
keyStringKey app to access API
Send a Sample Request

Success 200
FieldTypeDescriptionstatusStringReturn status, OK if success and Error if any error occured.
data-availabilityStringAvailability status
dataObject[]Response Data
  0ObjectInformation status
    pageNumberInformation page
    pagesNumberInformation total page
    per_pageNumbersum of per page
    countNumbercount on this return list
    totalNumbertotal page
  _sourceObjectData List
    kontenStringContent: Glosarium
    jenisStringType of content: Glosarium
    idNumberUnique ID of glosarium
    idSdsNumberUnique ID of SDS
    noIndikatorNumberNumber of Indicator
    judulIndikatorStringTitle of Indicator in Bahasa
    judulIndikator_enStringTitle of Indicator in English
    konsepStringStatistical Concept in Bahasa
    konsep_enStringStatistical Concept in English
    definisiStringDefinition of a Statistical Concept in Bahasa
    definisi_enStringDefinition of a Statistical Concept in English
    namaKlasifikasiStringName of Classification in Bahasa
    namaKlasifikasi_enStringName of Classification in English
    ukuranStringSize in Bahasa
    ukuran_enStringSize in English
    satuanStringunit in Bahasa
    satuan_enStringunit in English
    flagSdsStringFlag of Sds
    sumberKontenStringSource of content in Bahasa
    sumberKonten_enStringSource of Content in English
    sumberDataStringSource of Data in Bahasa
    sumberData_enStringSource of data in English
    EndpointStringType of ENdpoint
    flagboolean

Success Response
HTTP/1.1 200 OK
{
  "status": "OK",
  "data-availability": "available",
  "data": [
    {
      "page": 1,
      "pages": 1,
      "per_page": 1,
      "count": 1,
      "total": 1 
    },
    [
      {
        "_index": "glosarium",
        "_type": "_doc",
        "_id": "glosarium_4406_web",
        "_score": null,
        "_source": {
          "konten": "glosarium",
          "jenis": "glosarium",
          "id": "4406",
          "idSds": null,
          "noIndikator": null,
          "judulIndikator": "",
          "judulIndikator_en": "",
          "konsep": "Agama",
          "konsep_en": "Religion",
          "definisi": "Agama merupakan keyakinan terhadap Tuhan Yang Maha Esa yang harus dimiliki oleh setiap manusia. Agama dibedakan menjadi Islam, Kristen, Katholik, Hindu, Budha, Khong Hu Chu, dan Agama Lainnya. Agama berguna dalam menentukan kebijakan yang berkaitan dengan kerukunan umat beragama, contoh: kebijakan Kementerian Agama dalam pembangunan tempat-tempat ibadahberagama, untuk memelihara dan menyuburkan kesadaran umat dalam menghayati danmelaksanakan ajaran-ajarannya. Termasuk dalam acara agama: Sepercik Iman Pembasuh Kalbu,Terjemahan Al-Quran, Mimbar Agama Islam, Mimbar Agama Katolik, Mimbar Agama Protestan.",
          "definisi_en": "Religion is belief in Almighty God that must be possessed by every human being. Religion can be divided into Muslim, Christian, Catholic, Hindu, Buddhist, Hu Khong Chu, and Other Religion. ",
          "namaKlasifikasi": "",
          "namaKlasifikasi_en": "",
          "klasifikasi": "",
          "klasifikasi_en": "",
          "ukuran": "",
          "ukuran_en": "",
          "satuan": "",
          "satuan_en": "",
          "flagSds": "",
          "sumberKonten": "",
          "sumberKonten_en": "",
          "sumberData": "",
          "sumberData_en": "",
          "endpoint": "web",
          "flag": "t"
        },
        "sort": [
          "agama"
        ]
      },
    ]
  ]
}

Error 4xx
NameDescriptionUserNotFoundThe id of the User was not found.

Error Response
HTTP/1.1 404 Not Found
  {
    "error": "UserNotFound"
  }

Foreign Trade Data (Export&Import)
This service is used to displays data of foreign trade from the website
https://webapi.bps.go.id/v1/api/dataexim/

Parameter
FieldTypeDescriptionsumberNumberSource of the data
1: Export
2: Import
periodeNumberPeriod of the data
1: monthly
2: annually
kodehsnumberHS Code of the data, use separator ; for multiple HS Code. e.g. firstHScode;secondHScode.
jenishsNumberType of HS Code
1: Two digit
2: Full HS Code
If jenishs = 1 then the kodehs is two digits. If jenishs = 2 then the full digit kodehs follows the master hscode by year. For more information
TahunStringYear of data
keyStringKey app to access API
Send a Sample Request

Success 200
FieldTypeDescriptionstatusStringReturn status, OK if success and Error if any error occured.
data-availabilityStringAvailability status of list indicators.
MetadataObject[]source: source of the data
value: Export/Import value in US Dollar ($)
netweight: weight of Export/Import in Kilogram (Kg)
kodehs: Code and Description from HS
pod: Incoming/Outgoing Ports in Indonesia
ctr: Country of Origin/Destination
year: data year

Success Response
HTTP/1.1 200 OK
{
  "status": "OK",
  "data-availability": "not-available",
  "metadata": {
    "source": "Sumber : https://www.bps.go.id diakses pada 23-06-2021 12:38:14 WIB",
    "value": "Nilai Ekspor/Impor dalam US Dollar ($)",
    "netweight": "Berat Ekspor/Impor dalam Kilogram (KG)",
    "kodehs": "Kode dan Deskripsi dari HS",
    "pod": "Pelabuhan Masuk/Keluar di Indonesia",
    "ctr": "Negara Asal/Tujuan",
    "tahun": "Tahun Data"
  },
  "data": [
    {
      "value": 1015060.142,
      "netweight": 243755,
      "kodehs": "[03] Ikan dan krustasea, moluska serta invertebrata air lainnya",
      "pod": "BELAWAN",
      "ctr": "ALBANIA",
      "tahun": "2019"
    },...

}

Error 4xx
NameDescriptionUserNotFoundThe id of the User was not found.

Error Response
HTTP/1.1 404 Not Found
  {
    "error": "UserNotFound"
  }

Sustainable Development Goals (SDGs)
List All SDGs Table
This service is used to displays all SDGs table, domain must be "0000"
https://webapi.bps.go.id/v1/api/list/

Parameter
FieldTypeDescriptionmodelStringModel to display sdgs table is "sdgs"
goal optionalStringNumber of Goal
Allowed values: 1... 17
keyStringKey app to access API
Send a Sample Request

SDGs Table List
This table is updated annually without prior notice
GoalsVariableVariable (id)Id VarNumber of Deaths, Disappeared, and Hurt Victims AffectedJumlah Korban Meninggal, Hilang, dan Terluka Terkena Dampak Bencana1804Number of Deaths, Disappeared, and Hurt Victims Affected by 100,000 PeopleJumlah Korban Meninggal, Hilang, dan Terluka Terkena Dampak Bencana Per 100.000 Orang1246Percentage of Poor People by ProvincePersentase Penduduk Miskin Menurut Provinsi192Percentage of Poor People by RegionPersentase Penduduk Miskin Menurut Wilayah184Percentage of Poor People In Disadvantaged AreasPersentase Penduduk Miskin Di Daerah Tertinggal1238Percentage of population living below the national poverty line, according to age groupPersentase Penduduk Yang Hidup Di Bawah Garis Kemiskinan Nasional, Menurut Kelompok Umur1539Percentage of Population Living Below the National Poverty Line, According to GenderPersentase Penduduk Yang Hidup di Bawah Garis Kemiskinan Nasional, Menurut Jenis Kelamin1538Proportion of households with access to basic services by area of residenceProporsi rumah tangga dengan akses terhadap pelayanan dasar menurut Daerah Tempat Tinggal2017Proportion of households with access to basic services by provinceProporsi rumah tangga dengan akses terhadap pelayanan dasar menurut provinsi2016Proportion of households with ownership and lease / contract status by provinceProporsi rumah tangga dengan status kepemilikan rumah milik dan sewa/kontrak menurut provinsi2018Proportion of households with ownership status of owned and leased / contracted houses according to genderProporsi rumah tangga dengan status kepemilikan rumah milik dan sewa/kontrak menurut jenis kelamin2020Proportion of households with ownership status of owned and leased / contracted houses by area of residenceProporsi rumah tangga dengan status kepemilikan rumah milik dan sewa/kontrak menurut Daerah Tempat Tinggal2019Spending on basic services (education, health and social protection) as a percentage of total government spending.Pengeluaran untuk layanan pokok (pendidikan, kesehatan dan perlindungan sosial) sebagai persentase dari total belanja pemerintah1759Agricultural Added Value Divided by Number of Labor in Agricultural SectorNilai Tambah Pertanian Dibagi Jumlah Tenaga Kerja Di Sektor Pertanian1344Percentage of Toddlers (Under Five Years Old) Short And Very ShortPersentase Balita Pendek Dan Sangat Pendek1325Population Prevalence With Moderate Or Severe Food Insecurity, Based On The Scale Of Food Insecurity ExperiencePrevalensi Penduduk Dengan Kerawanan Pangan Sedang Atau Berat, Berdasarkan Pada Skala Pengalaman Kerawanan Pangan1474Prevalence of Anemia in Pregnant WomenPrevalensi Anemia Pada Ibu Hamil1333Prevalence of Insufficient Food ConsumptionPrevalensi Ketidakcukupan Konsumsi Pangan1473Prevalence of Toddler Very Short and Short in Regency / City SSGBIPrevalensi Balita Sangat Pendek dan Pendek pada Kabupaten/Kota SSGBI1614The prevalence of anemia in pregnant women according to age groupPrevalensi anemia pada ibu hamil menurut kelompok umur1782Toddler Prevalence is Very Short and Short by Regency / City in 2018Prevalensi Balita Sangat Pendek dan Pendek Menurut Kabupaten/Kota Tahun 20181531Age Specific Fertility Rate/ASFR (15-19) by AreaAngka Kelahiran Pada Perempuan Usia 15-19 Tahun Menurut Daerah Tempat Tinggal1398Age Specific Fertility Rate/ASFR (15-19) by ProvinceAngka Kelahiran Pada Perempuan Usia 15-19 Tahun Menurut Provinsi1397Alcohol consumption by people aged ≥ 15 years in the past yearKonsumsi Alkohol Oleh Penduduk Umur ≥ 15 Tahun Dalam Satu Tahun Terakhir1475Birth Rate In Women Aged 15-19 Years by ProvinsiAngka Kelahiran Pada Perempuan Umur 15-19 Tahun Menurut Provinsi1353Birth Rates for Women Aged 15-19 Years by Region of ResidenceAngka Kelahiran Pada Perempuan Umur 15-19 Tahun (ASFR) (per 1.000 perempuan umur 15-19 tahun) Menurut Daerah Tempat Tinggal1612Density and Distribution of Health WorkersKepadatan Dan Distribusi Tenaga Kesehatan1477Incidence of Tuberculosis (ITB) Per 100,000 PopulationInsiden Tuberkolosis (ITB) Per 100.000 Penduduk1763Infant Mortality Rate (IMR) Per 1000 Live Births According to Wealth QuantileAngka Kematian Bayi (AKB) Per 1000 Kelahiran Hidup Menurut Kuantil Kekayaan1572Infant Mortality Rate (IMR) Per 1000 Live Births by Age of Mother During ChildbirthAngka Kematian Bayi (AKB) Per 1000 Kelahiran Hidup Menurut Umur Ibu Saat Melahirkan1569Infant Mortality Rate (IMR) Per 1000 Live Births by ProvinceAngka Kematian Bayi (AKB) Per 1000 Kelahiran Hidup Menurut Provinsi1584Infant Mortality Rate (IMR) Per 1000 Live Births by Residence AreaAngka Kematian Bayi (AKB) Per 1000 Kelahiran Hidup Menurut Daerah Tempat Tinggal1568Infant Mortality Rate (IMR) Per 1000 Live Births of Mothers EducationAngka Kematian Bayi (AKB) Per 1000 Kelahiran Hidup Menurut Pendidikan Ibu1574Malaria Occurrences Per 1000 PersonsKejadian Malaria Per 1000 Orang1393Maternal Mortality Rate by IslandAngka Kematian Ibu Menurut Pulau1349Mortality Rate Per 1000 Live Births by Area of ResidenceAngka Kematian Balita Per 1000 Kelahiran Hidup Menurut Daerah Tempat Tinggal1379Mortality Rate Per 1000 Live Births by Maternal age at deliveryAngka Kematian Balita Per 1000 Kelahiran Hidup Menurut Umur Ibu saat Melahirkan1381Mortality Rate Per 1000 Live Births by Mother education levelAngka Kematian Balita Per 1000 Kelahiran Hidup Menurut Pendidikan Ibu1374Mortality Rate Per 1000 Live Births by ProvinceAngka Kematian Balita Per 1000 Kelahiran Hidup Menurut Provinsi1373Mortality Rate Per 1000 Live Births by Wealth QuintileAngka Kematian Balita Per 1000 Kelahiran Hidup Menurut Kuantil Kekayaan1382Neonatal Death Rate And Infant Mortality Rate Per 1000 Birth By Area Of ResidenceAngka Kematian Neonatal (AKN) Dan Angka Kematian Bayi Per 1000 Kelahiran Menurut Daerah tempat tinggal1384Neonatal Death Rate And Infant Mortality Rate Per 1000 Birth By Maternal age at deliveryAngka Kematian Neonatal (AKN) Dan Angka Kematian Bayi Per 1000 Kelahiran Menurut Umur Ibu saat Melahirkan1388Neonatal Death Rate And Infant Mortality Rate Per 1000 Birth By Mother education levelAngka Kematian Neonatal (AKN) Dan Angka Kematian Bayi Per 1000 Kelahiran Menurut Pendidikan Ibu1385Neonatal Death Rate And Infant Mortality Rate Per 1000 Birth By ProvinceAngka Kematian Neonatal (AKN) Dan Angka Kematian Bayi Per 1000 Kelahiran Menurut Provinsi1383Neonatal Death Rate And Infant Mortality Rate Per 1000 Birth By Wealth quintileAngka Kematian Neonatal (AKN) Dan Angka Kematian Bayi Per 1000 Kelahiran Menurut Kuantil Kekayaan1387Number of Clients Accessing Post-rehabilitation ServicesJumlah Klien Yang Mengakses Layanan Pascarehabilitasi1479Number of districts / cities that have achieved malaria eliminationJumlah Kabupaten/Kota yang mencapai eliminasi Malaria1764Number of districts / cities with filariasis elimination (successfully passed the phase I transmission assessment survey)Jumlah Kabupaten/Kota dengan eliminasi filariasis (berhasil lolos dalam survei penilaian transmisi tahap I)1778Number of People Accessing Post Rehabilitation ServicesJumlah yang Mengakses Layanan Pasca Rehabilitasi1790Number of Population Which Is Included Health Insurance Or Public Health System Per 1000 peopleJumlah Penduduk Yang Dicakup Asuransi Kesehatan Atau Sistem Kesehatan Masyarakat per 1000 Penduduk1434Number of Provinces with Leprosy EliminationJumlah Provinsi dengan eliminasi Kusta1770Percentage of Smokers Age √¢‚Ä∞¬• 15 years by AgePersentase Merokok Pada Penduduk Umur ≥ 15 Tahun Menurut Kelompok Umur1438Percentage of Smokers Age √¢‚Ä∞¬• 15 years by AreaPersentase Merokok Pada Penduduk Umur ≥ 15 Tahun Menurut Daerah Tempat Tinggal1436Percentage of Smokers Age √¢‚Ä∞¬• 15 years by Percentile Group of ExpenditurePersentase Merokok Pada Penduduk Umur ≥ 15 Tahun Menurut Kelompok Pengeluaran1437Percentage of Smokers Age √¢‚Ä∞¬• 15 years by ProvincePersentase Merokok Pada Penduduk Umur ≥ 15 Tahun Menurut Provinsi1435Persentase Perempuan Pernah Kawin Berusia 15-49 Tahun Yang Proses Kelahiran Terakhirnya Ditolong Oleh Tenaga Kesehatan Terlatih Menurut Daerah Tempat TinggalPersentase Perempuan Pernah Kawin Berusia 15-49 Tahun Yang Proses Kelahiran Terakhirnya Ditolong Oleh Tenaga Kesehatan Terlatih Menurut Daerah Tempat Tinggal1346Persentase Perempuan Pernah Kawin Berusia 15-49 Tahun Yang Proses Kelahiran Terakhirnya Ditolong Oleh Tenaga Kesehatan Terlatih Menurut Kelompok PengeluaranPersentase Perempuan Pernah Kawin Berusia 15-49 Tahun Yang Proses Kelahiran Terakhirnya Ditolong Oleh Tenaga Kesehatan Terlatih Menurut Kelompok Pengeluaran1347Persentase Perempuan Pernah Kawin Berusia 15-49 Tahun Yang Proses Kelahiran Terakhirnya Ditolong Oleh Tenaga Kesehatan Terlatih Menurut ProvinsiPersentase Perempuan Pernah Kawin Berusia 15-49 Tahun Yang Proses Kelahiran Terakhirnya Ditolong Oleh Tenaga Kesehatan Terlatih Menurut Provinsi1345Prevalence of high blood pressure according to sexPrevalensi tekanan darah tinggi menurut jenis kelamin1780Prevalence of high blood pressure according to the area of residencePrevalensi tekanan darah tinggi menurut daerah tempat tinggal1779Prevalence of High Blood Pressure by ProvincePrevalensi Tekanan Darah Tinggi Menurut Provinsi1480Prevalence of Obesity in Age Population> 18 Years OldPrevalensi Obesitas Pada Penduduk Umur > 18 Tahun1481The Number Of Drug Abuse And Harmful Alcohol Users, Who Access Medical Rehabilitation ServicesJumlah Penyalahgunaan Narkotika dan Pengguna Alkohol Yang Merugikan, Yang Mengakses Layanan Rehabilitasi Medis1789The prevalence of obesity in people aged> 18 years according to sexPrevalensi Obesitas Pada Penduduk Umur > 18 Tahun Menurut Jenis Kelamin1781The proportion of women of reproductive age (15-49 years) or their partners who have family planning needs and use contraception methodsProporsi Perempuan Usia Reproduksi (15-49 tahun) atau Pasangannya yang Memiliki Kebutuhan Keluarga Berencana dan Menggunakan Alat Kontrasepsi Metode Modern1394Total Fertility Rate by AreaAngka Kelahiran Total Menurut Daerah Tempat Tinggal1401Total Fertility Rate by Expenditure GroupsAngka Kelahiran Total Menurut Kelompok Pengeluaran1400Total Fertility Rate by ProvinceAngka Kelahiran Total Menurut Provinsi1399Unmet Need Pelayanan Kesehatan Menurut Daerah Tempat TinggalUnmet Need Pelayanan Kesehatan Menurut Daerah Tempat Tinggal1403Unmet Need Pelayanan Kesehatan Menurut Jenis KelaminUnmet Need Pelayanan Kesehatan Menurut Jenis Kelamin1404Unmet Need Pelayanan Kesehatan Menurut Kelompok PengeluaranUnmet Need Pelayanan Kesehatan Menurut Kelompok Pengeluaran1405Unmet Need Pelayanan Kesehatan Menurut Kelompok UmurUnmet Need Pelayanan Kesehatan Menurut Kelompok Umur1406Unmet Need Pelayanan Kesehatan Menurut ProvinsiUnmet Need Pelayanan Kesehatan Menurut Provinsi1402Education Completion Rate According to Education Level and Expenditure GroupTingkat Penyelesaian Pendidikan Menurut Jenjang Pendidikan dan Kelompok Pengeluaran1983Education Completion Rate According to Education Level and GenderTingkat Penyelesaian Pendidikan Menurut Jenjang Pendidikan dan Jenis Kelamin1982Education Completion Rate According to Education Level and ProvinceTingkat Penyelesaian Pendidikan Menurut Jenjang Pendidikan dan Provinsi1980Education Completion Rate According to Education Level and RegionTingkat Penyelesaian Pendidikan Menurut Jenjang Pendidikan dan Wilayah1981Literacy Rate (AMH) of Population above 15 Years Old by AreaAngka Melek Huruf Penduduk Berumur 15 Tahun Ke Atas Menurut Daerah Tempat Tinggal1461Literacy Rate (AMH) of Population above 15 Years Old by Group of IncomeAngka Melek Huruf Penduduk Berumur 15 Tahun Ke Atas Menurut Kelompok Pendapatan1459Literacy Rate (AMH) of Population above 15 Years Old by ProvinceAngka Melek Huruf Penduduk Berumur 15 Tahun Ke Atas Menurut Provinsi1458Literacy Rate (AMH) of Population above 15 Years Old by SexAngka Melek Huruf Penduduk Berumur 15 Tahun Ke Atas Menurut Jenis Kelamin1460Number of Children Out of School by Education Level and Area of ResidenceAngka Anak Tidak Sekolah Menurut Jenjang Pendidikan dan Daerah Tempat Tinggal1984Number of Children Out of School by Education Level and Expenditure GroupAngka Anak Tidak Sekolah Menurut Jenjang Pendidikan dan Kelompok Pengeluaran1988Number of Children Out of School by Education Level and GenderAngka Anak Tidak Sekolah Menurut Jenjang Pendidikan dan Jenis Kelamin1986Participation rate in organized learning (one year before primary school age) by GenderTingkat partisipasi dalam pembelajaran yang teroganisir (satu tahun sebelum usia sekolah dasar) menurut Jenis Kelamin1994Participation rate in organized learning (one year before primary school age) by provinceTingkat partisipasi dalam pembelajaran yang teroganisir (satu tahun sebelum usia sekolah dasar) menurut provinsi1990Participation rate in organized learning (one year before primary school age) by ResidenceTingkat partisipasi dalam pembelajaran yang teroganisir (satu tahun sebelum usia sekolah dasar) menurut Daerah Tempat Tinggal1992Proportion of Adolescents And Adults Aged 15-24 Years With The Information and Computer Technology Skills (ICT) by AreaProporsi Remaja Dan Dewasa Usia 15-24 Tahun Dengan Keterampilan Teknologi Informasi Dan Komputer (TIK) Menurut Daerah Tempat Tinggal1453Proportion of Adolescents And Adults Aged 15-24 Years With The Information and Computer Technology Skills (ICT) by ProvinceProporsi Remaja Dan Dewasa Usia 15-24 Tahun Dengan Keterampilan Teknologi Informasi Dan Komputer (TIK) Menurut Provinsi1451Proportion of Adolescents And Adults Aged 15-24 Years With The Information and Computer Technology Skills (ICT) by SexProporsi Remaja Dan Dewasa Usia 15-24 Tahun Dengan Keterampilan Teknologi Informasi Dan Komputer (TIK) Menurut Jenis Kelamin1454Proportion of Adolescents And Adults Aged 15-59 Years With The Information and Computer Technology Skills (ICT) by AreaProporsi Remaja Dan Dewasa Usia 15-59 Tahun Dengan Keterampilan Teknologi Informasi Dan Komputer (TIK) Menurut Daerah Tempat Tinggal1449Proportion of Adolescents And Adults Aged 15-59 Years With The Information and Computer Technology Skills (ICT) by ProvinceProporsi Remaja Dan Dewasa Usia 15-59 Tahun Dengan Keterampilan Teknologi Informasi Dan Komputer (TIK) Menurut Provinsi1447Proportion of Adolescents And Adults Aged 15-59 Years With The Information and Computer Technology Skills (ICT) by SexProporsi Remaja Dan Dewasa Usia 15-59 Tahun Dengan Keterampilan Teknologi Informasi Dan Komputer (TIK) Menurut Jenis Kelamin1450Proportion of Schools with Access to Proper Water Source FacilitiesProporsi Sekolah dengan Akses Fasilitas Sumber Air Layak1797Proportion of Schools with Computer AccessProporsi Sekolah dengan Akses Komputer1796Proportion of Schools with Electricity AccessProporsi Sekolah dengan Akses Listrik1794Ratio of Pure Participation Participation (APM) Female / Male by AreaRasio Angka Partisipasi Murni (APM) Perempuan/Laki-Laki Menurut Daerah Tempat Tinggal1456Ratio of Pure Participation Participation (APM) Female / Male by ProvinceRasio Angka Partisipasi Murni (APM) Perempuan/Laki-Laki Menurut Provinsi1455Ratio of Pure Participation Participation (APM) Female / Male by Revenue Group (Expenditures)Rasio Angka Partisipasi Murni (APM) Perempuan/Laki-Laki Menurut Kelompok Pendapatan (Pengeluaran)1608Ratio of Pure Participation Rate (APM) for Women / Men by Expenditure GroupRasio Angka Partisipasi Murni (APM) Perempuan/Laki-Laki Menurut Kelompok Pendapatan1607Rough Participation Rate of University by AreaAngka Partisipasi Kasar (APK) Perguruan Tinggi (PT) Menurut Daerah Tempat Tinggal1445Rough Participation Rate of University by Groups of ExpenditureAngka Partisipasi Kasar (APK) Perguruan Tinggi (PT) Menurut Kelompok Pengeluaran1444Rough Participation Rate of University by ProvinceAngka Partisipasi Kasar (APK) Perguruan Tinggi (PT) Menurut Provinsi1443Rough Participation Rate of University by SexAngka Partisipasi Kasar (APK) Perguruan Tinggi (PT) Menurut Jenis Kelamin1446Youth and adult participation rates in formal and non-formal education and training in the last 12 months, by genderTingkat partisipasi remaja dan dewasa dalam pendidikan dan pelatihan formal dan non formal dalam 12 bulan terakhir, menurut jenis kelamin1998Youth and adult participation rates in formal and non-formal education and training in the last 12 months, by ResidenceTingkat partisipasi remaja dan dewasa dalam pendidikan dan pelatihan formal dan non formal dalam 12 bulan terakhir, menurut Daerah Tempat Tinggal1996Youth and adult participation rates in formal and non-formal education and training in the past 12 months, according to Expenditure GroupsTingkat partisipasi remaja dan dewasa dalam pendidikan dan pelatihan formal dan non formal dalam 12 bulan terakhir, menurut Kelompok Pengeluaran2000Level of Proportion of women in managerial positions, according to marital statusProporsi perempuan yang berada di posisi managerial, menurut status perkawinan2007Level of Proportion of women in managerial positions, by area of residenceProporsi perempuan yang berada di posisi managerial, menurut Daerah Tempat Tinggal2004Level Proportion of women in managerial positions by provinceProporsi perempuan yang berada di posisi managerial menurut provinsi2003Level The proportion of women in managerial positions, by education levelProporsi perempuan yang berada di posisi managerial, menurut tingkat pendidikan2006Percentage of Seats Occupied In DPR and DPRDPersentase Kursi Yang Diduduki Perempuan Di DPR Dan DPRD1337Proportion of Adult Women and Girls (Aged 15-64 Years) Experiencing Violence (Physical, Sexual, Or Emotional) By Couples Or Former Couples In The Last 12 MonthsProporsi Perempuan Dewasa Dan Anak Perempuan (Umur 15-64 Tahun) Mengalami Kekerasan (Fisik, Seksual, Atau Emosional) Oleh Pasangan Atau Mantan Pasangan Dalam 12 Bulan Terakhir1375Proportion of Adult Women and Girls (Aged 15-64 Years) Experiencing Violence (Physical, Sexual, Or Emotional) By Couples Or Former Couples In The Last 12 Months by Type of ViolenceProporsi Perempuan Dewasa Dan Anak Perempuan (Umur 15-64 Tahun) Mengalami Kekerasan (Fisik, Seksual, Atau Emosional) Oleh Pasangan Atau Mantan Pasangan Dalam 12 Bulan Terakhir Menurut Jenis Kekerasan1378Proportion of Adult Women and Girls (Ages 15-64 Years) Experiencing Sexual Violence By Others In addition to Couples In The Last 12 MonthsProporsi Perempuan Dewasa Dan Anak Perempuan (Umur 15-64 Tahun) Mengalami Kekerasan Seksual Oleh Orang Lain Selain Pasangan Dalam 12 Bulan Terakhir1362Proportion of Individuals Using Mobile PhonesProporsi Individu Yang Menggunakan Telepon Genggam1221Proportion of Individuals Who Use Mobile Phones by Age GroupProporsi Individu Yang Menggunakan Telepon Genggam Menurut Kelompok Umur1222Proportion of Individuals Who Use Mobile Phones by SexProporsi Individu Yang Menggunakan Telepon Genggam Menurut Jenis Kelamin1224Proportion of Women Aged 20-24 Years Who Are Married Or Living Status Together Before Age 15 YearsProporsi Perempuan Umur 20-24 Tahun Yang Berstatus Kawin Atau Berstatus Hidup Bersama Sebelum Umur 15 Tahun1358Proportion of Women Aged 20-24 Years Who Are Married or Living Status Together Before Age 15 Years by Area of ResidenceProporsi Perempuan Umur 20-24 Tahun Yang Berstatus Kawin Atau Berstatus Hidup Bersama Sebelum Umur 15 Tahun Menurut Daerah Tempat Tinggal1359Proportion of Women Aged 20-24 Years Who Are Married or Living Status Together Before Age 18 Years By Area of ResidenceProporsi Perempuan Umur 20-24 Tahun Yang Berstatus Kawin Atau Berstatus Hidup Bersama Sebelum Umur 18 Tahun Menurut Daerah Tempat Tinggal1361Proportion of Women Aged 20-24 Years Who Are Married Or Living Status Together Before Age 18 Years by ProvinceProporsi Perempuan Umur 20-24 Tahun Yang Berstatus Kawin Atau Berstatus Hidup Bersama Sebelum Umur 18 Tahun Menurut Provinsi1360Percentage of Household Population by Province and Improved SanitationPersentase Rumah Tangga menurut Provinsi dan Memiliki Akses terhadap Sanitasi Layak847Percentage of Industrial Wastewater Flows Safely TreatedPersentase Limbah Cair Industri Cair yang Diolah Secara Aman1279Proportion of Hazardous and Toxic Waste (B3) Processed In accordance with the RegulationsProporsi Limbah Bahan Berbahaya dan Beracun (B3) Yang Diolah Sesuai Peraturan1281Proportion of Households Having Hand Washing Facility With Soap And Water By ProvinceProporsi Rumah Tangga Yang Memiliki Fasilitas Cuci Tangan Dengan Sabun Dan Air Menurut Provinsi1273Proportion of Households Who Have Access to Decent Sanitation Service by Area of ResidenceProporsi Rumah Tangga Penduduk Yang Memiliki Akses Terhadap Layanan Sanitasi Layak Dan Berkelanjutan Menurut Daerah Tempat Tinggal1270Proportion of Households Who Have Handwashing Facility With Soap And Water by Area of ResidenceProporsi Rumah Tangga Yang Memiliki Fasilitas Cuci Tangan Dengan Sabun Dan Air Menurut Daerah Tempat Tinggal1274Proportion of Population Populations Who Have Access to Decent and Sustainable Sanitation Services By Revenue GroupPersentase Rumah Tangga yang Memiliki Akses Terhadap Layanan Sanitasi Layak Menurut Kelompok Pengeluaran1272Electricity Consumption per CapitaKonsumsi Listrik per Kapita1156Electrification RatioRasio Elektrifikasi1155Number of gas network connections for householdsJumlah sambungan jaringan gas untuk rumah tangga1786Primary Energy IntensityIntensitas Energi Primer1808Ratio of Domestic Gas UseRasio Penggunaan Gas Rumah Tangga1157Supply of Primary EnergyBauran Energi Terbarukan1824[2010 Version] Growth Rate of per Capita Gross Regional Domestic Product at 2010 Constant Market Prices[Seri 2010] Laju Pertumbuhan Produk Domestik Regional Bruto Per Kapita Atas Dasar Harga Konstan 2010296[2010 Version] Per Capita Gross Regional Domestic Product by Province[Seri 2010] Produk Domestik Regional Bruto Per Kapita288Average Working Hourly Wage by ProvinceUpah Rata - Rata Per Jam Pekerja Menurut Provinsi1172Average Working Hour Rate by Area of ResidenceUpah Rata - Rata Per Jam Pekerja Menurut Daerah Tempat Tinggal1173Average Working Hours Period by Age GroupUpah Rata - Rata Per Jam Pekerja Menurut Kelompok Umur1176Average Working Hours Rate by Education LevelUpah Rata - Rata Per Jam Pekerja Menurut Tingkat Pendidikan1175Average Working Hours Wage by GenderUpah Rata - Rata Per Jam Pekerja Menurut Jenis Kelamin1174Growth Rate of GDP Per Labor / Growth Rate of Real GDP Per Person Work Per YearLaju Pertumbuhan PDB Per Tenaga Kerja/Tingkat Pertumbuhan PDB Riil Per Orang Bekerja Per Tahun1161Half Unemployment Rate by Age GroupTingkat Setengah Pengangguran Menurut Kelompok Umur1185Half Unemployment Rate by Area of ResidenceTingkat Setengah Pengangguran Menurut Daerah Tempat Tinggal1182Half Unemployment Rate by Education LevelTingkat Setengah Pengangguran Menurut Tingkat Pendidikan1184Half Unemployment Rate by ProvinceTingkat Setengah Pengangguran Menurut Provinsi1181Half Unemployment Rate by SexTingkat Setengah Pengangguran Menurut Daerah Jenis Kelamin1183Number of foreign tourist visits per month to Indonesia according to the entrance, 2008 - 2017Jumlah Kunjungan Wisatawan Mancanegara per bulan ke Indonesia Menurut Pintu Masuk, 2008 - 201774Number of foreign tourist visits per month to Indonesia according to the entrance, 2017 - nowJumlah Kunjungan Wisatawan Mancanegara per bulan ke Indonesia Menurut Pintu Masuk, 2017 - sekarang1150Number of Foreign Tourist Visits to Indonesia by Nationality, 2000-2014Jumlah Kunjungan Wisatawan Mancanegara ke Indonesia Menurut Kebangsaan, 2000-2014351Number of Foreign Tourist Visits to Indonesia by Nationality, 2015-nowJumlah Kunjungan Wisatawan Mancanegara ke Indonesia Menurut Kebangsaan1821Number of Nusantara Tourist TravelsJumlah Perjalanan Wisatawan Nusantara1189Percentage and number of working children aged 10-17 years by provincePersentase dan jumlah anak usia 10-17 tahun yang bekerja menurut provinsi2008Percentage and number of working children aged 10-17 years by sexPersentase dan jumlah anak usia 10-17 tahun yang bekerja menurut jenis kelamin2009Percentage of Young Age (15-24 Years) Who Are Not School, Working Or Following TrainingPersentase Usia Muda (15-24 Tahun) Yang Sedang Tidak Sekolah, Bekerja Atau Mengikuti Pelatihan1186Proportion of Informal Employment in Total Employment by Age GroupProporsi Lapangan Kerja Informal Menurut Kelompok Umur2156Proportion of Informal Employment in Total Employment by Educational LevelProporsi Lapangan Kerja Informal Menurut Tingkat Pendidikan2157Proportion of Informal Employment in Total Employment by ProvinceProporsi Lapangan Kerja Informal Menurut Provinsi2153Proportion of Informal Employment in Total Employment by SexProporsi Lapangan Kerja Informal Menurut Jenis Kelamin2155Proportion of Informal Employment in Total Employment by Urban-Rural ClassificationProporsi Lapangan Kerja Informal Menurut Daerah Tempat Tinggal2154Proportion of MSME Credits to Total CreditProporsi Kredit UMKM Terhadap Total Kredit1192Proportion of Tourism Contribution to GDPProporsi Kontribusi Pariwisata Terhadap PDB1188Total Foreign Exchange of Tourism SectorJumlah Devisa Sektor Pariwisata1160Unemployment Rate by Age GroupTingkat Pengangguran Terbuka Berdasarkan Kelompok Umur1180Unemployment Rate by Area of ResidenceTingkat Pengangguran Terbuka Berdasarkan Daerah Tempat Tinggal1178Unemployment Rate by Education LevelTingkat Pengangguran Terbuka Berdasarkan Tingkat Pendidikan1179Unemployment Rate by SexTingkat Pengangguran Terbuka Berdasarkan Jenis Kelamin1177Growth Rate of GDP Manufacturing IndustryLaju Pertumbuhan PDB Industri Manufaktur1216Number of Airports In Indonesia By Airport UsageJumlah Bandara Di Indonesia Menurut Penggunaan Bandar Udara1202Number of Domestic Passengers by Airplane Mode of Transportation by provinceJumlah Penumpang Domestik berdasarkan Moda Transportasi Pesawat Terbang menurut provinsi2024Number of Domestic Passengers by Mode of Ship Transportation by provinceJumlah Penumpang Domestik berdasarkan Moda Transportasi Kapal menurut provinsi2022Number of Ferry Ports in IndonesiaJumlah Pelabuhan Penyeberangan Di Indonesia1208Number of Ferry Ports in Indonesia by Type of OperationJumlah Pelabuhan Penyeberangan Di Indonesia Menurut Jenis Pengoperasian1210Number of International Passengers by Airplane Mode of Transportation by provinceJumlah Penumpang Internasional berdasarkan Moda Transportasi Pesawat Terbang menurut provinsi2027Number of Passengers based on Railway Transportation ModeJumlah Penumpang berdasarkan Moda Transportasi Kereta Api2051Number of Strategic PortsJumlah Pelabuhan Strategis1211Number of Strategic Ports According to Their ManagementJumlah Pelabuhan Strategis Menurut Pengelolaannya1213Percentage of Toll Road Lengths Operated By OperatorPersentase Panjang Jalan Tol yang Beroperasi Menurut Operatornya1200Proportion of Added Value of Manufacture Sector To GDPProporsi Nilai Tambah Sektor Industri Manufaktur Terhadap PDB1214Proportion of Added Value of Manufacturing Industry Sector per CapitaProporsi Nilai Tambah Sektor Industri Manufaktur per Kapita1215Proportion of Added Value of Small Industry to Total Value Added IndustryProporsi Nilai Tambah Industri Kecil Terhadap Total Nilai Tambah Industri1219Proportion of Government Research Budget to GDPProporsi Anggaran Riset Pemerintah Terhadap PDB1825Proportion of Manpower in Manufacturing Industry SectorProporsi Tenaga Kerja pada Sektor Industri Manufaktur1217Proportion of Small Industry With Loans Or CreditProporsi Industri Kecil Dengan Pinjaman Atau Kredit1220Railway Network Length In IndonesiaPanjang Jaringan Jalan Rel Kereta Api Di Indonesia1195Steady Condition of National RoadsKondisi Mantap Jalan Nasional1197Average Economic Growth In Disadvantaged AreasRata-Rata Pertumbuhan Ekonomi Di Daerah Tertinggal1237Gini RatioGini Rasio98Indonesia Democracy Index (IDI) by Aspect and ProvinceIndeks Demokrasi Indonesia (IDI) Menurut Aspek dan Provinsi599Number of complaints handling of human rights violations of women especially violence against womenJumlah penanganan pengaduan pelanggaran Hak Asasi Manusia (HAM) perempuan terutama kekerasan terhadap perempuan1414Number of Disadvantaged VillagesJumlah Desa Tertinggal1231Number of Independent Villages by Province (Villages)Jumlah Desa Mandiri Menurut Provinsi2190Number of Underdeveloped Villages (Villages)Jumlah Desa Tertinggal menurut Provinsi (Desa)2191Percentage of Budget Plan for Central Government Social Protection Function ExpendituresPersentase Rencana Anggaran Untuk Belanja Fungsi Perlindungan Sosial Pemerintah Pusat1611Persentase Penduduk Miskin Menurut Kabupaten/KotaPersentase Penduduk Miskin Menurut Kabupaten/Kota621Proportion of population living below 50 percent of median income, by provinceProporsi penduduk yang hidup di bawah 50 persen dari median pendapatan, menurut provinsi2011Number of Deaths, Disappeared, and Hurt Victims AffectedJumlah Korban Meninggal, Hilang, dan Terluka Terkena Dampak Bencana1804Number of Deaths, Disappeared, and Hurt Victims Affected by 100,000 PeopleJumlah Korban Meninggal, Hilang, dan Terluka Terkena Dampak Bencana Per 100.000 Orang1246Percentage of Households who Have Access To A Decent And Affordable Housing According to the Area of ResidencePersentase Rumah Tangga yang Memiliki Akses Terhadap Hunian Yang Layak Dan Terjangkau Menurut Daerah Tempat Tinggal1242Percentage of Households who Have Access To A Decent And Affordable Residential by ProvincePersentase Rumah Tangga yang Memiliki Akses Terhadap Hunian Yang Layak Dan Terjangkau Menurut Provinsi1241Percentage of households with convenient access (0.5 km distance) to public transportation by provincePersentase rumah tangga yang memiliki akses nyaman (jarak 0.5 km) ke transportasi umum menurut provinsi2012Percentage of population aged 10 years and over using public motorized vehicles on certain routes by provincePersentase penduduk berumur 10 tahun ke atas yang menggunakan kendaraan bermotor umum dengan rute tertentu menurut provinsi2013Percentage of Victims of Violence in the Last 12 Months Reporting to the PolicePersentase Korban Kekerasan Dalam 12 Bulan Terakhir Yang Melaporkan Kepada Polisi1252Percentage of Victims of Violence in the Last 12 Months Reporting to the Police by SexPersentase Korban Kekerasan Dalam 12 Bulan Terakhir Yang Melaporkan Kepada Polisi Menurut Jenis Kelamin1253Proportion of People Who Became Victims of Violent Violence In The Last 12 Months By Age GroupProporsi Penduduk Yang Menjadi Korban Kejahatan Kekerasan Dalam 12 Bulan Terakhir Menurut Kelompok Umur1310Proportion of People Who Became Victims of Violent Violence In The Last 12 Months By SexProporsi Penduduk Yang Menjadi Korban Kejahatan Kekerasan Dalam 12 Bulan Terakhir Menurut Jenis Kelamin1309Proportion of Population Who Became Victims of Violent Violence in the Last 12 Months by ProvinceProporsi Penduduk Yang Menjadi Korban Kejahatan Kekerasan Dalam 12 Bulan Terakhir Menurut Provinsi1311Proportion of Population Who Became Victims of Violent Violence In The Last 12 Months By Region ClassificationProporsi Penduduk Yang Menjadi Korban Kejahatan Kekerasan Dalam 12 Bulan Terakhir Menurut Klasifikasi Wilayah1308Unemployment Rate by SexTingkat Pengangguran Terbuka Berdasarkan Jenis Kelamin1177Number of Companies Implementing SNI ISO 14001 CertificationJumlah Perusahaan yang Menerapkan Sertifikasi SNI ISO 140011744Number of Public Facilities that Implement Community Service Standards (SPM) and RegisteredJumlah Fasilitas Publik yang Menerapkan Standar Pelayanan Masyarakat (SPM) dan Teregister1748Number of Registered Green ProductsJumlah Produk Ramah Lingkungan yang Teregister1746Number of Deaths, Disappeared, and Hurt Victims AffectedJumlah Korban Meninggal, Hilang, dan Terluka Terkena Dampak Bencana1804Number of Deaths, Disappeared, and Hurt Victims Affected by 100,000 PeopleJumlah Korban Meninggal, Hilang, dan Terluka Terkena Dampak Bencana Per 100.000 Orang1246Number of Water Conservation AreasJumlah Kawasan Konservasi Perairan1289Proportion of catches of fish species that are within safe biological limitsProporsi Tangkapan Jenis Ikan yang Berada Dalam Batasan Biologis yang Aman1586Number of Endangered AnimalsJumlah Satwa Terancam Punah1297Anti-Corruption Behaviour Index (ACBI) by Age GroupIndeks Perilaku Anti Korupsi (IPAK) Menurut Kelompok Umur1499Anti-Corruption Behaviour Index (ACBI) by DimensionIndeks Perilaku Anti Korupsi (IPAK) Menurut Dimensi635Anti-Corruption Behaviour Index (ACBI) by Dimension and Age GroupIndeks Perilaku Anti Korupsi (IPAK) Menurut Dimensi dan Kelompok Umur594Anti-Corruption Behaviour Index (ACBI) by Dimension and Level of EducationIndeks Perilaku Anti Korupsi (IPAK) Menurut Dimensi dan Jenjang Pendidikan597Anti-Corruption Behaviour Index (ACBI) by Dimension and SexIndeks Perilaku Anti Korupsi (IPAK) Menurut Dimensi dan Jenis Kelamin592Anti-Corruption Behaviour Index (ACBI) by Dimension Urban-Rural ClassificationIndeks Perilaku Anti Korupsi (IPAK) Menurut Dimensi dan Daerah Tempat Tinggal595Anti-Corruption Behaviour Index (ACBI) by Level of EducationIndeks Perilaku Anti Korupsi (IPAK) Menurut Jenjang Pendidikan1504Anti-Corruption Behaviour Index (ACBI) by Urban-Rural ClassificationIndeks Perilaku Anti Korupsi (IPAK) Menurut Daerah Tempat Tinggal1501Household Poporsi Who Has Child Age 1-17 Years Who Have Physical Sentence And / Or Psychological Aggression From The Caregiver In The Last Year By Region Of ResidencePoporsi Rumah Tangga Yang Memiliki Anak Umur 1-17 Tahun Yang Mengalami Hukuman Fisik Dan/Atau Agresi Psikologis Dari Pengasuh Dalam Setahun Terakhir Menurut Wilayah Tempat Tinggal1392Indonesia Democracy Index (IDI) by IndicatorsIndeks Demokrasi Indonesia (IDI) Menurut Indikator598Indonesia Democracy Index (IDI) by VariablesIndeks Demokrasi Indonesia (IDI) Menurut Variabel598Indonesian Democracy Index (IDI) by ProvinceIndeks Demokrasi Indonesia (IDI) Menurut Provinsi598Number of Complaints Handling Human Rights ViolationsJumlah Penanganan Pengaduan Pelanggaran Hak Asasi Manusia1240Number of Murder Crimes cases in the past yearJumlah Kasus Kejahatan Pembunuhan Pada Satu Tahun Terakhir1306Percentage of children who have birth certificate by Area of ResidencePersentase anak yang memiliki akta kelahiran Menurut Daerah Tempat Tinggal1413Percentage of children who have birth certificate by ProvincePersentase anak yang memiliki akta kelahiran Menurut Provinsi1412Percentage of Compliance with the implementation of Public Service Law for Ministry/InstitutionPersentase Kepatuhan pelaksanaan UU Pelayanan Publik untuk KL1236Percentage of coverage of birth certificate ownership among population 0-17 years old by provincePersentase cakupan kepemilikan akta kelahiran pada penduduk 0-17 tahun menurut provinsi2014Percentage of Population Age 0-17 With Birth Certificate Ownership (Bottom 40%), by ProvincePersentase Penduduk Usia 0-17 Tahun Dengan Kepemilikan Akta Lahir (40% Terbawah), Menurut Provinsi1570Percentage of Population Age 0-17 With Birth Certificate Ownership (Lower 40%), According to GenderPersentase Penduduk Usia 0-17 Tahun Dengan Kepemilikan Akta Lahir (40% Terbawah), Menurut Jenis Kelamin1573Percentage of Population Age 0-17 With Birth Certificate Ownership (Lower 40%), by Area TypePersentase Penduduk Usia 0-17 Tahun Dengan Kepemilikan Akta Lahir (40% Terbawah), Menurut Daerah Tempat Tinggal1487Poporsi Rumah Tangga Yang Memiliki Anak Umur 1-17 Tahun Yang Mengalami Hukuman Fisik Dan/Atau Agresi Psikologis Dari Pengasuh Dalam Setahun TerakhirPoporsi Rumah Tangga Yang Memiliki Anak Umur 1-17 Tahun Yang Mengalami Hukuman Fisik Dan/Atau Agresi Psikologis Dari Pengasuh Dalam Setahun Terakhir1391Prevalence of Violence Against GirlsPrevalensi Kekerasan Terhadap Anak Perempuan1364Prevalence of Violence Against Girls by AgeProporsi laki-laki muda umur 18-24 tahun yang mengalami kekerasan seksual sebelum umur 18 tahun1371Prevalence of Violence Against Girls by Type of ViolencePrevalensi Kekerasan Terhadap Anak Laki-Laki1369Proportion of Households with 1-17 Years Old Children Who Have Physical Sentence And / Or Psychological Aggression From Caretakers In The Last YearProporsi Rumah Tangga Yang Memiliki Anak Umur 1-17 Tahun Yang Mengalami Hukuman Fisik Dan/Atau Agresi Psikologis Dari Pengasuh Dalam Setahun Terakhir1313Proportion of Households with Children Aged 1-17 Years Experiencing Physical Sentence And / Or Psychological Aggression From Caretakers In The Last Year By TerritoryProporsi Rumah Tangga Yang Memiliki Anak Umur 1-17 Tahun Yang Mengalami Hukuman Fisik Dan/Atau Agresi Psikologis Dari Pengasuh Dalam Setahun Terakhir Menurut Wilayah Tempat Tinggal1314Proportion of prisoners who exceed the period of detention of the entire number of prisonersProporsi tahanan yang melebihi masa penahanan terhadap seluruh jumlah tahanan1191Proportion of Safe Residents Walking Alone In The Area Where Its HealedProporsi Penduduk Yang Merasa Aman Berjalan Sendirian Di Area Tempat Tinggalnya1312The proportion of children under 5 years of age whose birth is recorded by civil registration agencies by ProvinceProporsi anak umur di bawah 5 tahun yang kelahirannya dicatat oleh lembaga pencatatan sipil Menurut Provinsi1410The proportion of children under 5 years of age whose birth is recorded by civil registration agencies by sexProporsi anak umur di bawah 5 tahun yang kelahirannya dicatat oleh lembaga pencatatan sipil Menurut Jenis Kelamin1411The proportion of crime victims in the last 12 months reporting to the policeProporsi Korban Kekerasan dalam 12 bulan terakhir yang Melaporkan Kepada Polisi1187The proportion of major government expenditures to approved budgetsProporsi pengeluaran utama pemerintah terhadap anggaran yang disetujui1235The proportion of women and young men aged 18-24 years who experienced sexual violence before the age of 18 yearsProporsi perempuan dan laki-laki muda umur 18-24 tahun yang mengalami kekerasan seksual sebelum umur 18 tahun1318Growth of Non Oil and Gas Product ExportsPertumbuhan Ekspor Produk Non Migas1261Percentage of Data Users Who Use BPS Data as The Basis for National Development Planning, Monitoring and EvaluationPersentase Pengguna Data yang Menggunakan Data BPS Sebagai Dasar Perencanaan, Monitoring dan Evaluasi Pembangunan Nasional1606Percentage of subscribers served by fixed broadband internet access networks to total households, by provincePersentase pelanggan terlayani jaringan internet akses tetap pitalebar (fixed broadband) terhadap total rumah tangga, menurut provinsi2015Proportion of Debt and Debt Service to Export of Goods and ServicesProporsi Pembayaran Utang Dan Bunga (Debt Service) Terhadap Ekspor Barang Dan Jasa1260Proportion of Realization of Government Revenues to Gross Domestic ProductProporsi Realisasi Pendapatan Pemerintah Terhadap Produk Domestik Bruto1588Proportion of Remittance Volume (In US Dollars) To Total GDPProporsi Volume Remitansi (Dalam US Dollars) Terhadap Total PDB1258Ratio of Tax Revenue to GDPRasio Penerimaan Pajak Terhadap PDB1529

How to View SDGs data
Data table can be consumed using "data" Model, and 0000 Domain to display specific id var (refer to menu Dynamic Data documentation above).
https://webapi.bps.go.id/v1/api/list/model/data/domain/0000/var/id_var_in_table_above/key/your_api_key/
example: Number of Deaths, Disappeared, and Hurt Victims Affectedhttps://webapi.bps.go.id/v1/api/list/model/data/domain/0000/var/1804/key/your_api_key/

              
Send a Sample Request

Special Data Dissemination Standard (SDDS)
List All SDDS Table
This service is used to displays all SDDS table, domain must be "0000"
https://webapi.bps.go.id/v1/list

Parameter
FieldTypeDescriptionmodelStringModel to display sdds table is "sdds"
keyStringKey app to access API
Send a Sample Request

SDDS Table List
This table is updated annually without prior notice
VariableVariable (id)ModelId VarWholesale Price Index (WPI) (2018=100)Indeks Harga Perdagangan Besar (IHPB) Indonesia (2018=100)data1721Number and Percentage of Employment and UnemploymentJumlah dan Persentase Penduduk Bekerja dan Penganggurandata1953Average of Net Wage/SalaryRata-Rata Upah/Gajidata1521Inflation by Personal Care and Other Services Group and Sub (2018=100)Inflasi (2018=100) Menurut Kelompok dan Sub Kelompok 11 Perawatan Pribadi dan Jasa Lainnyadata1904Inflation by Provision of Food and Beverages / Restaurant Group and Sub (2018=100)Inflasi (2018=100) Menurut Kelompok dan Sub Kelompok 10 Penyediaan Makanan dan Minuman / Restorandata1903Penduduk Berumur 15 tahun ke atas menurut jenis kegiatanPenduduk Berumur 15 tahun ke atas menurut jenis kegiatandata529Value of Export Oil&Gas - Non Oil&GasNilai Ekspor Migas-NonMigasdata1753[2010 Version] 3. Distribution of GDP at Current Market Prices by Expenditure[Seri 2010] 3. Distribusi PDB Triwulanan Atas Dasar Harga Berlaku menurut Pengeluarandata110[2010 Version] 4. Growth Rate of GDP at Constant Market Prices By Expenditure[Seri 2010] 4. Laju Pertumbuhan PDB menurut Pengeluarandata108Consumer Price Index of 90 City (General)Indeks Harga Konsumen 90 Kota (Umum)data1709Consumer Price Index of Foods, Beverages and Tobacco Group and Sub (2022=100)Indeks Harga Konsumen (2022=100) Menurut Kelompok dan Sub Kelompok 01 Makanan, Minuman dan Tembakaudata2212Value of Import Oil&Gas - Non Oil&GasNilai Impor Migas-NonMigasdata1754GDP Implicit Growth by Industry (2010=100)[Seri 2010] Laju Implisit PDB Menurut Lapangan Usaha Seri 2010data105Distribution of GDP at Current Market Prices by Industry (2010=100)[Seri 2010] Distribusi PDB Menurut Lapangan Usaha Seri 2010 Atas Dasar Harga Berlakudata106Growth Rate of GDP by Industry (2010=100)[Seri 2010] Laju Pertumbuhan PDB Seri 2010data104Consumer Price Index of Health Group and Sub (2022=100)Indeks Harga Konsumen (2022=100) Menurut Kelompok dan Sub Kelompok 05 Kesehatandata2216Consumer Price Index of 38 Province (2022=100)Indeks Harga Konsumen 38 Provinsi (2022=100)data2261Inflation by Food, Beverage and Tobacco Group and Sub (2018 = 100)Inflasi (2018=100) Menurut Kelompok dan Sub Kelompok 01 Makanan, Minuman dan Tembakaudata1890Inflation by Clothing and Footwear Group and Sub (2018=100)Inflasi (2018=100) Menurut Kelompok dan Sub Kelompok 02 Pakaian dan Alas Kakidata1894Inflation by Housing, Water, Electricity and Household Fuel Group and Sub (2018=100)Inflasi (2018=100) Menurut Kelompok dan Sub Kelompok 03 Perumahan, Air, Listrik dan Bahan Bakar Rumah Tanggadata1895Inflation by Equipments and Routine Household Maintenance Group and Sub (2018=100)Inflasi (2018=100) Menurut Kelompok dan Sub Kelompok 04 Perlengkapan, Peralatan dan Pemeliharaan Rutin Rumah Tanggadata1897Inflation by Health Group and Sub (2018=100)Inflasi (2018=100) Menurut Kelompok dan Sub Kelompok 05 Kesehatandata1898Inflation by Transportation Group and Sub (2018=100)Inflasi (2018=100) Menurut Kelompok dan Sub Kelompok 06 Transportasidata1899Inflation by Information, Communication and Financial Services Group and Sub (2018=100)Inflasi (2018=100) Menurut Kelompok dan Sub Kelompok 07 Informasi, Komunikasi dan Jasa Keuangandata1900Inflation by Recreation, Sports and Culture Group and Sub (2018=100)Inflasi (2018=100) Menurut Kelompok dan Sub Kelompok 08 Rekreasi, Olahraga dan Budayadata1901Inflation by Education Group and Sub (2018=100)Inflasi (2018=100) Menurut Kelompok dan Sub Kelompok 09 Pendidikandata1902Source of Growth of GDP by Industry (2010=100)[Seri 2010] Sumber Pertumbuhan PDB Menurut Lapangan Usaha Seri 2010data554Mid Year PopulationJumlah Penduduk Pertengahan Tahundata1975Population Growth RateLaju Pertumbuhan Pendudukdata1976Consumer Price Index of Transportation Group and Sub (2022=100)Indeks Harga Konsumen (2022=100) Menurut Kelompok dan Sub Kelompok 06 Transportasidata2217Consumer Price Index of Information, Communication and Financial Service Group and Sub (2022=100)Indeks Harga Konsumen (2022=100) Menurut Kelompok dan Sub Kelompok 07 Informasi, Komunikasi dan Jasa Keuangandata2218Consumer Price Index of Recreation, Sport and Culture Group and Sub (2022=100)Indeks Harga Konsumen (2022=100) Menurut Kelompok dan Sub Kelompok 08 Rekreasi, Olahraga dan Budayadata2219Consumer Price Index of Education Group and Sub (2022=100)Indeks Harga Konsumen (2022=100) Menurut Kelompok dan Sub Kelompok 09 Pendidikandata2220Consumer Price Index of Provision of Food and Beverages / Restaurant Group and Sub (2022=100)Indeks Harga Konsumen (2022=100) Menurut Kelompok dan Sub Kelompok 10 Penyediaan Makanan dan Minuman / Restorandata2221Unemployment Rate by ProvinceTingkat Pengangguran Terbuka Menurut Provinsidata543Consumer Price Index of Foods, Beverages and Tobacco Group and Sub (2018=100)Indeks Harga Konsumen (2018=100) Menurut Kelompok dan Sub Kelompok 01 Makanan, Minuman dan Tembakaudata1905Consumer Price Index of Clothing and Footwear Group and Sub (2018=100)Indeks Harga Konsumen (2018=100) Menurut Kelompok dan Sub Kelompok 02 Pakaian dan Alas Kakidata1906Consumer Price Index of Housing, Water, Electricity and Household Fuel Group and Sub (2018=100)Indeks Harga Konsumen (2018=100) Menurut Kelompok dan Sub Kelompok 03 Perumahan, Air, Listrik dan Bahan Bakar Rumah Tanggadata1907Consumer Price Index of Equipments and Routine Household Maintenance Group and Sub (2018=100)Indeks Harga Konsumen (2018=100) Menurut Kelompok dan Sub Kelompok 04 Perlengkapan, Peralatan dan Pemeliharaan Rutin Rumah Tanggadata1908Consumer Price Index of Health Group and Sub (2018=100)Indeks Harga Konsumen (2018=100) Menurut Kelompok dan Sub Kelompok 05 Kesehatandata1909Consumer Price Index of Transportation Group and Sub (2018=100)Indeks Harga Konsumen (2018=100) Menurut Kelompok dan Sub Kelompok 06 Transportasidata1910Consumer Price Index of Information, Communication and Financial Service Group and Sub (2018=100)Indeks Harga Konsumen (2018=100) Menurut Kelompok dan Sub Kelompok 07 Informasi, Komunikasi dan Jasa Keuangandata1911Consumer Price Index of Recreation, Sport and Culture Group and Sub (2018=100)Indeks Harga Konsumen (2018=100) Menurut Kelompok dan Sub Kelompok 08 Rekreasi, Olahraga dan Budayadata1912Consumer Price Index of Education Group and Sub (2018=100)Indeks Harga Konsumen (2018=100) Menurut Kelompok dan Sub Kelompok 09 Pendidikandata1913Consumer Price Index of Provision of Food and Beverages / Restaurant Group and Sub (2018=100)Indeks Harga Konsumen (2018=100) Menurut Kelompok dan Sub Kelompok 10 Penyediaan Makanan dan Minuman / Restorandata1915Consumer Price Index of Personal Care and Other Services Group and Sub (2018=100)Indeks Harga Konsumen (2018=100) Menurut Kelompok dan Sub Kelompok 11 Perawatan Pribadi dan Jasa Lainnyadata1916GDP by Industry (2010=100)[Seri 2010] PDB Menurut Lapangan Usaha Seri 2010data65Consumer Price Index of Clothing and Footwear Group and Sub (2022=100)Indeks Harga Konsumen (2022=100) Menurut Kelompok dan Sub Kelompok 02 Pakaian dan Alas Kakidata2213Consumer Price Index of Housing, Water, Electricity and Household Fuel Group and Sub (2022=100)Indeks Harga Konsumen (2022=100) Menurut Kelompok dan Sub Kelompok 03 Perumahan, Air, Listrik dan Bahan Bakar Rumah Tanggadata2214Quaterly Large and Medium Manufacturing (2010=100)IBS Triwulanan (2010=100)data89Monthly Large and Medium Manufacturing (2010=100)IBS Bulanan (2010=100)data88[2010 Version] 1. GDP at Current Market Prices by Expenditure[Seri 2010] 1. PDB Triwulanan Atas Dasar Harga Berlaku menurut Pengeluarandata1955[2010 Version] 2. GDP at Constant Market Prices by Expenditure[Seri 2010] 2. PDB Triwulanan Atas Dasar Harga Konstan menurut Pengeluarandata1956Wholesale Price Index (WPI) of Indonesia (2023=100)Indeks Harga Perdagangan Besar (IHPB) Indonesia (2023=100)data2498Consumer Price Index of Equipments and Routine Household Maintenance Group and Sub (2022=100)Indeks Harga Konsumen (2022=100) Menurut Kelompok dan Sub Kelompok 04 Perlengkapan, Peralatan dan Pemeliharaan Rutin Rumah Tanggadata2215Consumer Price Index of Personal Care and Other Services Group and Sub (2022=100)Indeks Harga Konsumen (2022=100) Menurut Kelompok dan Sub Kelompok 11 Perawatan Pribadi dan Jasa Lainnyadata2222Indeks Harga Perdagangan Internasional (IHPI) 2010=100Indeks Harga Perdagangan Internasional (IHPI) 2010=100data1722Export Price Index (2023=100)Indeks Harga Ekspor (2023=100)data2487Import Price Index (2023=100)Indeks Harga Impor (2023=100)data2490Quarterly Number and Percentage of Employed and Unemployed PopulationJumlah dan Persentase Penduduk Bekerja dan Pengangguran (Triwulanan)data2560Quarterly Average of Net Wage/SalaryRata-Rata Upah/Gaji (Triwulanan)data2563Quarterly Unemployment Rate by ProvinceTingkat Pengangguran Terbuka menurut Provinsi (Triwulanan)data2562Quarterly Population aged 15 years and over according to type of activityPenduduk Berumur 15 tahun ke Atas menurut Jenis Kegiatan (Triwulanan)data2561

How to View SDDS data
Data table can be consumed using "data" or "statictable" Model (check the table below), and 0000 Domain to display specific id var (refer to menu Dynamic Data documentation above). For more information about SDDS, click here
https://webapi.bps.go.id/v1/api/list/model/Model_in_table_below/domain/0000/var/id_var_in_table_below/key/your_api_key/
example: Value of Export Oil&Gas - Non Oil&Gashttps://webapi.bps.go.id/v1/api/list/model/data/domain/0000/var/1753/key/your_api_key/

              
Send a Sample Request

Statistical Classifications
There are two kind of classifications that WebAPI provides: Klasifikasi Baku Lapangan Usaha Indonesia (KBLI: 2009, 2015, 2017, and 2020) that based on International Standard Industrial Classification of All Economic Activities (ISIC), and Klasifikasi Baku Komoditi Indonesia (KBKI 2015). For more information, Click here
Detail of Statistical Classification
This service is used to displays detail of a statistical classification are shown on the website
https://webapi.bps.go.id/v1/api/view

Parameter
FieldTypeDescriptionmodelStringModel that allowed:
Allowed values:
KBLI: "kbli2009", "kbli2015", "kbli2017", "kbli2020"
KBKI: "kbki2015"
langStringLanguage to display
Default value: ind
Allowed values: "ind", "eng"
idStringstatistical classification id to display
Example: kbli_2009_01, kbki_2020_012
keyStringKey app to access API
Send a Sample Request


Success Response
{
  "status": "OK",
  "data-availability": "available",
  "data": [
    {
      "page": x,
      "pages": x,
      "per_page": x,
      "count": x,
      "total": x
    },
    [
      {
        "_index": "...",
        "_type": "...",
        "_id": "kbli_2020_011",
        "_score": x,
        "_source": {
          "konten": "...",
          "jenis": "...",
          "id": "...",
          "source": "Metadata Management System (MMS)",
          "judul": "...",
          "title": "...",
          "deskripsi": "...",
          "description": "...",
          "isbn": x,
          "issn": x,
          "no_katalog": x,
          "no_publikasi": x,
          "last_update": "date",
          "tgl_rilis": "date",
          "lokasi": null,
          "url": "https://www.bps.go.id/klasifikasi/app/view/model/code",
          "level": "...",
          "mfd": null,
          "sebelumnya": [
            {
            ...,
              "kode": "...",
              "judul": "...",
              "deskripsi": "..."
            },
            ...
          ],
          "turunan": [
            {
              ...,
              "kode": "...",
              "deskripsi": "...",
              "judul": "..."
            },
            ...

          ],
          "flag": ...,
          "tags": [
            ...,
            "...",
            ...
          ]
        }
      }
    ]
  ]
}

Error 4xx
NameDescriptionUserNotFoundThe id of the User was not found.

Error Response
HTTP/1.1 404 Not Found
  {
    "error": "UserNotFound"
  }

List of Statistical Classification
This service is used to list all of the statistical classification
https://webapi.bps.go.id/v1/api/list/

Parameter
FieldTypeDescriptionmodelStringModel that allowed:
Allowed values:
KBLI: "kbli2009", "kbli2015", "kbli2017", "kbli2020"
KBKI: "kbki2015"
page optionalNumberPage to display statistical classification
Allowed values: 1, 2, 3, 4, ..., n
per page optionalNumberNumber of statistical classification to display
level optionalStringlevel of item
KBLI: kategori, golongan pokok, golongan, subgolongan, kelompok
KBKI: seksi, divisi, kelompok, kelas, subkelas, kelompok komoditas, kelompok
keyStringKey app to access API
Send a Sample Request

Success Response
{
  "status": "OK",
  "data-availability": "available",
  "data": [
    {
      "page": 1,
      "pages": 2710,
      "per_page": 1,
      "count": 1,
      "total": 2710
    },
    [
      {
        "_index": "datacontent",
        "_type": "_doc",
        "_id": "kbli_2020_01",
        "_score": null,
        "_source": {
          "konten": "...",
          "jenis": "...",
          "id": "klasifikasi_tahun_kode",
          "source": "Metadata Management System (MMS)",
          "judul": "...",
          "title": "...",
          "deskripsi": "...",
          "description": "...",
          "isbn": null,
          "issn": null,
          "no_katalog": null,
          "no_publikasi": null,
          "last_update": "date",
          "tgl_rilis": "date",
          "lokasi": null,
          "url": "https://www.bps.go.id/klasifikasi/app/view/klasifikasi/kode",
          "level": "...",
          "mfd": null,
          "sebelumnya": [
            {
              "kode": "...",
              "judul": "...",
              "deskripsi": "..."
            }
          ],
          "turunan": [
            ...,
            {
              "kode": "...",
              "deskripsi": "...",
              "judul": "..."
            },
            ...
          ],
          "flag": true,
          "tags": [
            ...,
            "...",
            ...
          ]
        },
        "sort": [
          "..."
        ]
      }
    ]
  ]
}

Error 4xx
NameDescriptionUserNotFoundThe id of the User was not found.

Error Response
HTTP/1.1 404 Not Found
  {
    "error": "UserNotFound"
  }

Searching
This service is used to search website contents
https://webapi.bps.go.id/v1/api/list/

Parameter
FieldTypeDescriptionmodelStringModel that user wants to search
lang optionalStringLanguage to display strategic indicators
Default value: ind
Allowed values: "ind", "eng"
domainNumberDomains that will be displayed derived period data (see master domain)
Size range: 4
pageNumberPage to display contents
Allowed values: 1, 2, 3, 4, ..., n
keyStringKey app to access API
keyword optionalStringKeyword to search. (Use "+" symbol if you have space on your keyword)
Send a Sample Request

News
Detail News
This service is used to display detail of news
https://webapi.bps.go.id/v1/view

Parameter
FieldTypeDescriptiondomainNumberDomains that will be displayed news (see master domain)
Size range: 4
modelStringModel to display news (news) for news is "news"
langStringLanguage to display news
Default value: ind
Allowed values: "ind", "eng"
idNumbernews id to display
Allowed values: 1, 2, 3, 4, ..., n
keyStringKey app to access API
Send a Sample Request

Success 200
FieldTypeDescriptionstatusStringReturn status, OK if success and Error if any error occured.
data-availabilityStringAvailability status of list news.
dataObjectInformation status
  news_idNumberID unique of news
  newscat_idStringID of news category
  titleStringTitle of news
  newsStringNews
  rl_dateStringRelease Date of news
  pictureStringPicture of news if available

Success Response
HTTP/1.1 200 OK
{
  "status": "OK",
  "data-availability": "available",
  "data":{
         "news_id":"news-890232",
         "newscat_id": "Statistik Lain",
         "title": "1212 1212 314",
         "news": "Saat ini telah dilaksanakan Sensus Ekonomi 2016 tahap kedua.",
         "rl_date":"2016-09-01",
         "picture" : "http://jabar-dev.bps.go.id/new/website/galeri/"
     }         
}

Error 4xx
NameDescriptionUserNotFoundThe id of the User was not found.

Error Response
HTTP/1.1 404 Not Found
  {
    "error": "UserNotFound"
  }

List All BPS News
This service is used to displays all BPS News are shown on the website
https://webapi.bps.go.id/v1/list

Parameter
FieldTypeDescriptionmodelStringModel to display news (news) for news is "news"
lang optionalStringLanguage to display news
Default value: ind
Allowed values: "ind", "eng"
domainNumberDomains that will be displayed news (see master domain)
Size range: 4
page optionalNumberPage to display news
Allowed values: 1, 2, 3, 4, ..., n
newscat optionalStringNews Category to display news
Allowed values: "sensus", "survey", "lainnya"
month optionalNumberMonth selected to display news
Allowed values: "01", "02", "03", "04", "12"
year optionalNumberYear selected to display news
Allowed values: 1, 2, 3, 4, ..., n
keyword optionalStringKeyword to search
keyStringKey app to access API
Send a Sample Request

Success 200
FieldTypeDescriptionstatusStringReturn status, OK if success and Error if any error occured.
data-availabilityStringAvailability status of list news.
dataObject[]Response Data
  0ObjectInformation status
    pageNumberInformation page
    pagesNumberInformation total page
    per_pageNumbersum of per page
    countNumbercount on this return list
    totalNumbertotal page
  1ObjectList news
    news_idNumberID unique of news
    newscat_idStringID of news category
    newscat_nameStringName of news category
    titleStringTitle of news
    newsStringNews
    rl_dateStringRelease Date of news

Success Response
HTTP/1.1 200 OK
   {
  "status": "OK",
  "data-availability": "available",
   "data": [
       {
           "page": 0,
           "pages": 1,
           "per_page": 10,
           "count": 3,
           "total": 3
       },
       [
           {
               "news_id": 9,
               "newscat_id": "Sensus dan Survey",
               "newscat_name": "KEGIATAN STATISTIK",
               "title": "tes berita OK",
               "news": "tes berita.....",
               "rl_date": "2016-12-27"
           },
          {
               "news_id": 4,
               "newscat_id": "Statistik Lain",
               "newscat_name": "KEGIATAN STATISTIK LAINNYA",
               "title": "Apel Siaga Sensus Ekonomi 2016 Jawa Barat",
               "news": "Apel siaga yang dilaksanakan pada Minggu pagi tanggal 28 Februari 2016 dipimpin oleh Gubernur Jawa Barat Ahmad \r\nHeryawan (Aher) di Halaman Gedung \r\nSate, Jl. Diponegoro No. 22, Kota Bandung......",
               "rl_date": "2016-02-28"
           },
           {
               "news_id": 2,
               "newscat_id": "Sensus dan Survey",
               "newscat_name": "KEGIATAN STATISTIK",
               "title": "Perubahan Tahun Dasar PDB Indonesia Berbasis SNA 2008",
               "news": "Perubahan tahun dasar Produk Domestik Bruto (PDB) merupakan suatu proses\r\n yang lazim dilakukan oleh kantor statistik suatu negara untuk \r\nmenggambarkan kondisi perekonomian terkini. BPS telah melakukan \r\nperubahan tahun dasar PDB sebanyak 5 (lima) kali yaitu pada tahun 1960, \r\n1973, 1983, 1993, dan 2000. Saat ini, BPS sedang melakukan proses \r\npenyusunan perubahan tahun dasar PDB dari tahun 2000 m.....",
               "rl_date": "2014-12-31"
           }
       ]
  ]
}

Error 4xx
NameDescriptionUserNotFoundThe id of the User was not found.

Error Response
HTTP/1.1 404 Not Found
  {
    "error": "UserNotFound"
  }

List News Category
This service is used to display list of news category
https://webapi.bps.go.id/v1/api/list

Parameter
FieldTypeDescriptionmodelStringModel to display list news category (newscategory) for news is "newscategory"
lang optionalStringLanguage to display news category
Default value: ind
Allowed values: "ind", "eng"
domainNumberDomains that will be displayed news (see master domain)
Size range: 4
keyStringKey app to access API
Send a Sample Request

Success 200
FieldTypeDescriptionstatusStringReturn status, OK if success and Error if any error occured.
data-availabilityStringAvailability status of list news.
dataObject[]Response Data
  0ObjectInformation status
    pageNumberInformation page
    pagesNumberInformation total page
    per_pageNumbersum of per page
    countNumbercount on this return list
    totalNumbertotal page
  1ObjectList news category
    newscat_idNumberID unique of news
    newscat_nameStringName of news category

Success Response
HTTP/1.1 200 OK
{
  "status": "OK",
  "data-availability": "available",
  "data": [
       {
           "page": 1,
           "pages": 1,
           "per_page": 10,
           "count": 2,
           "total": 2
       },
       [
         {
           "newscat_id": "Sensus dan Survey",
           "newscat_name": "KEGIATAN STATISTIK"
           },
           {
           "newscat_id": "Statistik Lain",
           "newscat_name": "KEGIATAN STATISTIK LAINNYA"
           }
       ] 
   ]     
}

Error 4xx
NameDescriptionUserNotFoundThe id of the User was not found.

Error Response
HTTP/1.1 404 Not Found
  {
    "error": "UserNotFound"
  }