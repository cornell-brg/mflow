#=========================================================================
# proc_ubmark_vvadd_data.py
#=========================================================================

ref = [ 282492056 ,
        -1687373565,
        1614320202,
        1558878422,
        -828951664 ,
        1939002605,
        1858727534,
        1252330490,
        1457814056,
        966921452 ,
        -1923589824,
        -1032052430,
        -1346266803,
        1601773377,
        -1895820145,
        -703260373 ,
        665542779 ,
        -2009365853,
        -1312007168,
        -1382171896,
        -1654444657,
        -1125246567,
        1555217230,
        -1038647977,
        1522826551,
        -1623011142,
        1100974652,
        1129087158,
        -1322476976,
        2082570433,
        -1268784908,
        1793846573,
        -1115362642,
        766388385 ,
        -2101284135,
        1900199279,
        -1737530648,
        2135013679,
        2128293599,
        -1005626202,
        2046944209,
        1512522130,
        -1078486584,
        -1156126787,
        -240453547 ,
        1158603311,
        1856046387,
        -1208828978,
        -1602900243,
        1470407582,
        -2136270898,
        999739699 ,
        1557730495,
        1794135574,
        -2076767098,
        -636399456 ,
        -1191163376,
        -1144847363,
        799978541 ,
        1814918380,
        785073817 ,
        896129602 ,
        1582042363,
        -1765643653,
        1070381968,
        -989883989 ,
        1786021934,
        1661164588,
        1390010407,
        -1218133724,
        -975993875 ,
        1512467795,
        -1305515890,
        1517666319,
        1590514341,
        -1234533226,
        699624414 ,
        2036928677,
        1670669049,
        -1235432265,
        1555365629,
        1272522583,
        1997264332,
        1220884064,
        -1379114396,
        -2111326676,
        546260101 ,
        937167434 ,
        833581709 ,
        -1635393726,
        1721904602,
        -557016485 ,
        1861641632,
        -883658915 ,
        -1909144253,
        2098560112,
        -1249931646,
        -1679142137,
        -893125243 ,
        -1580488465,
]

src0 = [ 16807     ,
         1622650073,
         1144108930,
         101027544 ,
         1458777923,
         823564440 ,
         1784484492,
         114807987 ,
         1441282327,
         823378840 ,
         896544303 ,
         1264817709,
         1817129560,
         197493099 ,
         893351816 ,
         1954899097,
         563613512 ,
         1580723810,
         1358580979,
         2128236579,
         530511967 ,
         1551901393,
         1399125485,
         1356425228,
         585640194 ,
         1646035001,
         510616708 ,
         771515668 ,
         1044788124,
         1952509530,
         1942727722,
         1108728549,
         2118797801,
         571540977 ,
         2035308228,
         1075260298,
         595028635 ,
         1137623865,
         2020739063,
         1635339425,
         1777724115,
         34075629  ,
         1864546517,
         1581030105,
         2146319451,
         500782188 ,
         753799505 ,
         1269406752,
         884936716 ,
         578354438 ,
         1153851501,
         616783871 ,
         330111137 ,
         1723153177,
         1147722294,
         2051621609,
         1190959745,
         1341853635,
         343098142 ,
         1534827968,
         195400260 ,
         6441594   ,
         57716395  ,
         2014119113,
         388471006 ,
         1904797942,
         322842082 ,
         828530767 ,
         1073185695,
         1260973671,
         1267248590,
         1194314738,
         2111631616,
         304555640 ,
         541437335 ,
         996497972 ,
         270649095 ,
         685583454 ,
         272112289 ,
         1334948905,
         532236123 ,
         836045813 ,
         60935238  ,
         915896220 ,
         2034712366,
         281725226 ,
         197941363 ,
         152607844 ,
         543436550 ,
         1681808623,
         750597385 ,
         1737195272,
         1399399247,
         1459413496,
         537140623 ,
         1012028144,
         1289335735,
         1623161625,
         2043046042,
         943454679 ,
]

src1 = [ 282475249 ,
         984943658 ,
         470211272 ,
         1457850878,
         2007237709,
         1115438165,
         74243042  ,
         1137522503,
         16531729  ,
         143542612 ,
         1474833169,
         1998097157,
         1131570933,
         1404280278,
         1505795335,
         1636807826,
         101929267 ,
         704877633 ,
         1624379149,
         784558821 ,
         2110010672,
         1617819336,
         156091745 ,
         1899894091,
         937186357 ,
         1025921153,
         590357944 ,
         357571490 ,
         1927702196,
         130060903 ,
         1083454666,
         685118024 ,
         1060806853,
         194847408 ,
         158374933 ,
         824938981 ,
         1962408013,
         997389814 ,
         107554536 ,
         1654001669,
         269220094 ,
         1478446501,
         1351934195,
         1557810404,
         1908194298,
         657821123 ,
         1102246882,
         1816731566,
         1807130337,
         892053144 ,
         1004844897,
         382955828 ,
         1227619358,
         70982397  ,
         1070477904,
         1606946231,
         1912844175,
         1808266298,
         456880399 ,
         280090412 ,
         589673557 ,
         889688008 ,
         1524325968,
         515204530 ,
         681910962 ,
         1400285365,
         1463179852,
         832633821 ,
         316824712 ,
         1815859901,
         2051724831,
         318153057 ,
         877819790 ,
         1213110679,
         1049077006,
         2063936098,
         428975319 ,
         1351345223,
         1398556760,
         1724586126,
         1023129506,
         436476770 ,
         1936329094,
         304987844 ,
         881140534 ,
         1901915394,
         348318738 ,
         784559590 ,
         290145159 ,
         977764947 ,
         971307217 ,
         2000755539,
         462242385 ,
         1951894885,
         1848682420,
         1086531968,
         1755699915,
         992663534 ,
         1358796011,
         1771024152,
]