from collections import defaultdict


def _safe_mean(lst):
    """Return mean of a list, or None if empty."""
    valid = [x for x in lst if x is not None]
    return round(sum(valid) / len(valid), 2) if valid else None


def get_class_action_plan(cc, bt, el):
    plans = []
    if cc is not None and cc > 15.0:
        plans.append("1. Giảng viên điểm danh nghiêm ngặt đầu và giữa giờ. 2. CTSV gọi điện khẩn cấp cho học viên/phụ huynh ngay sau ca học. 3. TA lập danh sách gửi PM cảnh báo nghỉ học.")
    if bt is not None and bt > 15.0:
        plans.append("1. TA bắt buộc mở ca phụ đạo 1-1 tăng cường cho nhóm nợ bài. 2. Giảng viên dành 10 phút đầu giờ kiểm tra ngẫu nhiên code của học viên và chữa bài chi tiết.")
    if el is not None and el > 15.0:
        plans.append("1. Giảng viên tóm tắt nhanh kiến thức Elearning trong 10 phút đầu giờ. 2. TA nhắc nhở học viên hoàn thành Elearning trước ca học tối thiểu 2 giờ.")
    
    if not plans:
        return "Duy trì quy trình kiểm soát hiện tại. Tiếp tục khích lệ tinh thần tự học của lớp."
    return " <br> ".join(plans)


def get_class_metrics(class_course_map):
    """
    For each class, compute all metrics needed for Screen 1 and Screen 2.

    Returns dict[class_name -> metrics_dict]:
        current_course_name: str   — name of current course sheet
        current_teacher:     str
        prev_course_name:    str | None
        prev_teacher:        str | None
        all_courses:         list of (sheet, teacher) tuples
        curr_cc_avg:         float | None — mean CC% across entire current course
        curr_bt_avg:         float | None
        curr_el_avg:         float | None
        prev_cc_avg:         float | None — mean CC% across entire prev course
        prev_bt_avg:         float | None
        daily_latest_cc:     float | None — CC% on the last recorded day
        daily_latest_bt:     float | None
        daily_latest_el:     float | None
        daily_latest_date:   date  | None
        weekly_current:      (cc, bt, el) means for the latest calendar week | None
        weekly_prev_wk:      (cc, bt, el) means for the week before that  | None
        delta_cc:            float | None — positive = violation decreased (improved)
        delta_bt:            float | None
        is_first_course:     bool
    """
    results = {}

    for cname, courses in class_course_map.items():
        curr = courses[-1]
        prev = courses[-2] if len(courses) >= 2 else None

        # ── Latest recorded day ──
        daily_latest_cc = daily_latest_bt = daily_latest_el = None
        daily_latest_date = None
        if curr['daily']:
            last = curr['daily'][-1]
            daily_latest_date = last[0]
            daily_latest_cc   = last[1]
            daily_latest_bt   = last[2]
            daily_latest_el   = last[3]

        # ── Group current course data by ISO calendar week ──
        week_groups = defaultdict(lambda: {'cc': [], 'bt': [], 'el': []})
        for d, cc, bt, el in curr['daily']:
            wk = d.isocalendar()[1]
            if cc is not None: week_groups[wk]['cc'].append(cc)
            if bt is not None: week_groups[wk]['bt'].append(bt)
            if el is not None: week_groups[wk]['el'].append(el)

        sorted_weeks = sorted(week_groups.keys())
        weekly_current = weekly_prev_wk = None
        if sorted_weeks:
            g = week_groups[sorted_weeks[-1]]
            weekly_current = (
                _safe_mean(g['cc']),
                _safe_mean(g['bt']),
                _safe_mean(g['el'])
            )
            if len(sorted_weeks) >= 2:
                g2 = week_groups[sorted_weeks[-2]]
                weekly_prev_wk = (
                    _safe_mean(g2['cc']),
                    _safe_mean(g2['bt']),
                    _safe_mean(g2['el'])
                )

        # ── Course-level averages ──
        curr_cc_avg = _safe_mean(curr['cc_all'])
        curr_bt_avg = _safe_mean(curr['bt_all'])
        curr_el_avg = _safe_mean(curr['el_all'])

        prev_cc_avg = _safe_mean(prev['cc_all']) if prev else None
        prev_bt_avg = _safe_mean(prev['bt_all']) if prev else None

        # ── Delta (positive = improvement, violations went DOWN) ──
        delta_cc = delta_bt = delta_el = None
        if prev_cc_avg is not None and curr_cc_avg is not None:
            delta_cc = round(prev_cc_avg - curr_cc_avg, 2)
        if prev_bt_avg is not None and curr_bt_avg is not None:
            delta_bt = round(prev_bt_avg - curr_bt_avg, 2)
        if prev and curr_el_avg is not None:
            prev_el_avg = _safe_mean(prev['el_all'])
            if prev_el_avg is not None:
                delta_el = round(prev_el_avg - curr_el_avg, 2)

        action_plan = get_class_action_plan(curr_cc_avg, curr_bt_avg, curr_el_avg)

        results[cname] = {
            'current_course_name': curr['sheet'],
            'current_teacher':     curr['teacher'],
            'ta':                  curr.get('ta', 'Không có'),
            'class_size':          curr.get('class_size', 0),
            'prev_course_name':    prev['sheet'] if prev else None,
            'prev_teacher':        prev['teacher'] if prev else None,
            'all_courses':         [(c['sheet'], c['teacher'], c.get('ta', 'Không có')) for c in courses],
            'curr_cc_avg':         curr_cc_avg,
            'curr_bt_avg':         curr_bt_avg,
            'curr_el_avg':         curr_el_avg,
            'prev_cc_avg':         prev_cc_avg,
            'prev_bt_avg':         prev_bt_avg,
            'daily_latest_cc':     daily_latest_cc,
            'daily_latest_bt':     daily_latest_bt,
            'daily_latest_el':     daily_latest_el,
            'daily_latest_date':   daily_latest_date,
            'weekly_current':      weekly_current,
            'weekly_prev_wk':      weekly_prev_wk,
            'delta_cc':            delta_cc,
            'delta_bt':            delta_bt,
            'delta_el':            delta_el,
            'is_first_course':     prev is None,
            'action_plan':         action_plan,
        }

    return results


# ── Quadrant thresholds (calibrated from actual Excel data) ──
STAR_CC_MAX     = 18.0   # avg CC% for current course
STAR_BT_MAX     = 12.0   # avg BT% for current course
STAR_DELTA_MIN  = -3.0   # minimum acceptable delta (not declining badly)

RESCUER_DELTA_CC_MIN = 5.0   # big improvement in CC
RESCUER_DELTA_BT_MIN = 5.0   # big improvement in BT

NEEDS_CC_MIN    = 20.0   # high current CC% → concern (v3 updated to 20)
NEEDS_BT_MIN    = 15.0   # high current BT% → concern (v3 updated to 15)
NEEDS_EL_MIN    = 20.0   # high current EL% → concern (v3 updated to 20)
NEEDS_DELTA_MIN = -3.0   # delta worse than this → concern (v3 updated to -3)


def _classify_quadrant(avg_cc, avg_bt, avg_el, avg_delta_cc, avg_delta_bt, avg_delta_el):
    """Return tuple (quadrant, weighted_delta)"""
    d_cc = avg_delta_cc if avg_delta_cc is not None else 0.0
    d_bt = avg_delta_bt if avg_delta_bt is not None else 0.0
    d_el = avg_delta_el if avg_delta_el is not None else 0.0
    weighted_delta = round(0.4 * d_cc + 0.4 * d_bt + 0.2 * d_el, 2)

    # Rescuers: Weighted Delta >= 5% hoặc bất kỳ Delta đơn lẻ nào >= 5%
    is_rescuer = (
        weighted_delta >= 5.0 or
        (avg_delta_cc is not None and avg_delta_cc >= 5.0) or
        (avg_delta_bt is not None and avg_delta_bt >= 5.0) or
        (avg_delta_el is not None and avg_delta_el >= 5.0)
    )

    # Needs Support: Vi phạm hiện tại cao ĐỒNG THỜI Weighted Delta <= 0, HOẶC bất kỳ Delta đơn lẻ nào < -3%
    has_high_violation = (
        (avg_cc is not None and avg_cc > NEEDS_CC_MIN) or
        (avg_bt is not None and avg_bt > NEEDS_BT_MIN) or
        (avg_el is not None and avg_el > NEEDS_EL_MIN)
    )
    has_severe_decline = (
        (avg_delta_cc is not None and avg_delta_cc < NEEDS_DELTA_MIN) or
        (avg_delta_bt is not None and avg_delta_bt < NEEDS_DELTA_MIN) or
        (avg_delta_el is not None and avg_delta_el < NEEDS_DELTA_MIN)
    )

    is_needs_support = (
        not is_rescuer and
        (
            (has_high_violation and weighted_delta <= 0) or
            has_severe_decline
        )
    )

    if is_rescuer:
        return 'Rescuers', weighted_delta
    if is_needs_support:
        return 'Needs Support', weighted_delta
    return 'Maintainers', weighted_delta


def get_teacher_metrics(class_metrics):
    """
    Aggregate class_metrics by current teacher/TA.

    Returns dict[name -> teacher_dict]:
        role:              'Giảng viên' | 'Trợ giảng'
        classes:           list of class names they teach right now
        class_details:     list of per-class breakdown dicts
        avg_curr_cc:       float | None
        avg_curr_bt:       float | None
        avg_curr_el:       float | None
        avg_delta_cc:      float | None
        avg_delta_bt:      float | None
        weighted_delta:    float | None
        quadrant:          'Rescuers' | 'Maintainers' | 'Needs Support'
        ai_recommendation: str
    """
    teacher_buckets = defaultdict(lambda: {
        'role':           None,
        'classes':        [],
        'class_details':  [],
        'curr_cc_list':   [],
        'curr_bt_list':   [],
        'curr_el_list':   [],
        'delta_cc_list':  [],
        'delta_bt_list':  [],
        'delta_el_list':  [],
    })

    # 1. Identify all main teachers (Lecturers)
    lecturers = set()
    for m in class_metrics.values():
        t = m['current_teacher']
        if t and t not in ('Chưa phân công', 'None', ''):
            lecturers.add(t)

    # 2. Populate buckets for both main teachers and TAs
    for cname, m in class_metrics.items():
        teacher = m['current_teacher']
        ta = m['ta']

        # Add as Lecturer
        if teacher and teacher not in ('Chưa phân công', 'None', ''):
            tb = teacher_buckets[teacher]
            tb['role'] = 'Giảng viên'
            tb['classes'].append(cname)
            tb['class_details'].append({
                'class_name':       cname,
                'course':           m['current_course_name'],
                'prev_course':      m['prev_course_name'],
                'prev_teacher':     m['prev_teacher'],
                'curr_cc_avg':      m['curr_cc_avg'],
                'curr_bt_avg':      m['curr_bt_avg'],
                'curr_el_avg':      m['curr_el_avg'],
                'prev_cc_avg':      m['prev_cc_avg'],
                'prev_bt_avg':      m['prev_bt_avg'],
                'delta_cc':         m['delta_cc'],
                'delta_bt':         m['delta_bt'],
                'delta_el':         m['delta_el'],
                'daily_latest_cc':  m['daily_latest_cc'],
                'daily_latest_bt':  m['daily_latest_bt'],
                'daily_latest_el':  m['daily_latest_el'],
                'daily_latest_date': str(m['daily_latest_date']) if m['daily_latest_date'] else None,
                'is_first_course':  m['is_first_course'],
                'class_size':       m['class_size'],
                'ta':               ta,
                'action_plan':      m['action_plan'],
            })
            if m['curr_cc_avg'] is not None:
                tb['curr_cc_list'].append(m['curr_cc_avg'])
            if m['curr_bt_avg'] is not None:
                tb['curr_bt_list'].append(m['curr_bt_avg'])
            if m['curr_el_avg'] is not None:
                tb['curr_el_list'].append(m['curr_el_avg'])
            if m['delta_cc'] is not None:
                tb['delta_cc_list'].append(m['delta_cc'])
            if m['delta_bt'] is not None:
                tb['delta_bt_list'].append(m['delta_bt'])
            if m['delta_el'] is not None:
                tb['delta_el_list'].append(m['delta_el'])

        # Add as TA (if they are not a main teacher in any class)
        if ta and ta not in ('Không có', 'None', ''):
            if ta not in lecturers:
                tb = teacher_buckets[ta]
                tb['role'] = 'Trợ giảng'
                tb['classes'].append(cname)
                tb['class_details'].append({
                    'class_name':       cname,
                    'course':           m['current_course_name'],
                    'prev_course':      m['prev_course_name'],
                    'prev_teacher':     m['prev_teacher'],
                    'curr_cc_avg':      m['curr_cc_avg'],
                    'curr_bt_avg':      m['curr_bt_avg'],
                    'curr_el_avg':      m['curr_el_avg'],
                    'prev_cc_avg':      m['prev_cc_avg'],
                    'prev_bt_avg':      m['prev_bt_avg'],
                    'delta_cc':         m['delta_cc'],
                    'delta_bt':         m['delta_bt'],
                    'delta_el':         m['delta_el'],
                    'daily_latest_cc':  m['daily_latest_cc'],
                    'daily_latest_bt':  m['daily_latest_bt'],
                    'daily_latest_el':  m['daily_latest_el'],
                    'daily_latest_date': str(m['daily_latest_date']) if m['daily_latest_date'] else None,
                    'is_first_course':  m['is_first_course'],
                    'class_size':       m['class_size'],
                    'ta':               ta,
                    'action_plan':      m['action_plan'],
                })
                if m['curr_cc_avg'] is not None:
                    tb['curr_cc_list'].append(m['curr_cc_avg'])
                if m['curr_bt_avg'] is not None:
                    tb['curr_bt_list'].append(m['curr_bt_avg'])
                if m['curr_el_avg'] is not None:
                    tb['curr_el_list'].append(m['curr_el_avg'])
                if m['delta_cc'] is not None:
                    tb['delta_cc_list'].append(m['delta_cc'])
                if m['delta_bt'] is not None:
                    tb['delta_bt_list'].append(m['delta_bt'])
                if m['delta_el'] is not None:
                    tb['delta_el_list'].append(m['delta_el'])

    teacher_results = {}
    for name, tb in teacher_buckets.items():
        avg_cc       = _safe_mean(tb['curr_cc_list'])
        avg_bt       = _safe_mean(tb['curr_bt_list'])
        avg_el       = _safe_mean(tb['curr_el_list'])
        avg_delta_cc = _safe_mean(tb['delta_cc_list'])
        avg_delta_bt = _safe_mean(tb['delta_bt_list'])
        avg_delta_el = _safe_mean(tb['delta_el_list'])

        quadrant, weighted_delta = _classify_quadrant(avg_cc, avg_bt, avg_el, avg_delta_cc, avg_delta_bt, avg_delta_el)

        # AI recommendation text per quadrant
        rec_map = {
            'Rescuers':     "Có năng lực cảm hóa lớp khó — chỉ số vi phạm giảm mạnh so với môn trước. Ưu tiên phân công giải cứu các lớp đang báo động.",
            'Maintainers':  "Duy trì kỷ luật lớp ở mức ổn định. Tiếp tục theo dõi xu hướng qua các tuần tới.",
            'Needs Support':"Chỉ số vi phạm cao hoặc có dấu hiệu đi xuống so với môn trước. Cần PM và CTSV đồng hành hỗ trợ chấn chỉnh kỷ luật ngay.",
        }

        teacher_results[name] = {
            'role':              tb['role'],
            'classes':           tb['classes'],
            'class_details':     tb['class_details'],
            'avg_curr_cc':       avg_cc,
            'avg_curr_bt':       avg_bt,
            'avg_curr_el':       avg_el,
            'avg_delta_cc':      avg_delta_cc,
            'avg_delta_bt':      avg_delta_bt,
            'avg_delta_el':      avg_delta_el,
            'weighted_delta':    weighted_delta,
            'quadrant':          quadrant,
            'ai_recommendation': rec_map[quadrant],
        }

    return teacher_results

