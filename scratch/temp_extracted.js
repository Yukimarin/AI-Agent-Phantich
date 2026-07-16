
// --- Script Block 0 ---

        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['Inter', 'sans-serif'],
                    }
                }
            }
        }
    
// --- Script Block 1 ---

        const predictionsRawData = {
  "dashboard_data": {
    "KS24": {
      "cv": [
        {
          "class_name": "HN-KS24-CNTT1",
          "course_name": "[ IT211 - K24 ] Java Web Service",
          "size": 42,
          "v_class": 9.533216374269005,
          "mult_env": 1.0,
          "pred_old": 62.05156262563163,
          "actual_pass": 78.57142857142857,
          "err": 16.519865945796937
        },
        {
          "class_name": "HN-KS24-CNTT2",
          "course_name": "[ IT211 - K24 ] Java Web Service",
          "size": 40,
          "v_class": 4.793814814814815,
          "mult_env": 1.0,
          "pred_old": 78.2237486965288,
          "actual_pass": 92.5,
          "err": 14.276251303471199
        },
        {
          "class_name": "HN-KS24-CNTT4",
          "course_name": "[ IT211 - K24 ] Java Web Service",
          "size": 37,
          "v_class": 9.079961988304094,
          "mult_env": 1.0,
          "pred_old": 59.42249877660348,
          "actual_pass": 70.27027027027027,
          "err": 10.84777149366679
        },
        {
          "class_name": "HCM-KS24-CNTT1",
          "course_name": "[ IT211 - K24 ] Java Web Service",
          "size": 44,
          "v_class": 1.9688791423001948,
          "mult_env": 1.0,
          "pred_old": 70.95221985156279,
          "actual_pass": 68.18181818181817,
          "err": 2.770401669744615
        },
        {
          "class_name": "HN-KS24-CNTT3",
          "course_name": "[ IT211 - K24 ] Java Web Service",
          "size": 48,
          "v_class": 23.833867446393764,
          "mult_env": 0.9308306627680312,
          "pred_old": 78.01473972882606,
          "actual_pass": 62.5,
          "err": 15.514739728826058
        }
      ],
      "curr": [
        {
          "class_name": "HN-KS24-CNTT1",
          "course_name": "[IT-212] AI Application in Action",
          "size": 38,
          "v_class": 7.6146703296703295,
          "mult_env": 1.0,
          "pred_old": 62.43099306717229,
          "pred_new": 58.788739518912124,
          "actual_pass": 0.0
        },
        {
          "class_name": "HN-KS24-CNTT2",
          "course_name": "[IT-212] AI Application in Action",
          "size": 39,
          "v_class": 5.263956043956044,
          "mult_env": 1.0,
          "pred_old": 70.56620512820511,
          "pred_new": 70.56620512820511,
          "actual_pass": 5.128205128205128
        },
        {
          "class_name": "HN-KS24-CNTT4",
          "course_name": "[IT-212] AI Application in Action",
          "size": 33,
          "v_class": 4.3700183150183145,
          "mult_env": 1.0,
          "pred_old": 68.34223149398346,
          "pred_new": 65.663894638065,
          "actual_pass": 0.0
        },
        {
          "class_name": "HCM-KS24-CNTT1",
          "course_name": "[IT-212] AI Application in Action",
          "size": 44,
          "v_class": 4.901324786324786,
          "mult_env": 1.0,
          "pred_old": 53.461760614730686,
          "pred_new": 44.79906304529491,
          "actual_pass": 0.0
        },
        {
          "class_name": "HN-KS24-CNTT3",
          "course_name": "[IT-212] AI Application in Action",
          "size": 43,
          "v_class": 8.807399267399267,
          "mult_env": 1.0,
          "pred_old": 61.73543643391371,
          "pred_new": 49.119894591902074,
          "actual_pass": 0.0
        }
      ]
    },
    "KS25": {
      "cv": [
        {
          "class_name": "HN-KS25-CNTT6",
          "course_name": "[IT205-K25] Lập trình ứng dụng với Python",
          "size": 34,
          "v_class": 14.938418972332016,
          "mult_env": 0.9753079051383399,
          "pred_old": 47.4220534587324,
          "actual_pass": 58.82352941176471,
          "err": 11.40147595303231
        },
        {
          "class_name": "HN-KS25-CNTT5",
          "course_name": "[IT205-K25] Lập trình ứng dụng với Python",
          "size": 44,
          "v_class": 19.02689723320158,
          "mult_env": 0.9548655138339921,
          "pred_old": 59.95764726294688,
          "actual_pass": 68.18181818181817,
          "err": 8.224170918871295
        },
        {
          "class_name": "HN-KS25-CNTT4",
          "course_name": "[IT205-K25] Lập trình ứng dụng với Python",
          "size": 44,
          "v_class": 17.87443346508564,
          "mult_env": 0.9606278326745717,
          "pred_old": 59.65163436550872,
          "actual_pass": 70.45454545454545,
          "err": 10.802911089036733
        },
        {
          "class_name": "HN-KS25-CNTT3",
          "course_name": "[IT205-K25] Lập trình ứng dụng với Python",
          "size": 40,
          "v_class": 15.295461133069828,
          "mult_env": 0.9735226943346509,
          "pred_old": 58.8369894567882,
          "actual_pass": 70.0,
          "err": 11.163010543211797
        },
        {
          "class_name": "HN-KS25-CNTT2",
          "course_name": "[IT205-K25] Lập trình ứng dụng với Python",
          "size": 43,
          "v_class": 17.200553359683795,
          "mult_env": 0.963997233201581,
          "pred_old": 62.57933304461897,
          "actual_pass": 65.11627906976744,
          "err": 2.536946025148474
        },
        {
          "class_name": "HN-KS25-CNTT1",
          "course_name": "[IT205-K25] Lập trình ứng dụng với Python",
          "size": 44,
          "v_class": 20.00102108036891,
          "mult_env": 0.9499948945981554,
          "pred_old": 50.96426167237141,
          "actual_pass": 63.63636363636363,
          "err": 12.672101963992226
        },
        {
          "class_name": "HCM-KS25-CNTT5_HK2",
          "course_name": "[IT205-K25] Lập trình ứng dụng với Python",
          "size": 39,
          "v_class": 8.80419631093544,
          "mult_env": 1.0,
          "pred_old": 73.66819050564817,
          "actual_pass": 69.23076923076923,
          "err": 4.437421274878943
        },
        {
          "class_name": "HCM-KS25-CNTT6_HK2",
          "course_name": "[IT205-K25] Lập trình ứng dụng với Python",
          "size": 41,
          "v_class": 7.118498023715415,
          "mult_env": 1.0,
          "pred_old": 64.7949206566918,
          "actual_pass": 60.97560975609756,
          "err": 3.819310900594239
        },
        {
          "class_name": "HCM-KS25-CNTT7_HK2",
          "course_name": "[IT205-K25] Lập trình ứng dụng với Python",
          "size": 42,
          "v_class": 13.889453227931488,
          "mult_env": 0.9805527338603426,
          "pred_old": 59.709315460427284,
          "actual_pass": 52.38095238095239,
          "err": 7.328363079474897
        },
        {
          "class_name": "HCM-KS25-CNTT8_HK2",
          "course_name": "[IT205-K25] Lập trình ứng dụng với Python",
          "size": 38,
          "v_class": 39.46669960474308,
          "mult_env": 0.9,
          "pred_old": 35.96565076850699,
          "actual_pass": 18.421052631578945,
          "err": 17.544598136928045
        },
        {
          "class_name": "HN-KS25-CNTT8_HL",
          "course_name": "[IT205-K25] Lập trình ứng dụng với Python",
          "size": 24,
          "v_class": 13.504,
          "mult_env": 0.98248,
          "pred_old": 53.90632823273515,
          "actual_pass": 0.0,
          "err": 53.90632823273515
        }
      ],
      "curr": [
        {
          "class_name": "HN-KS25-CNTT6",
          "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
          "size": 33,
          "v_class": 7.937060606060605,
          "mult_env": 1.0,
          "pred_old": 56.86885171873297,
          "pred_new": 48.29559930614557,
          "actual_pass": 0.0
        },
        {
          "class_name": "HN-KS25-CNTT5",
          "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
          "size": 42,
          "v_class": 4.2570303030303025,
          "mult_env": 1.0,
          "pred_old": 56.81938271870287,
          "pred_new": 55.54330349870718,
          "actual_pass": 0.0
        },
        {
          "class_name": "HN-KS25-CNTT4",
          "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
          "size": 42,
          "v_class": 4.735757575757575,
          "mult_env": 1.0,
          "pred_old": 57.038407736479215,
          "pred_new": 55.37492543525102,
          "actual_pass": 0.0
        },
        {
          "class_name": "HN-KS25-CNTT3",
          "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
          "size": 37,
          "v_class": 4.250787878787879,
          "mult_env": 1.0,
          "pred_old": 57.28846479833678,
          "pred_new": 56.52581393762992,
          "actual_pass": 0.0
        },
        {
          "class_name": "HN-KS25-CNTT2",
          "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
          "size": 43,
          "v_class": 5.531333333333333,
          "mult_env": 1.0,
          "pred_old": 55.45908882379248,
          "pred_new": 53.58851735241502,
          "actual_pass": 0.0
        },
        {
          "class_name": "HN-KS25-CNTT1",
          "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
          "size": 42,
          "v_class": 4.583939393939393,
          "mult_env": 1.0,
          "pred_old": 54.824909094176846,
          "pred_new": 51.75604753089589,
          "actual_pass": 0.0
        },
        {
          "class_name": "HCM-KS25-CNTT5_HK2",
          "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
          "size": 39,
          "v_class": 3.151454545454545,
          "mult_env": 1.0,
          "pred_old": 62.41128394477319,
          "pred_new": 62.41128394477319,
          "actual_pass": 0.0
        },
        {
          "class_name": "HCM-KS25-CNTT6_HK2",
          "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
          "size": 40,
          "v_class": 2.212121212121212,
          "mult_env": 1.0,
          "pred_old": 61.7292425,
          "pred_new": 61.7292425,
          "actual_pass": 0.0
        },
        {
          "class_name": "HCM-KS25-CNTT7_HK2",
          "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
          "size": 42,
          "v_class": 1.8448484848484847,
          "mult_env": 1.0,
          "pred_old": 58.383194007822375,
          "pred_new": 57.80159048517679,
          "actual_pass": 0.0
        },
        {
          "class_name": "HCM-KS25-CNTT8_HK2",
          "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
          "size": 38,
          "v_class": 16.358545454545453,
          "mult_env": 0.9682072727272727,
          "pred_old": 46.8128944759727,
          "pred_new": 20.99079311585696,
          "actual_pass": 0.0
        },
        {
          "class_name": "HN-KS25-CNTT8_HL",
          "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
          "size": 22,
          "v_class": 10.571969696969695,
          "mult_env": 0.9971401515151516,
          "pred_old": 57.71656519075837,
          "pred_new": 39.00034732522213,
          "actual_pass": 0.0
        }
      ]
    },
    "QTKD": {
      "cv": [
        {
          "class_name": "HN-K25-QTKD3",
          "course_name": "[DTB201] Chuyển đổi số trong kinh doanh",
          "size": 28,
          "v_class": 0.0,
          "mult_env": 1.0,
          "pred_old": 77.34269642857141,
          "actual_pass": 67.85714285714286,
          "err": 9.485553571428554
        },
        {
          "class_name": "HN-K25-QTKD2",
          "course_name": "[DTB201] Chuyển đổi số trong kinh doanh",
          "size": 40,
          "v_class": 0.0,
          "mult_env": 1.0,
          "pred_old": 82.45414373569488,
          "actual_pass": 85.0,
          "err": 2.5458562643051152
        },
        {
          "class_name": "HN-K25-QTKD1",
          "course_name": "[DTB201] Chuyển đổi số trong kinh doanh",
          "size": 37,
          "v_class": 0.0,
          "mult_env": 1.0,
          "pred_old": 70.87677014655036,
          "actual_pass": 56.75675675675676,
          "err": 14.120013389793598
        }
      ],
      "curr": []
    }
  },
  "care_list": [
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT1",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 120,
      "full_name": "Mai Duy Anh",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (21.1%)"
      ],
      "p_final": 33.17125579591088,
      "att": 21.12077537422457,
      "hw": 100.0,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT1",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 205,
      "full_name": "Nguyễn Sỹ Trung",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (36.5%)"
      ],
      "p_final": 31.135204641609292,
      "att": 36.48128691724036,
      "hw": 100.0,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT1",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 103,
      "full_name": "Đinh Trọng An",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (13.4%)"
      ],
      "p_final": 69.07857426653578,
      "att": 13.440462000654387,
      "hw": 100.0,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT1",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 288,
      "full_name": "Nguyễn Văn Tùng",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (15.4%)"
      ],
      "p_final": 60.29455283765106,
      "att": 15.360569145078076,
      "hw": 100.0,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT1",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 411,
      "full_name": "Đinh Đình Thành",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (11.5%)"
      ],
      "p_final": 68.86258417500808,
      "att": 11.520412458292986,
      "hw": 100.0,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT1",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 203,
      "full_name": "Trần Quang Hiệp",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (19.2%)",
        "Vắng 3 buổi liên tiếp",
        "Học lực yếu (Xác suất đỗ 33.9%)"
      ],
      "p_final": 33.913266510353246,
      "att": 19.20066822980088,
      "hw": 100.0,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT1",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 249,
      "full_name": "Lê Xuân Ánh",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (13.4%)"
      ],
      "p_final": 61.003574266535786,
      "att": 13.440462000654387,
      "hw": 100.0,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT1",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 152,
      "full_name": "Nguyễn Nhật Minh",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (15.4%)",
        "Vắng 3 buổi liên tiếp",
        "Học lực yếu (Xác suất đỗ 33.0%)"
      ],
      "p_final": 32.99727641882553,
      "att": 15.360569145078076,
      "hw": 100.0,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT1",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 83,
      "full_name": "Tôn Phạm Quang Huy",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (38.4%)",
        "Nợ bài tập > 20% (63.8%)"
      ],
      "p_final": 25.352548171425216,
      "att": 38.40139406166405,
      "hw": 36.20672881605441,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT1",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 198,
      "full_name": "Quàng Duy Mạnh",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (49.9%)",
        "Nợ bài tập > 20% (63.8%)"
      ],
      "p_final": 24.373313112470317,
      "att": 49.921806519957045,
      "hw": 36.20672881605441,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT1",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 394,
      "full_name": "Nguyễn Hoàng Long",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (49.9%)",
        "Nợ bài tập > 20% (63.8%)"
      ],
      "p_final": 24.373313112470317,
      "att": 49.921806519957045,
      "hw": 36.20672881605441,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT2",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 98,
      "full_name": "Nguyễn Dương Phương Trang",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (13.3%)"
      ],
      "p_final": 66.03026805863415,
      "att": 13.30699304016254,
      "hw": 88.0273158868121,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT2",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 139,
      "full_name": "Nguyễn Văn Kiên",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận nợ bài tập (19.3%)"
      ],
      "p_final": 72.06666666666666,
      "att": 0.0,
      "hw": 80.69166343852856,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT2",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 230,
      "full_name": "Nguyễn Công Gia Huy",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (16.6%)"
      ],
      "p_final": 65.73990343622144,
      "att": 16.633816152226153,
      "hw": 100.0,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT4",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 149,
      "full_name": "Phạm Ngọc Linh",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (11.1%)"
      ],
      "p_final": 69.13798875495544,
      "att": 11.14338955855608,
      "hw": 100.0,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT4",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 266,
      "full_name": "Nguyễn Tiến Minh",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (11.1%)"
      ],
      "p_final": 65.80048837348573,
      "att": 11.14338955855608,
      "hw": 100.0,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT4",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 888,
      "full_name": "Nguyễn Quang Vinh",
      "risk_level": "RED",
      "reasons": [
        "Nợ bài tập > 20% (28.3%)"
      ],
      "p_final": 64.03080674068305,
      "att": 13.92929962991807,
      "hw": 71.71297401887949,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT4",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 175,
      "full_name": "Đinh Quốc Khánh",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (50.1%)"
      ],
      "p_final": 24.35430950462606,
      "att": 50.14537837694831,
      "hw": 86.05554874303068,
      "el": 1.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HCM-KS24-CNTT1",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 591,
      "full_name": "Hồ Quốc Khải",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (12.6%)"
      ],
      "p_final": 55.05514086389773,
      "att": 12.565962347177987,
      "hw": 98.51106760443626,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HCM-KS24-CNTT1",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 639,
      "full_name": "Đoàn Nhật Cường",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (25.1%)"
      ],
      "p_final": 50.52396347360941,
      "att": 25.131849298619585,
      "hw": 98.51106760443626,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HCM-KS24-CNTT1",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 684,
      "full_name": "Nguyễn Trọng Đăng Dương",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (25.1%)"
      ],
      "p_final": 50.62996347360942,
      "att": 25.131849298619585,
      "hw": 98.51106760443626,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HCM-KS24-CNTT1",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 680,
      "full_name": "Mai Sơn Việt",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (12.6%)"
      ],
      "p_final": 52.75514086389774,
      "att": 12.565962347177987,
      "hw": 91.47452055651898,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HCM-KS24-CNTT1",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 620,
      "full_name": "Phạm Công Thành",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (12.6%)"
      ],
      "p_final": 56.54314086389773,
      "att": 12.565962347177987,
      "hw": 98.51106760443626,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HCM-KS24-CNTT1",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 588,
      "full_name": "Huỳnh La Tiến Lộc",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (12.6%)"
      ],
      "p_final": 55.54314086389775,
      "att": 12.565962347177987,
      "hw": 98.51106760443626,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HCM-KS24-CNTT1",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 676,
      "full_name": "Hoàng Đình Tùng",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (25.1%)"
      ],
      "p_final": 51.729963473609416,
      "att": 25.131849298619585,
      "hw": 98.51106760443626,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HCM-KS24-CNTT1",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 592,
      "full_name": "Lu Nhựt Đình",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (12.6%)"
      ],
      "p_final": 54.84314086389773,
      "att": 12.565962347177987,
      "hw": 98.51106760443626,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HCM-KS24-CNTT1",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 614,
      "full_name": "Nguyễn Đại Phát",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (12.6%)"
      ],
      "p_final": 54.54314086389774,
      "att": 12.565962347177987,
      "hw": 98.51106760443626,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HCM-KS24-CNTT1",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 625,
      "full_name": "Trần Hoàng Duy",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (12.6%)"
      ],
      "p_final": 54.343140863897744,
      "att": 12.565962347177987,
      "hw": 98.51106760443626,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HCM-KS24-CNTT1",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 613,
      "full_name": "Nguyễn Văn Toàn",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (37.7%)"
      ],
      "p_final": 25.214379847406683,
      "att": 37.69786819259986,
      "hw": 98.51106760443626,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HCM-KS24-CNTT1",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 628,
      "full_name": "Trần Minh Đức",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (31.4%)"
      ],
      "p_final": 23.960671367638646,
      "att": 31.414952990280202,
      "hw": 98.51106760443626,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HCM-KS24-CNTT1",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 616,
      "full_name": "Phan Trung Kiên",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (25.1%)"
      ],
      "p_final": 51.12996347360942,
      "att": 25.131849298619585,
      "hw": 91.47452055651898,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HCM-KS24-CNTT1",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 615,
      "full_name": "Phan Lê Duy Thịnh",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (12.6%)"
      ],
      "p_final": 52.75514086389774,
      "att": 12.565962347177987,
      "hw": 98.51106760443626,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HCM-KS24-CNTT1",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 690,
      "full_name": "Trương Công Quý",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (12.6%)"
      ],
      "p_final": 55.255140863897736,
      "att": 12.565962347177987,
      "hw": 98.51106760443626,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HCM-KS24-CNTT1",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 610,
      "full_name": "Nguyễn Tá Thọ",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (25.1%)"
      ],
      "p_final": 51.32996347360942,
      "att": 25.131849298619585,
      "hw": 91.47452055651898,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HCM-KS24-CNTT1",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 635,
      "full_name": "Võ Thanh Khang",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (31.4%)"
      ],
      "p_final": 50.47334273527729,
      "att": 31.414952990280202,
      "hw": 91.47452055651898,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HCM-KS24-CNTT1",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 626,
      "full_name": "Trần Hoàng Thanh",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (25.1%)"
      ],
      "p_final": 26.16648173680471,
      "att": 25.131849298619585,
      "hw": 91.47452055651898,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT6",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1329,
      "full_name": "Nguyễn Minh Đức 8",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (10.5%)"
      ],
      "p_final": 60.44304572969087,
      "att": 10.467168224299066,
      "hw": 100.0,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT6",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1547,
      "full_name": "Trần Nguyễn Duy Đức",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (27.9%)"
      ],
      "p_final": 53.15839245866283,
      "att": 27.91244859813084,
      "hw": 100.0,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT6",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1551,
      "full_name": "Trịnh Xuân Hùng",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (14.0%)"
      ],
      "p_final": 58.16512507548526,
      "att": 13.95622429906542,
      "hw": 100.0,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT6",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1541,
      "full_name": "Nguyễn Văn Cường 3",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (34.9%)"
      ],
      "p_final": 53.99760115025162,
      "att": 34.89056074766355,
      "hw": 96.3185894206549,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT6",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1562,
      "full_name": "Hoàng Văn Thắng",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (10.5%)"
      ],
      "p_final": 58.258045729690856,
      "att": 10.467168224299066,
      "hw": 100.0,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT6",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1578,
      "full_name": "Trần Nhật Anh 2",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (55.8%)"
      ],
      "p_final": 24.345038612508986,
      "att": 55.82489719626168,
      "hw": 84.27876574307304,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT6",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1552,
      "full_name": "Đoàn Huy Hoàng 2",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (27.9%)"
      ],
      "p_final": 49.163788612508974,
      "att": 27.91244859813084,
      "hw": 92.30531486146096,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT6",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1599,
      "full_name": "Trịnh Quốc Trung",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (14.0%)"
      ],
      "p_final": 59.40012507548526,
      "att": 13.95622429906542,
      "hw": 96.3185894206549,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT6",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1422,
      "full_name": "Nguyễn Tấn Phong",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (31.4%)"
      ],
      "p_final": 54.280521804457216,
      "att": 31.401504672897193,
      "hw": 80.26549118387909,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT6",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1559,
      "full_name": "Hoàng Đức Duy Anh",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (14.0%)"
      ],
      "p_final": 57.785125075485254,
      "att": 13.95622429906542,
      "hw": 100.0,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT6",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1642,
      "full_name": "Nguyễn Ngọc Hiển Vinh",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (10.5%)"
      ],
      "p_final": 59.30304572969087,
      "att": 10.467168224299066,
      "hw": 100.0,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT6",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1381,
      "full_name": "Nguyễn Trần Trọng Đức",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (38.4%)",
        "Nợ bài tập > 20% (27.8%)"
      ],
      "p_final": 23.587513324946077,
      "att": 38.3796168224299,
      "hw": 72.23894206549119,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT6",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1625,
      "full_name": "Phùng Minh Công",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (34.9%)"
      ],
      "p_final": 24.384473652048882,
      "att": 34.89056074766355,
      "hw": 92.30531486146096,
      "el": 1.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT5",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1633,
      "full_name": "Trần Khắc Huy Hoàng",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (28.1%)",
        "Nợ bài tập > 20% (24.5%)"
      ],
      "p_final": 28.028318552036197,
      "att": 28.053529411764707,
      "hw": 75.4515068977715,
      "el": 1.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT5",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1283,
      "full_name": "Vũ Văn Hiếu",
      "risk_level": "RED",
      "reasons": [
        "Xác suất đỗ quá thấp (26.7%)"
      ],
      "p_final": 26.69232839366515,
      "att": 18.70235294117647,
      "hw": 87.36490272373541,
      "el": 1.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT5",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1588,
      "full_name": "Nguyễn Thạch Anh",
      "risk_level": "RED",
      "reasons": [
        "Xác suất đỗ quá thấp (25.9%)"
      ],
      "p_final": 25.92235339366516,
      "att": 18.70235294117647,
      "hw": 87.36490272373541,
      "el": 1.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT5",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1377,
      "full_name": "Phạm Anh Quân",
      "risk_level": "RED",
      "reasons": [
        "Xác suất đỗ quá thấp (25.4%)"
      ],
      "p_final": 25.447353393665157,
      "att": 18.70235294117647,
      "hw": 87.36490272373541,
      "el": 1.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT5",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1641,
      "full_name": "Đặng Việt Anh",
      "risk_level": "RED",
      "reasons": [
        "Xác suất đỗ quá thấp (25.4%)"
      ],
      "p_final": 25.447353393665157,
      "att": 18.70235294117647,
      "hw": 87.36490272373541,
      "el": 1.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT5",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1278,
      "full_name": "Ngô Đình Phát",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (22.4%)"
      ],
      "p_final": 25.5670086877828,
      "att": 22.442823529411765,
      "hw": 87.36490272373541,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT4",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1391,
      "full_name": "Trần Tuấn Anh",
      "risk_level": "YELLOW",
      "reasons": [
        "Vắng 2 buổi liên tiếp",
        "Học lực yếu (Xác suất đỗ 30.0%)"
      ],
      "p_final": 30.016702081447953,
      "att": 2.6731764705882353,
      "hw": 99.50435865504359,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT4",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1554,
      "full_name": "Phạm Danh Quốc Anh",
      "risk_level": "RED",
      "reasons": [
        "Xác suất đỗ quá thấp (25.7%)"
      ],
      "p_final": 25.747866334841625,
      "att": 16.039058823529412,
      "hw": 95.52418430884184,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT4",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1687,
      "full_name": "Nguyễn Đức Phong 2",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (18.7%)"
      ],
      "p_final": 51.84282914027148,
      "att": 18.712235294117647,
      "hw": 91.54400996264009,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT4",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1548,
      "full_name": "Ngô Trung Kiên",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (37.4%)",
        "Nợ bài tập > 20% (28.4%)"
      ],
      "p_final": 23.47875221719456,
      "att": 37.424470588235295,
      "hw": 71.64313823163138,
      "el": 1.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT4",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1332,
      "full_name": "Trần Đức Anh 2",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (48.1%)",
        "Nợ bài tập > 20% (32.3%)"
      ],
      "p_final": 21.70294515837103,
      "att": 48.11717647058824,
      "hw": 67.66296388542963,
      "el": 1.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT4",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1622,
      "full_name": "Nguyễn Như Huy",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (26.7%)"
      ],
      "p_final": 24.684559276018092,
      "att": 26.731764705882355,
      "hw": 87.56383561643835,
      "el": 1.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT3",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1545,
      "full_name": "Trần Tuấn Anh 2",
      "risk_level": "RED",
      "reasons": [
        "Xác suất đỗ quá thấp (26.1%)"
      ],
      "p_final": 26.079040923076914,
      "att": 9.553010526315788,
      "hw": 87.49681415929204,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT3",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 67,
      "full_name": "Nguyễn Thị Huyền Diệp",
      "risk_level": "RED",
      "reasons": [
        "Xác suất đỗ quá thấp (27.9%)"
      ],
      "p_final": 27.85777292307692,
      "att": 14.329515789473684,
      "hw": 87.49681415929204,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT3",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 187,
      "full_name": "Nguyễn Công Thắng",
      "risk_level": "RED",
      "reasons": [
        "Nợ bài tập > 20% (20.5%)"
      ],
      "p_final": 28.218081846153844,
      "att": 19.106021052631576,
      "hw": 79.54255832662913,
      "el": 1.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT3",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1509,
      "full_name": "Phạm Trung Hiếu 3",
      "risk_level": "RED",
      "reasons": [
        "Xác suất đỗ quá thấp (25.6%)"
      ],
      "p_final": 25.625272923076913,
      "att": 14.329515789473684,
      "hw": 87.49681415929204,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT2",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1359,
      "full_name": "Phạm Hồng Phong",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (11.3%)"
      ],
      "p_final": 58.571915192307685,
      "att": 11.315223684210526,
      "hw": 99.2576481835564,
      "el": 1.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT2",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1515,
      "full_name": "Nguyễn Văn Thi",
      "risk_level": "RED",
      "reasons": [
        "Nợ bài tập > 20% (20.6%)"
      ],
      "p_final": 57.399643846153836,
      "att": 6.4658421052631585,
      "hw": 79.40611854684512,
      "el": 1.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT2",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 259,
      "full_name": "Hoàng Minh Chiến",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (29.1%)",
        "Nợ bài tập > 20% (36.5%)"
      ],
      "p_final": 23.034929423076917,
      "att": 29.096289473684212,
      "hw": 63.52489483747609,
      "el": 1.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT2",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1344,
      "full_name": "Mai Quân Minh",
      "risk_level": "RED",
      "reasons": [
        "Xác suất đỗ quá thấp (24.7%)"
      ],
      "p_final": 24.73843942307692,
      "att": 16.164605263157895,
      "hw": 87.34673040152963,
      "el": 1.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT2",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1594,
      "full_name": "Nguyễn Hồng Minh",
      "risk_level": "RED",
      "reasons": [
        "Xác suất đỗ quá thấp (24.4%)"
      ],
      "p_final": 24.382189423076916,
      "att": 16.164605263157895,
      "hw": 87.34673040152963,
      "el": 1.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT2",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 70,
      "full_name": "Nguyễn Nam Hưng",
      "risk_level": "RED",
      "reasons": [
        "Xác suất đỗ quá thấp (26.9%)"
      ],
      "p_final": 26.93341442307692,
      "att": 16.164605263157895,
      "hw": 87.34673040152963,
      "el": 1.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT2",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1304,
      "full_name": "Phạm Việt Thành",
      "risk_level": "RED",
      "reasons": [
        "Xác suất đỗ quá thấp (24.8%)"
      ],
      "p_final": 24.833439423076918,
      "att": 16.164605263157895,
      "hw": 87.34673040152963,
      "el": 1.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT1",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1511,
      "full_name": "Vi Anh Dũng",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (38.0%)"
      ],
      "p_final": 25.708869266714597,
      "att": 37.96878504672897,
      "hw": 92.28084895649098,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT1",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1347,
      "full_name": "Đồng Nguyễn Tiến Đạt",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (22.3%)"
      ],
      "p_final": 28.619118799424875,
      "att": 22.334579439252337,
      "hw": 92.28084895649098,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT1",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1499,
      "full_name": "Nguyễn Xuân Sơn 2",
      "risk_level": "RED",
      "reasons": [
        "Xác suất đỗ quá thấp (28.6%)"
      ],
      "p_final": 28.568475808770664,
      "att": 17.86766355140187,
      "hw": 96.29305978068625,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT1",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1682,
      "full_name": "Trần Trung Dũng 2",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (26.8%)"
      ],
      "p_final": 23.727934867002155,
      "att": 26.801495327102803,
      "hw": 80.2442164839052,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT1",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 165,
      "full_name": "Nguyễn Vũ Hoàng",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (31.3%)"
      ],
      "p_final": 27.108327857656356,
      "att": 31.268411214953268,
      "hw": 84.25642730810047,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT1",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1502,
      "full_name": "Hà Duy Thành",
      "risk_level": "RED",
      "reasons": [
        "Xác suất đỗ quá thấp (28.8%)"
      ],
      "p_final": 28.75847580877067,
      "att": 17.86766355140187,
      "hw": 96.29305978068625,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT1",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 94,
      "full_name": "Trần Kim Tiến",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (26.8%)"
      ],
      "p_final": 23.727934867002155,
      "att": 26.801495327102803,
      "hw": 80.2442164839052,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HCM-KS25-CNTT7_HK2",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1480,
      "full_name": "Đặng Đức Tín",
      "risk_level": "RED",
      "reasons": [
        "Xác suất đỗ quá thấp (28.3%)"
      ],
      "p_final": 28.348539539899352,
      "att": 17.66355140186916,
      "hw": 100.0,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HCM-KS25-CNTT7_HK2",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1463,
      "full_name": "Nguyễn Nhật Quốc Hưng",
      "risk_level": "RED",
      "reasons": [
        "Xác suất đỗ quá thấp (28.6%)"
      ],
      "p_final": 28.58536033429187,
      "att": 11.77570093457944,
      "hw": 96.48251748251748,
      "el": 1.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HCM-KS25-CNTT7_HK2",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1660,
      "full_name": "Trương Định Hải",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (29.4%)"
      ],
      "p_final": 24.4273479511143,
      "att": 29.4392523364486,
      "hw": 88.4423076923077,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HCM-KS25-CNTT8_HK2",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1590,
      "full_name": "Nguyễn Hoàng Đức Huy",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (21.4%)"
      ],
      "p_final": 55.50215004247812,
      "att": 21.360508474576275,
      "hw": 95.21015151515152,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HCM-KS25-CNTT8_HK2",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1468,
      "full_name": "Bạch Chí Lân",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (21.4%)"
      ],
      "p_final": 54.39839375156903,
      "att": 21.360508474576275,
      "hw": 95.21015151515152,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HCM-KS25-CNTT8_HK2",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1634,
      "full_name": "Nguyễn Văn Hoàng",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (51.3%)"
      ],
      "p_final": 24.062256019952773,
      "att": 51.265220338983056,
      "hw": 91.40174545454545,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HCM-KS25-CNTT8_HK2",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1353,
      "full_name": "Lê Phúc Duy",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (29.9%)"
      ],
      "p_final": 48.31960252330154,
      "att": 29.90471186440678,
      "hw": 95.21015151515152,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HCM-KS25-CNTT8_HK2",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1512,
      "full_name": "Trần Phạm Minh Cường",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (42.7%)"
      ],
      "p_final": 50.376948126354854,
      "att": 42.72101694915255,
      "hw": 95.21015151515152,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HCM-KS25-CNTT8_HK2",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1597,
      "full_name": "Phạm Minh Tài",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (59.8%)"
      ],
      "p_final": 21.901726352455395,
      "att": 59.80942372881356,
      "hw": 83.78493333333334,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HCM-KS25-CNTT8_HK2",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 627,
      "full_name": "Trần Minh Ân",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (21.4%)"
      ],
      "p_final": 51.501033487932666,
      "att": 21.360508474576275,
      "hw": 91.40174545454545,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HCM-KS25-CNTT8_HK2",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 681,
      "full_name": "Nguyễn Anh Dũng",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (25.6%)"
      ],
      "p_final": 53.6160382451276,
      "att": 25.632610169491528,
      "hw": 91.40174545454545,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HCM-KS25-CNTT8_HK2",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 643,
      "full_name": "Đỗ Đình Long",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (21.4%)"
      ],
      "p_final": 47.86783569702358,
      "att": 21.360508474576275,
      "hw": 91.40174545454545,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HCM-KS25-CNTT8_HK2",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 642,
      "full_name": "Đỗ Tiến Phúc",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (21.4%)"
      ],
      "p_final": 50.76519596065994,
      "att": 21.360508474576275,
      "hw": 95.21015151515152,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HCM-KS25-CNTT8_HK2",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 586,
      "full_name": "Dương Trung Dũng",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (12.8%)"
      ],
      "p_final": 56.80153502389248,
      "att": 12.816305084745764,
      "hw": 95.21015151515152,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HCM-KS25-CNTT8_HK2",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 619,
      "full_name": "Phan Đình Nghị",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (17.1%)"
      ],
      "p_final": 51.78103837479369,
      "att": 17.088406779661018,
      "hw": 95.21015151515152,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HCM-KS25-CNTT8_HK2",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 587,
      "full_name": "Hoàng Công Dũng",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (42.7%)"
      ],
      "p_final": 49.27319183544576,
      "att": 42.72101694915255,
      "hw": 95.21015151515152,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HCM-KS25-CNTT8_HK2",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 633,
      "full_name": "Võ Chí Đức",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (29.9%)"
      ],
      "p_final": 49.150957421902945,
      "att": 29.90471186440678,
      "hw": 95.21015151515152,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HCM-KS25-CNTT8_HK2",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1303,
      "full_name": "Nguyễn Thiện Tân",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (51.3%)",
        "Nợ bài tập > 20% (23.8%)"
      ],
      "p_final": 22.516997212680046,
      "att": 51.265220338983056,
      "hw": 76.1681212121212,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HCM-KS25-CNTT8_HK2",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1404,
      "full_name": "Nguyễn Khắc Tiến",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (59.8%)",
        "Nợ bài tập > 20% (20.0%)"
      ],
      "p_final": 21.17922588036448,
      "att": 59.80942372881356,
      "hw": 79.97652727272727,
      "el": 1.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HCM-KS25-CNTT8_HK2",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 601,
      "full_name": "Nguyễn Gia Huy 2",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (51.3%)",
        "Nợ bài tập > 20% (27.6%)"
      ],
      "p_final": 41.44678647990555,
      "att": 51.265220338983056,
      "hw": 72.35971515151515,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HCM-KS25-CNTT8_HK2",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1631,
      "full_name": "Đặng Trần Anh Khoa",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (21.4%)"
      ],
      "p_final": 48.971591987932655,
      "att": 21.360508474576275,
      "hw": 95.21015151515152,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HCM-KS25-CNTT8_HK2",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1486,
      "full_name": "Trần Bảo Trân",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (17.1%)"
      ],
      "p_final": 55.73616508388459,
      "att": 17.088406779661018,
      "hw": 91.40174545454545,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HCM-KS25-CNTT8_HK2",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1645,
      "full_name": "Nguyễn Hoàng Thiên Phúc",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (59.8%)"
      ],
      "p_final": 19.960494975819028,
      "att": 59.80942372881356,
      "hw": 91.40174545454545,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HCM-KS25-CNTT8_HK2",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1327,
      "full_name": "Lê Chí Vỹ",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (51.3%)"
      ],
      "p_final": 43.286380298087366,
      "att": 51.265220338983056,
      "hw": 83.78493333333334,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HCM-KS25-CNTT8_HK2",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1690,
      "full_name": "Nguyễn Khánh Tùng",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (17.1%)"
      ],
      "p_final": 50.63129223843005,
      "att": 17.088406779661018,
      "hw": 91.40174545454545,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HCM-KS25-CNTT8_HK2",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1527,
      "full_name": "Trần Anh Tuấn",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (34.2%)"
      ],
      "p_final": 22.364164381856625,
      "att": 34.176813559322035,
      "hw": 95.21015151515152,
      "el": 1.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HCM-KS25-CNTT8_HK2",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 1282,
      "full_name": "Bùi Gia Anh",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (51.3%)",
        "Nợ bài tập > 20% (31.4%)"
      ],
      "p_final": 20.723393239952774,
      "att": 51.265220338983056,
      "hw": 68.55130909090909,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HCM-KS25-CNTT8_HK2",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 636,
      "full_name": "Vũ Trần Anh Hoàng",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (59.8%)",
        "Nợ bài tập > 20% (35.3%)"
      ],
      "p_final": 20.443388353091756,
      "att": 59.80942372881356,
      "hw": 64.74290303030303,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HCM-KS25-CNTT8_HK2",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 718,
      "full_name": "Nguyễn Gia Huy",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (21.4%)"
      ],
      "p_final": 54.30641406065994,
      "att": 21.360508474576275,
      "hw": 91.40174545454545,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HCM-KS25-CNTT8_HK2",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 611,
      "full_name": "Nguyễn Việt Hoàng Anh",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (21.4%)"
      ],
      "p_final": 55.689647104715874,
      "att": 21.360508474576275,
      "hw": 95.21015151515152,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HCM-KS25-CNTT8_HK2",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 692,
      "full_name": "Võ Thanh Nguyên",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (25.6%)"
      ],
      "p_final": 53.6160382451276,
      "att": 25.632610169491528,
      "hw": 95.21015151515152,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT8_HL",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 142,
      "full_name": "Nguyễn Phạm Vĩnh Thành",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (15.4%)"
      ],
      "p_final": 57.922892615316975,
      "att": 15.356785714285712,
      "hw": 95.91941391941391,
      "el": 1.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT8_HL",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 135,
      "full_name": "Nguyễn Khắc Phong",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (46.1%)"
      ],
      "p_final": 51.65025428847714,
      "att": 46.07035714285714,
      "hw": 92.08263736263737,
      "el": 1.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT8_HL",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 112,
      "full_name": "Nguyễn Hải Đăng 2",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (30.7%)"
      ],
      "p_final": 49.98652893161577,
      "att": 30.713571428571424,
      "hw": 95.91941391941391,
      "el": 1.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT8_HL",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 311,
      "full_name": "Đỗ Ngọc Dân",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (30.7%)"
      ],
      "p_final": 55.96073090880994,
      "att": 30.713571428571424,
      "hw": 95.91941391941391,
      "el": 1.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT8_HL",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 191,
      "full_name": "Thái Hồng Đức",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (30.7%)"
      ],
      "p_final": 56.28470174403722,
      "att": 30.713571428571424,
      "hw": 95.91941391941391,
      "el": 1.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT8_HL",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 116,
      "full_name": "Hà Bích Ngọc",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (15.4%)"
      ],
      "p_final": 59.98418073652909,
      "att": 15.356785714285712,
      "hw": 95.91941391941391,
      "el": 1.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT8_HL",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 299,
      "full_name": "Chu Văn Ninh",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (30.7%)"
      ],
      "p_final": 54.43181591449176,
      "att": 30.713571428571424,
      "hw": 95.91941391941391,
      "el": 1.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT8_HL",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 101,
      "full_name": "Trần Văn Thắng",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (92.1%)"
      ],
      "p_final": 44.79659307899392,
      "att": 92.14071428571428,
      "hw": 95.91941391941391,
      "el": 1.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT8_HL",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 900,
      "full_name": "Trần Mạnh Dương",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (61.4%)"
      ],
      "p_final": 46.3527086321595,
      "att": 61.42714285714285,
      "hw": 88.2458608058608,
      "el": 1.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT8_HL",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 279,
      "full_name": "Nguyễn Tùng Dương",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (15.4%)"
      ],
      "p_final": 60.95419867592303,
      "att": 15.356785714285712,
      "hw": 95.91941391941391,
      "el": 1.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT8_HL",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 107,
      "full_name": "Nguyễn Khắc Hưng",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (46.1%)"
      ],
      "p_final": 52.293459543211995,
      "att": 46.07035714285714,
      "hw": 95.91941391941391,
      "el": 1.0,
      "rp": 100.0
    },
    {
      "batch": "K25",
      "class_name": "HN-KS25-CNTT8_HL",
      "course_name": "[IT-215] Phát triển dịch vụ Web với FastAPI",
      "student_id": 153,
      "full_name": "Nguyễn Hữu Đại",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (15.4%)"
      ],
      "p_final": 58.615356593536674,
      "att": 15.356785714285712,
      "hw": 95.91941391941391,
      "el": 1.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT3",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 185,
      "full_name": "Trần Khánh An",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (57.7%)",
        "Nợ bài tập > 20% (29.8%)"
      ],
      "p_final": 19.01598136542751,
      "att": 57.67351967905823,
      "hw": 70.19983582465298,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT3",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 137,
      "full_name": "Đặng Khánh An",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (15.4%)"
      ],
      "p_final": 67.99075330691953,
      "att": 15.379566798735743,
      "hw": 98.27973084262183,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT3",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 99,
      "full_name": "Đỗ Thảo Minh",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (26.9%)"
      ],
      "p_final": 44.983812519757194,
      "att": 26.91427073454739,
      "hw": 98.27973084262183,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT3",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 92,
      "full_name": "Nguyễn Duy Mạnh",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (11.5%)"
      ],
      "p_final": 66.85972587950434,
      "att": 11.534703935811647,
      "hw": 98.27973084262183,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT3",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 122,
      "full_name": "Trương Hà Cẩm Linh",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (23.1%)"
      ],
      "p_final": 65.452785092342,
      "att": 23.069407871623294,
      "hw": 98.27973084262183,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT3",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 162,
      "full_name": "Bùi Văn Phương",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (26.9%)"
      ],
      "p_final": 62.6588125197572,
      "att": 26.91427073454739,
      "hw": 98.27973084262183,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT3",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 173,
      "full_name": "Đỗ Gia Hưng",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (11.5%)"
      ],
      "p_final": 68.95972587950435,
      "att": 11.534703935811647,
      "hw": 91.2597079482642,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT3",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 223,
      "full_name": "Trần Anh Dũng",
      "risk_level": "YELLOW",
      "reasons": [
        "Học lực yếu (Xác suất đỗ 48.8%)"
      ],
      "p_final": 48.82870537291152,
      "att": 7.6898064687757435,
      "hw": 98.27973084262183,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT3",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 221,
      "full_name": "Vi Trung Quý",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (11.5%)"
      ],
      "p_final": 68.08472587950433,
      "att": 11.534703935811647,
      "hw": 98.27973084262183,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT3",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 208,
      "full_name": "Hoàng Nguyên Đức",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (15.4%)"
      ],
      "p_final": 52.20741997358619,
      "att": 15.379566798735743,
      "hw": 98.27973084262183,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT3",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 222,
      "full_name": "Hà Quang Huy",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (15.4%)"
      ],
      "p_final": 68.59075330691952,
      "att": 15.379566798735743,
      "hw": 98.27973084262183,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT3",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 218,
      "full_name": "Hoàng Trung Dũng",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (15.4%)",
        "Cận nợ bài tập (15.8%)"
      ],
      "p_final": 68.08175330691952,
      "att": 15.379566798735743,
      "hw": 84.23978333363739,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT3",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 227,
      "full_name": "Đỗ Hồng Kỳ",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (11.5%)"
      ],
      "p_final": 64.10972587950434,
      "att": 11.534703935811647,
      "hw": 98.27973084262183,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT3",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 226,
      "full_name": "Hoàng Thiên Sơn",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (30.8%)",
        "Nợ bài tập > 20% (22.8%)"
      ],
      "p_final": 52.004261012766484,
      "att": 30.759248944510844,
      "hw": 77.21976043927975,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT3",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 238,
      "full_name": "Lê Thanh Tùng",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (11.5%)"
      ],
      "p_final": 65.88472587950433,
      "att": 11.534703935811647,
      "hw": 98.27973084262183,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT3",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 252,
      "full_name": "Lê Thành Long",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (11.5%)"
      ],
      "p_final": 66.94172587950433,
      "att": 11.534703935811647,
      "hw": 98.27973084262183,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT3",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 887,
      "full_name": "Nguyễn Minh Hoàng",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (23.1%)"
      ],
      "p_final": 53.31153399515737,
      "att": 23.069407871623294,
      "hw": 98.27973084262183,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT3",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 285,
      "full_name": "Nguyễn Văn Hiếu",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (11.5%)"
      ],
      "p_final": 67.33472587950433,
      "att": 11.534703935811647,
      "hw": 91.2597079482642,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT3",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 901,
      "full_name": "Trần Thị Khánh Huyền",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (15.4%)"
      ],
      "p_final": 66.79075330691953,
      "att": 15.379566798735743,
      "hw": 91.2597079482642,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT3",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 239,
      "full_name": "Nguyễn Ngọc Thanh",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (15.4%)"
      ],
      "p_final": 56.2977533069195,
      "att": 15.379566798735743,
      "hw": 98.27973084262183,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT3",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 308,
      "full_name": "Đỗ Chung Hiếu",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (26.9%)"
      ],
      "p_final": 58.30881251975719,
      "att": 26.91427073454739,
      "hw": 91.2597079482642,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT3",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 910,
      "full_name": "Đặng Tô Ngọc Dũng",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (23.1%)"
      ],
      "p_final": 62.42778509234201,
      "att": 23.069407871623294,
      "hw": 98.27973084262183,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT3",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 416,
      "full_name": "Nguyễn Hoàng Nhật",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (30.8%)"
      ],
      "p_final": 50.4148168777645,
      "att": 30.759248944510844,
      "hw": 91.2597079482642,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT3",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 723,
      "full_name": "Phan Phước Anh",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (88.4%)",
        "Nợ bài tập > 20% (71.9%)"
      ],
      "p_final": 21.099881333663294,
      "att": 88.43276862356909,
      "hw": 28.079895017968852,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT3",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 303,
      "full_name": "Nguyễn Thế Kiên",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (19.2%)"
      ],
      "p_final": 65.62175766492683,
      "att": 19.224545008699195,
      "hw": 98.27973084262183,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT3",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 933,
      "full_name": "Ngô Quang Anh",
      "risk_level": "RED",
      "reasons": [
        "Vắng chuyên cần > 20% (30.8%)"
      ],
      "p_final": 52.789816877764494,
      "att": 30.759248944510844,
      "hw": 98.27973084262183,
      "el": 0.0,
      "rp": 100.0
    },
    {
      "batch": "K24",
      "class_name": "HN-KS24-CNTT3",
      "course_name": "[IT-212] AI Application in Action",
      "student_id": 902,
      "full_name": "Trịnh Khắc Hưng",
      "risk_level": "YELLOW",
      "reasons": [
        "Cận vắng chuyên cần (11.5%)"
      ],
      "p_final": 55.27243366424535,
      "att": 11.534703935811647,
      "hw": 91.2597079482642,
      "el": 0.0,
      "rp": 100.0
    }
  ]
};
        const chartLabels = ["HN-KS24-CNTT1", "HN-KS24-CNTT2", "HN-KS24-CNTT4", "HCM-KS24-CNTT1", "HN-KS24-CNTT3", "HN-KS25-CNTT6", "HN-KS25-CNTT5", "HN-KS25-CNTT4", "HN-KS25-CNTT3", "HN-KS25-CNTT2", "HN-KS25-CNTT1", "HCM-KS25-CNTT5_HK2", "HCM-KS25-CNTT6_HK2", "HCM-KS25-CNTT7_HK2", "HCM-KS25-CNTT8_HK2", "HN-KS25-CNTT8_HL", "HN-K25-QTKD3", "HN-K25-QTKD2", "HN-K25-QTKD1"];
        const chartPredData = [62.1, 78.2, 59.4, 71.0, 78.0, 47.4, 60.0, 59.7, 58.8, 62.6, 51.0, 73.7, 64.8, 59.7, 36.0, 53.9, 77.3, 82.5, 70.9];
        const chartActualData = [78.6, 92.5, 70.3, 68.2, 62.5, 58.8, 68.2, 70.5, 70.0, 65.1, 63.6, 69.2, 61.0, 52.4, 18.4, 0.0, 67.9, 85.0, 56.8];
        let currentChart = null;

        document.addEventListener("DOMContentLoaded", () => {
            if (localStorage.getItem('theme') === 'dark' || 
                (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
                document.documentElement.classList.add('dark');
                updateThemeIcon(true);
            } else {
                document.documentElement.classList.remove('dark');
                updateThemeIcon(false);
            }
            
            renderChart();
            initTab3Charts();
        });

        function toggleDarkMode() {
            const isDark = document.documentElement.classList.toggle('dark');
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
            updateThemeIcon(isDark);
            
            if (currentChart) {
                currentChart.destroy();
            }
            renderChart();
            initTab3Charts();
        }

        function updateThemeIcon(isDark) {
            const icon = document.getElementById("theme-icon");
            if (isDark) {
                icon.className = "fas fa-sun text-amber-400";
            } else {
                icon.className = "fas fa-moon text-indigo-500";
            }
        }

        function switchTab(tabId) {
            const kpiTab = document.getElementById("tab-kpi-container");
            const predTab = document.getElementById("tab-predictions-container");
            const logsTab = document.getElementById("tab-daily-logs-container");
            const btnKpi = document.getElementById("btn-tab-kpi");
            const btnPred = document.getElementById("btn-tab-predictions");
            const btnLogs = document.getElementById("btn-tab-daily-logs");
            
            kpiTab.classList.add("hidden");
            predTab.classList.add("hidden");
            logsTab.classList.add("hidden");
            btnKpi.classList.remove("active-tab-btn");
            btnPred.classList.remove("active-tab-btn");
            btnLogs.classList.remove("active-tab-btn");
            
            if (tabId === "tab-kpi") {
                kpiTab.classList.remove("hidden");
                btnKpi.classList.add("active-tab-btn");
            } else if (tabId === "tab-predictions") {
                predTab.classList.remove("hidden");
                btnPred.classList.add("active-tab-btn");
                setTimeout(() => {
                    if (currentChart) currentChart.resize();
                }, 50);
            } else if (tabId === "tab-daily-logs") {
                logsTab.classList.remove("hidden");
                btnLogs.classList.add("active-tab-btn");
                setTimeout(() => {
                    if (typeof taskStatusChart !== 'undefined') taskStatusChart.resize();
                    if (typeof monthlyPerformanceChart !== 'undefined') monthlyPerformanceChart.resize();
                }, 50);
            }
        }

        function toggleCareList(rowId) {
            const row = document.getElementById(rowId);
            const icon = document.getElementById("icon-" + rowId);
            
            if (row.classList.contains("hidden")) {
                row.classList.remove("hidden");
                if (icon) icon.classList.add("rotate-180");
            } else {
                row.classList.add("hidden");
                if (icon) icon.classList.remove("rotate-180");
            }
        }

        function applyFilters() {
            const searchVal = document.getElementById("search-class").value.trim().toLowerCase();
            const batchVal = document.getElementById("filter-batch").value;
            const riskVal = document.getElementById("filter-risk").value;
            
            const rows = document.querySelectorAll(".class-row");
            rows.forEach(row => {
                const className = row.getAttribute("data-class-name").toLowerCase();
                const batch = row.getAttribute("data-batch").toUpperCase();
                const risk = row.getAttribute("data-risk-level");
                const accordionId = row.getAttribute("data-accordion-id");
                
                const matchSearch = className.includes(searchVal);
                const matchBatch = (batchVal === "ALL" || batch === batchVal.toUpperCase());
                const matchRisk = (riskVal === "ALL" || risk === riskVal);
                
                const accordionRow = accordionId ? document.getElementById(accordionId) : null;
                
                if (matchSearch && matchBatch && matchRisk) {
                    row.classList.remove("hidden");
                } else {
                    row.classList.add("hidden");
                    if (accordionRow) {
                        accordionRow.classList.add("hidden");
                        const icon = document.getElementById("icon-" + accordionId);
                        if (icon) icon.classList.remove("rotate-180");
                    }
                }
            });
        }

        function exportCareListCSV() {
            if (!predictionsRawData || !predictionsRawData.care_list) {
                alert("Không có dữ liệu Care List để xuất!");
                return;
            }
            
            let csvContent = "\uFEFF"; // BOM chống lỗi tiếng Việt trong Excel
            csvContent += "Lớp,Mã SV,Họ và tên,Chuyên cần vắng (%),Bài tập nợ (%),L LMS vi phạm (bài),Xác suất đỗ (%),Nguy cơ,Lý do\n";
            
            predictionsRawData.care_list.forEach(s => {
                const reasons = s.reasons.join(" | ");
                const riskLabel = s.risk_level === "RED" ? "Đỏ - Cao" : "Vàng - Vừa";
                csvContent += `"${s.class_name}","${s.student_id}","${s.full_name}",${s.att.toFixed(1)},${(100.0 - s.hw).toFixed(1)},${s.el},${s.p_final.toFixed(1)},"${riskLabel}","${reasons}"\n`;
            });
            
            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const url = URL.createObjectURL(blob);
            const link = document.createElement("a");
            link.setAttribute("href", url);
            link.setAttribute("download", `care_list_${new Date().toISOString().slice(0,10)}.csv`);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }

        function exportKPICSV() {
            const table = document.querySelector(".tab-1-container table");
            if (!table) {
                alert("Không tìm thấy bảng KPI để xuất!");
                return;
            }
            
            let csvContent = "\uFEFF"; // BOM UTF-8
            const rows = table.querySelectorAll("tr");
            
            rows.forEach((row, idx) => {
                if (idx === 0) {
                    // Dòng tiêu đề
                    const cols = row.querySelectorAll("th");
                    const rowData = [];
                    cols.forEach(col => {
                        rowData.push(`"${col.textContent.trim().replace(/"/g, '""')}"`);
                    });
                    csvContent += rowData.join(",") + "\n";
                    return;
                }
                const cols = row.querySelectorAll("td");
                const rowData = [];
                cols.forEach(col => {
                    let text = col.textContent.replace(/\s+/g, ' ').trim();
                    text = text.replaceAll("[[", "").replaceAll("]]", "");
                    rowData.push(`"${text.replace(/"/g, '""')}"`);
                });
                csvContent += rowData.join(",") + "\n";
            });
            
            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const url = URL.createObjectURL(blob);
            const link = document.createElement("a");
            link.setAttribute("href", url);
            link.setAttribute("download", `kpi_gv_tg_${new Date().toISOString().slice(0,10)}.csv`);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }

        function renderChart() {
            const isDark = document.documentElement.classList.contains('dark');
            const textColor = isDark ? '#94a3b8' : '#64748b';
            const gridColor = isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.04)';
            
            const ctx = document.getElementById('passRateChart').getContext('2d');
            currentChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: chartLabels,
                    datasets: [
                        {
                            label: 'Dự báo tỉ lệ đỗ',
                            data: chartPredData,
                            backgroundColor: 'rgba(99, 102, 241, 0.75)',
                            borderColor: 'rgba(99, 102, 241, 1)',
                            borderWidth: 1.5,
                            borderRadius: 6,
                            barPercentage: 0.85,
                            categoryPercentage: 0.75
                        },
                        {
                            label: 'Thực tế qua môn (DB)',
                            data: chartActualData,
                            backgroundColor: 'rgba(16, 185, 129, 0.75)',
                            borderColor: 'rgba(16, 185, 129, 1)',
                            borderWidth: 1.5,
                            borderRadius: 6,
                            barPercentage: 0.85,
                            categoryPercentage: 0.75
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            labels: {
                                color: textColor,
                                font: {
                                    family: 'Inter',
                                    weight: 'bold',
                                    size: 11
                                }
                            }
                        },
                        tooltip: {
                            padding: 12,
                            cornerRadius: 12,
                            bodyFont: { family: 'Inter' },
                            titleFont: { family: 'Inter', weight: 'bold' }
                        }
                    },
                    scales: {
                        x: {
                            grid: {
                                display: false
                            },
                            ticks: {
                                color: textColor,
                                font: {
                                    family: 'Inter',
                                    size: 10,
                                    weight: '500'
                                }
                            }
                        },
                        y: {
                            min: 0,
                            max: 100,
                            grid: {
                                color: gridColor
                            },
                            ticks: {
                                color: textColor,
                                callback: function(value) { return value + '%'; },
                                font: {
                                    family: 'Inter',
                                    size: 10
                                }
                            }
                        }
                    }
                }
            });
        }
        
        /* Tab 3 JavaScript code (Agent 4) */
        
        // Dữ liệu cho biểu đồ Tab 3
        const tab3StaffScores = [{"name": "Bùi Thanh Hải", "group": "Khối CNTT - Cơ sở HN (KS24)", "score": 100.0}, {"name": "Nguyễn Huyền Trang", "group": "Khối Quản lý Đào tạo (QLĐT)", "score": 100.0}, {"name": "Nguyễn Ngọc Vân Khanh", "group": "Khối QTKD", "score": 99.0}, {"name": "Trần Thị Mỹ Phước", "group": "Khối Quản lý Đào tạo (QLĐT)", "score": 99.0}, {"name": "Nguyễn Thị Hồng Minh", "group": "Khối QTKD", "score": 98.8}, {"name": "Hoàng Thị Kim Oanh", "group": "Khối QTKD", "score": 98.5}, {"name": "Hoàng Thị Hậu", "group": "Khối QTKD", "score": 96.4}, {"name": "Lâm Tùng Dương", "group": "Khối CNTT - Cơ sở HN (KS25)", "score": 94.8}, {"name": "Giáp Thị Minh Hằng", "group": "Khối Ngoại ngữ - Kỹ năng mềm", "score": 93.3}, {"name": "Đặng Quỳnh Trang", "group": "Khối QTKD", "score": 91.0}, {"name": "Lê Hà Thanh Sang", "group": "Khối CNTT - Cơ sở HCM", "score": 88.0}, {"name": "Phạm Ngọc Kiên", "group": "Khối CNTT - Cơ sở HCM", "score": 88.0}, {"name": "Nguyễn Quảng An", "group": "Khối CNTT - Cơ sở HCM", "score": 87.0}, {"name": "Trần Quốc Tuấn", "group": "Khối CNTT - Cơ sở HN (KS24)", "score": 86.0}, {"name": "Ngô Quang Huấn", "group": "Khối Ngoại ngữ - Kỹ năng mềm", "score": 84.7}, {"name": "Nguyễn Xuân Bách", "group": "Khối Quản lý Đào tạo (QLĐT)", "score": 84.0}, {"name": "Lê Thị Đỏ", "group": "Khối Ngoại ngữ - Kỹ năng mềm", "score": 81.6}, {"name": "Nguyễn Thị Tươi", "group": "Khối Quản lý Đào tạo (QLĐT)", "score": 79.8}, {"name": "Lại Trung Lâm", "group": "Khối QTKD", "score": 78.0}, {"name": "Phạm Viết Hùng", "group": "Khối CNTT - Cơ sở HN (KS24)", "score": 78.0}, {"name": "Lương Quốc Tuấn", "group": "Khối CNTT - Cơ sở HN (KS25)", "score": 74.3}, {"name": "Phạm Tuấn Bình", "group": "Khối QTKD", "score": 71.7}, {"name": "Trịnh Quốc Hai", "group": "Khối CNTT - Cơ sở HN (KS25)", "score": 71.0}, {"name": "Lê Thành Ngọc", "group": "Khối CNTT - Cơ sở HN (KS24)", "score": 68.0}, {"name": "Lò Thị Ngọc Anh", "group": "Khối Ngoại ngữ - Kỹ năng mềm", "score": 65.9}, {"name": "Ngọ Văn Quý", "group": "Khối CNTT - Cơ sở HN (KS25)", "score": 64.0}, {"name": "Nguyễn Bá Minh Đạo", "group": "Khối CNTT - Cơ sở HN (KS25)", "score": 64.0}];
        const tab3MissingTrend = [{"date": "01/07", "count": 16}, {"date": "02/07", "count": 16}, {"date": "03/07", "count": 14}, {"date": "06/07", "count": 10}, {"date": "07/07", "count": 13}, {"date": "08/07", "count": 10}, {"date": "09/07", "count": 7}, {"date": "10/07", "count": 8}, {"date": "13/07", "count": 4}, {"date": "14/07", "count": 3}];
        
        let taskStatusChart = null;
        let monthlyPerformanceChart = null;
        let missingLogsTrendChart = null;
        
        function initTab3Charts() {
            const isDark = document.documentElement.classList.contains('dark');
            const textColor = isDark ? '#94a3b8' : '#64748b';
            const gridColor = isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.04)';
            
            // 1. Doughnut Chart
            const canvasTask = document.getElementById('taskStatusChart');
            if (canvasTask) {
                const ctxTask = canvasTask.getContext('2d');
                if (taskStatusChart) taskStatusChart.destroy();
                taskStatusChart = new Chart(ctxTask, {
                    type: 'doughnut',
                    data: {
                        labels: ['Hoàn thành', 'Chờ duyệt', 'Chưa làm/Đang làm', 'Đã Hủy'],
                        datasets: [{
                            data: [238, 9, 119, 1],
                            backgroundColor: ['#10b981', '#818cf8', '#f59e0b', '#9ca3af'],
                            borderWidth: 1,
                            borderColor: isDark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.05)'
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                position: 'bottom',
                                labels: {
                                    color: textColor,
                                    font: { family: 'Inter', size: 10, weight: 'bold' }
                                }
                            }
                        }
                    }
                });
            }
            
            // 2. Cập nhật các biểu đồ phần Tháng
            updateMonthlyCharts('ALL');
        }
        
        function updateMonthlyCharts(groupFilter) {
            const isDark = document.documentElement.classList.contains('dark');
            const textColor = isDark ? '#94a3b8' : '#64748b';
            const gridColor = isDark ? 'rgba(255,255,255,0.06)' : 'rgba(0,0,0,0.04)';
            
            // Lọc dữ liệu nhân sự theo group
            const filteredStaff = tab3StaffScores.filter(s => {
                if (groupFilter === 'ALL') return true;
                if (groupFilter === 'HN-KS25') return s.group.includes('KS25');
                if (groupFilter === 'HN-KS24') return s.group.includes('KS24');
                if (groupFilter === 'HCM') return s.group.includes('HCM');
                if (groupFilter === 'Ngoại ngữ') return s.group.includes('Ngoại ngữ');
                if (groupFilter === 'QLĐT') return s.group.includes('QLĐT');
                return s.group === groupFilter;
            });
            
            // Chỉ lấy top 5 điểm cao nhất sau khi lọc
            const displayStaff = filteredStaff.slice(0, 5);
            const labels = displayStaff.map(s => s.name);
            const scores = displayStaff.map(s => s.score);
            
            const canvasMonthly = document.getElementById('monthlyPerformanceChart');
            if (canvasMonthly) {
                const ctxMonthly = canvasMonthly.getContext('2d');
                if (monthlyPerformanceChart) monthlyPerformanceChart.destroy();
                monthlyPerformanceChart = new Chart(ctxMonthly, {
                    type: 'bar',
                    data: {
                        labels: labels,
                        datasets: [{
                            data: scores,
                            backgroundColor: scores.map(s => s >= 85 ? '#10b981' : s >= 70 ? '#6366f1' : s >= 50 ? '#f59e0b' : '#ef4444'),
                            borderRadius: 6,
                            borderWidth: 0
                        }]
                    },
                    options: {
                        indexAxis: 'y',
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { display: false },
                            tooltip: {
                                callbacks: {
                                    label: function(context) { return 'Work Score: ' + context.raw.toFixed(1) + '/100'; }
                                }
                            }
                        },
                        scales: {
                            x: {
                                min: 0,
                                max: 100,
                                grid: { color: gridColor },
                                ticks: { color: textColor }
                            },
                            y: {
                                grid: { display: false },
                                ticks: { color: textColor, font: { family: 'Inter', size: 9 } }
                            }
                        }
                    }
                });
            }
            
            // 3. Biểu đồ đường xu hướng vắng báo cáo
            const trendLabels = tab3MissingTrend.map(t => t.date);
            const trendCounts = tab3MissingTrend.map(t => t.count);
            
            const canvasTrend = document.getElementById('missingLogsTrendChart');
            if (canvasTrend) {
                const ctxTrend = canvasTrend.getContext('2d');
                if (missingLogsTrendChart) missingLogsTrendChart.destroy();
                missingLogsTrendChart = new Chart(ctxTrend, {
                    type: 'line',
                    data: {
                        labels: trendLabels,
                        datasets: [{
                            label: 'Số ca thiếu báo cáo',
                            data: trendCounts,
                            borderColor: '#ef4444',
                            backgroundColor: 'rgba(239, 68, 68, 0.1)',
                            borderWidth: 2,
                            tension: 0.3,
                            fill: true,
                            pointBackgroundColor: '#ef4444',
                            pointBorderColor: '#fff',
                            pointBorderWidth: 1.5,
                            pointRadius: 3
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { display: false },
                            tooltip: {
                                padding: 10,
                                cornerRadius: 8
                            }
                        },
                        scales: {
                            x: {
                                grid: { display: false },
                                ticks: { color: textColor, font: { size: 8 } }
                            },
                            y: {
                                min: 0,
                                grid: { color: gridColor },
                                ticks: { color: textColor, stepSize: 1 }
                            }
                        }
                    }
                });
            }
        }
        
        // Điều khiển tương tác Tab 3
        var currentSubTabLogs = 'weekly';
        var currentGroupFilterLogs = 'ALL';
        
        function switchViewModeLogs(evt, mode) {
            currentSubTabLogs = mode;
            
            document.getElementById("view-weekly").classList.toggle("hidden", mode !== 'weekly');
            document.getElementById("view-monthly").classList.toggle("hidden", mode !== 'monthly');
            
            document.getElementById("panel-chart-weekly").classList.toggle("hidden", mode !== 'weekly');
            document.getElementById("panel-charts-monthly").classList.toggle("hidden", mode !== 'monthly');
            
            const btnWeekly = document.getElementById("btn-logs-weekly");
            const btnMonthly = document.getElementById("btn-logs-monthly");
            
            if (mode === 'weekly') {
                btnWeekly.className = "px-4 py-1.5 rounded-lg text-xs font-bold text-slate-500 dark:text-slate-400 hover:text-indigo-600 dark:hover:text-indigo-400 bg-white dark:bg-slate-900 shadow-sm border border-slate-200/40 dark:border-slate-700/60";
                btnMonthly.className = "px-4 py-1.5 rounded-lg text-xs font-bold text-slate-500 dark:text-slate-400 hover:text-indigo-600 dark:hover:text-indigo-400";
            } else {
                btnMonthly.className = "px-4 py-1.5 rounded-lg text-xs font-bold text-slate-500 dark:text-slate-400 hover:text-indigo-600 dark:hover:text-indigo-400 bg-white dark:bg-slate-900 shadow-sm border border-slate-200/40 dark:border-slate-700/60";
                btnWeekly.className = "px-4 py-1.5 rounded-lg text-xs font-bold text-slate-500 dark:text-slate-400 hover:text-indigo-600 dark:hover:text-indigo-400";
            }
            
            applyFiltersLogs();
            
            setTimeout(() => {
                if (taskStatusChart) taskStatusChart.resize();
                if (monthlyPerformanceChart) monthlyPerformanceChart.resize();
                if (missingLogsTrendChart) missingLogsTrendChart.resize();
            }, 50);
        }
        
        function filterGroupLogs(evt, group) {
            currentGroupFilterLogs = group;
            
            const buttons = evt.currentTarget.parentNode.getElementsByClassName("filter-btn-logs");
            for (let i = 0; i < buttons.length; i++) {
                buttons[i].className = "filter-btn-logs px-3.5 py-2 rounded-xl text-xs font-bold border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 text-slate-600 dark:text-slate-400 hover:border-indigo-500 dark:hover:border-indigo-400";
            }
            evt.currentTarget.className = "filter-btn-logs px-3.5 py-2 rounded-xl text-xs font-bold border bg-indigo-500 border-indigo-500 text-white hover:bg-indigo-600 shadow-sm";
            
            updateMonthlyCharts(group);
            applyFiltersLogs();
        }
        
        function applyFiltersLogs() {
            const searchVal = document.getElementById("log-search").value.trim().toLowerCase();
            const activeContainerId = "view-" + currentSubTabLogs;
            const activeContainer = document.getElementById(activeContainerId);
            
            const rows = activeContainer.querySelectorAll(".log-row");
            rows.forEach(row => {
                const group = row.getAttribute("data-group");
                const name = row.getAttribute("data-name");
                
                const matchesGroup = (currentGroupFilterLogs === 'ALL' || 
                                     (currentGroupFilterLogs === 'Khối QTKD' && group === 'Khối QTKD') ||
                                     (currentGroupFilterLogs === 'HN-KS25' && group.includes('KS25')) ||
                                     (currentGroupFilterLogs === 'HN-KS24' && group.includes('KS24')) ||
                                     (currentGroupFilterLogs === 'HCM' && group.includes('HCM')) ||
                                     (currentGroupFilterLogs === 'Ngoại ngữ' && group.includes('Ngoại ngữ')) ||
                                     (currentGroupFilterLogs === 'QLĐT' && group.includes('QLĐT')));
                                     
                const matchesSearch = name.includes(searchVal);
                
                row.style.display = (matchesGroup && matchesSearch) ? "" : "none";
            });
        }
    
    