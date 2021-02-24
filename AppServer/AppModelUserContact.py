# Outage Alert
# Application Server
# AppModelUserContact
#
# This script handles generating messages for users and sending messages to users.
# 
# ---------------------------------------------------------------------------------------

# Import custom modules
import AppTimeLib   # Custom date and time related functions for the OutageAlert application
import AppModelDB   # Database commands

# Import standard modules
import requests     # Allows Python to send HTTP requests, used to retrieve BC Hydro JSON file
import sys          # Used with requests module error handling
import datetime     # Provides datetime object functions
import json         # Provides encoding and decoding functions for JSON strings/files


newOutages = [
    {'id': 1594946, 'gisId': 1584998, 'regionId': 521980323, 'municipality': 'Abbotsford', 
        'area': 'West of TOWNLINE RD, East of PEARDONVILLE RD, South of MARSHALL RD, North of LIBERATOR AVE', 
        'cause': 'Planned work being done on our equipment', 'numCustomersOut': 102, 'crewStatusDescription': 'Crew on-site', 
        'crewEta': 1613931000000, 'dateOff': 1613930851000, 'dateOn': 1613952000000, 'lastUpdated': 1613930988000, 
        'regionName': 'Lower Mainland', 'crewEtr': 1613952000000, 'showEta': False, 'showEtr': True, 'latitude': 49.031038, 
        'longitude': -122.377685, 
        'polygon': [-122.378783, 49.022714, -122.377991, 49.023648, -122.371488, 49.03132, -122.371386, 49.031473, 
        -122.371328, 49.031635, -122.370883, 49.033758, -122.370872, 49.033933, -122.370914, 49.034106, -122.371005, 
        49.034271, -122.371144, 49.03442, -122.376513, 49.039123, -122.376661, 49.039233, -122.376834, 49.039326, 
        -122.377028, 49.039398, -122.377237, 49.039449, -122.3781, 49.039608, -122.37836, 49.039639, -122.378625, 49.039636, 
        -122.378883, 49.039599, -122.379126, 49.039531, -122.379344, 49.039433, -122.37953, 49.039309, -122.379676, 49.039164, 
        -122.379776, 49.039003, -122.38013, 49.038233, -122.380171, 49.038116, -122.383257, 49.025525, -122.383273, 49.025354, 
        -122.383184, 49.023514, -122.383155, 49.023358, -122.383086, 49.023207, -122.382978, 49.023067, -122.382834, 49.022941, 
        -122.382659, 49.022834, -122.382458, 49.022749, -122.382238, 49.022688, -122.380395, 49.022297, -122.380134, 49.02226, 
        -122.379866, 49.022257, -122.379603, 49.022288, -122.379354, 49.022352, -122.379128, 49.022448, -122.378936, 49.02257]}, 
    {'id': 1594775, 'gisId': 1584833, 'regionId': 521980323, 'municipality': 'Abbotsford', 
        'area': 'South of DAWSON RD, North of INDIAN RD, West of ELDRIDGE RD', 'cause': 'Planned work being done on our equipment', 
        'numCustomersOut': 18, 'crewStatusDescription': 'Crew on-site', 'crewEta': 1613923500000, 'dateOff': 1613921555000, 
        'dateOn': 1613955600000, 'lastUpdated': 1613927468000, 'regionName': 'Lower Mainland', 'crewEtr': 1613955600000, 
        'showEta': False, 'showEtr': True, 'latitude': 49.069899, 'longitude': -122.192929, 
        'polygon': [-122.18809, 49.06533, -122.18777, 49.070105, -122.187784, 49.070277, -122.187847, 49.070444, -122.187957, 49.0706, 
        -122.188111, 49.070739, -122.190559, 49.072562, -122.190742, 49.072676, -122.190954, 49.072765, -122.191187, 49.072827, -122.194518, 
        49.073493, -122.194751, 49.073525, -122.198965, 49.07386, -122.199236, 49.073863, -122.199504, 49.073832, -122.199756, 49.073766, 
        -122.199984, 49.073669, -122.200178, 49.073544, -122.200331, 49.073396, -122.200436, 49.073232, -122.200489, 49.073057, -122.200489, 
        49.072878, -122.200436, 49.072703, -122.20033, 49.072539, -122.200178, 49.072391, -122.190505, 49.064793, -122.190326, 49.064676, 
        -122.190118, 49.064583, -122.189887, 49.064517, -122.189641, 49.064479, -122.189389, 49.064472, -122.189139, 49.064496, -122.188901, 
        49.064549, -122.188681, 49.06463, -122.188487, 49.064736, -122.188326, 49.064864, -122.188204, 49.065009, -122.188125, 49.065166]}, 
    {'id': 1595095, 'gisId': 1585146, 'regionId': 521980323, 'municipality': 'Abbotsford', 'area': '2800 block TOLMIE RD', 
        'cause': 'Under investigation', 'numCustomersOut': 1, 'crewStatusDescription': 'Crew assigned', 'crewEta': 1613943300000, 
        'dateOff': 1613940660000, 'dateOn': None, 'lastUpdated': 1613943166000, 'regionName': 'Lower Mainland', 'crewEtr': None, 
        'showEta': True, 'showEtr': False, 'latitude': 49.054298, 'longitude': -122.094819, 
        'polygon': [-122.094836, 49.053399, -122.094569, 49.053414, -122.094312, 49.053463, -122.094074, 49.053544, -122.093865, 49.053654, 
        -122.093692, 49.053789, -122.093563, 49.053943, -122.093482, 49.054111, -122.093452, 49.054286, -122.093475, 49.054462, -122.09355, 
        49.054631, -122.093673, 49.054787, -122.093841, 49.054925, -122.094045, 49.055038, -122.09428, 49.055123, -122.094536, 49.055176, 
        -122.094802, 49.055196, -122.095069, 49.055181, -122.095326, 49.055132, -122.095564, 49.055051, -122.095773, 49.054941, -122.095946, 
        49.054806, -122.096075, 49.054652, -122.096156, 49.054484, -122.096186, 49.054309, -122.096163, 49.054133, -122.096088, 49.053964, 
        -122.095965, 49.053808, -122.095798, 49.05367, -122.095593, 49.053557, -122.095358, 49.053472, -122.095103, 49.053419]}, 
    {'id': 1595002, 'gisId': 1585054, 'regionId': 521980323, 'municipality': 'Abbotsford, Mission', 
        'area': 'East of NATHAN PL, North of HAVERMAN RD, South of MCTAVISH RD', 'cause': 'Tree down across our wires', 
        'numCustomersOut': 216, 'crewStatusDescription': 'Crew on their way', 'crewEta': 1613938200000, 'dateOff': 1613934372000, 
        'dateOn': None, 'lastUpdated': 1613942559000, 'regionName': 'Lower Mainland', 'crewEtr': None, 'showEta': True, 
        'showEtr': False, 'latitude': 49.11107, 'longitude': -122.40145, 
        'polygon': [-122.382025, 49.096341, -122.370951, 49.102964, -122.37079, 49.103077, -122.362172, 49.110375, -122.36204, 49.11051, 
        -122.361946, 49.110659, -122.361895, 49.110816, -122.361887, 49.110976, -122.361922, 49.111135, -122.362, 49.111287, -122.36831, 
        49.120712, -122.36844, 49.120864, -122.368611, 49.120996, -122.385241, 49.131571, -122.385443, 49.131677, -122.385671, 49.131756, 
        -122.385917, 49.131805, -122.386174, 49.131824, -122.392159, 49.13188, -122.392368, 49.131872, -122.392573, 49.131842, -122.392769, 
        49.131793, -122.392951, 49.131724, -122.395987, 49.130363, -122.396015, 49.13035, -122.454483, 49.102703, -122.454678, 49.102591, 
        -122.454837, 49.102457, -122.454954, 49.102306, -122.455027, 49.102143, -122.455051, 49.101974, -122.455027, 49.101805, -122.454954, 
        49.101642, -122.454837, 49.101491, -122.454678, 49.101357, -122.454483, 49.101246, -122.45426, 49.10116, -122.448881, 49.099517, 
        -122.44865, 49.099463, -122.448409, 49.099436, -122.383053, 49.096109, -122.382829, 49.09611, -122.382609, 49.096134, -122.382398, 
        49.096182, -122.382202, 49.096251]}, 
    {'id': 1595006, 'gisId': 1585058, 'regionId': 521980323, 'municipality': 'Abbotsford, Mission', 'area': '5600 block BAYNES ST', 
        'cause': 'Tree down across our wires', 'numCustomersOut': 1, 'crewStatusDescription': 'Crew assigned', 'crewEta': 1613938200000, 
        'dateOff': 1613934360000, 'dateOn': None, 'lastUpdated': 1613939879000, 'regionName': 'Lower Mainland', 'crewEtr': None, 
        'showEta': True, 'showEtr': False, 'latitude': 49.104072, 'longitude': -122.455701, 
        'polygon': [-122.455711, 49.103174, -122.455444, 49.103189, -122.455187, 49.103239, -122.454949, 49.103321, -122.454741, 49.103432, 
        -122.454569, 49.103567, -122.454441, 49.103722, -122.454361, 49.10389, -122.454333, 49.104065, -122.454357, 49.10424, -122.454433, 
        49.104409, -122.454558, 49.104565, -122.454726, 49.104702, -122.454932, 49.104815, -122.455168, 49.104899, -122.455424, 49.104952, 
        -122.455691, 49.10497, -122.455958, 49.104954, -122.456215, 49.104904, -122.456452, 49.104823, -122.456661, 49.104712, -122.456833, 
        49.104577, -122.456961, 49.104422, -122.457041, 49.104254, -122.457069, 49.104079, -122.457045, 49.103903, -122.456969, 49.103734, 
        -122.456844, 49.103578, -122.456676, 49.103441, -122.45647, 49.103329, -122.456234, 49.103245, -122.455978, 49.103192]}, 
    {'id': 1594788, 'gisId': 1584846, 'regionId': 521980323, 'municipality': 'Burnaby', 'area': '7300 block MEADOW AVE', 
        'cause': 'Planned work being done on our equipment', 'numCustomersOut': 1, 'crewStatusDescription': 'Crew on-site', 
        'crewEta': 1613925000000, 'dateOff': 1613924863000, 'dateOn': 1613955600000, 'lastUpdated': 1613924942000, 
        'regionName': 'Lower Mainland', 'crewEtr': 1613955600000, 'showEta': False, 'showEtr': True, 'latitude': 49.203641, 
        'longitude': -122.977716, 
        'polygon': [-122.977717, 49.202743, -122.977449, 49.20276, -122.977192, 49.202811, -122.976955, 49.202894, -122.976747, 49.203006, 
        -122.976576, 49.203142, -122.97645, 49.203297, -122.976372, 49.203466, -122.976345, 49.203641, -122.976371, 49.203816, -122.976449, 
        49.203985, -122.976576, 49.20414, -122.976746, 49.204276, -122.976954, 49.204388, -122.977191, 49.204471, -122.977448, 49.204522, 
        -122.977716, 49.20454, -122.977983, 49.204523, -122.978241, 49.204471, -122.978478, 49.204389, -122.978686, 49.204277, -122.978856, 
        49.204141, -122.978983, 49.203985, -122.979061, 49.203817, -122.979087, 49.203642, -122.979061, 49.203466, -122.978983, 49.203298, 
        -122.978857, 49.203142, -122.978686, 49.203006, -122.978478, 49.202894, -122.978241, 49.202811, -122.977984, 49.20276]}, 
    {'id': 1595202, 'gisId': 1585253, 'regionId': 521980323, 'municipality': 'Langley', 
        'area': 'East of 264TH ST, West of 272ND ST, South of 80TH AVE, North of 62ND AVE', 'cause': 'Tree down across our wires', 
        'numCustomersOut': 60, 'crewStatusDescription': 'Crew assigned', 'crewEta': None, 'dateOff': 1613941764000, 'dateOn': None, 
        'lastUpdated': 1613942563000, 'regionName': 'Lower Mainland', 'crewEtr': None, 'showEta': False, 'showEtr': False, 
        'latitude': 49.124482, 'longitude': -122.484242, 
        'polygon': [-122.485206, 49.116931, -122.479026, 49.117373, -122.478875, 49.11739, -122.476221, 49.117779, -122.475968, 49.117834, 
        -122.475735, 49.11792, -122.475532, 49.118034, -122.475367, 49.118172, -122.475246, 49.118329, -122.475173, 49.118497, -122.475152, 
        49.118672, -122.475183, 49.118846, -122.479764, 49.132732, -122.479847, 49.1329, -122.479979, 49.133055, -122.480155, 49.13319, 
        -122.480367, 49.133299, -122.480608, 49.133379, -122.480869, 49.133427, -122.486235, 49.134036, -122.486488, 49.13405, -122.48674, 
        49.134032, -122.486982, 49.133984, -122.487207, 49.133908, -122.487407, 49.133806, -122.487575, 49.133681, -122.487705, 49.133538, 
        -122.489756, 49.130717, -122.489827, 49.1306, -122.489872, 49.130477, -122.492901, 49.118461, -122.492918, 49.118283, -122.492882, 
        49.118107, -122.492794, 49.117939, -122.492656, 49.117785, -122.492476, 49.117652, -122.492258, 49.117546, -122.492014, 49.117469, 
        -122.49175, 49.117426, -122.487118, 49.116977, -122.486972, 49.116968, -122.485408, 49.116927]}, 
    {'id': 1594784, 'gisId': 1584842, 'regionId': 521980323, 'municipality': 'Pemberton', 
        'area': 'North of Tiyata Blvd , East of DOGWOOD DR, West of ASPEN BLV, South of PEMBERTON MEADOWS RD', 
        'cause': 'Planned work being done on our equipment', 'numCustomersOut': 17, 'crewStatusDescription': 'Crew on-site', 
        'crewEta': 1613924400000, 'dateOff': 1613924009000, 'dateOn': 1613962800000, 'lastUpdated': 1613924270000, 
        'regionName': 'Lower Mainland', 'crewEtr': 1613962800000, 'showEta': False, 'showEtr': True, 'latitude': 50.320804, 
        'longitude': -122.809081, 
        'polygon': [-122.807631, 50.320385, -122.807496, 50.320847, -122.807472, 50.321017, -122.807499, 50.321188, -122.807576, 50.321351, 
        -122.8077, 50.321503, -122.807867, 50.321637, -122.80807, 50.321748, -122.808302, 50.321832, -122.808555, 50.321887, -122.808819, 
        50.32191, -122.809086, 50.321901, -122.809345, 50.32186, -122.809587, 50.321788, -122.809835, 50.321749, -122.810069, 50.321683, 
        -122.810279, 50.321591, -122.81046, 50.321476, -122.810606, 50.321342, -122.810711, 50.321193, -122.810772, 50.321034, -122.810788, 
        50.320871, -122.810757, 50.320709, -122.810681, 50.320553, -122.810598, 50.320426, -122.810502, 50.320303, -122.810377, 50.320192, 
        -122.810087, 50.319971, -122.809899, 50.319852, -122.80968, 50.319758, -122.809437, 50.319692, -122.809179, 50.319657, -122.808915, 
        50.319652, -122.808654, 50.31968, -122.808407, 50.319738, -122.80818, 50.319825, -122.807983, 50.319937, -122.807822, 50.320071, 
        -122.807703, 50.320222]}, 
    {'id': 1594786, 'gisId': 1584844, 'regionId': 521980323, 'municipality': 'Sechelt', 
        'area': 'RTE 101 & EGMONT RD, HALLOWELL RD P24TOP9, HALLOWELL RD P24TOP11, 5300 block CEDARRIDGE PL, 16600 block BACKEDDY RD, SUN CST HWY & JERVIS INLET, HALLOWELL RD P24TOP12, 5300 block MOUNTAINVIEW RD, E EGMONT LINE P19, E EGMONT LINE P76...', 
        'cause': 'Planned work being done on our equipment', 'numCustomersOut': 458, 'crewStatusDescription': 'Crew on-site', 
        'crewEta': 1613924700000, 'dateOff': 1613924484000, 'dateOn': 1613948400000, 'lastUpdated': 1613924599000, 'regionName': 'Lower Mainland', 
        'crewEtr': 1613948400000, 'showEta': False, 'showEtr': True, 'latitude': 49.732882, 'longitude': -123.953819, 
        'polygon': [-123.983263, 49.686067, -123.966437, 49.687886, -123.966196, 49.687927, -123.965971, 49.687995, -123.965768, 49.688087, 
        -123.882566, 49.73384, -123.8824, 49.733948, -123.882264, 49.734074, -123.882163, 49.734213, -123.8821, 49.73436, -123.881879, 49.735126, 
        -123.881855, 49.735285, -123.881876, 49.735446, -123.88194, 49.735601, -123.889276, 49.748539, -123.889392, 49.748696, -123.889552, 49.748835, 
        -123.889751, 49.748951, -123.895593, 49.751762, -123.937721, 49.771973, -123.937898, 49.772045, -123.93809, 49.7721, -123.939302, 49.772373, 
        -123.939544, 49.772412, -123.939792, 49.772423, -123.94004, 49.772404, -123.940279, 49.772358, -124.010349, 49.753983, -124.010365, 49.753978, 
        -124.011961, 49.753544, -124.012072, 49.75351, -124.016264, 49.752073, -124.016465, 49.751989, -124.016641, 49.751884, -124.016786, 49.75176, 
        -124.016897, 49.751623, -124.017615, 49.750499, -124.017689, 49.750345, -124.01772, 49.750185, -124.017706, 49.750024, -124.017648, 49.749867, 
        -123.984804, 49.686667, -123.984706, 49.686522, -123.98457, 49.686391, -123.984401, 49.686276, -123.984204, 49.686183, -123.983984, 49.686114, 
        -123.983749, 49.686071, -123.983506, 49.686055]}, 
    {'id': 1594785, 'gisId': 1584843, 'regionId': 1602964060, 'municipality': 'Chetwynd', 'area': 'East of COWIE CK RD', 
        'cause': 'Under investigation', 'numCustomersOut': 11, 'crewStatusDescription': 'Crew on-site', 'crewEta': 1613941200000, 
        'dateOff': 1613924341000, 'dateOn': None, 'lastUpdated': 1613941355000, 'regionName': 'Northern', 'crewEtr': None, 'showEta': False, 
        'showEtr': False, 'latitude': 55.553908, 'longitude': -121.246855, 
        'polygon': [-121.303757, 55.534357, -121.256631, 55.54079, -121.256595, 55.540795, -121.236559, 55.543814, -121.236328, 55.54386, 
        -121.236112, 55.543926, -121.235917, 55.544009, -121.235746, 55.544109, -121.226537, 55.550403, -121.226465, 55.550456, -121.189969, 
        55.579533, -121.189815, 55.579685, -121.189716, 55.579851, -121.189676, 55.580025, -121.189696, 55.580199, -121.189776, 55.580369, 
        -121.189912, 55.580526, -121.190099, 55.580665, -121.190331, 55.580781, -121.190598, 55.58087, -121.19089, 55.580927, -121.191196, 
        55.580952, -121.191505, 55.580942, -121.191804, 55.580898, -121.192083, 55.580822, -121.283991, 55.549218, -121.28418, 55.549142, 
        -121.284347, 55.549051, -121.305307, 55.535831, -121.30549, 55.53569, -121.305621, 55.535531, -121.305696, 55.535361, -121.305711, 
        55.535186, -121.305666, 55.535013, -121.305562, 55.534848, -121.305404, 55.534697, -121.305197, 55.534567, -121.30495, 55.534462, 
        -121.304671, 55.534386, -121.304372, 55.534342, -121.304063, 55.534333]}, 
    {'id': 1595022, 'gisId': 1585073, 'regionId': 1602964060, 'municipality': 'Dawson Creek', 'area': '5300 block 233 RD', 
        'cause': 'Under investigation', 'numCustomersOut': 1, 'crewStatusDescription': 'Crew on their way', 'crewEta': 1613947500000, 
        'dateOff': 1613935080000, 'dateOn': None, 'lastUpdated': 1613943719000, 'regionName': 'Northern', 'crewEtr': None, 'showEta': True, 
        'showEtr': False, 'latitude': 55.885719, 'longitude': -120.42433, 
        'polygon': [-120.424388, 55.884822, -120.424075, 55.884833, -120.423772, 55.884878, -120.423491, 55.884955, -120.423241, 55.885062, 
        -120.423034, 55.885194, -120.422877, 55.885346, -120.422775, 55.885513, -120.422733, 55.885687, -120.422753, 55.885863, -120.422833, 
        55.886033, -120.42297, 55.886191, -120.42316, 55.886331, -120.423395, 55.886448, -120.423666, 55.886536, -120.423962, 55.886593, 
        -120.424273, 55.886617, -120.424586, 55.886606, -120.424888, 55.886561, -120.42517, 55.886484, -120.425419, 55.886377, -120.425626, 
        55.886245, -120.425784, 55.886093, -120.425886, 55.885926, -120.425927, 55.885752, -120.425908, 55.885576, -120.425828, 55.885406, 
        -120.42569, 55.885247, -120.4255, 55.885107, -120.425265, 55.884991, -120.424994, 55.884902, -120.424698, 55.884845]}, 
    {'id': 1595200, 'gisId': 1585251, 'regionId': 1602964060, 'municipality': 'Fort St. John', 
        'area': '14100 - 14400 block 249TH RD, 249 RD, 14400 block 249 ST, 4800 block 250 RD, 14000 - 14100 block 247TH RD, LSD 15 20 85 17, 7 20 85 17 W6M, 4800 - 5100 block 250TH RD, 4800 block 250 ROAD, LSD 10 8 85 17...', 
        'cause': 'Tree down across our wires', 'numCustomersOut': 22, 'crewStatusDescription': 'Crew assigned', 'crewEta': 1613943300000, 
        'dateOff': 1613941200000, 'dateOn': None, 'lastUpdated': 1613943773000, 'regionName': 'Northern', 'crewEtr': None, 'showEta': True, 
        'showEtr': False, 'latitude': 56.368892, 'longitude': -120.611757, 
        'polygon': [-120.611444, 56.354374, -120.609623, 56.35435, -120.60941, 56.354355, -120.6092, 56.354375, -120.556692, 56.361472, -120.556407, 
        56.361527, -120.556146, 56.361609, -120.555917, 56.361717, -120.555728, 56.361847, -120.555585, 56.361993, -120.555494, 56.362152, -120.555457, 
        56.362318, -120.555476, 56.362484, -120.55555, 56.362646, -120.555677, 56.362797, -120.555851, 56.362933, -120.556068, 56.363048, -120.55632, 
        56.363139, -120.643092, 56.388447, -120.643372, 56.388511, -120.643668, 56.388545, -120.64397, 56.388548, -120.644268, 56.388519, -120.644551, 
        56.38846, -120.644809, 56.388373, -120.645034, 56.388261, -120.645217, 56.388128, -120.645353, 56.387978, -120.649955, 56.381404, -120.650032, 
        56.381258, -120.650064, 56.381107, -120.650049, 56.380955, -120.649988, 56.380807, -120.63931, 56.362193, -120.639212, 56.362059, -120.639076, 
        56.361936, -120.638906, 56.361826, -120.638706, 56.361733, -120.638482, 56.361659, -120.612119, 56.354466, -120.611903, 56.354418, -120.611676, 
        56.354387]}, 
    {'id': 1594823, 'gisId': 1584877, 'regionId': 1602964060, 'municipality': 'Fort St. John', 'area': 'East of RD 249 , North of BALDONNEL RD', 
        'cause': 'Under investigation', 'numCustomersOut': 12, 'crewStatusDescription': 'Crew on-site', 'crewEta': 1613942100000, 
        'dateOff': 1613926440000, 'dateOn': 1613942100000, 'lastUpdated': 1613941894000, 'regionName': 'Northern', 'crewEtr': 1613942100000, 
        'showEta': False, 'showEtr': True, 'latitude': 56.240487, 'longitude': -120.598064, 
        'polygon': [-120.583171, 56.226139, -120.583095, 56.241646, -120.58312, 56.241804, -120.584305, 56.245536, -120.584373, 56.24568, -120.584482, 
        56.245815, -120.58463, 56.245938, -120.590076, 56.249757, -120.590265, 56.249868, -120.590485, 56.24996, -120.59073, 56.25003, -120.590993, 
        56.250075, -120.591266, 56.250095, -120.59154, 56.250089, -120.623136, 56.247876, -120.62343, 56.247839, -120.623706, 56.247773, -120.623955, 
        56.24768, -120.624169, 56.247562, -120.62434, 56.247425, -120.624463, 56.247272, -120.624532, 56.247109, -120.624545, 56.246941, -120.624503, 
        56.246776, -120.624406, 56.246617, -120.624257, 56.246472, -120.624063, 56.246344, -120.585912, 56.225501, -120.585667, 56.225391, 
        -120.585389, 56.225309, -120.585087, 56.22526, -120.584774, 56.225244, -120.584461, 56.225262, -120.584161, 56.225313, -120.583884, 
        56.225396, -120.583642, 56.225507, -120.583442, 56.225643, -120.583294, 56.225797, -120.583202, 56.225965]}, 
    {'id': 1594936, 'gisId': 1584989, 'regionId': 1602964060, 'municipality': 'Kitimat', 'area': '2200 block FOREST AVE', 
        'cause': 'Planned work being done on our equipment', 'numCustomersOut': 2, 'crewStatusDescription': 'Crew on-site', 
        'crewEta': 1613928603000, 'dateOff': 1613928339000, 'dateOn': 1613946600000, 'lastUpdated': 1613929959000, 'regionName': 'Northern', 
        'crewEtr': 1613946600000, 'showEta': False, 'showEtr': True, 'latitude': 54.05573, 'longitude': -128.603854, 
        'polygon': [-128.603735, 54.054833, -128.60344, 54.054864, -128.603161, 54.054929, -128.602908, 54.055024, -128.602692, 54.055146, 
        -128.602521, 54.05529, -128.602401, 54.055452, -128.602336, 54.055624, -128.60233, 54.0558, -128.602383, 54.055974, -128.602492, 
        54.056138, -128.602653, 54.056287, -128.602861, 54.056414, -128.603107, 54.056515, -128.603381, 54.056586, -128.603674, 54.056623, 
        -128.603974, 54.056627, -128.604269, 54.056596, -128.604548, 54.056532, -128.6048, 54.056437, -128.605017, 54.056315, -128.605188, 
        54.05617, -128.605308, 54.056008, -128.605373, 54.055836, -128.605379, 54.05566, -128.605326, 54.055486, -128.605217, 54.055322, 
        -128.605055, 54.055174, -128.604848, 54.055046, -128.604602, 54.054946, -128.604327, 54.054875, -128.604035, 54.054837]}, 
    {'id': 1594941, 'gisId': 1584994, 'regionId': 1602964060, 'municipality': 'Stewart', 'area': 'North of Kitsault Squish FSR', 
        'cause': 'Under investigation', 'numCustomersOut': 4, 'crewStatusDescription': 'Crew on-site', 'crewEta': 1613941500000, 
        'dateOff': 1613929260000, 'dateOn': None, 'lastUpdated': 1613941486000, 'regionName': 'Northern', 'crewEtr': None, 
        'showEta': False, 'showEtr': False, 'latitude': 55.436734, 'longitude': -129.430381, 
        'polygon': [-129.430766, 55.426859, -129.426141, 55.442946, -129.426121, 55.443109, -129.426153, 55.443272, -129.426237, 55.443429, 
        -129.42637, 55.443575, -129.428634, 55.445588, -129.428821, 55.445724, -129.42905, 55.445837, -129.429313, 55.445923, -129.429601, 
        55.445978, -129.429901, 55.446002, -129.430204, 55.445992, -129.430498, 55.44595, -129.430773, 55.445877, -129.431018, 55.445775, 
        -129.431224, 55.445648, -129.431384, 55.445502, -129.431491, 55.44534, -129.431542, 55.44517, -129.433902, 55.42707, -129.433895, 
        55.426899, -129.433832, 55.426732, -129.433714, 55.426574, -129.433545, 55.426432, -129.433332, 55.426311, -129.433083, 55.426215, 
        -129.432806, 55.426148, -129.432512, 55.426112, -129.432211, 55.426108, -129.431914, 55.426136, -129.431632, 55.426197, -129.431375, 
        55.426286, -129.431153, 55.426402, -129.430973, 55.426539, -129.430843, 55.426694]}, 
    {'id': 1594789, 'gisId': 1584847, 'regionId': 2072041405, 'municipality': 'Vernon', 'area': '2300 block 48 AVE', 
        'cause': 'Work being done on our equipment', 'numCustomersOut': 3, 'crewStatusDescription': 'Crew on-site', 'crewEta': 1613925000000, 
        'dateOff': 1613924984000, 'dateOn': 1613953812000, 'lastUpdated': 1613925082000, 'regionName': 'Okanagan/Kootenay', 
        'crewEtr': 1613953812000, 'showEta': False, 'showEtr': True, 'latitude': 50.282219, 'longitude': -119.262842, 
        'polygon': [-119.262915, 50.281321, -119.262641, 50.281329, -119.262374, 50.281371, -119.262125, 50.281446, -119.261903, 50.281551, 
        -119.261718, 50.281681, -119.261576, 50.281832, -119.261482, 50.281998, -119.261441, 50.282172, -119.261454, 50.282348, -119.26152, 
        50.282519, -119.261636, 50.282679, -119.2618, 50.282821, -119.262003, 50.28294, -119.262238, 50.283031, -119.262497, 50.28309, 
        -119.262769, 50.283117, -119.263044, 50.283109, -119.263311, 50.283066, -119.26356, 50.282992, -119.263782, 50.282887, -119.263967, 
        50.282757, -119.264109, 50.282606, -119.264203, 50.28244, -119.264244, 50.282266, -119.264231, 50.28209, -119.264165, 50.281918, 
        -119.264048, 50.281759, -119.263885, 50.281617, -119.263682, 50.281498, -119.263446, 50.281407, -119.263187, 50.281347]}, 
    {'id': 1595310, 'gisId': 1585361, 'regionId': 725364552, 'municipality': 'Salmon Arm', 'area': '2600 block YANKEE FLATS RD', 
        'cause': 'Under investigation', 'numCustomersOut': 1, 'crewStatusDescription': 'Crew assigned', 'crewEta': None, 'dateOff': 1613943540000, 
        'dateOn': None, 'lastUpdated': 1613944015000, 'regionName': 'Thompson/Shuswap', 'crewEtr': None, 'showEta': False, 'showEtr': False, 
        'latitude': 50.51399, 'longitude': -119.376688, 
        'polygon': [-119.37676, 50.513092, -119.376483, 50.5131, -119.376215, 50.513143, -119.375965, 50.513218, -119.375743, 50.513323, 
        -119.375557, 50.513453, -119.375414, 50.513604, -119.375321, 50.51377, -119.37528, 50.513945, -119.375293, 50.514121, -119.37536, 
        50.514292, -119.375478, 50.514451, -119.375642, 50.514593, -119.375847, 50.514712, -119.376083, 50.514802, -119.376344, 50.514862, 
        -119.376617, 50.514888, -119.376893, 50.51488, -119.377162, 50.514837, -119.377412, 50.514762, -119.377634, 50.514657, -119.37782, 
        50.514527, -119.377963, 50.514376, -119.378056, 50.51421, -119.378097, 50.514035, -119.378084, 50.513859, -119.378017, 50.513688, 
        -119.377899, 50.513529, -119.377735, 50.513387, -119.37753, 50.513268, -119.377293, 50.513178, -119.377033, 50.513118]}, 
    {'id': 1594819, 'gisId': 1584873, 'regionId': 1602896846, 'municipality': 'Port Alberni', 'area': 'South of DUNBAR ST, West of ANDERSON AVE', 
        'cause': 'Planned work being done on our equipment', 'numCustomersOut': 922, 'crewStatusDescription': 'Crew on-site', 
        'crewEta': 1613926852000, 'dateOff': 1613926577000, 'dateOn': 1613950201000, 'lastUpdated': 1613926690000, 'regionName': 'North VI', 
        'crewEtr': 1613950201000, 'showEta': False, 'showEtr': True, 'latitude': 49.220763, 'longitude': -124.804716, 
        'polygon': [-124.80014, 49.208758, -124.792715, 49.216365, -124.792614, 49.216488, -124.792544, 49.21662, -124.792506, 49.216758, 
        -124.792487, 49.216877, -124.792482, 49.217011, -124.792506, 49.217144, -124.79249, 49.21726, -124.792498, 49.217377, -124.792535, 
        49.217612, -124.792538, 49.217626, -124.794215, 49.226754, -124.79425, 49.226875, -124.794309, 49.226991, -124.794393, 49.227101, 
        -124.797138, 49.230169, -124.797244, 49.23027, -124.79737, 49.230362, -124.797663, 49.230546, -124.797858, 49.230649, -124.798079, 
        49.230726, -124.798318, 49.230776, -124.812288, 49.232801, -124.812542, 49.232821, -124.812797, 49.232811, -124.813045, 49.23277, 
        -124.813277, 49.232699, -124.813485, 49.232601, -124.813661, 49.23248, -124.813801, 49.23234, -124.813897, 49.232185, -124.813949, 
        49.232021, -124.816409, 49.217224, -124.816415, 49.217076, -124.816383, 49.216929, -124.816315, 49.216787, -124.816213, 49.216655, 
        -124.809409, 49.209429, -124.809266, 49.209303, -124.809091, 49.209196, -124.808891, 49.20911, -124.808671, 49.209048, -124.808438, 
        49.209012, -124.801492, 49.208353, -124.801231, 49.208345, -124.800972, 49.208369, -124.800725, 49.208425, -124.800499, 49.208511, 
        -124.800302, 49.208624]}
    ]


def GenerateOutageMessages(existingOutageInfo, updatedOutageInfo):
    outageMessages = [] # This is a list of strings for the current outage ID number. Each string is a message to the user about a change in this specific power outage.

    for key in updatedOutageInfo:
        oldValue = existingOutageInfo[key]
        newValue = updatedOutageInfo[key]

        # Generate generic power outage update messages for users

        if key == 'cause':
            if oldValue == None:
                outageMessages.append("Cause of power outage: " + newValue)
            else:
                outageMessages.append("Cause of power outage updated from \'" + oldValue + "\' to \'" + newValue + "\'.")
            break


        elif key == 'crewStatusDescription':
            if oldValue == None:
                outageMessages.append("Power restoration crew status: " + newValue)
            else:
                outageMessages.append("Power restoration crew status updated from \'" + oldValue + "\' to \'" + newValue + "\'.")
            break


        elif key == 'crewEta':
            dateTimeCrewETA = AppTimeLib.DateTimeFromJSToPython(newValue)
            dateTimeCrewETA = AppTimeLib.PythonChangeTimeZone(dateTimeCrewETA, 'America/Vancouver')
            if oldValue == None:
                outageMessages.append("Power restoration crew ETA: " + datetime.datetime.strftime(dateTimeOff, '%Y-%b-%d %I:%M:%S %p %Z'))
            else:
                outageMessages.append("Power restoration crew ETA updated to: " + datetime.datetime.strftime(dateTimeOff, '%Y-%b-%d %I:%M:%S %p %Z'))
            break


        elif key == 'dateOff':
            dateTimeOff = AppTimeLib.DateTimeFromJSToPython(newValue)
            dateTimeOff = AppTimeLib.PythonChangeTimeZone(dateTimeOff, 'America/Vancouver')
            if oldValue == None:
                outageMessages.append("Power outage began on " + datetime.datetime.strftime(dateTimeOff, '%Y-%b-%d %I:%M:%S %p %Z'))
            else:
                outageMessages.append("Power outage start time was updated to " + datetime.datetime.strftime(dateTimeOff, '%Y-%b-%d %I:%M:%S %p %Z'))
            break


        elif key == 'dateOn':
            dateTimeOn = AppTimeLib.DateTimeFromJSToPython(newValue)
            dateTimeOn = AppTimeLib.PythonChangeTimeZone(dateTimeOn, 'America/Vancouver')
            if oldValue == None:
                outageMessages.append("Power restored on " + datetime.datetime.strftime(dateTimeOn, '%Y-%b-%d %I:%M:%S %p %Z'))
            else:
                outageMessages.append("Power restoration time was updated to " + datetime.datetime.strftime(dateTimeOn, '%Y-%b-%d %I:%M:%S %p %Z'))
            break


        # OTHER DICTIONARY 'KEY' OPTIONS, saved in case we want to use them.
        # elif key == 'polygon':
        #     # need to check for newly affected customers, or newly restored customers if the polygon changes                 <----
        #     break
        # elif key == 'lastUpdated':
        #     # What do we do with this part? anything?                                                                        <----
        #     break
        # elif key == 'numCustomersOut':
        #     break
        # elif key == 'id':
        #     break
        # elif key == 'gisId':
        #     break
        # elif key == 'regionId':
        #     break
        # elif key == 'municipality':
        #     break
        # elif key == 'area':
        #     break
        # elif key == 'regionName':
        #     break
        # elif key == 'crewEtr':
        #     break
        # elif key == 'showEta':
        #     break
        # elif key == 'showEtr':
        #     break
        # elif key == 'latitude':
        #     break
        # elif key == 'longitude':
        #     break
    
    return outageMessages




# NEW POWER OUTAGES ---------------------------------------------------------------------
# Save new outage data to the database (Implemented in AppModelRetrieveJSON)

# err = AppModelDB.SaveNewOutages(newOutages)
# if err != None:
#     #There was a problem saving the new outages to the database. Handle this error                                        <----
#     print("NEW OUTAGE DATA NOT SAVED TO DATABASE!")
#     print(err)


# Alert users of new outages                                                                                                <----
# NEED TO COMPLETE THIS SECTION!
# NEED newOutages (list of outage dictionaries)




# EXISTING POWER OUTAGES ----------------------------------------------------------------
# NEED updateOutages (list of outage dictionaries)                                                                          <----
# Figure out what changed with each outage so we can act on those changes
for i in range(len(updateOutages)):
    (_, dbOutageInfo, updatedOutageInfo) = updateOutages[i] # Get the two outage dictionaries
    
    for key in updatedOutageInfo:                           # For each key in the dictionary...
        if updatedOutageInfo[key] == dbOutageInfo[key]:     # If the key values are the same...
            updateOutages[i].pop(key)                       # Remove the key & value from these dictionaries
            dbOutageInfo[i].pop(key)
            break
    if len(updatedOutageInfo) == len(dbOutageInfo) == 0:    # If an outage record has no keys left, remove it from the update list
        updateOutages.pop(i)


    
def SendOutageUpdateAlerts(updateOutages):

    updateAlerts = [] # This is a ist of tuples consisting of the outage ID number, and all the related update messages for that outage ID

    for i in range(len(updateOutages)):
        (outageID, dbOutageInfo, updatedOutageInfo) = updateOutages[i]

        updateAlerts.append((outageID, GenerateOutageMessages(dbOutageInfo, updatedOutageInfo))) # Create a tuple consisting of the outage ID number, and all the related update messages for that outage ID


    #send the updateAlerts tuple-list to a function that sends the messages to our users                                        <----





