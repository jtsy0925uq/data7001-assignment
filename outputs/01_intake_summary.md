# Social Media & Cognition — Dataset Intake Summary

> **Y** = Yes | **N** = No | **P** = Partial / Proxy

## Quick-Reference Relevance Table

| Dataset | Measures Usage? | Measures Attention? | Measures Performance? |
|---------|:--------------:|:------------------:|:--------------------:|
| `screen_time_attention_productivity.csv` | **Y** | **Y** | **Y** |
| `social_media_addiction_productivity.csv` | **Y** | **N** | **Y** |
| `student_social_media_academic_impact.csv` | **Y** | **N** | **Y** |
| `social_media_content_mental_fatigue.csv` | **Y** | **P** | **N** |
| `student_habits_exam_performance.csv` | **Y** | **N** | **Y** |
| `social_media_attention_mental_health_survey.csv` | **Y** | **Y** | **N** |

---

## screen_time_attention_productivity.csv

_Encoding detected: utf-8_

**Shape:** 200 rows × 16 columns


### Columns & Dtypes

| Column | dtype |
|--------|-------|
| `Unnamed: 0` | `int64` |
| `Age Group` | `str` |
| `Gender` | `str` |
| `Education Level` | `str` |
| `Occupation` | `str` |
| `Average Screen Time` | `str` |
| `Device` | `str` |
| `Screen Activity` | `str` |
| `App Category` | `str` |
| `Screen Time Period` | `str` |
| `Environment` | `str` |
| `Productivity` | `str` |
| `Attention Span` | `str` |
| `Work Strategy` | `str` |
| `Notification Handling` | `str` |
| `Usage of Productivity Apps` | `str` |



### Missing Values

| Column | Missing Count | Missing % |
|--------|:------------:|:---------:|
| `Environment` | 2 | 1.0% |
| `Work Strategy` | 3 | 1.5% |
| `Notification Handling` | 1 | 0.5% |


**Duplicate rows:** 0


### First 3 Rows

|   Unnamed: 0 | Age Group    | Gender   | Education Level   | Occupation   | Average Screen Time   | Device     | Screen Activity                                       | App Category                                                | Screen Time Period      | Environment                   | Productivity          | Attention Span   | Work Strategy                                 | Notification Handling                  | Usage of Productivity Apps               |
|-------------:|:-------------|:---------|:------------------|:-------------|:----------------------|:-----------|:------------------------------------------------------|:------------------------------------------------------------|:------------------------|:------------------------------|:----------------------|:-----------------|:----------------------------------------------|:---------------------------------------|:-----------------------------------------|
|            0 | 18–24        | Male     | Undergraduate     | Student      | More than 10          | Smartphone | Entertainment (gaming, streaming, social media, etc.) | Social Media (e.g., Facebook, Instagram, LinkedIn, Twitter) | Evening (6 PM–10 PM)    | Quite workplace               | Moderately productive | 10–30 minutes    | Take regular breaks                           | Check them briefly and resume my work  | Yes, but i did not find them of any help |
|            1 | 18–24        | Male     | Undergraduate     | Professional | 8-10                  | Smartphone | Entertainment (gaming, streaming, social media, etc.) | Streaming (e.g., YouTube, Netflix)                          | Late night (10 PM–6 AM) | Quite workplace               | Moderately productive | More than 1 hour | None, i prefer to work without any strategies | Ignore them until my task is completed | No, i do not use them                    |
|            2 | 45 and above | Female   | Graduate          | Professional | 4–6                   | Smartphone | Academic/Work-related                                 | Social Media (e.g., Facebook, Instagram, LinkedIn, Twitter) | Afternoon (12 PM–6 PM)  | I can work in any environment | Moderately productive | 10–30 minutes    | Take regular breaks                           | Check them briefly and resume my work  | No, i do not use them                    |


### Numeric Summary — describe()

|       |   Unnamed: 0 |
|:------|-------------:|
| count |      200     |
| mean  |       99.5   |
| std   |       57.879 |
| min   |        0     |
| 25%   |       49.75  |
| 50%   |       99.5   |
| 75%   |      149.25  |
| max   |      199     |


### Categorical Columns

**`Age Group`** — 5 unique values

| Value | Count | % |
|-------|------:|---:|
| 18–24 | 126 | 63.0% |
| Below 18 | 34 | 17.0% |
| 25–34 | 24 | 12.0% |
| 35–44 | 10 | 5.0% |
| 45 and above | 6 | 3.0% |

**`Gender`** — 2 unique values

| Value | Count | % |
|-------|------:|---:|
| Male | 132 | 66.0% |
| Female | 68 | 34.0% |

**`Education Level`** — 3 unique values

| Value | Count | % |
|-------|------:|---:|
| Undergraduate | 106 | 53.0% |
| Graduate | 47 | 23.5% |
| High school or below | 47 | 23.5% |

**`Occupation`** — 2 unique values

| Value | Count | % |
|-------|------:|---:|
| Student | 124 | 62.0% |
| Professional | 76 | 38.0% |

**`Average Screen Time`** — 6 unique values

| Value | Count | % |
|-------|------:|---:|
| 4–6 | 51 | 25.5% |
| 6–8 | 51 | 25.5% |
| 8-10 | 44 | 22.0% |
| More than 10 | 31 | 15.5% |
| 2–4 | 22 | 11.0% |
| Less than 2 | 1 | 0.5% |

**`Device`** — 4 unique values

| Value | Count | % |
|-------|------:|---:|
| Smartphone | 126 | 63.0% |
| Laptop/PC | 72 | 36.0% |
| Television | 1 | 0.5% |
| Tablet | 1 | 0.5% |

**`Screen Activity`** — 2 unique values

| Value | Count | % |
|-------|------:|---:|
| Entertainment (gaming, streaming, social media, etc.) | 112 | 56.0% |
| Academic/Work-related | 88 | 44.0% |

**`App Category`** — 5 unique values

| Value | Count | % |
|-------|------:|---:|
| Social Media (e.g., Facebook, Instagram, LinkedIn, Twitter) | 100 | 50.0% |
| Productivity (e.g., Microsoft Office, Notion) | 48 | 24.0% |
| Streaming (e.g., YouTube, Netflix) | 23 | 11.5% |
| Messaging (e.g., WhatsApp, Messenger) | 21 | 10.5% |
| Gaming | 8 | 4.0% |

**`Screen Time Period`** — 4 unique values

| Value | Count | % |
|-------|------:|---:|
| Evening (6 PM–10 PM) | 95 | 47.5% |
| Afternoon (12 PM–6 PM) | 50 | 25.0% |
| Late night (10 PM–6 AM) | 43 | 21.5% |
| Morning (6 AM–12 PM) | 12 | 6.0% |

**`Environment`** — 4 unique values

| Value | Count | % |
|-------|------:|---:|
| Quite workplace | 99 | 49.5% |
| I can work in any environment | 52 | 26.0% |
| Collaborative/team setting | 25 | 12.5% |
| Background noise/music | 22 | 11.0% |
| nan | 2 | 1.0% |

**`Productivity`** — 3 unique values

| Value | Count | % |
|-------|------:|---:|
| Moderately productive | 107 | 53.5% |
| Extremely productive, i efficiently complete my tasks | 55 | 27.5% |
| Unproductive, i might not have completed the task and got carried away | 38 | 19.0% |

**`Attention Span`** — 4 unique values

| Value | Count | % |
|-------|------:|---:|
| 10–30 minutes | 64 | 32.0% |
| 30–60 minutes | 53 | 26.5% |
| More than 1 hour | 48 | 24.0% |
| Less than 10 minutes | 35 | 17.5% |

**`Work Strategy`** — 4 unique values

| Value | Count | % |
|-------|------:|---:|
| None, i prefer to work without any strategies | 71 | 35.5% |
| Take regular breaks | 68 | 34.0% |
| Eliminate all distractions | 46 | 23.0% |
| Use some productivity tool (e.g, timers, blockers) | 12 | 6.0% |
| nan | 3 | 1.5% |

**`Notification Handling`** — 4 unique values

| Value | Count | % |
|-------|------:|---:|
| Check them briefly and resume my work | 72 | 36.0% |
| Turn off notifications altogether | 65 | 32.5% |
| Ignore them until my task is completed | 44 | 22.0% |
| Spend time interacting with the notifications | 18 | 9.0% |
| nan | 1 | 0.5% |

**`Usage of Productivity Apps`** — 3 unique values

| Value | Count | % |
|-------|------:|---:|
| No, i do not use them | 123 | 61.5% |
| Yes, they are extremely helpful | 44 | 22.0% |
| Yes, but i did not find them of any help | 33 | 16.5% |



### Relevance Assessment

| Question | Answer | Justification |
|----------|:------:|---------------|
| Measures social media **USAGE**? | **Y** | `avg_screen_time_hours`, `app_category`, `screen_time_period` |
| Measures **ATTENTION** / focus / distraction? | **Y** | `attention_span_duration` directly captures concentration duration |
| Measures **PRODUCTIVITY** / grades / academic performance? | **Y** | `productivity_level`, `work_strategy`, `uses_productivity_apps` |


---
## social_media_addiction_productivity.csv

_Encoding detected: utf-8_

**Shape:** 20 rows × 15 columns


### Columns & Dtypes

| Column | dtype |
|--------|-------|
| `User_ID` | `int64` |
| `Age` | `int64` |
| `Gender` | `str` |
| `Platform` | `str` |
| `Daily_Usage_Time_min` | `int64` |
| `Posts_Per_Day` | `int64` |
| `Likes_Received_Daily` | `int64` |
| `Comments_Received_Daily` | `int64` |
| `Messages_Sent_Daily` | `int64` |
| `Scroll_Rate_ppm` | `int64` |
| `Addiction_Level` | `str` |
| `Emotional_State_Post_Usage` | `str` |
| `Productivity_Loss_Score` | `int64` |
| `Mental_Health_Index` | `int64` |
| `FOMO_Score` | `int64` |



### Missing Values

_No missing values detected._

**Duplicate rows:** 0


### First 3 Rows

|   User_ID |   Age | Gender   | Platform   |   Daily_Usage_Time_min |   Posts_Per_Day |   Likes_Received_Daily |   Comments_Received_Daily |   Messages_Sent_Daily |   Scroll_Rate_ppm | Addiction_Level   | Emotional_State_Post_Usage   |   Productivity_Loss_Score |   Mental_Health_Index |   FOMO_Score |
|----------:|------:|:---------|:-----------|-----------------------:|----------------:|-----------------------:|--------------------------:|----------------------:|------------------:|:------------------|:-----------------------------|--------------------------:|----------------------:|-------------:|
|      1001 |    23 | Female   | Instagram  |                    145 |               3 |                    120 |                        25 |                    45 |                40 | High              | Anxious                      |                         7 |                    45 |            8 |
|      1002 |    19 | Male     | TikTok     |                    210 |               1 |                     45 |                         5 |                    10 |                85 | Severe            | Depressed                    |                         9 |                    30 |            9 |
|      1003 |    28 | Female   | LinkedIn   |                     45 |               0 |                      5 |                         2 |                    15 |                10 | Low               | Motivated                    |                         2 |                    80 |            3 |


### Numeric Summary — describe()

|       |   User_ID |    Age |   Daily_Usage_Time_min |   Posts_Per_Day |   Likes_Received_Daily |   Comments_Received_Daily |   Messages_Sent_Daily |   Scroll_Rate_ppm |   Productivity_Loss_Score |   Mental_Health_Index |   FOMO_Score |
|:------|----------:|-------:|-----------------------:|----------------:|-----------------------:|--------------------------:|----------------------:|------------------:|--------------------------:|----------------------:|-------------:|
| count |    20     | 20     |                 20     |           20    |                 20     |                    20     |                20     |            20     |                    20     |                 20    |       20     |
| mean  |  1010.5   | 26.5   |                132.5   |            3.35 |                 54.9   |                    14     |                45     |            34.5   |                     5.25  |                 56.75 |        5.7   |
| std   |     5.916 |  6.444 |                 77.111 |            4.44 |                 54.964 |                    16.157 |                71.451 |            26.453 |                     2.881 |                 19.62 |        2.557 |
| min   |  1001     | 18     |                 20     |            0    |                  1     |                     0     |                 0     |             5     |                     1     |                 25    |        2     |
| 25%   |  1005.75  | 21.75  |                 57.5   |            0    |                 13.75  |                     2     |                 8.75  |            10     |                     2.75  |                 40    |        3.75  |
| 50%   |  1010.5   | 25.5   |                137.5   |            1.5  |                 37.5   |                     9     |                22.5   |            27.5   |                     5     |                 57.5  |        5.5   |
| 75%   |  1015.25  | 30.25  |                182.5   |            4.25 |                 82.5   |                    21.25  |                41.25  |            50     |                     8     |                 71.25 |        8     |
| max   |  1020     | 40     |                300     |           15    |                200     |                    60     |               300     |            95     |                    10     |                 90    |       10     |


### Categorical Columns

**`Gender`** — 3 unique values

| Value | Count | % |
|-------|------:|---:|
| Female | 9 | 45.0% |
| Male | 9 | 45.0% |
| Non-binary | 2 | 10.0% |

**`Platform`** — 10 unique values

| Value | Count | % |
|-------|------:|---:|
| Instagram | 3 | 15.0% |
| TikTok | 3 | 15.0% |
| Facebook | 3 | 15.0% |
| LinkedIn | 2 | 10.0% |
| Twitter | 2 | 10.0% |
| YouTube | 2 | 10.0% |
| Snapchat | 2 | 10.0% |
| Pinterest | 1 | 5.0% |
| Reddit | 1 | 5.0% |
| Discord | 1 | 5.0% |

**`Addiction_Level`** — 4 unique values

| Value | Count | % |
|-------|------:|---:|
| High | 6 | 30.0% |
| Moderate | 6 | 30.0% |
| Low | 5 | 25.0% |
| Severe | 3 | 15.0% |

**`Emotional_State_Post_Usage`** — 17 unique values _(>15, showing 5 samples)_

Samples: `Anxious`, `Depressed`, `Motivated`, `Neutral`, `Stressed`



### Relevance Assessment

| Question | Answer | Justification |
|----------|:------:|---------------|
| Measures social media **USAGE**? | **Y** | `daily_usage_minutes`, `posts_per_day`, `scroll_rate_per_minute` |
| Measures **ATTENTION** / focus / distraction? | **N** | No direct attention/focus column; `fomo_score` is closest proxy |
| Measures **PRODUCTIVITY** / grades / academic performance? | **Y** | `productivity_loss_score` explicitly measures productivity impact |


---
## student_social_media_academic_impact.csv

_Encoding detected: utf-8_

**Shape:** 705 rows × 13 columns


### Columns & Dtypes

| Column | dtype |
|--------|-------|
| `Student_ID` | `int64` |
| `Age` | `int64` |
| `Gender` | `str` |
| `Academic_Level` | `str` |
| `Country` | `str` |
| `Avg_Daily_Usage_Hours` | `float64` |
| `Most_Used_Platform` | `str` |
| `Affects_Academic_Performance` | `str` |
| `Sleep_Hours_Per_Night` | `float64` |
| `Mental_Health_Score` | `int64` |
| `Relationship_Status` | `str` |
| `Conflicts_Over_Social_Media` | `int64` |
| `Addicted_Score` | `int64` |



### Missing Values

_No missing values detected._

**Duplicate rows:** 0


### First 3 Rows

|   Student_ID |   Age | Gender   | Academic_Level   | Country    |   Avg_Daily_Usage_Hours | Most_Used_Platform   | Affects_Academic_Performance   |   Sleep_Hours_Per_Night |   Mental_Health_Score | Relationship_Status   |   Conflicts_Over_Social_Media |   Addicted_Score |
|-------------:|------:|:---------|:-----------------|:-----------|------------------------:|:---------------------|:-------------------------------|------------------------:|----------------------:|:----------------------|------------------------------:|-----------------:|
|            1 |    19 | Female   | Undergraduate    | Bangladesh |                     5.2 | Instagram            | Yes                            |                     6.5 |                     6 | In Relationship       |                             3 |                8 |
|            2 |    22 | Male     | Graduate         | India      |                     2.1 | Twitter              | No                             |                     7.5 |                     8 | Single                |                             0 |                3 |
|            3 |    20 | Female   | Undergraduate    | USA        |                     6   | TikTok               | Yes                            |                     5   |                     5 | Complicated           |                             4 |                9 |


### Numeric Summary — describe()

|       |   Student_ID |     Age |   Avg_Daily_Usage_Hours |   Sleep_Hours_Per_Night |   Mental_Health_Score |   Conflicts_Over_Social_Media |   Addicted_Score |
|:------|-------------:|--------:|------------------------:|------------------------:|----------------------:|------------------------------:|-----------------:|
| count |       705    | 705     |                 705     |                 705     |               705     |                       705     |          705     |
| mean  |       353    |  20.66  |                   4.919 |                   6.869 |                 6.227 |                         2.85  |            6.437 |
| std   |       203.66 |   1.399 |                   1.257 |                   1.127 |                 1.105 |                         0.958 |            1.587 |
| min   |         1    |  18     |                   1.5   |                   3.8   |                 4     |                         0     |            2     |
| 25%   |       177    |  19     |                   4.1   |                   6     |                 5     |                         2     |            5     |
| 50%   |       353    |  21     |                   4.8   |                   6.9   |                 6     |                         3     |            7     |
| 75%   |       529    |  22     |                   5.8   |                   7.7   |                 7     |                         4     |            8     |
| max   |       705    |  24     |                   8.5   |                   9.6   |                 9     |                         5     |            9     |


### Categorical Columns

**`Gender`** — 2 unique values

| Value | Count | % |
|-------|------:|---:|
| Female | 353 | 50.1% |
| Male | 352 | 49.9% |

**`Academic_Level`** — 3 unique values

| Value | Count | % |
|-------|------:|---:|
| Undergraduate | 353 | 50.1% |
| Graduate | 325 | 46.1% |
| High School | 27 | 3.8% |

**`Country`** — 110 unique values _(>15, showing 5 samples)_

Samples: `Bangladesh`, `India`, `USA`, `UK`, `Canada`

**`Most_Used_Platform`** — 12 unique values

| Value | Count | % |
|-------|------:|---:|
| Instagram | 249 | 35.3% |
| TikTok | 154 | 21.8% |
| Facebook | 123 | 17.4% |
| WhatsApp | 54 | 7.7% |
| Twitter | 30 | 4.3% |
| LinkedIn | 21 | 3.0% |
| WeChat | 15 | 2.1% |
| Snapchat | 13 | 1.8% |
| LINE | 12 | 1.7% |
| KakaoTalk | 12 | 1.7% |
| VKontakte | 12 | 1.7% |
| YouTube | 10 | 1.4% |

**`Affects_Academic_Performance`** — 2 unique values

| Value | Count | % |
|-------|------:|---:|
| Yes | 453 | 64.3% |
| No | 252 | 35.7% |

**`Relationship_Status`** — 3 unique values

| Value | Count | % |
|-------|------:|---:|
| Single | 384 | 54.5% |
| In Relationship | 289 | 41.0% |
| Complicated | 32 | 4.5% |



### Relevance Assessment

| Question | Answer | Justification |
|----------|:------:|---------------|
| Measures social media **USAGE**? | **Y** | `Avg_Daily_Usage_Hours`, `Most_Used_Platform` |
| Measures **ATTENTION** / focus / distraction? | **N** | No attention/distraction column present |
| Measures **PRODUCTIVITY** / grades / academic performance? | **Y** | `Affects_Academic_Performance` and `Addicted_Score` relate to grades |


---
## social_media_content_mental_fatigue.csv

_Encoding detected: utf-8_

**Shape:** 5,000 rows × 9 columns


### Columns & Dtypes

| Column | dtype |
|--------|-------|
| `user_id` | `int64` |
| `age` | `int64` |
| `country` | `str` |
| `platform` | `str` |
| `daily_usage_minutes` | `int64` |
| `content_type` | `str` |
| `engagement_score` | `float64` |
| `mental_fatigue_level` | `int64` |
| `date` | `str` |



### Missing Values

_No missing values detected._

**Duplicate rows:** 0


### First 3 Rows

|   user_id |   age | country   | platform   |   daily_usage_minutes | content_type   |   engagement_score |   mental_fatigue_level | date                |
|----------:|------:|:----------|:-----------|----------------------:|:---------------|-------------------:|-----------------------:|:--------------------|
|         1 |    54 | UK        | Instagram  |                   253 | Reels          |               0.79 |                      9 | 2023-01-01 00:00:00 |
|         2 |    44 | Germany   | Instagram  |                   205 | Reels          |               7.46 |                      7 | 2023-01-01 01:00:00 |
|         3 |    30 | UK        | X          |                    63 | Live           |               2.86 |                      6 | 2023-01-01 02:00:00 |


### Numeric Summary — describe()

|       |   user_id |      age |   daily_usage_minutes |   engagement_score |   mental_fatigue_level |
|:------|----------:|---------:|----------------------:|-------------------:|-----------------------:|
| count |   5000    | 5000     |              5000     |           5000     |               5000     |
| mean  |   2500.5  |   40.232 |               182.877 |              5.242 |                  5.593 |
| std   |   1443.52 |   14.138 |               103.11  |              2.753 |                  2.848 |
| min   |      1    |   16     |                 5     |              0.5   |                  1     |
| 25%   |   1250.75 |   28     |                91.75  |              2.85  |                  3     |
| 50%   |   2500.5  |   40     |               184     |              5.205 |                  6     |
| 75%   |   3750.25 |   52     |               274     |              7.65  |                  8     |
| max   |   5000    |   64     |               359     |             10     |                 10     |


### Categorical Columns

**`country`** — 8 unique values

| Value | Count | % |
|-------|------:|---:|
| Pakistan | 659 | 13.2% |
| India | 654 | 13.1% |
| Canada | 636 | 12.7% |
| Brazil | 627 | 12.5% |
| Australia | 623 | 12.5% |
| Germany | 622 | 12.4% |
| UK | 601 | 12.0% |
| USA | 578 | 11.6% |

**`platform`** — 5 unique values

| Value | Count | % |
|-------|------:|---:|
| Facebook | 1,030 | 20.6% |
| Instagram | 1,010 | 20.2% |
| TikTok | 1,010 | 20.2% |
| YouTube | 977 | 19.5% |
| X | 973 | 19.5% |

**`content_type`** — 5 unique values

| Value | Count | % |
|-------|------:|---:|
| Shorts | 1,055 | 21.1% |
| Reels | 1,018 | 20.4% |
| Posts | 990 | 19.8% |
| Stories | 987 | 19.7% |
| Live | 950 | 19.0% |

**`date`** — 5000 unique values _(>15, showing 5 samples)_

Samples: `2023-01-01 00:00:00`, `2023-01-01 01:00:00`, `2023-01-01 02:00:00`, `2023-01-01 03:00:00`, `2023-01-01 04:00:00`



### Relevance Assessment

| Question | Answer | Justification |
|----------|:------:|---------------|
| Measures social media **USAGE**? | **Y** | `daily_usage_minutes`, `platform`, `content_type` |
| Measures **ATTENTION** / focus / distraction? | **P** | `mental_fatigue_level` is a proxy for cognitive load/distraction |
| Measures **PRODUCTIVITY** / grades / academic performance? | **N** | No productivity or academic performance column present |


---
## student_habits_exam_performance.csv

_Encoding detected: utf-8_

**Shape:** 1,000 rows × 16 columns


### Columns & Dtypes

| Column | dtype |
|--------|-------|
| `student_id` | `str` |
| `age` | `int64` |
| `gender` | `str` |
| `study_hours_per_day` | `float64` |
| `social_media_hours` | `float64` |
| `netflix_hours` | `float64` |
| `part_time_job` | `str` |
| `attendance_percentage` | `float64` |
| `sleep_hours` | `float64` |
| `diet_quality` | `str` |
| `exercise_frequency` | `int64` |
| `parental_education_level` | `str` |
| `internet_quality` | `str` |
| `mental_health_rating` | `int64` |
| `extracurricular_participation` | `str` |
| `exam_score` | `float64` |



### Missing Values

| Column | Missing Count | Missing % |
|--------|:------------:|:---------:|
| `parental_education_level` | 91 | 9.1% |


**Duplicate rows:** 0


### First 3 Rows

| student_id   |   age | gender   |   study_hours_per_day |   social_media_hours |   netflix_hours | part_time_job   |   attendance_percentage |   sleep_hours | diet_quality   |   exercise_frequency | parental_education_level   | internet_quality   |   mental_health_rating | extracurricular_participation   |   exam_score |
|:-------------|------:|:---------|----------------------:|---------------------:|----------------:|:----------------|------------------------:|--------------:|:---------------|---------------------:|:---------------------------|:-------------------|-----------------------:|:--------------------------------|-------------:|
| S1000        |    23 | Female   |                   0   |                  1.2 |             1.1 | No              |                    85   |           8   | Fair           |                    6 | Master                     | Average            |                      8 | Yes                             |         56.2 |
| S1001        |    20 | Female   |                   6.9 |                  2.8 |             2.3 | No              |                    97.3 |           4.6 | Good           |                    6 | High School                | Average            |                      8 | No                              |        100   |
| S1002        |    21 | Male     |                   1.4 |                  3.1 |             1.3 | No              |                    94.8 |           8   | Poor           |                    1 | High School                | Poor               |                      1 | No                              |         34.3 |


### Numeric Summary — describe()

|       |      age |   study_hours_per_day |   social_media_hours |   netflix_hours |   attendance_percentage |   sleep_hours |   exercise_frequency |   mental_health_rating |   exam_score |
|:------|---------:|----------------------:|---------------------:|----------------:|------------------------:|--------------:|---------------------:|-----------------------:|-------------:|
| count | 1000     |              1000     |             1000     |        1000     |                1000     |      1000     |             1000     |               1000     |     1000     |
| mean  |   20.498 |                 3.55  |                2.506 |           1.82  |                  84.132 |         6.47  |                3.042 |                  5.438 |       69.602 |
| std   |    2.308 |                 1.469 |                1.172 |           1.075 |                   9.399 |         1.226 |                2.025 |                  2.848 |       16.889 |
| min   |   17     |                 0     |                0     |           0     |                  56     |         3.2   |                0     |                  1     |       18.4   |
| 25%   |   18.75  |                 2.6   |                1.7   |           1     |                  78     |         5.6   |                1     |                  3     |       58.475 |
| 50%   |   20     |                 3.5   |                2.5   |           1.8   |                  84.4   |         6.5   |                3     |                  5     |       70.5   |
| 75%   |   23     |                 4.5   |                3.3   |           2.525 |                  91.025 |         7.3   |                5     |                  8     |       81.325 |
| max   |   24     |                 8.3   |                7.2   |           5.4   |                 100     |        10     |                6     |                 10     |      100     |


### Categorical Columns

**`student_id`** — 1000 unique values _(>15, showing 5 samples)_

Samples: `S1000`, `S1001`, `S1002`, `S1003`, `S1004`

**`gender`** — 3 unique values

| Value | Count | % |
|-------|------:|---:|
| Female | 481 | 48.1% |
| Male | 477 | 47.7% |
| Other | 42 | 4.2% |

**`part_time_job`** — 2 unique values

| Value | Count | % |
|-------|------:|---:|
| No | 785 | 78.5% |
| Yes | 215 | 21.5% |

**`diet_quality`** — 3 unique values

| Value | Count | % |
|-------|------:|---:|
| Fair | 437 | 43.7% |
| Good | 378 | 37.8% |
| Poor | 185 | 18.5% |

**`parental_education_level`** — 3 unique values

| Value | Count | % |
|-------|------:|---:|
| High School | 392 | 39.2% |
| Bachelor | 350 | 35.0% |
| Master | 167 | 16.7% |
| nan | 91 | 9.1% |

**`internet_quality`** — 3 unique values

| Value | Count | % |
|-------|------:|---:|
| Good | 447 | 44.7% |
| Average | 391 | 39.1% |
| Poor | 162 | 16.2% |

**`extracurricular_participation`** — 2 unique values

| Value | Count | % |
|-------|------:|---:|
| No | 682 | 68.2% |
| Yes | 318 | 31.8% |



### Relevance Assessment

| Question | Answer | Justification |
|----------|:------:|---------------|
| Measures social media **USAGE**? | **Y** | `social_media_hours` and `netflix_hours` |
| Measures **ATTENTION** / focus / distraction? | **N** | No direct attention column; `study_hours_per_day` is a weak proxy |
| Measures **PRODUCTIVITY** / grades / academic performance? | **Y** | `exam_score` and `attendance_percentage` are direct academic measures |


---
## social_media_attention_mental_health_survey.csv

_Encoding detected: utf-8_

**Shape:** 481 rows × 21 columns


### Columns & Dtypes

| Column | dtype |
|--------|-------|
| `Timestamp` | `str` |
| `Age` | `float64` |
| `Gender` | `str` |
| `Relationship` | `str` |
| `Occupation` | `str` |
| `Affiliations` | `str` |
| `Social Media Use` | `str` |
| `Platforms` | `str` |
| `Daily Time` | `str` |
| `9. How often do you find yourself using Social media without a specific purpose?` | `int64` |
| `10. How often do you get distracted by Social media when you are busy doing something?` | `int64` |
| `11. Do you feel restless if you haven't used Social media in a while?` | `int64` |
| `12. On a scale of 1 to 5, how easily distracted are you?` | `int64` |
| `13. On a scale of 1 to 5, how much are you bothered by worries?` | `int64` |
| `14. Do you find it difficult to concentrate on things?` | `int64` |
| `15. On a scale of 1-5, how often do you compare yourself to other successful people through the use of social media?` | `int64` |
| `16. Following the previous question, how do you feel about these comparisons, generally speaking?` | `int64` |
| `17. How often do you look to seek validation from features of social media?` | `int64` |
| `18. How often do you feel depressed or down?` | `int64` |
| `19. On a scale of 1 to 5, how frequently does your interest in daily activities fluctuate?` | `int64` |
| `20. On a scale of 1 to 5, how often do you face health issues?` | `int64` |



### Missing Values

| Column | Missing Count | Missing % |
|--------|:------------:|:---------:|
| `Affiliations` | 30 | 6.24% |


**Duplicate rows:** 0


### First 3 Rows

| Timestamp          |   Age | Gender   | Relationship      | Occupation         | Affiliations   | Social Media Use   | Platforms                                              | Daily Time            |   9. How often do you find yourself using Social media without a specific purpose? |   10. How often do you get distracted by Social media when you are busy doing something? |   11. Do you feel restless if you haven't used Social media in a while? |   12. On a scale of 1 to 5, how easily distracted are you? |   13. On a scale of 1 to 5, how much are you bothered by worries? |   14. Do you find it difficult to concentrate on things? |   15. On a scale of 1-5, how often do you compare yourself to other successful people through the use of social media? |   16. Following the previous question, how do you feel about these comparisons, generally speaking? |   17. How often do you look to seek validation from features of social media? |   18. How often do you feel depressed or down? |   19. On a scale of 1 to 5, how frequently does your interest in daily activities fluctuate? |   20. On a scale of 1 to 5, how often do you face health issues? |
|:-------------------|------:|:---------|:------------------|:-------------------|:---------------|:-------------------|:-------------------------------------------------------|:----------------------|-----------------------------------------------------------------------------------:|-----------------------------------------------------------------------------------------:|------------------------------------------------------------------------:|-----------------------------------------------------------:|------------------------------------------------------------------:|---------------------------------------------------------:|-----------------------------------------------------------------------------------------------------------------------:|----------------------------------------------------------------------------------------------------:|------------------------------------------------------------------------------:|-----------------------------------------------:|---------------------------------------------------------------------------------------------:|-----------------------------------------------------------------:|
| 4/18/2022 19:18:47 |    21 | Male     | In a relationship | University Student | University     | Yes                | Facebook, Twitter, Instagram, YouTube, Discord, Reddit | Between 2 and 3 hours |                                                                                  5 |                                                                                        3 |                                                                       2 |                                                          5 |                                                                 2 |                                                        5 |                                                                                                                      2 |                                                                                                   3 |                                                                             2 |                                              5 |                                                                                            4 |                                                                5 |
| 4/18/2022 19:19:28 |    21 | Female   | Single            | University Student | University     | Yes                | Facebook, Twitter, Instagram, YouTube, Discord, Reddit | More than 5 hours     |                                                                                  4 |                                                                                        3 |                                                                       2 |                                                          4 |                                                                 5 |                                                        4 |                                                                                                                      5 |                                                                                                   1 |                                                                             1 |                                              5 |                                                                                            4 |                                                                5 |
| 4/18/2022 19:25:59 |    21 | Female   | Single            | University Student | University     | Yes                | Facebook, Instagram, YouTube, Pinterest                | Between 3 and 4 hours |                                                                                  3 |                                                                                        2 |                                                                       1 |                                                          2 |                                                                 5 |                                                        4 |                                                                                                                      3 |                                                                                                   3 |                                                                             1 |                                              4 |                                                                                            2 |                                                                5 |


### Numeric Summary — describe()

|       |     Age |   9. How often do you find yourself using Social media without a specific purpose? |   10. How often do you get distracted by Social media when you are busy doing something? |   11. Do you feel restless if you haven't used Social media in a while? |   12. On a scale of 1 to 5, how easily distracted are you? |   13. On a scale of 1 to 5, how much are you bothered by worries? |   14. Do you find it difficult to concentrate on things? |   15. On a scale of 1-5, how often do you compare yourself to other successful people through the use of social media? |   16. Following the previous question, how do you feel about these comparisons, generally speaking? |   17. How often do you look to seek validation from features of social media? |   18. How often do you feel depressed or down? |   19. On a scale of 1 to 5, how frequently does your interest in daily activities fluctuate? |   20. On a scale of 1 to 5, how often do you face health issues? |
|:------|--------:|-----------------------------------------------------------------------------------:|-----------------------------------------------------------------------------------------:|------------------------------------------------------------------------:|-----------------------------------------------------------:|------------------------------------------------------------------:|---------------------------------------------------------:|-----------------------------------------------------------------------------------------------------------------------:|----------------------------------------------------------------------------------------------------:|------------------------------------------------------------------------------:|-----------------------------------------------:|---------------------------------------------------------------------------------------------:|-----------------------------------------------------------------:|
| count | 481     |                                                                            481     |                                                                                  481     |                                                                 481     |                                                    481     |                                                           481     |                                                  481     |                                                                                                                481     |                                                                                             481     |                                                                       481     |                                        481     |                                                                                      481     |                                                          481     |
| mean  |  26.137 |                                                                              3.553 |                                                                                    3.32  |                                                                   2.588 |                                                      3.349 |                                                             3.559 |                                                    3.245 |                                                                                                                  2.832 |                                                                                               2.775 |                                                                         2.455 |                                          3.256 |                                                                                        3.17  |                                                            3.202 |
| std   |   9.915 |                                                                              1.096 |                                                                                    1.328 |                                                                   1.257 |                                                      1.176 |                                                             1.283 |                                                    1.347 |                                                                                                                  1.408 |                                                                                               1.056 |                                                                         1.248 |                                          1.313 |                                                                                        1.257 |                                                            1.462 |
| min   |  13     |                                                                              1     |                                                                                    1     |                                                                   1     |                                                      1     |                                                             1     |                                                    1     |                                                                                                                  1     |                                                                                               1     |                                                                         1     |                                          1     |                                                                                        1     |                                                            1     |
| 25%   |  21     |                                                                              3     |                                                                                    2     |                                                                   2     |                                                      3     |                                                             3     |                                                    2     |                                                                                                                  2     |                                                                                               2     |                                                                         1     |                                          2     |                                                                                        2     |                                                            2     |
| 50%   |  22     |                                                                              4     |                                                                                    3     |                                                                   2     |                                                      3     |                                                             4     |                                                    3     |                                                                                                                  3     |                                                                                               3     |                                                                         2     |                                          3     |                                                                                        3     |                                                            3     |
| 75%   |  26     |                                                                              4     |                                                                                    4     |                                                                   3     |                                                      4     |                                                             5     |                                                    4     |                                                                                                                  4     |                                                                                               3     |                                                                         3     |                                          4     |                                                                                        4     |                                                            5     |
| max   |  91     |                                                                              5     |                                                                                    5     |                                                                   5     |                                                      5     |                                                             5     |                                                    5     |                                                                                                                  5     |                                                                                               5     |                                                                         5     |                                          5     |                                                                                        5     |                                                            5     |


### Categorical Columns

**`Timestamp`** — 458 unique values _(>15, showing 5 samples)_

Samples: `4/18/2022 19:18:47`, `4/18/2022 19:19:28`, `4/18/2022 19:25:59`, `4/18/2022 19:29:43`, `4/18/2022 19:33:31`

**`Gender`** — 9 unique values

| Value | Count | % |
|-------|------:|---:|
| Female | 263 | 54.7% |
| Male | 211 | 43.9% |
| Nonbinary  | 1 | 0.2% |
| Non-binary | 1 | 0.2% |
| NB | 1 | 0.2% |
| unsure  | 1 | 0.2% |
| Trans | 1 | 0.2% |
| Non binary  | 1 | 0.2% |
| There are others??? | 1 | 0.2% |

**`Relationship`** — 4 unique values

| Value | Count | % |
|-------|------:|---:|
| Single | 285 | 59.3% |
| Married | 101 | 21.0% |
| In a relationship | 88 | 18.3% |
| Divorced | 7 | 1.5% |

**`Occupation`** — 4 unique values

| Value | Count | % |
|-------|------:|---:|
| University Student | 292 | 60.7% |
| Salaried Worker | 132 | 27.4% |
| School Student | 49 | 10.2% |
| Retired | 8 | 1.7% |

**`Affiliations`** — 18 unique values _(>15, showing 5 samples)_

Samples: `University`, `Private`, `School, University`, `Company`, `School, Private`

**`Social Media Use`** — 2 unique values

| Value | Count | % |
|-------|------:|---:|
| Yes | 478 | 99.4% |
| No | 3 | 0.6% |

**`Platforms`** — 125 unique values _(>15, showing 5 samples)_

Samples: `Facebook, Twitter, Instagram, YouTube, Discord, Reddit`, `Facebook, Instagram, YouTube, Pinterest`, `Facebook, Instagram`, `Facebook, Instagram, YouTube`, `Facebook, Twitter, Instagram, YouTube, Discord, Pinterest, TikTok`

**`Daily Time`** — 6 unique values

| Value | Count | % |
|-------|------:|---:|
| More than 5 hours | 116 | 24.1% |
| Between 2 and 3 hours | 101 | 21.0% |
| Between 3 and 4 hours | 93 | 19.3% |
| Between 1 and 2 hours | 70 | 14.6% |
| Between 4 and 5 hours | 67 | 13.9% |
| Less than an Hour | 34 | 7.1% |



### Relevance Assessment

| Question | Answer | Justification |
|----------|:------:|---------------|
| Measures social media **USAGE**? | **Y** | `Daily Time`, `Platforms`, and `Social Media Use` capture time and breadth of use |
| Measures **ATTENTION** / focus / distraction? | **Y** | Q10 (distracted when busy), Q12 (easily distracted), Q14 (difficulty concentrating) are direct Likert-scale attention measures |
| Measures **PRODUCTIVITY** / grades / academic performance? | **N** | No productivity or grades column; `Occupation` identifies students but captures no performance outcome |


---
